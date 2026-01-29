import asyncio
import json
import random
import websockets
import time
from core.state_manager import CONNECTED_CLIENTS, register_client, unregister_client

# 1. Conjunto Global para almacenar todas las conexiones activas
#CONNECTED_CLIENTS = set() - se crea 

# Función para enviar datos a todos los clientes conectados
async def broadcast_data(data):
     """
     Envía datos JSON a todos los clientes conectados de forma asíncrona.
     """
     if CONNECTED_CLIENTS:
         message = json.dumps(data)
         # websockets.broadcast es la forma más eficiente y correcta
         # de enviar a un conjunto de clientes en esta librería.
         websockets.broadcast(CONNECTED_CLIENTS, message)
         print(f"[WS ✅] Enviado broadcast a {len(CONNECTED_CLIENTS)} clientes: {message}")
     else:
         # print("🤖 No hay clientes para broadcast.")
         pass

# Nueva función asíncrona para simular un servicio de envío de datos (Tu bucle 'while True')
# async def data_sender_task():
#     """Ejecuta un bucle infinito que envía datos JSON cada 1 segundo."""
#     print("🤖 Tarea de envío de datos iniciada.")
#     while True:
#         # Pausa asíncrona (permite que otras tareas se ejecuten)
#         await asyncio.sleep(1) 
        
#         # 1. Generar datos simulados
#         data = {
#             "deviceId": "sensor-1",
#             "value": random.randint(0, 100),
#             "timestamp": time.strftime("%H:%M:%S")
#         }
        
#         # 2. Enviar a todos los clientes
#         await broadcast_data(data)


# 3. Función manejadora de la conexión (Ahora con la firma correcta y limpieza)
# SOLUCIÓN 1: Debe recibir 'path' para evitar el TypeError
async def echo(websocket):
    print(f" Cliente conectado!")
    
    # --- REGISTRO ---
    register_client(websocket)
    #CONNECTED_CLIENTS.add(websocket)
    print(f"Clientes activos: {len(CONNECTED_CLIENTS)}")
    
    try:
        # Lo más importante para un servidor que solo envía datos:
        # Mantener la conexión abierta. Usamos un bucle infinito aquí.
        # Si NO pones un bucle de recepción, el manejador terminará inmediatamente
        # y la conexión se cerrará. Puedes usar un bucle de recepción comentado
        # o esta tarea de por vida.
        await websocket.wait_closed() 

    # El bloque 'finally' asegura la limpieza incluso si hay un error o desconexión
    finally:
        # --- LIMPIEZA ---
        if websocket in CONNECTED_CLIENTS:
            unregister_client(websocket)
            print("Conexión cerrada y removida.")
            print(f"Clientes activos restantes: {len(CONNECTED_CLIENTS)}")


# 4. Iniciar el servidor y el proceso de envío de datos concurrentemente
async def start_websocket_server():

    # MODIFICACIÓN CLAVE AQUÍ:
    websocket_server = await websockets.serve(
        echo, 
        "0.0.0.0",      # 1. Escuchar en TODAS las interfaces (evita problemas IPv4/IPv6)
        8765, 
        origins=None    # 2. Desactivar protección CORS (permitir conexión desde Angular :4200)
                        #    Si quieres seguridad estricta, usa: origins=["http://localhost:4200"]
    )
    
    # Imprimir para confirmar dónde está escuchando realmente
    for sock in websocket_server.sockets:
        print(f"[WS ✅] WS escuchando en: {sock.getsockname()}")
    #data_sender = data_sender_task() # Tu bucle de envío de datos

    # SOLUCIÓN 2: Ejecutamos ambas tareas al mismo tiempo (concurrentemente)
    # await asyncio.gather ejecuta ambas tareas hasta que sean canceladas
    #await asyncio.gather(websocket_server, data_sender)
    return websocket_server
