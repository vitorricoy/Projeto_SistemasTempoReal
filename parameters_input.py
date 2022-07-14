import eel
import threading
import random

class ParametersInput:

    def __init__(self):
        self.parameters = {}
        self.client_data = {}
        self.company_data = {}

    def read_parameters(self):
        eel.init('parameters_interface')

        @eel.expose
        def set_values(values):
            self.parameters = values

        @eel.expose
        def set_client_data(values):
            self.client_data = values

        @eel.expose
        def set_company_data(values):
            self.company_data = values

        @eel.expose
        def get_parameters_and_random_client_data():
            decision_times = [round(random.uniform(1, self.parameters['max_client_processing_time']), 2) for _ in range(self.parameters['investors_num'])]
            perceptions = [round(random.uniform(-self.parameters['perception_variation'], self.parameters['perception_variation']), 2) for _ in range(self.parameters['investors_num'])]
            latencies = [round(random.uniform(1, int(self.parameters['maximum_latency'])), 2) for _ in range(self.parameters['investors_num'])]
            return self.parameters, decision_times, perceptions, latencies

        @eel.expose
        def get_parameters_and_prices():
            prices = [round(random.uniform(self.parameters['min_stock_value'], self.parameters['max_stock_value']), 2) for _ in range(self.parameters['companies_num'])]
            return self.parameters, prices

        def close_callback(route, websockets):
            if not websockets:
                if route == 'index.html':
                    if not self.parameters:
                        exit()
                    thread = threading.Thread(target = lambda: eel.start('client-data.html', port=8001, close_callback=close_callback))
                    thread.start()
                    thread.join()
                    exit()
                elif route == 'client-data.html':
                    if not self.parameters or not self.client_data:
                        exit()
                    thread = threading.Thread(target = lambda: eel.start('company-data.html', port=8002, close_callback=close_callback))
                    thread.start()
                    thread.join()
                    exit()
                else:
                    exit()
        
        thread = threading.Thread(target = lambda: eel.start('index.html', close_callback=close_callback))
        thread.start()
        thread.join()
        print('Starting...')
        if not self.parameters or not self.client_data or not self.company_data:
            exit()
        print(self.client_data)
        return self.parameters, self.client_data, self.company_data
