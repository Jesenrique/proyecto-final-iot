# services/mqtt_service.py
import asyncio
import json
from gmqtt import Client as MQTTClient
import websockets
from services.websocket_service import broadcast_data
#from core.state_manager import get_active_clients

# --- CONFIGURACIÓN ---
BROKER = 'localhost'
PORT = 1883
TOPIC = "plantaTratamiento/santander/01/image_processed"

# Esta función puede estar afuera porque no depende de la queue,
# aunque necesitará acceso a los clientes websockets.
#async def broadcast_data_mqtt(data: dict):
    # ... tu lógica de broadcast ...
    #print(f"📡 Broadcast simulado de: {data}")
    

async def start_mqtt_client_task(queue: asyncio.Queue):
    """
    Inicializa el cliente MQTT (gmqtt) dentro del loop de asyncio.
    """
    client = MQTTClient(client_id='mqtt-client-bridge')

    # ---------------------------------------------------------
    # 1. DEFINIMOS LOS CALLBACKS AQUÍ DENTRO (CLOSURE)
    #    Para que tengan acceso a la variable 'queue'
    # ---------------------------------------------------------
    
    async def on_message(client, topic, payload, qos, properties):
        try:
            data = json.loads(payload.decode('utf-8'))
            print(f"[MQTT-SUB-WS-DB ✅] Recibido")
            
            # ✅ AHORA SÍ FUNCIONA: 'queue' es visible aquí porque estamos dentro de la función padre
            await queue.put(data)
            
            # Broadcast
            await broadcast_data(data)
            
        except Exception as e:
            print(f"[MQTT-SUB-WS-DB ❌] Error procesando mensaje: {e}")

    def on_connect(client, flags, rc, properties):
        print(f"[MQTT-SUB-WS-DB ✅] Conectado a {BROKER}")
        client.subscribe(TOPIC)

    # ---------------------------------------------------------
    # 2. ASIGNAMOS LOS CALLBACKS
    # ---------------------------------------------------------
    client.on_message = on_message
    client.on_connect = on_connect

    # ---------------------------------------------------------
    # 3. CONEXIÓN Y BUCLE
    # ---------------------------------------------------------
    try:
        await client.connect(BROKER, PORT)
        
        # Mantenemos la tarea viva esperando indefinidamente.
        # gmqtt no bloquea, así que esto es seguro.
        await asyncio.Future() 

    except asyncio.CancelledError:
        print("🛑 Tarea MQTT cancelada, desconectando...")
        await client.disconnect()
        
    except Exception as e:
        print(f"[MQTT-SUB-WS-DB ❌]  Error crítico en MQTT: {e}")