from random import uniform
import time
import numpy as np
from server.server import Server
from state.sell_request import SellRequest
from state.buy_request import BuyRequest
from state.state import GlobalState
from decimal import Decimal
from typing import Dict, List

class Client:
    def __init__(self, client_id: str, global_state: GlobalState, prefered_stocks : List[str], latency : Decimal, decision_time : Decimal, values_perceptions: Dict[str, Decimal], server: Server):
        self.global_state = global_state
        self.prefered_stocks = prefered_stocks
        self.latency = latency
        self.server = server
        self.client_id = client_id
        self.decision_time = decision_time
        self.values_perceptions = values_perceptions

    def run_stocks_evaluation(self):
        self.update_stock_prices()
        self.evaluate_stocks()

    def update_stock_prices(self):
        time.sleep(self.latency/1000)
        for _ in range(int(self.latency/100)):
            if self.check_for_interruption():
                return
            time.sleep(0.01)

    def register_lost_deadline(self):
        self.global_state.clients_data[self.client_id].lost_deadline += 1

    def check_for_interruption(self):
        if self.global_state.stop_threads:
            self.register_lost_deadline()
            return True
        return False

    def evaluate_stocks(self):
        for stock in self.prefered_stocks:
            if self.check_for_interruption():
                return
            self.global_state.state_mutex.acquire()
            price = self.global_state.stock_prices[stock]
            has_stock = self.client_id == 'Exchange' or stock in self.global_state.clients_data[self.client_id].portfolio

            perceived_value = self.global_state.stock_values[stock] + self.global_state.stock_values[stock] * self.values_perceptions[stock]
            self.global_state.state_mutex.release()
            for _ in range(int(self.decision_time/100)):
                if self.check_for_interruption():
                    return
                time.sleep(0.01)
            if self.check_for_interruption():
                return
            
            if self.global_state.clients_data[self.client_id].balance >= price and perceived_value > price:
                diff = abs(perceived_value - price)
                price_perturbation = np.random.beta(2, 5) * diff
                buy_price = perceived_value + price_perturbation
                print(f"{self.client_id} buying {stock} at {buy_price}")
                self.server.receive_request(BuyRequest(self.client_id, stock, buy_price))
            
            if has_stock and price >= perceived_value:
                diff = abs(perceived_value - price)
                price_perturbation = np.random.beta(2, 5) * diff
                sell_price = price - price_perturbation
                print(f"{self.client_id} selling {stock} at {sell_price}")
                self.server.receive_request(SellRequest(self.client_id, stock, sell_price))
    
    def wait_for_next_period(self):
        # TODO: use thread events to handle the synchronization of the different server periods
        pass