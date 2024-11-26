from aio_pika import connect_robust, Message

from core.config import RABBITMQ_URL, RABBITMQ_QUEUE


async def send_task_to_rabbitmq(task_id: int) -> None:
    connection = await connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            Message(body=str(task_id).encode()),
            routing_key=RABBITMQ_QUEUE,
        )
