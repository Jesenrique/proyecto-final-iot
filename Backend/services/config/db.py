import asyncpg
from fastapi import FastAPI

async def connect_to_db():
    print("📌 Creando pool de conexiones a PostgreSQL...")
    return await asyncpg.create_pool(
        user="postgres",
        password="Nacional1.",
        database="db_manometro",
        host="localhost",
        port=5434,
        min_size=1,
        max_size=5
    )

async def close_db_connection(pool):
    await pool.close()
