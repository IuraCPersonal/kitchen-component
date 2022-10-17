import time
from threading import Thread

from app.modules import *
from app.helpers.OrderQueue import OrderQueue


# Extend the Thread class to create Threads for the Cooks.
class Stove(Thread):
    def __init__(self, stove_id, *args, **kwargs):
        super(Stove, self).__init__(name=f'Stove-{stove_id}', *args, **kwargs)

    # Overide the run() method of the Thread class.
    def run(self):
        while True:
            food = OrderQueue.cooking_apparatus['stove'].get()

            time.sleep(FOOD[food['food_id']]['preparation-time'] * TIME_UNIT)

            OrderQueue.handle_ready_cooking_apparatus(food)