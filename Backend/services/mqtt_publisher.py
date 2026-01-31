import json
import os
from gmqtt import Client as MQTTClient

BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = 1883
TOPIC = "plantaTratamiento/santander/01/image_uploaded"

_client: MQTTClient | None = None


async def connect():
    global _client
    _client = MQTTClient("backend-publisher")
    await _client.connect(BROKER, PORT)
    print("[MQTT-PUB ✅] MQTT PUB conectado")


async def publish(event: dict):
    if _client is None:
        raise RuntimeError("[MQTT-PUB ❌] MQTT PUB conectado")

    payload = json.dumps(event)
    _client.publish(TOPIC, payload, qos=1)
