from enum import Enum


class TaskStatus(str, Enum):
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'


class Broker(str, Enum):
    kafka = 'kafka'
    rabbitmq = 'rabbitmq'
