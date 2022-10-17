import json

from app import app
from flask import request
from app.helpers.Print import Print
from app.helpers.OrderQueue import OrderQueue


# Setup the 'order' endpoint.
@app.route('/order', methods=['POST'])
def order():
    content = request.get_json()
    OrderQueue.add_new_order(content)

    # DEBUG:
    Print.order_received(content)

    return json.dumps({'succes': True}), 200