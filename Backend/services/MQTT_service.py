# services/mqtt_service.py (¡ASÍNCRONO y limpio!)

import asyncio
import json
from gmqtt import Client as MQTTClient # Usamos gmqtt
from core.state_manager import get_active_clients
import websockets
#from core.models import SensorReading # Importar si has definido modelos

# --- CONFIGURACIÓN ---
BROKER = 'localhost'
PORT = 1883
TOPIC = "python/mqtt/" # Usamos # para suscribirse a todos los subtemas

# --- FUNCIÓN DE BROADCAST ASÍNCRONA ---
async def broadcast_data(data: dict):
    """Envía el JSON procesado a todos los clientes WS activos."""
    clients = await get_active_clients() # Obtener el conjunto de forma asíncrona
    
    if clients:
        try:
            # 1. Validación de datos (opcional si usas models.py)
            # processed_data = SensorReading(**data).model_dump_json() 
            message = json.dumps(data)
            
            # 2. Envío asíncrono (requiere await)
            websockets.broadcast(clients, message)
            print(f"🤖 [MQTT Service] Enviado broadcast a {len(clients)} WS clientes.")
        except Exception as e:
            print(f"❌ Error al enviar broadcast: {e}")
    
# --- MANEJADOR DE MENSAJES MQTT ---
async def on_message(client, topic, payload, qos, properties):
    """Se ejecuta cuando llega un mensaje MQTT."""
    try:
        data = json.loads(payload.decode('utf-8'))
        print(f"📥 [MQTT Service] Recibido de '{topic}': {data}")
        
        # --- Lógica de Procesamiento y Persistencia aquí ---
        
        # 3. Llamada al broadcast (debe ser await)
        await broadcast_data(data)
        
    except json.JSONDecodeError:
        print(f"⚠️ Error: Payload no es JSON válido: {payload}")
    except Exception as e:
        print(f"❌ Error en on_message: {e}")

# --- TAREA ASÍNCRONA PRINCIPAL ---
async def start_mqtt_client_task():
    """
    Inicializa el cliente MQTT y lo ejecuta como una tarea asíncrona.
    """
    client = MQTTClient(client_id='mqtt-client-bridge')
    
    # Manejadores de eventos (asíncronos)
    client.on_message = on_message
    
    def on_connect(client, flags, rc, properties):
        if rc == 0:
            print(f"✅ [MQTT Service] Conectado al broker: {client._host}")
            client.subscribe(TOPIC)
        else:
            print(f"❌ [MQTT Service] Fallo de conexión: {rc}")

    client.on_connect = on_connect

    try:
        # 4. Inicia la conexión y mantiene el bucle de eventos MQTT
        await client.connect(BROKER, PORT)
        # Esto mantiene la tarea viva, similar a client.loop_forever(), pero sin bloquear
        await asyncio.Future() 
        
    except ConnectionRefusedError:
        print(f"🚨 [MQTT Service] No se pudo conectar al broker en {BROKER}:{PORT}. Verifique el broker.")
    except Exception as e:
        print(f"❌ Error en la tarea MQTT: {e}")
    finally:
        await client.disconnect()

# Nota: El bloque 'if __name__ == "__main__":' se elimina, ya que 'main.py' lo ejecutará.