import decimal
from typing import List, Dict

from state.client_data import ClientData


class Statistics:
    def __init__(self, clients_data: List[ClientData], lost_server_deadlines: List[int], buy_orders: List[decimal.Decimal], sell_orders: List[decimal.Decimal], stock_prices: List[Dict[str, decimal.Decimal]], stock_values: List[Dict[str, decimal.Decimal]]) -> None:
        self.clients_data = clients_data
        self.lost_server_deadlines = lost_server_deadlines
        self.buy_orders = buy_orders
        self.sell_orders = sell_orders
        self.stock_prices = stock_prices
        self.stock_values = stock_values

    def __repr__(self) -> str:
        return f'client data={self.clients_data}, lost server deadlines={self.lost_server_deadlines}, buy orders={self.buy_orders}, sell orders={self.sell_orders}, stock prices={self.stock_prices}, stock values={self.stock_values}'