import asyncio
import json
import os
import boto3
import cv2
import numpy as np
from gmqtt import Client as MQTTClient

from services.cv_worker.processing import process_image

# --- CONFIG ---
BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = 1883

TOPIC_IN = "python/mqtt/image_uploaded"
TOPIC_OUT = "python/mqtt/image_processed"

BUCKET = os.getenv("S3_BUCKET_NAME", "iot-image-gauge")
AWS_REGION = os.getenv("AWS_REGION", "us-east-2")

# --- CLIENTES ---
s3 = boto3.client("s3", region_name=AWS_REGION)
mqtt = MQTTClient("cv-worker")


# --- CALLBACK MQTT ---
async def on_message(client, topic, payload, qos, properties):
    try:
        event = json.loads(payload.decode())
        print(f"[CV ✅] Evento recibido: {event}")

        s3_key = event["s3_key"]
        device_id = event["device_id"]

        # 1️⃣ Descargar imagen desde S3
        obj = s3.get_object(Bucket=BUCKET, Key=s3_key)
        img_bytes = obj["Body"].read()

        # 2️⃣ Bytes → OpenCV
        img_np = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("No se pudo decodificar la imagen")

        # 3️⃣ Procesar imagen
        result = process_image(img)

        # 4️⃣ Publicar resultado
        out_event = {
            "event": "image_processed",
            "device_id": device_id,
            "s3_key": s3_key,
            "result": result
        }

        mqtt.publish(TOPIC_OUT, json.dumps(out_event), qos=1)
        print(f"[CV ✅] Resultado publicado: {out_event}")

    except Exception as e:
        print(f"[CV ❌] Error en CV Worker: {e}")


async def main():
    mqtt.on_message = on_message

    await mqtt.connect(BROKER, PORT)
    mqtt.subscribe(TOPIC_IN)

    print("[CV ✅] Worker escuchando eventos...")
    await asyncio.Future()  # keep alive


if __name__ == "__main__":
    asyncio.run(main())
