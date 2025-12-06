# main.py (SOLUCIÓN FINAL, SIN FUNCIONES INTERMEDIAS ASYNC)

import asyncio
import websockets
# Importar la tarea final que queremos ejecutar
from services.websocket_service import start_websocket_server 
from services.MQTT_service import start_mqtt_client_task 


# Importa el conjunto de clientes
from core.state_manager import CONNECTED_CLIENTS 


async def main():
    """
    Coordina e inicia todas las tareas asíncronas concurrentemente.
    """
    print("=============================================")
    print("  🚀 Iniciando Coordinador de Servicios IoT  ")
    print("=============================================")

    # 1. Tarea WebSockets: Llama y espera el resultado de start_websocket_server(),
    # que es la tarea de escucha (el objeto Server de websockets).
    # Este resultado es un objeto 'Server', que es AWAITABLE pero NO una corrutina simple.
    websocket_server_task = start_websocket_server()
    print("🌐 Servidor WebSockets escuchando en ws://localhost:8765")
    
    # 2. Tarea MQTT: Llama a la corrutina FINAL.
    # Esta variable es la corrutina 'start_mqtt_client_task'.
    mqtt_client_task = start_mqtt_client_task()

    
    print(f"Clientes activos iniciales (Verificación): {len(CONNECTED_CLIENTS)}")

    try:
        print("--- Ejecutando Tareas Concurrently ---")
        
        # gather necesita las corrutinas (awaitable) o tasks.
        # websocket_server_task (el objeto Server) es awaitable.
        # mqtt_client_task (la corrutina) es awaitable.
        await asyncio.gather(websocket_server_task, mqtt_client_task, ) 
        
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido por el usuario (Ctrl+C).")
        
    except Exception as e:
        print(f"\n❌ Ocurrió un error inesperado en el Coordinador: {e}")


if __name__ == "__main__":
    asyncio.run(main())