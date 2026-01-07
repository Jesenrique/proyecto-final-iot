from fastapi import APIRouter, Request, Depends, Query
from datetime import datetime, timedelta

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



@router.get("/lecturas/agregadas")
async def obtener_lecturas_agregadas(
    id_manometro: int = Query(..., description="ID del manómetro"),
    fecha_inicio: datetime = Query(..., description="Fecha inicio"),
    fecha_fin: datetime = Query(..., description="Fecha fin"),
    puntos_por_hora: int = Query(20, ge=1, le=60, description="Puntos por hora"),
    pool = Depends(get_db_pool)
):
    
    intervalo_minutos = 60.0 / puntos_por_hora
    sql = """
    WITH parametros AS (
        SELECT
            $1::int AS puntos_por_hora,
            60.0 / $1::int AS intervalo_minutos
    ),
    base AS (
        SELECT
            fecha_lectura,
            valor,
            date_trunc('hour', fecha_lectura) AS hora_base
        FROM lectura
        WHERE
            id_manometro = $2
            AND fecha_lectura BETWEEN $3 AND $4
    ),
    cajones AS (
        SELECT
            b.fecha_lectura,
            b.valor,
            b.hora_base
            + FLOOR(
                EXTRACT(MINUTE FROM b.fecha_lectura)
                / p.intervalo_minutos
            ) * (p.intervalo_minutos || ' minutes')::interval
            AS inicio_subperiodo
        FROM base b
        CROSS JOIN parametros p
    )
    SELECT
        inicio_subperiodo AS periodo,
        ROUND(AVG(valor)::numeric, 2) AS promedio,
        MAX(valor) AS maximo,
        MIN(valor) AS minimo
    FROM cajones
    GROUP BY inicio_subperiodo
    ORDER BY inicio_subperiodo;
    """

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            sql,
            puntos_por_hora,
            id_manometro,
            fecha_inicio,
            fecha_fin
        )

    return [dict(row) for row in rows]