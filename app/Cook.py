import time, queue

from app.modules import *
from threading import Thread
from app.helpers.SafePriorityQueue import SafePriorityQueue

# Extend the Thread class to create Threads for the Cooks.
class Cook(Thread):
    def __init__(self, cook_id, cook_rank, proficiency, *args, **kwargs):
        super(Cook, self).__init__(
            name=f'Cook-{cook_id}-{proficiency}', *args, **kwargs)
        self.cook_id = cook_id
        self.cook_rank = cook_rank

    # def distribute_food(self, food):
    #     while True:
    #         try:
    #             food = SafePriorityQueue.get_requires_cooking_aparatus(self.cook_rank)

    #             if food['cooking_aparatus'] == 'oven':
    #                 SafePriorityQueue._oven_queue.put(food)
    #             elif food['cooking_aparatus'] == 'stove':
    #                 SafePriorityQueue._stove_queue.put(food)
    #         except queue.Empty:
    #             break

    # Overide the run() method of the Thread class.
    def run(self):
        while True:
            food = SafePriorityQueue.unload(rank=self.cook_rank)
            food["cook_id"] = self.cook_id

            # self.distribute_food(food)

            time.sleep(FOOD[food['food_id']]['preparation-time'] * TIME_UNIT)

            SafePriorityQueue.ready(food)