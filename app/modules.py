import os, json, queue


# Function to read the content of a JSON file.
def read_json(file):    
    current_directory = os.getcwd()
    with open(f'./{current_directory}/data/{file}', 'r') as f:
        data = json.load(f)
    
    return data


threads = dict()
cooks = read_json('cooks.json').get('cooks')
restaurants = read_json('restaurants.json').get('restaurants')


HOST_NAME = os.getenv('HOST_NAME')
RESTAURANT_ID = os.getenv('RESTAURANT_ID')

KITCHEN_PORT = restaurants.get(str(RESTAURANT_ID)).get('kitchen-port')

TIME_UNIT = int(os.getenv('TIME_UNIT'))
CTX_SWITCH_FACTOR = int(os.getenv('CTX_SWITCH_FACTOR'))

AMOUNT_OF_COOKS = int(os.getenv('AMOUNT_OF_COOKS'))

AMOUNT_OF_STOVES = int(os.getenv('AMOUNT_OF_STOVES'))
AMOUNT_OF_OVENS = int(os.getenv('AMOUNT_OF_OVENS'))


