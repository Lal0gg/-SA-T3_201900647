import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database.db import get_db
from src.models.ci import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://root:2020@localhost:5432/cmdb_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def test_crear_ci(client):
    response = client.post("/cis", json={
        "nombre": "ServidorPrueba",
        "tipo": "Hardware",
        "descripción": "Servidor de prueba",
        "número_serie": "SN789101",
        "versión": "v1.0",
        "fecha_adquisición": "2022-01-01T00:00:00",
        "estado_actual": "Activo",
        "ubicación_física": "Sala de Servidores"
    })
    assert response.status_code == 200
    assert response.json()["nombre"] == "ServidorPrueba"