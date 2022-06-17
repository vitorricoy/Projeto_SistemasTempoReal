from decimal import Decimal
from glob import glob
import random
import threading
from client.client import Client
from server.server import Server
from state.buy_request import BuyRequest
from state.client_data import ClientData
from state.sell_request import SellRequest
from state.state import GlobalState
import PySimpleGUI as sg
import time

def read_parameters():
    # FIXME: Hard coded parameters to make debugging easier
    return {
        'balance': 100,
        'investors_num': 5,
        'perception_variation': 30,
        'maximum_latency': 200,
        'companies_num': 5,
        'request_period': 500,
        'process_period': 100,
        'number_of_stocks': 5
    }

    layout = [
        [sg.Text("Parâmetros para Execução do Algoritmo")], 
        [sg.Text("Patrimônio Inicial dos Investidores:"), sg.In(key="balance")],
        [sg.Text("Número de Investidores:"), sg.In(key="investors_num")],
        [sg.Text("Número de Empresas:"), sg.In(key="companies_num")],
        [sg.Text("Latência Máxima dos Clientes:"), sg.In(key="maximum_latency")],
        [sg.Text("Variação da Percepção dos Investidores:"), sg.In(key="perception_variation"), sg.Text("%")],
        [sg.Text("Duração do Período de Recebimento de Requests:"), sg.In(key="request_period"), sg.Text("ms")],
        [sg.Text("Duração do Período de Processamento das Requests:"), sg.In(key="process_period"), sg.Text("ms")],
        [sg.Button("Executar")]
    ]

    window = sg.Window("Projeto - Sistemas de Tempo Real", layout)

    values = []
    while True:
        event, values = window.read()
        sucesso = True
        print(event)
        if ('balance' in values and values['balance'] != '' and not values['balance'].isnumeric()):
            window['balance'].update('Digite um número')
            sucesso = False

        if ('investors_num' in values and values['investors_num'] != '' and not values['investors_num'].isnumeric()):
            window['investors_num'].update('Digite um número')
            sucesso = False

        if ('perception_variation' in values and values['perception_variation'] != '' and not values['perception_variation'].isnumeric()):
            window['perception_variation'].update('Digite um número')
            sucesso = False

        if ('maximum_latency' in values and values['maximum_latency'] != '' and not values['maximum_latency'].isnumeric()):
            window['maximum_latency'].update('Digite um número')
            sucesso = False

        if ('companies_num' in values and values['companies_num'] != '' and not values['companies_num'].isnumeric()):
            window['companies_num'].update('Digite um número')
            sucesso = False

        if ('request_period' in values and values['request_period'] != '' and not values['request_period'].isnumeric()):
            window['request_period'].update('Digite um número')
            sucesso = False

        if ('process_period' in values and values['process_period'] != '' and not values['process_period'].isnumeric()):
            window['process_period'].update('Digite um número')
            sucesso = False
        
        if (event == "Executar" or event == sg.WIN_CLOSED) and sucesso:
            break

    window.close()
    return values

def test():
    read_parameters()
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

    import matplotlib as mpl
    import matplotlib.pyplot as plt
    plt.plot([1,2,3,4], [1,4,2,3])
    plt.show()

def main():
    parameters = read_parameters()
    global_state = create_initial_state(parameters)

    server = Server(global_state)

    investors_num = int(parameters["investors_num"])

    companies = list(global_state.stock_prices.keys())

    perception_variation = float(parameters['perception_variation'])

    decision_times, perception_by_index = generate_decision_time_and_perceptions(investors_num, perception_variation)

    clients = []
    for i in range(investors_num):
        random.shuffle(companies)
        decision_time = decision_times[i]
        perception = perception_by_index[i]
        clients.append(Client('Client'+str(i), global_state, companies, random.uniform(1, int(parameters['maximum_latency']))/1000, decision_time, perception/1000, server))

    run_loop(clients, server, global_state, int(parameters['request_period']), int(parameters['process_period']), int(parameters['number_of_stocks']))

def run_loop(clients, server, global_state, request_period, process_period, number_of_stocks):
    for i in range(10):
        simulate_IPO(global_state, number_of_stocks)
        threads = []
        for client in clients:
            threads.append(threading.Thread(target = client.run_stocks_evaluation))
        global_state.stop_threads = False
        for thread in threads:
            thread.start()
        time.sleep(request_period/1000)
        global_state.stop_threads = True
        for thread in threads:
            thread.join()
        global_state.stop_threads = False
        thread = threading.Thread(target = server.process)
        thread.start()
        time.sleep(process_period/1000)
        global_state.stop_threads = True
        thread.join()
        global_state.buy_queue = []
        global_state.sell_queue = []
    print(global_state.clients_data)
    print(global_state.stock_prices)
    print(global_state.stock_values)
    print()

def simulate_IPO(global_state, number_of_stocks):
    for company in list(global_state.stock_prices.keys()):
        ocurrences = 0
        for client in list(global_state.clients_data.keys()):
            ocurrences += global_state.clients_data[client].portfolio.count(company)
        missing_ocurrences = number_of_stocks - ocurrences
        for _ in range(missing_ocurrences):
            global_state.sell_queue.append(SellRequest('Exchange', company, global_state.stock_values[company]))

def generate_decision_time_and_perceptions(investors_num, perception_variation):
    decision_times = [random.uniform(1, 1000)/1000 for _ in range(investors_num)]
    perceptions = [random.uniform(-perception_variation, perception_variation) for _ in range(investors_num)]
    perceptions.sort()
    sorted_decision_times = list(enumerate(decision_times))
    sorted_decision_times.sort(key= lambda x: x[1])
    mapping_index_perception_position = dict()
    for i in range(investors_num):
        mapping_index_perception_position[sorted_decision_times[i][0]] = i
    perception_by_index = [perceptions[mapping_index_perception_position[i]] for i in range(investors_num)]
    return decision_times, perception_by_index

def create_initial_state(parameters):
    global_state = GlobalState()
    investors_num = int(parameters["investors_num"])
    companies_num = int(parameters["companies_num"])
    starting_balance = int(parameters["balance"])

    for i in range(investors_num):
        client_name = 'Client' + str(i)
        global_state.clients_data[client_name] = ClientData(client_name, starting_balance, [])

    for i in range(companies_num):
        company_name = 'STOCK' + str(i)
        global_state.stock_prices[company_name] = random.uniform(starting_balance*0.05, starting_balance*0.2)
        global_state.stock_values[company_name] = global_state.stock_prices[company_name]

    return global_state


def print_clients_state(global_state: GlobalState):
    for (id, data) in global_state.clients_data.items():
        print(f'Client Id={id}, balance={data.balance}, portfolio={data.portfolio}')


if __name__ == '__main__':
    main()
