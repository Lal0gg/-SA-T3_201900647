from fastapi import FastAPI
from src.database.db import Base, engine
from src.routes import ci

app = FastAPI()
app.include_router(ci.router)

Base.metadata.create_all(bind=engine)