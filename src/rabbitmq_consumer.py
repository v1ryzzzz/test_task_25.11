import asyncio
import time

from aio_pika import connect_robust, IncomingMessage

from core.config import RABBITMQ_URL, RABBITMQ_QUEUE, UTF8
from work_emulator.utils import process_task


async def handle_message(message: IncomingMessage) -> None:
    async with message.process():
        task_id = int(message.body.decode(UTF8))
        await process_task(task_id)


async def worker():
    connection = await connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        queue = await channel.declare_queue(RABBITMQ_QUEUE, durable=True)
        await queue.consume(handle_message)

        print('Worker started. Waiting for messages...')
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(worker())
