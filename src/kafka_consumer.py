import asyncio
import time

from aiokafka import AIOKafkaConsumer

from core.config import KAFKA_TOPIC, KAFKA_BOOTSTRAP_SERVERS, UTF8
from work_emulator.utils import process_task


async def handle_message(message: str) -> None:
    task_id = int(message)
    await process_task(task_id)


async def worker():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="task_worker_group",
        enable_auto_commit=False
    )
    await consumer.start()

    try:
        print('Worker started. Waiting for messages...')
        async for message in consumer:
            await handle_message(message.value.decode(UTF8))
            await consumer.commit()
    finally:
        await consumer.stop()


if __name__ == '__main__':
    time.sleep(30)
    asyncio.run(worker())
