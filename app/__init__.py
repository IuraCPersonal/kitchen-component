import sys
import logging
import requests

from flask import Flask
from threading import Thread

from app.modules import *
from app.Oven import Oven
from app.Cook import Cook
from app.Stove import Stove


# Disable Flask console messages and start messsage.
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

# Setup Flask and other dependencies.
app = Flask(__name__)

# Import flask routes.
from app import routes

# Register each Restaurant to the Aggregator.
_ = requests.post(
    url=f'http://restaurant-aggregator:7777/register',
    json={
        'restaurant_id': RESTAURANT_ID,
        'name': RESTAURANT_CFG[RESTAURANT_ID]['name'],
        'address': f'http://{RESTAURANT_CFG[RESTAURANT_ID]["HOST_NAME"]}:{RESTAURANT_CFG[RESTAURANT_ID]["DINING_HALL_PORT"]}',
        'menu_items': len(RESTAURANT_CFG[RESTAURANT_ID]['menu']),
        'menu': RESTAURANT_CFG[RESTAURANT_ID]['menu']
    }
)

# Create the FLASK thread.
threads['Flask'] = (
    Thread(
        name='Flask',
        target=lambda: app.run(
            host=HOST_NAME,
            port=KITCHEN_PORT,
            debug=False,
            use_reloader=False
        )
    )
)

# Create the STOVE threads.
for index in range(1, AMOUNT_OF_STOVES + 1):
    stove = Stove(index)
    threads[stove.name] = stove

# Create the OVEN threads.
for index in range(1, AMOUNT_OF_OVENS + 1):
    oven = Oven(index)
    threads[oven.name] = oven

# Create the COOK threads.
for index in range(1, AMOUNT_OF_COOKS + 1):
    # According to the PROFICIENCY - create same types of cooks X times.
    for proficiency in range(COOKS[index]['proficiency']):
        cook = Cook(index, COOKS[index]['rank'], proficiency) 
        threads[cook.name] = cook

# Start the threads.
for index, thread in enumerate(threads.values()):
    thread.start()