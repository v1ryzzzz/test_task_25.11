from aio_pika import connect_robust, Message
from aio_pika.exceptions import AMQPConnectionError
from core.config import RABBITMQ_URL, RABBITMQ_QUEUE
from logger.logger import logger


async def send_task_to_rabbitmq(task_id: int) -> None:
    try:
        connection = await connect_robust(RABBITMQ_URL)
        async with connection:
            channel = await connection.channel()
            await channel.default_exchange.publish(
                Message(body=str(task_id).encode()),
                routing_key=RABBITMQ_QUEUE,
            )
    except AMQPConnectionError as e:
        logger.error('Rabbitmq connection error: %s', e)
