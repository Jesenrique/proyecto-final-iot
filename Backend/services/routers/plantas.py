from fastapi import APIRouter, Request, Depends

# 1. Ya no usamos FastAPI(), usamos APIRouter()
router = APIRouter()

# 2. Dependencia para obtener el pool desde la app principal
# (Esto funciona porque el router se "pegará" a la app principal)
def get_db_pool(request: Request):
    return request.app.state.db_pool

# 3. Definimos la ruta usando @router en lugar de @app
@router.get("/plantas")
async def obtener_plantas(pool = Depends(get_db_pool)):
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