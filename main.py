from fastapi import FastAPI

from .database import Base, engine
from .routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Combate à Dengue",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def home():
    return {
        "projeto": "Combate à Dengue",
        "status": "online"
    }