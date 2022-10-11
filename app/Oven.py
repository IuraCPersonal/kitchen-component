import time

from app.modules import *
from threading import Thread
from app.helpers.SafePriorityQueue import SafePriorityQueue

# Extend the Thread class to create Threads for the Cooks.
class Oven(Thread):
    def __init__(self, *args, **kwargs):
        super(Oven, self).__init__(*args, **kwargs)

    # Overide the run() method of the Thread class.
    def run(self):
        while True:
            food = SafePriorityQueue._oven_queue.get()

            time.sleep(FOOD[food['food_id']]['preparation-time'] * TIME_UNIT)

            SafePriorityQueue.food_cooked(food)