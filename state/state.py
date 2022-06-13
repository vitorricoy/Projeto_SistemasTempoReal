from collections import defaultdict
from typing import Dict, List
from state.buy_request import BuyRequest
from state.client_data import ClientData
from state.sell_request import SellRequest


class GlobalState:
    def __init__(self):
        self.buy_queue: List[BuyRequest] = []
        self.sell_queue: List[SellRequest] = []
        self.clients_data: Dict[str, ClientData] = defaultdict(lambda: None)
