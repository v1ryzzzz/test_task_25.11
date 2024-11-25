from aiokafka import AIOKafkaProducer

KAFKA_TOPIC = 'tasks'
KAFKA_BOOTSTRAP_SERVERS = 'kafka:9092'


async def send_task_to_kafka(task_id: int):
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        await producer.send_and_wait(KAFKA_TOPIC, str(task_id).encode())
    finally:
        await producer.stop()
