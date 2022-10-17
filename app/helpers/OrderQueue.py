import time
import queue
import requests
import threading

from app.modules import *
from app.helpers.Print import Print


# https://superfastpython.com/thread-priority-queue/
class OrderQueue:
    lock = threading.Lock()

    progress = {}
    priority_queue = queue.PriorityQueue()
    ready_cooking_apparatus_queue = queue.Queue()

    rank_queue = {
        'Rank-1': queue.Queue(),
        'Rank-2': queue.Queue(),
        'Rank-3': queue.Queue(),
    }

    requires_cooking_apparatus = {
        'Rank-1': queue.Queue(),
        'Rank-2': queue.Queue(),
        'Rank-3': queue.Queue(),
    }

    cooking_apparatus = {
        'oven': queue.Queue(),
        'stove': queue.Queue()
    }

    @staticmethod
    def add_new_order(order):
        with OrderQueue.lock:
            OrderQueue.priority_queue.put((order['priority'], order))

        OrderQueue.handle_new_order()

    @staticmethod
    def handle_new_order():
        priority, order = OrderQueue.priority_queue.get()
        order['progress'] = []

        with OrderQueue.lock:
            OrderQueue.progress[order['order_id']] = order

        for food_id in order['items']:
            complexity = FOOD[food_id]['complexity']
            cooking_apparatus = FOOD[food_id]['cooking-apparatus']

            # Check if cooking aparatus is required.
            if cooking_apparatus == None:
                OrderQueue.rank_queue[f'Rank-{complexity}'].put(
                    {
                        'food_id': food_id,
                        'order_id': order['order_id'],
                    }
                )
            else:
                OrderQueue.requires_cooking_apparatus[f'Rank-{complexity}'].put(
                    {
                        'food_id': food_id,
                        'order_id': order['order_id'],
                        'cooking_apparatus': cooking_apparatus
                    }
                )

    @staticmethod
    def handle_ready_food(food):
        with OrderQueue.lock:
            # Get food from ORDER...
            cooking_order = OrderQueue.progress[food['order_id']]
            cooking_order['progress'].append(food)

            dishes_done = len(cooking_order['progress'])
            total_dishes = len(cooking_order['items'])

        Print.log_prog(food["order_id"], dishes_done, total_dishes)

        if (total_dishes - dishes_done) == 0:
            # Order READY...
            cooking_order['cooking_time'] = time.time() - \
                cooking_order['pick_up_time']
            cooks = set(str(food['cook_id'])
                        for food in cooking_order['progress'])

            Print.order_done(cooking_order, cooks)

            _ = requests.post(
                url=f'http://dining-hall:{DINING_HALL_PORT}/distribution',
                json=cooking_order
            )

    @staticmethod
    def handle_ready_cooking_apparatus(food=None):
        if food is not None:
            OrderQueue.ready_cooking_apparatus_queue.put(food)
        while True:
            try:
                food = OrderQueue.ready_cooking_apparatus_queue.get(block=False)
                OrderQueue.handle_ready_food(food)
            except queue.Empty:
                break
