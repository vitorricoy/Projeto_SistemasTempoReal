from collections import defaultdict
from decimal import Decimal
from typing import Dict, List
from state.buy_request import BuyRequest
from state.request import Request
from state.sell_request import SellRequest
from state.state import GlobalState

class Server:
    def __init__(self, global_state: GlobalState):
        self.global_state = global_state
        self.index = 0
    
    def process(self):
        all_requests: List[Request] = self.global_state.buy_queue + self.global_state.sell_queue
        all_requests.sort(key=lambda req: req.index)

        prices = defaultdict(lambda: None)
        all_stock_prices = defaultdict(lambda: None)

        for request in all_requests:
            if self.check_for_interruption():
                return
            if request.ticker in prices:
                if request.type == 'BUY':
                    all_stock_prices[request.ticker].append(request.max_price)
                else:
                    all_stock_prices[request.ticker].append(request.min_price)
            else:
                if request.type == 'BUY':
                    all_stock_prices[request.ticker] = [request.max_price]
                else:
                    all_stock_prices[request.ticker] = [request.min_price]
        if self.check_for_interruption():
                return
        while len(all_requests) > 0:
            if self.check_for_interruption():
                return
            request = all_requests.pop(0)
            match = self.get_potential_match(request, all_requests)
            if match is None:
                # no match, nothing we can do
                continue
            else:
                if self.check_for_interruption():
                    return
                if request.type == 'BUY':
                    effective_price = request.max_price # Here the BUY price is chosen - could be the other way around
                    self.perform_buy_operation(effective_price, request, match)
                else:
                    effective_price = match.max_price # Here the BUY price is chosen - could be the other way around
                    self.perform_sell_operation(effective_price, request, match)
                
                if self.check_for_interruption():
                    return
                if request.ticker in prices:
                    prices[request.ticker] = min(prices[request.ticker], effective_price)
                else:
                    prices[request.ticker] = effective_price
                all_requests.remove(match)
            if self.check_for_interruption():
                    return
            self.update_prices(prices, all_stock_prices, list(self.global_state.stock_prices.keys()))
    
    def check_for_interruption(self):
        if self.global_state.stop_threads:
            self.register_lost_deadline()
            return True
        return False

    def update_prices(self, seen_prices: Dict[str, Decimal], all_seen_prices: Dict[str, List[Decimal]], stocks: List[str]):
        for stock in stocks:
            if stock in seen_prices:
                self.global_state.stock_prices[stock] = seen_prices[stock]
            elif stock in all_seen_prices:
                current_price = self.global_state.stock_prices[stock]
                delta = -1
                chosen_price = self.global_state.stock_prices[stock]
                for price in all_seen_prices[stock]:
                    if delta == -1 or abs(current_price - price) < delta:
                        delta = abs(current_price - price)
                        chosen_price = price
                self.global_state.stock_prices[stock] = chosen_price

    def register_lost_deadline(self):
        self.global_state.lost_server_deadlines += 1

    def perform_buy_operation(self, effective_price: Decimal, request: BuyRequest, match: SellRequest):
        buyer_id = request.client_id
        seller_id = match.client_id
        
        if seller_id == 'Exchange':
            buyer = self.global_state.clients_data[buyer_id]
            if buyer is None:
                return # Not found

            if buyer.can_buy(effective_price):
                print(buyer_id, 'bought stock', request.ticker, 'from client', seller_id, 'at price', effective_price)
                buyer.buy(effective_price, request.ticker)
        elif buyer_id == 'Exchange':
            seller = self.global_state.clients_data[seller_id]
            if seller is None:
                return # Not found

            if seller.can_sell(effective_price):
                print(buyer_id, 'bought stock', request.ticker, 'from client', seller_id, 'at price', effective_price)
                seller.sell(effective_price, request.ticker)
        else:
            buyer = self.global_state.clients_data[buyer_id]
            seller = self.global_state.clients_data[seller_id]
            if buyer is None or seller is None:
                return # Not found

            if buyer.can_buy(effective_price) and seller.can_sell(request.ticker):
                print(buyer_id, 'bought stock', request.ticker, 'from client', seller_id, 'at price', effective_price)
                seller.sell(effective_price, request.ticker)
                buyer.buy(effective_price, request.ticker)

    def perform_sell_operation(self, effective_price: Decimal, request: SellRequest, match: BuyRequest):
        seller_id = request.client_id
        buyer_id = match.client_id
        
        if seller_id == 'Exchange':
            buyer = self.global_state.clients_data[buyer_id]
            if buyer is None:
                return # Not found
            if buyer.can_buy(effective_price):
                print(buyer_id, 'bought stock', request.ticker, 'from client', seller_id, 'at price', effective_price)
                buyer.buy(effective_price, request.ticker)
        elif buyer_id == 'Exchange':
            seller = self.global_state.clients_data[seller_id]
            if seller is None:
                return # Not found

            if seller.can_sell(effective_price):
                print(buyer_id, 'bought stock', request.ticker, 'from client', seller_id, 'at price', effective_price)
                seller.sell(effective_price, request.ticker)
        else:
            seller = self.global_state.clients_data[seller_id]
            buyer = self.global_state.clients_data[buyer_id]

            if seller is None or buyer is None:
                return # Not found

            if buyer.can_buy(effective_price) and seller.can_sell(request.ticker):
                print(buyer_id, 'bought stock', request.ticker, 'from client', seller_id, 'at price', effective_price)
                seller.sell(effective_price, request.ticker)
                buyer.buy(effective_price, request.ticker)

    def get_potential_match(self, request: Request, all_requests: List[Request]):
        if request.type == 'BUY':
            return self.get_potential_buy_match(request, all_requests)
        else:
            return self.get_potential_sell_match(request, all_requests)

    def get_potential_buy_match(self, request: BuyRequest, all_requests: List[Request]):
        max_price_to_buy = request.max_price
        for other in all_requests:
            if request.client_id == other.client_id:
                continue
            if other.type == 'SELL' and other.ticker == request.ticker and other.min_price <= max_price_to_buy:
                return other
        
        return None

    def get_potential_sell_match(self, request: SellRequest, all_requests: List[Request]):
        min_price_to_sell = request.min_price
        for other in all_requests:
            if request.client_id == other.client_id:
                continue
            if other.type == 'BUY' and other.ticker == request.ticker and other.max_price >= min_price_to_sell:
                return other
        
        return None

    def receive_request(self, request):
        request.index = self.index
        self.global_state.state_mutex.acquire()
        if request.type == 'BUY':
            self.global_state.buy_queue.append(request)
        elif request.type == 'SELL':
            self.global_state.sell_queue.append(request)
        self.global_state.state_mutex.release()
        self.index += 1

    def current_prices(self) -> Dict[str, Decimal]:
        return self.global_state.stock_prices
