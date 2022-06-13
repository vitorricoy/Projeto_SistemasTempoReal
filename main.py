from decimal import Decimal
from server.server import Server
from state.buy_request import BuyRequest
from state.client_data import ClientData
from state.sell_request import SellRequest
from state.state import GlobalState

def main():
    global_state = create_initial_state()

    server = Server(global_state)

    """
    Client1 wants to buy B for 50
    Client2 wants to sell B for 47
    Client3 wants to sell B for 49

    Client1 will buy B from Client2 for 50, because Client2's sell order arrived first.

    Client1 wants to sell C for 30
    Client2 wants to buy C for 30
    Client2 will buy C from Client1 for 30

    Final state will be:
    Client1(balance = 80, portfolio = ['STOCK_A', 'STOCK_B'])
    Client2(balance = 320, portfolio = ['STOCK_C'])
    Client3(balance = 1000, portfolio = ['STOCK_B'])
    """

    # "Phase 1": accept requests
    server.receive_request(BuyRequest('Client1', 'STOCK_B', Decimal(50)))
    server.receive_request(SellRequest('Client1', 'STOCK_C', Decimal(30)))
    server.receive_request(BuyRequest('Client2', 'STOCK_C', Decimal(30)))
    server.receive_request(SellRequest('Client2', 'STOCK_B', Decimal(47)))
    server.receive_request(SellRequest('Client3', 'STOCK_B', Decimal(49)))

    print('State before processing\n')
    print_clients_state(global_state)

    # "Phase 2": process requests
    server.process()

    print('\n\nState after processing\n')
    print_clients_state(global_state)

    print(server.current_prices())


def create_initial_state():
    global_state = GlobalState()
    global_state.clients_data['Client1'] = ClientData('Client1', 100, ['STOCK_A', 'STOCK_C'])
    global_state.clients_data['Client2'] = ClientData('Client2', 300, ['STOCK_B'])
    global_state.clients_data['Client3'] = ClientData('Client3', 1000, ['STOCK_B'])

    global_state.stock_prices['STOCK_A'] = Decimal(50)
    global_state.stock_prices['STOCK_B'] = Decimal(51)
    global_state.stock_prices['STOCK_C'] = Decimal(29)
    return global_state


def print_clients_state(global_state: GlobalState):
    for (id, data) in global_state.clients_data.items():
        print(f'Client Id={id}, balance={data.balance}, portfolio={data.portfolio}')


if __name__ == '__main__':
    main()
