import decimal
from typing import Dict, List


class ClientData:
    def __init__(self, id: str, balance: decimal.Decimal, lost_deadline: int, initial_portfolio: List[str] = [],
        values_perceptions: Dict[str, decimal.Decimal] = {}) -> None:
        self.id = id
        self.balance = balance
        self.portfolio = initial_portfolio
        self.lost_deadline = lost_deadline
        self.values_perceptions = values_perceptions

    def can_buy(self, price: decimal.Decimal):
        if self.id == 'Exchange':
            return True
        return price <= self.balance

    def can_sell(self, ticker: str):
        if self.id == 'Exchange':
            return True
        return ticker in self.portfolio

    def buy(self, price: decimal.Decimal, ticker: str):
        if price > self.balance:
            raise Exception(f"client {self.id} with balance={self.balance} cant buy {ticker} for {price}")
        
        self.balance -= price
        self.portfolio.append(ticker)
    
    def sell(self, price: decimal.Decimal, ticker: str):
        if ticker not in self.portfolio:
            raise Exception(f"client {self.id} cant sell {ticker} because it doesnt own it. portfolio={self.portfolio}")
        
        self.balance += price
        self.portfolio.remove(ticker)

    def __repr__(self) -> str:
        return f'Id={self.id}, balance={self.balance}, portfolio={self.portfolio}'
