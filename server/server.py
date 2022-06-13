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

        while len(all_requests) > 0:
            request = all_requests.pop(0)
            match = self.get_potential_match(request, all_requests)
            if match is None:
                # no match, nothing we can do
                continue
            else:
                # TODO: maybe add locks?
                if request.type == 'BUY':
                    effective_price = request.max_price # Here the BUY price is chosen - could be the other way around
                    self.perform_buy_operation(effective_price, request, match)
                else:
                    effective_price = match.max_price # Here the BUY price is chosen - could be the other way around
                    self.perform_sell_operation(effective_price, request, match)
                
                prices[request.ticker] = effective_price
                all_requests.remove(match)
            
            self.update_prices(prices)
    
    def update_prices(self, seen_prices: Dict[str, Decimal]):
        # If necessary, we can calculate some sort of delta here for display purposes
        for (ticker, price) in seen_prices.items():
            self.global_state.stock_prices[ticker] = price

    def perform_buy_operation(self, effective_price: Decimal, request: BuyRequest, match: SellRequest):
        buyer_id = request.client_id
        seller_id = match.client_id
        
        buyer = self.global_state.clients_data[buyer_id]
        seller = self.global_state.clients_data[seller_id]
        if buyer is None or seller is None:
            print('none')
            return # Not found

        buyer.buy(effective_price, request.ticker)
        seller.sell(effective_price, request.ticker)

    def perform_sell_operation(self, effective_price: Decimal, request: SellRequest, match: BuyRequest):
        client_id = request.client_id
        other_client_id = match.client_id
        
        seller = self.global_state.clients_data[client_id]
        buyer = self.global_state.clients_data[other_client_id]
        if seller is None or buyer is None:
            print('none')
            return # Not found

        buyer.buy(effective_price, request.ticker)
        seller.sell(effective_price, request.ticker)

    def get_potential_match(self, request: Request, all_requests: List[Request]):
        if request.type == 'BUY':
            return self.get_potential_buy_match(request, all_requests)
        else:
            return self.get_potential_sell_match(request, all_requests)

    def get_potential_buy_match(self, request: BuyRequest, all_requests: List[Request]):
        max_price_to_buy = request.max_price
        for other in all_requests:
            if other.index == request.index:
                continue
            if other.type == 'SELL' and other.ticker == request.ticker and other.min_price <= max_price_to_buy:
                return other
        
        return None

    def get_potential_sell_match(self, request: SellRequest, all_requests: List[Request]):
        min_price_to_sell = request.min_price
        for other in all_requests:
            if other.index == request.index:
                continue
            if other.type == 'BUY' and other.ticker == request.ticker and other.max_price >= min_price_to_sell:
                return other
        
        return None

    def receive_request(self, request):
        request.index = self.index
        if request.type == 'BUY':
            self.global_state.buy_queue.append(request)
        elif request.type == 'SELL':
            self.global_state.sell_queue.append(request)
        
        self.index += 1

    def current_prices(self) -> Dict[str, Decimal]:
        return self.global_state.stock_prices