import time
import queue
import requests
import threading

from app.modules import *
from app.utils.Print import Print


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

        # menu = restaurants[f'{RESTAURANT_ID}']['menu']

        with OrderQueue.lock:
            OrderQueue.progress[order['order_id']] = order

        for food_id in order['items']:
            # complexity = restaurants[f'{RESTAURANT_ID}']['menu'][f'{food_id}']['complexity']
            # cooking_apparatus = restaurants[f'{RESTAURANT_ID}']['menu'][f'{food_id}']['cooking-apparatus']

            complexity = restaurants.get(str(RESTAURANT_ID)).get('menu').get(str(food_id)).get('complexity')
            cooking_apparatus = restaurants.get(str(RESTAURANT_ID)).get('menu').get(str(food_id)).get('cooking-apparatus')

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
            try:
                cooking_order['cooking_time'] = time.time() - \
                    cooking_order['pick_up_time']
            except KeyError:
                cooking_order['cooking_time'] = time.time() - \
                    cooking_order['registered_time']
                
            cooks = set(str(food['cook_id'])
                        for food in cooking_order['progress'])
            
            Print.order_done(cooking_order, cooks)

            DPORT = restaurants.get(str(RESTAURANT_ID)).get('dining-port')

            _ = requests.post(
                url=f'http://dining-hall-{RESTAURANT_ID}:{DPORT}/distribution',
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
