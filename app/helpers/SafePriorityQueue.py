import threading, queue, time, requests

from app.modules import *
from app.helpers.SafePrint import SafePrint

# https://superfastpython.com/thread-priority-queue/
class SafePriorityQueue:
    __lock = threading.Lock()
    __progress = {}
    __priority_queue = queue.PriorityQueue()

    __rank_queue = {
        'Rank-1': queue.Queue(),
        'Rank-2': queue.Queue(),
        'Rank-3': queue.Queue(),
    }

    __requires_cooking_aparatus = {
        'Rank-1': queue.Queue(),
        'Rank-2': queue.Queue(),
        'Rank-3': queue.Queue(),
    }

    _stove_queue = queue.Queue()
    _oven_queue = queue.Queue()

    @staticmethod
    def add_priority_queue(order):
        SafePriorityQueue.__priority_queue.put((order['priority'], order))
        SafePriorityQueue.adjoin()

    @staticmethod
    def adjoin():
        priority, order = SafePriorityQueue.__priority_queue.get()
        order['progress'] = []

        with SafePriorityQueue.__lock:
            SafePriorityQueue.__progress[order['order_id']] = order

        for food_id in order['items']:
            complexity = FOOD[food_id]['complexity']

            # Check if cooking aparatus is required.
            check = FOOD[food_id]['cooking-apparatus'] == None

            if check:
                SafePriorityQueue.__rank_queue[f'Rank-{complexity}'].put(
                    {
                        'food_id': food_id,
                        'order_id': order['order_id'],
                    }
                )
            else:
                SafePriorityQueue.__requires_cooking_aparatus[f'Rank-{complexity}'].put(
                    {
                        'food_id': food_id,
                        'order_id': order['order_id'],
                        'cooking_aparatus': FOOD[food_id]['cooking-apparatus']
                    }
                )

    @staticmethod
    def unload(rank):
        return SafePriorityQueue.__rank_queue[f'Rank-{rank}'].get()

    @staticmethod
    def ready(food):
        with SafePriorityQueue.__lock:
            # Get food from ORDER...
            cooking_order = SafePriorityQueue.__progress[food['order_id']]
            cooking_order['progress'].append(food)

            dishes_done = len(cooking_order['progress'])
            total_dishes = len(cooking_order['items'])

        SafePrint.log_prog(food["order_id"], dishes_done, total_dishes)

        if (total_dishes - dishes_done) == 0:
            # Order READY...
            cooking_order['cooking_time'] = time.time() - cooking_order['pick_up_time']
            cooks = set(str(food['cook_id']) for food in cooking_order['progress'])

            SafePrint.order_done(cooking_order, cooks)

            _ = requests.post(
                url=f'http://dining-hall:{DINING_HALL_PORT}/distribution',
                json=cooking_order
            )

    @staticmethod
    def get_requires_cooking_aparatus(cook_rank):
        SafePriorityQueue.__requires_cooking_aparatus[f'Rank-{cook_rank}'].get(block=False)