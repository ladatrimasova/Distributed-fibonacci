import numpy as np
import os
import redis

from DBCommunicator import DBCommunicator
from rq import Worker, Queue, Connection

listen = ['default']

redis_url = os.getenv('REDISTOGO_URL', 'http://redis:6379')
conn = redis.from_url(redis_url)

user_is_busy_key = "user {} is busy"

def count_fib(n):
    golden_ratio = (1 + np.sqrt(5)) / 2
    val = (golden_ratio ** n - (1 - golden_ratio) ** n) / np.sqrt(5)
    return int(round(val))

def count_store_new_fib_value(user_id):
    dbc = DBCommunicator()
    user_is_busy = True
    while user_is_busy:
        print(user_is_busy)
        p = conn.pipeline(transaction=True)
        user_is_busy = p.get(user_id)
        p.set(user_is_busy_key.format(user_id), True)
        fib_number, fib_value = dbc.get_user_fib_value(user_id)
        new_fib_number = fib_number + 1
        new_fib_value = count_fib(new_fib_number + 1)
        dbc.set_user_fib_value(user_id, new_fib_number, new_fib_value)
        p.set(user_is_busy_key.format(user_id), False)
        p.execute()

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
