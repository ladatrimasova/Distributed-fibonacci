import json
import os
import redis

from DBCommunicator import DBCommunicator
from flask import Flask, request
from rq import Queue

USER_ID_KEY = "user_id"

app = Flask(__name__)

redis_url = os.getenv('REDISTOGO_URL', 'https://redis:6379')

conn = redis.from_url(redis_url)

dbc = DBCommunicator()

q = Queue(connection=conn)


@app.route("/get_and_inc_fib", methods=['PUT'])
def fib_inc():
    user_id = request.headers[USER_ID_KEY]
    dbc.insert_new_user_if_not_exists(user_id, 0, 0)
    fib_number, fib_value = dbc.get_user_fib_value(user_id)

    job = q.enqueue_call(
        func="worker.count_store_new_fib_value", args=(user_id,), result_ttl=5000
    )

    return json.dumps({"curr_fib_value": fib_value})


@app.route("/get_fib", methods=['GET'])
def fib_get():
    user_id = request.headers[USER_ID_KEY]
    dbc.insert_new_user_if_not_exists(user_id, 0, 0)
    fib_number, fib_value = dbc.get_user_fib_value(user_id)
    return json.dumps({"curr_fib_value": fib_value})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1234, debug=True, threaded=True)
1
