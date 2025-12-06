import asyncpg

async def connect_db():
    return await asyncpg.connect(
        user="postgres",
        password="Nacional1.",
        database="db_manometro",
        host="localhost",
        port=5434
    )
