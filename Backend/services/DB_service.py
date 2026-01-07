from fastapi import FastAPI, Request, Depends, Query, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List
from typing import Literal

from datetime import datetime, timedelta

from config.db import connect_to_db, close_db_connection

import logging

logger = logging.getLogger(__name__)

# Definimos tipos estrictos para que FastAPI valide por nosotros (Swagger se verá genial)
RangoTiempo = Literal["1h", "24h", "7d", "30d", "1y"]
Granularidad = Literal["minute", "hour", "day", "week", "month"]

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
    

@app.get("/lectura")
async def obtener_lecturas(pool = Depends(get_db_pool)): # <--- Inyección aquí
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
    

@app.get("/lecturas/agregadas")
async def obtener_historico(
    id_manometro: int = Query(..., description="ID del manómetro"),
    pool = Depends(get_db_pool)
):
    periodo = 'hour'

    fecha_fin = datetime.now()
    fecha_inicio = fecha_fin - timedelta(hours=1)

    logger.info(f"fecha inicio: {fecha_inicio}, fecha fin: {fecha_fin}")

    async with pool.acquire() as conn:
        sql = """
            SELECT 
                date_trunc('hour', fecha_lectura) AS periodo,
                ROUND(AVG(valor), 2) AS promedio_valor,
                MAX(valor) AS max_valor,
                MIN(valor) AS min_valor
            FROM lectura 
            WHERE 
                id_manometro = $1
                AND fecha_lectura BETWEEN $2 AND $3
            GROUP BY 1
            ORDER BY 1 ASC;
        """

        rows = await conn.fetch(sql, id_manometro, fecha_inicio, fecha_fin)
        return [dict(row) for row in rows]