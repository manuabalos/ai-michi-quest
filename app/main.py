from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="AI Michi Quest 🐾")

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Bienvenido a 'Michi: Camino al Dominio Mundial'! Comienza tu aventura accediendo a /start."}