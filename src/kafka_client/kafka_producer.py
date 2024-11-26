from aiokafka import AIOKafkaProducer

from core.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC


async def send_task_to_kafka(task_id: int):
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        await producer.send_and_wait(KAFKA_TOPIC, str(task_id).encode())
    finally:
        await producer.stop()
