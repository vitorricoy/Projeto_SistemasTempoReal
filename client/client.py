import time
import random
from server.server import Server
from state.sell_request import SellRequest
from state.buy_request import BuyRequest

class Client:
    def __init__(self, client_id: str, global_state: GlobalState, prefered_stocks : List[str], latency : Decimal, value_perception_modifier : Dict[str, Decimal], server: Server):
        self.global_state = global_state
        self.prefered_stocks = prefered_stocks
        self.latency = latency
        self.value_perception_modifier = value_perception_modifier
        self.server = server
        self.client_id = client_id

    def update_stock_prices(self):
        # The update happens on the global state list, so we only need to simulate the latency
        time.sleep(self.latency)

    def evaluate_stocks(self):
        for stock in self.prefered_stocks:
            price = self.global_state.stock_prices[stock]
            perceived_value = self.global_state.stock_values[stock] * value_perception_modifier[stock]
            #TODO: Maybe we can also implement a price history analysis for deciding to buy or sell
            price_perturbation = random.beta(2, 5) * abs(price - perceived_value)
            if perceived_value > price:
                # Should sell the current price minus a small variation with a certain probability
                sell_price = price - price_perturbation
                server.receive_request(SellRequest(self.client_id, stock, sell_price))
            else:
                # Should buy, paying the current price plus a small variation with a certain probability
                buy_price = price + price_perturbation
                server.receive_request(BuyRequest(self.client_id, stock, sell_price))
    
    def wait_for_next_period(self):
        # TODO: use thread events to handle the synchronization of the different server periods





    