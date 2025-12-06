from fastapi import FastAPI, Request, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List

# Asumo que tienes estas funciones en tu config
from config.db import connect_to_db, close_db_connection

# --- 1. LIFESPAN (Gestiona el ciclo de vida) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicio: Crear el pool y guardarlo en el estado de la app
    print("📌 Conectando a la base de datos...")
    app.state.pool = await connect_to_db() 
    print("📌 Pool creado correctamente")
    
    yield # Aquí la app corre
    
    # Cierre: Cerrar conexión
    print("📌 Cerrando conexión...")
    await close_db_connection(app.state.pool)
    print("📌 Pool cerrado correctamente")

# --- 2. CREACIÓN DE LA APP ---
# La variable app debe estar a nivel global para que Uvicorn la vea
app = FastAPI(lifespan=lifespan)

# --- 3. CONFIGURACIÓN CORS ---
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 4. DEPENDENCIA PARA OBTENER EL POOL ---
# Esta función permite que tus rutas pidan el pool sin usar variables globales
def get_db_pool(request: Request):
    return request.app.state.pool

# --- 5. TUS RUTAS (Ahora separadas) ---
# Si quisieras mover esto a otro archivo, usarías APIRouter.
# Aquí lo dejo junto para que veas el cambio en la lógica.

@app.get("/plantas")
async def obtener_plantas(pool = Depends(get_db_pool)): # <--- Inyección aquí
    async with pool.acquire() as conn:
        query = """
            SELECT 
                m.id_manometro,
                m.identificador,
                l.valor AS ultima_lectura,
                l.fecha_lectura AS fecha_ultima_lectura
            FROM manometro m
            LEFT JOIN LATERAL (
                SELECT valor, fecha_lectura
                FROM lectura
                WHERE id_manometro = m.id_manometro
                ORDER BY fecha_lectura DESC
                LIMIT 1
            ) l ON TRUE
            WHERE m.id_planta = 1
        """
        rows = await conn.fetch(query)
        return [dict(row) for row in rows]