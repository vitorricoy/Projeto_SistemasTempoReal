from collections import defaultdict
from email.policy import default
from http import client
import random
import threading
from client.client import Client
from graphics import Graphics
from parameters_input import ParametersInput
from server.server import Server
from state import statistics
from state.buy_request import BuyRequest
from state.client_data import ClientData
from state.sell_request import SellRequest
from state.state import GlobalState
import time

def main():
    parameters_input = ParametersInput()
    parameters, client_data, company_data = parameters_input.read_parameters()
    global_state = create_initial_state(parameters, company_data, client_data)

    server = Server(global_state)

    investors_num = int(parameters["investors_num"])

    companies = list(global_state.stock_prices.keys())

    clients_id = []
    clients = []
    for i in range(investors_num):
        decision_time = client_data[i]['decision_time']
        values_perceptions = client_data[i]['values_perceptions']
        clients_id.append('Client'+str(i))
        clients.append(Client('Client'+str(i), global_state, client_data[i]['prefered_stocks'], client_data[i]['latency'], decision_time, values_perceptions, server))

    # thread
    graphics = Graphics()
    thread = threading.Thread(target = graphics.plot_graph, args= (global_state, int(parameters['request_period']) + int(parameters['process_period']), companies, clients_id))
    thread.start()

    run_loop(clients, server, global_state, int(parameters['request_period']), int(parameters['process_period']), int(parameters['number_of_stocks']), float(parameters['stock_price_variation']))

def run_loop(clients, server, global_state, request_period, process_period, number_of_stocks, stock_price_variation):
    cont = 0
    while True:
        run_client_request_period(clients, request_period, global_state)
        put_exchange_orders(global_state, number_of_stocks)
        print(global_state.stock_prices)
        run_server_process_period(server, process_period, global_state)
        register_statistics(global_state)
        empty_order_queues(global_state)
        if cont == 10:
            cont = 0
            handle_stock_price_variation(global_state, stock_price_variation)
        else:
            cont+=1

def handle_stock_price_variation(global_state, stock_price_variation):
    for company in list(global_state.stock_values.keys()):
        variation = random.uniform(-stock_price_variation, stock_price_variation)/100
        global_state.stock_values[company] *= (1+variation)


def run_server_process_period(server, process_period, global_state):
    global_state.stop_threads = False
    thread = threading.Thread(target = server.process)
    thread.start()
    time.sleep(process_period/1000)
    global_state.stop_threads = True
    thread.join()

def empty_order_queues(global_state):
    global_state.buy_queue = []
    global_state.sell_queue = []
    global_state.exchange_buy_requests = 0
    global_state.exchange_sell_requests = 0

def register_statistics(global_state):
    buy_orders = len(global_state.buy_queue) - global_state.exchange_buy_requests
    sell_orders = len(global_state.sell_queue) - global_state.exchange_sell_requests
    global_state.statistics = (statistics.Statistics(
            global_state.statistics.clients_data + [global_state.clients_data],
            global_state.statistics.lost_server_deadlines + [global_state.lost_server_deadlines], 
            global_state.statistics.buy_orders + [buy_orders], 
            global_state.statistics.sell_orders + [sell_orders], 
            global_state.statistics.stock_prices + [global_state.stock_prices], 
            global_state.statistics.stock_values + [global_state.stock_values])) 

def run_client_request_period(clients, request_period, global_state):
    threads = []
    global_state.stop_threads = False
    for client in clients:
        threads.append(threading.Thread(target = client.run_stocks_evaluation))
    for thread in threads:
        thread.start()
    time.sleep(request_period/1000)
    global_state.stop_threads = True
    for thread in threads:
        thread.join()

def put_exchange_orders(global_state, number_of_stocks):
    for company in list(global_state.stock_prices.keys()):
        ocurrences = 0
        for client in list(global_state.clients_data.keys()):
            ocurrences += global_state.clients_data[client].portfolio.count(company)
        missing_ocurrences = number_of_stocks - ocurrences
        for _ in range(missing_ocurrences):
            global_state.exchange_sell_requests += 1
            global_state.sell_queue.append(SellRequest('Exchange', company, global_state.stock_prices[company]))
    
    for company in list(global_state.stock_prices.keys()):
        num_orders = random.randint(0, number_of_stocks)
        for _ in range(num_orders):
            global_state.exchange_buy_requests += 1
            if random.random() < 0.5:
                global_state.buy_queue.append(BuyRequest('Exchange', company, global_state.stock_prices[company]))
            else:
                global_state.buy_queue.append(BuyRequest('Exchange', company, global_state.stock_values[company]))

def create_initial_state(parameters, company_data, client_data):
    global_state = GlobalState()
    investors_num = int(parameters["investors_num"])
    companies_num = int(parameters["companies_num"])
    num_of_stocks = int(parameters["number_of_stocks"])

    stock_quantity_division = defaultdict(int)
    for i in range(investors_num):
        client_portfolio = client_data[i]['portifolio']
        for stock in client_portfolio:
            stock_quantity_division[stock] += 1

    # Divide initial offer evenly to clients
    for stock in stock_quantity_division:
        stock_quantity_division[stock] = num_of_stocks // stock_quantity_division[stock]


    for i in range(investors_num):
        client_name = 'Client' + str(i)
        client_portfolio = client_data[i]['portifolio']
        real_portfolio = []
        for stock in client_portfolio:
            stocks = [stock] * stock_quantity_division[stock] # copy stock
            real_portfolio += stocks

        client_values_perceptions = client_data[i]['values_perceptions']
        global_state.clients_data[client_name] = ClientData(client_name, client_data[i]['balance'], 0, real_portfolio, client_values_perceptions)

    for i in range(companies_num):
        company_name = 'STOCK' + str(i)
        global_state.stock_prices[company_name] = company_data[i]['price']
        global_state.stock_values[company_name] = global_state.stock_prices[company_name]

    return global_state

    
if __name__ == '__main__':
    main()
