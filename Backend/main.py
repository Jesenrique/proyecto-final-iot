# main.py
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

# Importar tus servicios
from services.websocket_service import start_websocket_server 
from services.MQTT_service import start_mqtt_client_task 
from services.db_worker import db_writer_worker

# Asumo que tienes estas funciones de DB
from services.config.db import connect_to_db, close_db_connection

from fastapi.middleware.cors import CORSMiddleware

from services.routers.plantas import router as plantas_router

# Variable global para almacenar las tareas de larga duración y el pool
LONG_RUNNING_TASKS = [] 
DB_POOL = None 
DATA_QUEUE = asyncio.Queue()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # FASE DE INICIO (Antes del yield)

    print("=============================================")
    print("  🚀 FastAPI: Inicializando Recursos y Tareas  ")
    print("=============================================")
    
    # 1. Conexión a la DB
    global DB_POOL
    DB_POOL = await connect_to_db() 
    app.state.db_pool = DB_POOL # Guardar en el estado de la app
    print("✅ Pool de DB creado y disponible en app.state.db_pool")
    
    # 2. Iniciando Tareas de Larga Duración
    # Creamos las tasks y las agregamos a la lista, pero NO las esperamos.
    
    websocket_awaitable = start_websocket_server()
    websocket_server_instance = await websocket_awaitable
    app.state.websocket_server = websocket_server_instance
    print("🌐 Servidor WebSockets lanzado y disponible.")

    #crea la tarea que permite guardar data en la db pasando la cola y el pool
    db_task = asyncio.create_task(db_writer_worker(DATA_QUEUE, DB_POOL))
    LONG_RUNNING_TASKS.append(db_task)

    # Tarea MQTT
    # se pasa la cola creada para que ponga alli la data que llega
    mqtt_task = asyncio.create_task(start_mqtt_client_task(DATA_QUEUE))
    LONG_RUNNING_TASKS.append(mqtt_task)
    print("📡 Cliente MQTT lanzado como tarea asíncrona.")
    
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
    
    # 2. Cierre de la DB
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


# (No necesitas el if __name__ == "__main__": asyncio.run(main())
# Ya que usas Uvicorn para ejecutar la app: uvicorn main:app --reload)