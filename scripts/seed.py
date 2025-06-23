from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.ci import CI, CIRelacion, CITipo, EstadoActual, NivelSeguridad, Cumplimiento, EstadoConfiguración
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "postgresql://usuario:contraseña@localhost:5432/cmdb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_data():
    db = SessionLocal()
    try:
        # Crear CIs de ejemplo basados en CMDB.xlsx
        ci1 = CI(
            nombre="Servidor1",
            tipo=CITipo.HARDWARE,
            descripción="Servidor de aplicaciones",
            número_serie="SN123456",
            versión="v1.0",
            fecha_adquisición=datetime(2022, 1, 1),
            estado_actual=EstadoActual.ACTIVO,
            relaciones={"padres": [], "hijos": []},
            ubicación_física="Sala de Servidores",
            propietario_responsable="Equipo Infraestructura",
            fecha_cambio=datetime(2022, 2, 1),
            descripción_cambio="Actualización de software",
            documentación_relacionada="Enlace a Manual[url]",
            enlaces_incidentes_problemas="Enlace a incidente[url]",
            nivel_seguridad=NivelSeguridad.ALTO,
            cumplimiento=Cumplimiento.CUMPLE,
            estado_configuración=EstadoConfiguración.APROBADO,
            número_licencia="ABC123",
            fecha_vencimiento=datetime(2023, 1, 1)
        )
        ci2 = CI(
            nombre="Aplicación1",
            tipo=CITipo.SOFTWARE,
            descripción="Aplicación de contabilidad",
            número_serie="XYZ456",
            versión="v2.0",
            fecha_adquisición=datetime(2022, 3, 15),
            estado_actual=EstadoActual.ACTIVO,
            relaciones={"padres": [], "hijos": []},
            ubicación_física="Servidor1",
            propietario_responsable="Equipo Desarrollo",
            fecha_cambio=datetime(2022, 4, 1),
            descripción_cambio="Parche de Seguridad",
            documentación_relacionada="Enlace a Documentación[url]",
            enlaces_incidentes_problemas="Enlace a incidente[url]",
            nivel_seguridad=NivelSeguridad.MEDIO,
            cumplimiento=Cumplimiento.CUMPLE,
            estado_configuración=EstadoConfiguración.APROBADO,
            número_licencia="XYZ456",
            fecha_vencimiento=datetime(2024, 1, 1)
        )
        db.add_all([ci1, ci2])
        db.commit()

        # Crear relación
        relacion = CIRelacion(ci_origen_id=ci1.id, ci_destino_id=ci2.id, tipo="ALOJA")
        db.add(relacion)
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()