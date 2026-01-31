import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from datetime import datetime
import boto3
import time

from core.state_manager import emit_event

router_image = APIRouter(prefix="/upload-image", tags=["Upload"])

MAX_FILE_SIZE = 500 * 1024
ALLOWED_MIME = {"image/jpeg", "image/png"}
BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "iot-image-gauge")

s3 = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION", "us-east-2")
)



def build_s3_key(device_id: str) -> str:
    now = datetime.utcnow()
    ts = int(time.time())

    return (
        "santander/"
        "01/"
        f"{now.year}/"
        f"{now.month:02d}/"
        f"{now.day:02d}/"
        f"{device_id}/"
        f"img_{ts}.jpg"
    )


@router_image.post("/")
async def upload_image(
    device_id: str = Form(...),
    image: UploadFile = File(...)
):
    
    print (image.content_type)
    if image.content_type not in ALLOWED_MIME:
        raise HTTPException(400, "El formato {image.content_type} no es permitido")

    content = await image.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(400, "La imagen supera los 500 KB")

    s3_key = build_s3_key(device_id)

    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=content,
            ContentType=image.content_type
        )
    except Exception as e:
        print(e)
        raise HTTPException(500, "Error subiendo imagen")
    

    event = {
        "event": "image_uploaded",
        "device_id": device_id,
        "s3_key": s3_key,
        "bucket": BUCKET_NAME,
        "timestamp": int(time.time())
    }
         
    await emit_event(event)

    return {
        "status": "ok",
        "device_id": device_id,
        "s3_key": s3_key
    }
