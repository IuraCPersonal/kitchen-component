import time
from threading import Thread

from app.modules import *
from app.utils.OrderQueue import OrderQueue


# Extend the Thread class to create Threads for the Cooks.
class Oven(Thread):
    def __init__(self, oven_id, *args, **kwargs):
        super(Oven, self).__init__(name=f'Oven-{oven_id}', *args, **kwargs)
    
    # Overide the run() method of the Thread class.
    def run(self):
        while True:
            food = OrderQueue.cooking_apparatus['oven'].get()

            time.sleep(restaurants.get(str(RESTAURANT_ID)).get('menu')
                        .get(str(food['food_id'])).get('preparation-time') / CTX_SWITCH_FACTOR * TIME_UNIT)

            OrderQueue.handle_ready_cooking_apparatus(food)
