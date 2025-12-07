import asyncio
import json

async def db_writer_worker(queue: asyncio.Queue, db_pool):
    """
    Este worker corre siempre en segundo plano.
    Saca datos de la cola y los guarda en la BD.
    """
    print("💾 Worker de Base de Datos iniciado...")
    
    while True:
        # 1. Esperar a que llegue un dato a la cola (Esto no bloquea el resto de la app)
        data_packet = await queue.get()
        
        try:
            # data_packet es lo que enviaste desde MQTT (ej: un dict)
            # Ejemplo de lógica de guardado:
            async with db_pool.acquire() as conn:
                query = """
                    INSERT INTO lectura (id_manometro, valor, fecha_lectura)
                    VALUES ($1, $2, NOW())
                """
                # Asumiendo que data_packet tiene {'id': 1, 'val': 50.5}
                await conn.execute(query, data_packet['id'], data_packet['val'])
                
            # print(f"✅ Dato guardado: {data_packet}")

        except Exception as e:
            print(f"❌ Error guardando en BD: {e}")
        
        finally:
            # Avisamos a la cola que ya procesamos este item
            queue.task_done()