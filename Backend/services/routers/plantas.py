from fastapi import APIRouter, Request, Depends, Query, HTTPException
from datetime import datetime, timedelta

# 1. Ya no usamos FastAPI(), usamos APIRouter()
router = APIRouter()

# 2. Dependencia para obtener el pool desde la app principal
# (Esto funciona porque el router se "pegará" a la app principal)
def get_db_pool(request: Request):
    return request.app.state.db_pool


@router.get("/ping")
def ping():
    return {"status": "ok"}

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
    periodo: str = Query(..., description="Opciones: hour, day, week, month, year"),
    puntos_objetivo: int = Query(20, alias="puntos_por_hora", description="Cuantos puntos quieres ver en la grafica"),
    pool = Depends(get_db_pool)
):
    fecha_fin = datetime.now()
    
    # 1. Configuración de Estrategia
    # Definimos variables por defecto
    trunc_unit = 'day' 
    intervalo_segundos = 0
    usar_logica_matematica = True # Switch para decidir qué query usar

    if periodo == "hour":
        fecha_inicio = fecha_fin - timedelta(hours=1)
        trunc_unit = 'hour'
        # 3600 segundos / puntos deseados
        intervalo_segundos = int(3600 / puntos_objetivo) 
        
    elif periodo == "day":
        fecha_inicio = fecha_fin - timedelta(hours=24)
        trunc_unit = 'day'
        # 86400 segundos / 270 puntos (o los que pidas)
        # Nota: Ajusté 270 a puntos_objetivo para hacerlo dinámico si quieres, o déjalo fijo
        intervalo_segundos = int(86400 / 270) 

    elif periodo == "week":
        fecha_inicio = fecha_fin - timedelta(weeks=1)
        trunc_unit = 'week'
        # Una semana en segundos / puntos
        intervalo_segundos = int(604800 / 300) 

    elif periodo == "month": # O "1M"
        fecha_inicio = fecha_fin - timedelta(days=30)
        usar_logica_matematica = False # Cambiamos estrategia
        trunc_unit = 'day' # En mes, agrupamos por día natural
        
    elif periodo == "year":
        fecha_inicio = fecha_fin - timedelta(days=365)
        usar_logica_matematica = False
        trunc_unit = 'month' # En año, agrupamos por mes natural
    
    else:
        raise HTTPException(status_code=400, detail="Periodo no válido")

    print(f"Rango: {fecha_inicio} - {fecha_fin}. Intervalo(s): {intervalo_segundos}")

    async with pool.acquire() as conn:
        
        # ESTRATEGIA A: Downsampling Matemático (Hour, Day, Week)
        if usar_logica_matematica:
            sql = """
            WITH parametros AS (
                SELECT $1::int AS intervalo_segundos
            ),
            base AS (
                SELECT
                    fecha_lectura,
                    valor,
                    -- Ancla dinámica: Inicio de la hora, del día o de la semana
                    date_trunc($2, fecha_lectura) AS periodo_base
                FROM lectura
                WHERE
                    id_manometro = $3
                    AND fecha_lectura BETWEEN $4 AND $5
            ),
            cajones AS (
                SELECT
                    valor,
                    -- LA FORMULA MAESTRA CORREGIDA:
                    -- 1. Calculamos segundos desde el ancla de ESA lectura
                    -- 2. Dividimos por el intervalo (floor)
                    -- 3. Reconstruimos sumando segundos al ancla
                    periodo_base + make_interval(secs => 
                        FLOOR(
                            EXTRACT(EPOCH FROM (fecha_lectura - periodo_base)) / p.intervalo_segundos
                        ) * p.intervalo_segundos
                    ) AS inicio_subperiodo
                FROM base
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
            rows = await conn.fetch(sql, intervalo_segundos, trunc_unit, id_manometro, fecha_inicio, fecha_fin)

        # ESTRATEGIA B: Agrupación Calendario Simple (Month, Year)
        else:
            sql = """
            SELECT
                date_trunc($1, fecha_lectura) AS periodo,
                ROUND(AVG(valor)::numeric, 2) AS promedio,
                MAX(valor) AS maximo,
                MIN(valor) AS minimo
            FROM lectura
            WHERE
                id_manometro = $2
                AND fecha_lectura BETWEEN $3 AND $4
            GROUP BY 1
            ORDER BY 1;
            """
            rows = await conn.fetch(sql, trunc_unit, id_manometro, fecha_inicio, fecha_fin)

    return [dict(row) for row in rows]