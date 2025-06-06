from fastapi import FastAPI
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="AI Michi Quest 🐾")

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción, cambia esto a tu dominio
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Bienvenido a 'Michi: Camino al Dominio Mundial'! Comienza tu aventura accediendo a /start."}