from typing import List
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

        while len(all_requests) > 0:
            request = all_requests.pop(0)
            print(f'looking at request {request.index}')
            match = self.get_potential_match(request, all_requests)
            if match is None:
                # no match
                continue # TODO: maybe persist this order for the next period
            else:
                print(f'request {request.index} matched with {match.index}')
                # TODO: maybe add locks?
                if request.type == 'BUY':
                    self.perform_buy_operation(request, match)
                else:
                    self.perform_sell_operation(request, match)

                all_requests.remove(match)

    def perform_buy_operation(self, request: BuyRequest, match: SellRequest):
        effective_price = request.max_price # Here the BUY price is chosen - could be the other way around
        buyer_id = request.client_id
        seller_id = match.client_id
        
        buyer = self.global_state.clients_data[buyer_id]
        seller = self.global_state.clients_data[seller_id]
        if buyer is None or seller is None:
            print('none')
            return # Not found

        buyer.buy(effective_price, request.ticker)
        seller.sell(effective_price, request.ticker)

    def perform_sell_operation(self, request: SellRequest, match: BuyRequest):
        effective_price = match.max_price # Here the BUY price is chosen - could be the other way around
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

    def current_prices(self):
        pass
