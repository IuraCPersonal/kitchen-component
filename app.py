import json
import time
import requests
import random
import logging

from modules import *
from threading import Thread
from flask import Flask, jsonify, redirect, url_for, request

app = Flask(__name__)
order_list = QueueWorker()

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/order', methods=['POST'])
def order():
    content = request.get_json()
    order_list.adjoin(content)

    # DEBUG:
    Format.log(f'Order {content["order_id"]} recieved. Time {content["pick_up_time"]}')

    return json.dumps({'succes': True}), 200


class Cook(Thread):
    def __init__(self, cook_id, *args, **kwargs):
        super(Cook, self).__init__(*args, **kwargs)
        self.cook_id = cook_id

    def prepare_order(self, order):
        time.sleep(random.randint(10, 16) * TIME_UNIT)
        order['about'] = [
            {
                'food_id': food_id,
                'cook_id': self.cook_id
            } for food_id in order['items']
        ]
        return order

    def run(self):
        while True:
            if order_list.is_empty():
                time.sleep(0.50 * TIME_UNIT)
                continue

            order = order_list.unload()
            order = self.prepare_order(order)

            r = requests.post(
                url=f'http://dining-hall:{DINING_HALL_PORT}/distribution',
                json=order
            )


if __name__ == '__main__':
    threads = list()

    threads.append(
        Thread(target=lambda: app.run(
            host=HOST_NAME,
            port=KITCHEN_PORT,
            debug=False,
            use_reloader=False
        ))
    )

    for index in range(1, AMOUNT_OF_COOKS + 1):
        cook = Cook(index)
        threads.append(cook)

    for index, thread in enumerate(threads):
        thread.start()
