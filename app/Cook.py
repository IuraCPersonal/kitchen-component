import time
import queue

from app.modules import *
from threading import Thread
from app.helpers.OrderQueue import OrderQueue


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
                # TODO: Find a better way to cook the foods. What food to cook first?
                while True:
                    try:
                        #TODO: Fix Priority Inversion in Order Queues.
                        food = OrderQueue.requires_cooking_apparatus[f'Rank-{complexity}'].get(block=False)
                        food['cook_id'] = self.cook_id

                        OrderQueue.cooking_apparatus[food['cooking_apparatus']].put(food)
                    except queue.Empty:
                        break

                OrderQueue.handle_ready_cooking_apparatus()

                try:
                    #TODO: Fix Priority Inversion in Order Queues.
                    food = OrderQueue.rank_queue[f'Rank-{complexity}'].get(timeout=0.01*TIME_UNIT)
                    food['cook_id'] = self.cook_id

                    self.cook_food(food)
                except queue.Empty:
                    pass
        
    def cook_food(self, food):
        preparation_time = FOOD[food['food_id']]['preparation-time'] * TIME_UNIT
        
        # TODO: Implement the context switching.
        ctx_switch_time = preparation_time / CTX_SWITCH_FACTOR
        time.sleep(ctx_switch_time)

        OrderQueue.handle_ready_food(food)
