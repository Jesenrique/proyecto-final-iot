import asyncio
import json

async def db_writer_worker(queue: asyncio.Queue, db_pool):
    """
    Este worker corre siempre en segundo plano.
    Saca datos de la cola y los guarda en la BD.
    """
    print("[DB ✅] Worker de Base de Datos iniciado...")
    
    while True:
        # 1. Esperar a que llegue un dato a la cola (Esto no bloquea el resto de la app)
        data_packet = await queue.get()
        
        try:
            raw_value = data_packet.get('value')
            if raw_value is None:
                raise ValueError("Mensaje sin campo 'value'")

            value = float(raw_value)

            # data_packet es lo que enviaste desde MQTT (ej: un dict)
            # Ejemplo de lógica de guardado:
            async with db_pool.acquire() as conn:
                query = """
                    INSERT INTO lectura (id_manometro, valor)
                    VALUES ($1, $2)
                """
                # Prueba controlada: id_manometro fijo en 3 y valor desde MQTT
                await conn.execute(query, 3, value)
                
            print(f"[DB ✅] Dato guardado: {data_packet}")

        except Exception as e:
            print(f"[DB ❌] Error guardando en BD: {e}")
        
        finally:
            # Avisamos a la cola que ya procesamos este item
            queue.task_done()
