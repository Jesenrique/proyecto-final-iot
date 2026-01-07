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
async def obtener_historico(
    id_manometro: int = Query(..., description="ID del manómetro"),
    pool = Depends(get_db_pool)
):
    periodo = 'hour'  
    fecha_fin = datetime.now() 

    match periodo:
        case 'hour':
            fecha_inicio = fecha_fin - timedelta(hours=1)
        case 'day':
            fecha_inicio = fecha_fin - timedelta(days=1)
        case _:
            raise ValueError("Periodo no soportado")

    print(f"fecha inicio: {fecha_inicio}, fecha fin: {fecha_fin}")

    async with pool.acquire() as conn:

        sql = """
            SELECT 
                date_trunc($1, fecha_lectura) AS periodo,
                ROUND(AVG(valor), 2) AS promedio_valor,
                MAX(valor) AS max_valor,
                MIN(valor) AS min_valor
            FROM lectura 
            WHERE 
                id_manometro = $2
                AND fecha_lectura >= $3
                AND fecha_lectura <= $4
            GROUP BY 1
            ORDER BY 1 ASC;
        """

        rows = await conn.fetch(sql, periodo, id_manometro, fecha_inicio, fecha_fin)

        return [dict(row) for row in rows]
