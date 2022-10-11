import json

from app import app
from flask import request
from app.helpers.SafePrint import SafePrint
from app.helpers.SafePriorityQueue import SafePriorityQueue

# Setup the 'order' endpoint.
@app.route('/order', methods=['POST'])
def order():
    content = request.get_json()

    SafePriorityQueue.add_priority_queue(content)

    # DEBUG:
    SafePrint.order_received(content)

    return json.dumps({'succes': True}), 200