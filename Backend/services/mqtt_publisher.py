import json
import os
from gmqtt import Client as MQTTClient

BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = 1883
TOPIC = "python/mqtt/image_uploaded"

_client: MQTTClient | None = None


async def connect():
    global _client
    _client = MQTTClient("backend-publisher")
    await _client.connect(BROKER, PORT)
    print("✅ MQTT publisher conectado")


async def publish(event: dict):
    if _client is None:
        raise RuntimeError("MQTT publisher no conectado")

    payload = json.dumps(event)
    _client.publish(TOPIC, payload, qos=1)
