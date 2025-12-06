# core/state_manager.py

import websockets
from typing import Set

# El conjunto global que almacena las referencias a las conexiones activas
CONNECTED_CLIENTS: Set[websockets.WebSocketServerProtocol] = set()

# Función que el servicio WebSockets llama al conectar
def register_client(websocket: websockets.WebSocketServerProtocol):
    """Añade una nueva conexión al conjunto."""
    CONNECTED_CLIENTS.add(websocket)
    print(f"[{__name__}] Cliente registrado. Total: {len(CONNECTED_CLIENTS)}")

# Función que el servicio WebSockets llama al desconectar
def unregister_client(websocket: websockets.WebSocketServerProtocol):
    """Elimina una conexión del conjunto."""
    if websocket in CONNECTED_CLIENTS:
        CONNECTED_CLIENTS.remove(websocket)
        print(f"[{__name__}] Cliente desconectado. Total: {len(CONNECTED_CLIENTS)}")

# Función que el servicio MQTT llama para enviar datos a todos
async def get_active_clients() -> Set[websockets.WebSocketServerProtocol]:
    """Devuelve la lista actual de clientes para el broadcast."""
    return CONNECTED_CLIENTS