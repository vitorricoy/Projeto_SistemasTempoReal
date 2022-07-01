import random
import threading
from client.client import Client
from graphics import Graphics
from parameters_input import ParametersInput
from server.server import Server
from state import statistics
from state.client_data import ClientData
from state.sell_request import SellRequest
from state.state import GlobalState
import time

def main():
    parameters_input = ParametersInput()
    parameters = parameters_input.new_read_parameters()
    global_state = create_initial_state(parameters)

    server = Server(global_state)

    investors_num = int(parameters["investors_num"])

    companies = list(global_state.stock_prices.keys())

    perception_variation = float(parameters['perception_variation'])

    max_processing_time = float(parameters['max_client_processing_time'])

    decision_times, perception_by_index = generate_decision_time_and_perceptions(investors_num, perception_variation, max_processing_time)

    clients_id = []
    clients = []
    for i in range(investors_num):
        random.shuffle(companies)
        decision_time = decision_times[i]
        perception = perception_by_index[i]
        clients_id.append('Client'+str(i))
        clients.append(Client('Client'+str(i), global_state, companies, random.uniform(1, int(parameters['maximum_latency']))/1000, decision_time, perception/1000, server))

    # thread
    graphics = Graphics()
    thread = threading.Thread(target = graphics.plot_graph, args= (global_state, int(parameters['request_period']) + int(parameters['process_period']), companies, clients_id))
    thread.start()

    run_loop(clients, server, global_state, int(parameters['request_period']), int(parameters['process_period']), int(parameters['number_of_stocks']), float(parameters['stock_price_variation']))

def run_loop(clients, server, global_state, request_period, process_period, number_of_stocks, stock_price_variation):
    cont = 0
    while True:
        simulate_IPO(global_state, number_of_stocks)
        run_client_request_period(clients, request_period, global_state)
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
    global_state.stop_threads = True
    time.sleep(process_period/1000)
    thread.join()

def empty_order_queues(global_state):
    global_state.buy_queue = []
    global_state.sell_queue = []

def register_statistics(global_state):
    buy_orders = len(global_state.buy_queue)
    sell_orders = len(global_state.sell_queue)
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

def simulate_IPO(global_state, number_of_stocks):
    for company in list(global_state.stock_prices.keys()):
        ocurrences = 0
        for client in list(global_state.clients_data.keys()):
            ocurrences += global_state.clients_data[client].portfolio.count(company)
        missing_ocurrences = number_of_stocks - ocurrences
        for _ in range(missing_ocurrences):
            global_state.sell_queue.append(SellRequest('Exchange', company, global_state.stock_values[company]))

def generate_decision_time_and_perceptions(investors_num, perception_variation, max_processing_time):
    decision_times = [random.uniform(1, max_processing_time)/1000 for _ in range(investors_num)]
    perceptions = [random.uniform(-perception_variation, perception_variation) for _ in range(investors_num)]
    perceptions.sort(key=lambda x: abs(x))
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
        global_state.clients_data[client_name] = ClientData(client_name, starting_balance, 0, [])

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
