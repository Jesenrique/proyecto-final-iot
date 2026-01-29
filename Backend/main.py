# main.py
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

# Importar tus servicios
from services.websocket_service import start_websocket_server 
from services.MQTT_service import start_mqtt_client_task 
from services.db_worker import db_writer_worker
from services.mqtt_publisher import connect

# Asumo que tienes estas funciones de DB
from services.config.db import connect_to_db, close_db_connection

from fastapi.middleware.cors import CORSMiddleware

from services.routers.plantas import router as plantas_router
from services.routers.upload import router_image as image_router

import os


# Variable global para almacenar las tareas de larga duración y el pool
LONG_RUNNING_TASKS = [] 
DB_POOL = None 
DATA_QUEUE = asyncio.Queue()


@asynccontextmanager
async def lifespan(app: FastAPI):
    ENABLE_DB = "true"
    ENABLE_MQTT = "true"
    ENABLE_WS = "true"
    ENABLE_MQTT_PUBLISHER = "true"
    # FASE DE INICIO (Antes del yield)

    print("=============================================")
    print("  🚀 FastAPI: Inicializando Recursos y Tareas  ")
    print("=============================================")
    
    global DB_POOL
    if ENABLE_DB:
        try:
            DB_POOL = await connect_to_db()
            app.state.db_pool = DB_POOL
            print("✅ Pool de DB creado y disponible en app.state.db_pool")
        except Exception as e:
            DB_POOL = None
            print(f"❌ DB no disponible: {e}")
    else:
        print("⏭️ DB deshabilitada por configuración")


    # 2. Iniciando Tareas de Larga Duración
    # Creamos las tasks y las agregamos a la lista, pero NO las esperamos.

    if ENABLE_WS:
        try:
            websocket_awaitable = start_websocket_server()
            websocket_server_instance = await websocket_awaitable
            app.state.websocket_server = websocket_server_instance
            print("🌐 Servidor WebSockets lanzado y disponible.")
        except Exception as e:
            print(f"❌ WS no iniciado: {e}")
    else:
        print("⏭️ WebSockets deshabilitados")

    
    if DB_POOL:
        db_task = asyncio.create_task(db_writer_worker(DATA_QUEUE, DB_POOL))
        LONG_RUNNING_TASKS.append(db_task)
    else:
        print("⏭️ DB worker no iniciado (sin DB)")

    if ENABLE_MQTT:
        try:
            mqtt_task = asyncio.create_task(start_mqtt_client_task(DATA_QUEUE))
            LONG_RUNNING_TASKS.append(mqtt_task)
            print("📡 Cliente MQTT lanzado como tarea asíncrona.")
        except Exception as e:
            print(f"❌ MQTT no iniciado: {e}")
    else:
        print("⏭️ MQTT deshabilitado")

    if ENABLE_MQTT_PUBLISHER:
        try:
            mqtt_task_publisher = asyncio.create_task(connect())
            LONG_RUNNING_TASKS.append(mqtt_task_publisher)
            print("Publicador MQTT lanzado como tarea asíncrona.")
        except Exception as e:
            print(f"❌ MQTT no iniciado: {e}")
    else:
        print("⏭️ MQTT deshabilitado")

    
    # --- YIELD: La aplicación está lista para recibir peticiones y tareas de fondo ---
    yield 
    
    # FASE DE LIMPIEZA (Después del yield)
    print("=============================================")
    print("  🛑 FastAPI: Deteniendo Recursos y Tareas  ")
    print("=============================================")
    
    # 1. Cancelar Tareas de Larga Duración
    for task in LONG_RUNNING_TASKS:
        task.cancel()
    
    # Esperamos un momento para que se limpien.
    await asyncio.gather(*LONG_RUNNING_TASKS, return_exceptions=True)
    print("✅ Tareas de I/O canceladas y detenidas.")
    
    if DB_POOL:
        await close_db_connection(DB_POOL)
        print("✅ Pool de DB cerrado.")




# ----------------------------------------------------
# Instancia de FastAPI (Uvicorn buscará 'app')
app = FastAPI(lifespan=lifespan)

# --- CORS ÚNICO Y CENTRALIZADO ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONECTAR EL ROUTER A LA APP ---
app.include_router(plantas_router)
app.include_router(image_router)


# (No necesitas el if __name__ == "__main__": asyncio.run(main())
# Ya que usas Uvicorn para ejecutar la app: uvicorn main:app --reload)