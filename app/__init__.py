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
    for proficiency in range(cooks[f'{index}']['proficiency']):
        cook = Cook(index, cooks[f'{index}']['rank'], proficiency) 
        threads[cook.name] = cook


# Start the threads.
for index, thread in enumerate(threads.values()):
    thread.start()