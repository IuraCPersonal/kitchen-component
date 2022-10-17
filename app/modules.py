# Create a Thread-Safe Queue
threads = dict()

TIME_UNIT = 1

HOST_NAME = '0.0.0.0'
DINING_HALL_PORT = 8080
KITCHEN_PORT = 3000
KITCHEN_HOSTNAME = "localhost"

AMOUNT_OF_TABLES = 10
AMOUNT_OF_COOKS = 4

AMOUNT_OF_STOVES = 1
AMOUNT_OF_OVENS = 2

CTX_SWITCH_FACTOR = 5

FOOD = {
    1: {
        "id": 1,
        "name": "pizza",
        "preparation-time": 20,
        "complexity": 2,
        "cooking-apparatus": "oven"
    },
    2: {
        "id": 2,
        "name": "salad",
        "preparation-time": 10,
        "complexity": 1,
        "cooking-apparatus": None
    },
    3: {
        "id": 3,
        "name": "zeama",
        "preparation-time": 7,
        "complexity": 1,
        "cooking-apparatus": "stove"
    },
    4: {
        "id": 4,
        "name": "Scallop Sashimi with Meyer Lemon Confit",
        "preparation-time": 32,
        "complexity": 3,
        "cooking-apparatus": None
    },
    5: {
        "id": 5,
        "name": "Island Duck with Mulberry Mustard",
        "preparation-time": 35,
        "complexity": 3,
        "cooking-apparatus": "oven"
    },
    6: {
        "id": 6,
        "name": "Waffles",
        "preparation-time": 10,
        "complexity": 1,
        "cooking-apparatus": "stove"
    },
    7: {
        "id": 7,
        "name": "Aubergine",
        "preparation-time": 20,
        "complexity": 2,
        "cooking-apparatus": "oven"
    },
    8: {
        "id": 8,
        "name": "Lasagna",
        "preparation-time": 30,
        "complexity": 2,
        "cooking-apparatus": "oven"
    },
    9: {
        "id": 9,
        "name": "Burger",
        "preparation-time": 15,
        "complexity": 1,
        "cooking-apparatus": "stove"
    },
    10: {
        "id": 10,
        "name": "Gyros",
        "preparation-time": 15,
        "complexity": 1,
        "cooking-apparatus": None
    },
    11: {
        "id": 11,
        "name": "Kebab",
        "preparation-time": 15,
        "complexity": 1,
        "cooking-apparatus": None
    },
    12: {
        "id": 12,
        "name": "Unagi Maki",
        "preparation-time": 20,
        "complexity": 2,
        "cooking-apparatus": None
    },
    13: {
        "id": 13,
        "name": "Tobacco Chicken",
        "preparation-time": 30,
        "complexity": 2,
        "cooking-apparatus": "oven"
    }
}

COOKS = {
    1: {
        "rank": 3,
        "proficiency": 4,
        "name": None,
        "catchphrase": None
    },
    2: {
        "rank": 2,
        "proficiency": 3,
        "name": None,
        "catchphrase": None
    },
    3: {
        "rank": 2,
        "proficiency": 2,
        "name": None,
        "catchphrase": None
    },
    4: {
        "rank": 1,
        "proficiency": 2,
        "name": None,
        "catchphrase": None
    }
}
