import time
import queue

from app.modules import *
from threading import Thread
from app.utils.OrderQueue import OrderQueue


# Extend the Thread class to create Threads for the Cooks.
class Cook(Thread):
    def __init__(self, cook_id, cook_rank, proficiency, *args, **kwargs):
        super(Cook, self).__init__(name=f'Cook-{cook_id}-{proficiency}', *args, **kwargs)
        self.cook_id = cook_id
        self.cook_rank = cook_rank

    
    # Overide the run() method of the Thread class.
    def run(self):
        while True:
            for complexity in range(self.cook_rank, 0, -1):
                self.handle_ca_food()
                OrderQueue.handle_ready_cooking_apparatus()

                try:
                    food = OrderQueue.rank_queue[f'Rank-{complexity}'].get(timeout=0.01*TIME_UNIT)
                    food['cook_id'] = self.cook_id

                    self.cook_food(food)
                except queue.Empty:
                    pass


    def handle_ca_food(self):
        for complexity in range(self.cook_rank, 0, -1):
            while True:
                try:
                    food = OrderQueue.requires_cooking_apparatus[f'Rank-{complexity}'].get(block=False)
                    food['cook_id'] = self.cook_id

                    OrderQueue.cooking_apparatus[food['cooking_apparatus']].put(food)
                except queue.Empty:
                    break


    def cook_food(self, food):
        preparation_time = restaurants.get(str(RESTAURANT_ID)).get(
            'menu').get(str(food["food_id"])).get('preparation-time')

        for _ in range(CTX_SWITCH_FACTOR):
            self.handle_ca_food()
            OrderQueue.handle_ready_cooking_apparatus()

            ctx_switch_time = preparation_time / CTX_SWITCH_FACTOR
            time.sleep(ctx_switch_time)

        OrderQueue.handle_ready_food(food)
