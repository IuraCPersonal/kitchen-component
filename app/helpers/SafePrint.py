import threading
from pprint import pprint
from colorama import init, Fore, Back, Style

class SafePrint:
    __lock = threading.Lock()
    __green = '\033[32m'
    __lightgreen = '\033[92m'
    __blue = '\033[34m'
    __red = '\033[31m'
    __pink = '\033[95m'
    __yellow = '\033[93m'

    # @staticmethod
    # def log(text):
    #     with SafePrint.__lock:
    #         print(f' DH : {SafePrint.__lightgreen}{text}')
    
    @staticmethod
    def log(text):
        with SafePrint.__lock:
            print(f'[{Fore.GREEN}KN{Style.RESET_ALL}] {text}')

    @staticmethod
    def order_received(content):
        with SafePrint.__lock:
            print(f'[{Fore.GREEN}KN{Style.RESET_ALL}] ORDER ({Fore.BLUE}{content["order_id"]}{Style.RESET_ALL}) received to KITCHEN. Cooking...')
            pprint(content)


    @staticmethod
    def log_prog(order_id, dishes_done, total_dishes):
        with SafePrint.__lock:
            print(f'[{Fore.GREEN}KN{Style.RESET_ALL}] ORDER ({Fore.BLUE}{order_id}{Style.RESET_ALL}) progress: |' + '#' * dishes_done + '.' * (total_dishes - dishes_done) + f'| {dishes_done}/{total_dishes}')

    @staticmethod
    def order_done(cooking_order, cooks):
        with SafePrint.__lock:
            print(f'[{Fore.GREEN}KN{Style.RESET_ALL}] ORDER ({Fore.BLUE}{cooking_order["order_id"]}{Style.RESET_ALL}) made by COOKS {Back.LIGHTRED_EX}{" ".join(cooks)}{Style.RESET_ALL} in TIME ({Fore.GREEN}{cooking_order["cooking_time"]}{Style.RESET_ALL}) was served to TABLE ({Fore.YELLOW}{cooking_order["table_id"]}{Style.RESET_ALL})')