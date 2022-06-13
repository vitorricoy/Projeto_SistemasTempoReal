import decimal
from state.request import Request


class BuyRequest(Request):
    def __init__(self, client_id: str, ticker: str, max_price: decimal.Decimal):
        super().__init__('BUY', client_id, ticker)
        self.max_price = max_price
