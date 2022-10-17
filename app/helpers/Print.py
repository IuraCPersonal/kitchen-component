import threading, time

from pprint import pprint
from progress.bar import Bar
from app.modules import FOOD
from colorama import init, Fore, Back, Style

class Print:
    __lock = threading.Lock()
    
    @staticmethod
    def log(text):
        with Print.__lock:
            print(f'[{Fore.GREEN}KN{Style.RESET_ALL}] {text}')

    @staticmethod
    def order_received(content):
        with Print.__lock:
            print(f'[{Fore.GREEN}KN{Style.RESET_ALL}] ORDER ({Fore.BLUE}{content["order_id"]}{Style.RESET_ALL}) received to KITCHEN. Cooking...')
            pprint(content)

    @staticmethod
    def log_prog(order_id, dishes_done, total_dishes):
        with Print.__lock:
            print(f'[{Fore.GREEN}KN{Style.RESET_ALL}] ORDER ({Fore.BLUE}{order_id}{Style.RESET_ALL}) progress: |' + '#' * dishes_done + '.' * (total_dishes - dishes_done) + f'| {dishes_done}/{total_dishes}')

    @staticmethod
    def order_done(cooking_order, cooks):
        with Print.__lock:
            print(f'[{Fore.GREEN}KN{Style.RESET_ALL}] ORDER ({Fore.BLUE}{cooking_order["order_id"]}{Style.RESET_ALL}) made by COOKS {Back.LIGHTRED_EX}{" ".join(cooks)}{Style.RESET_ALL} in TIME ({Fore.GREEN}{cooking_order["cooking_time"]}{Style.RESET_ALL}) was served to TABLE ({Fore.YELLOW}{cooking_order["table_id"]}{Style.RESET_ALL})')
    