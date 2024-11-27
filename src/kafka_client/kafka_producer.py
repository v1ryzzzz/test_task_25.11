from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaConnectionError

from core.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC
from logger.logger import logger


async def send_task_to_kafka(task_id: int):
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    try:
        await producer.start()
    except KafkaConnectionError as e:
        logger.error('Kafka connection error: %s', e)

    try:
        await producer.send_and_wait(KAFKA_TOPIC, str(task_id).encode())
    finally:
        await producer.stop()
