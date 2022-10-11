import logging, random

from app.Cook import Cook

from app.modules import *
from flask import Flask
from threading import Thread

# Setup Flask and other dependencies.
app = Flask(__name__)

# Disable Flask console messages.
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

from app import routes

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

for index in range(1, AMOUNT_OF_COOKS + 1):
    for proficiency in range(COOKS[index]['proficiency']):
        cook = Cook(index, COOKS[index]['rank'], proficiency) 
        threads[cook.name] = cook

for index, thread in enumerate(threads.values()):
    thread.start()