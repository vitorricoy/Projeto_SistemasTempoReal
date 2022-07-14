import eel
import threading
import random

class ParametersInput:

    def __init__(self):
        self.parameters = {}

    def new_read_parameters(self):
        eel.init('parameters_interface')

        @eel.expose
        def set_values(values):
            self.parameters = values

        @eel.expose
        def get_parameters_and_random_client_data():
            decision_times = [random.uniform(1, self.parameters['max_client_processing_time'])/1000 for _ in range(self.parameters['investors_num'])]
            perceptions = [random.uniform(-self.parameters['perception_variation'], self.parameters['perception_variation']) for _ in range(self.parameters['investors_num'])]
            perceptions.sort(key=lambda x: abs(x))
            sorted_decision_times = list(enumerate(decision_times))
            sorted_decision_times.sort(key= lambda x: x[1])
            mapping_index_perception_position = dict()
            for i in range(self.parameters['investors_num']):
                mapping_index_perception_position[sorted_decision_times[i][0]] = i
            perception_by_index = [perceptions[mapping_index_perception_position[i]] for i in range(self.parameters['investors_num'])]
            latencies = [random.uniform(1, int(self.parameters['maximum_latency']))/1000 for _ in range(self.parameters['investors_num'])]
            return self.parameters, decision_times, perception_by_index, latencies

        def close_callback(route, websockets):
            print(route)
            if not websockets:
                thread = threading.Thread(target = lambda: eel.start('client-data.html', port=8001, close_callback=close_callback))
                thread.start()
                thread.join()
                exit()
        
        thread = threading.Thread(target = lambda: eel.start('index.html', close_callback=close_callback))
        thread.start()
        thread.join()
        print('Starting...')
        if not self.parameters:
            exit()
        return self.parameters

    def read_parameters(self):
        return {
            'balance': 100,
            'investors_num': 5,
            'perception_variation': 30,
            'maximum_latency': 10,
            'companies_num': 5,
            'request_period': 500,
            'process_period': 100,
            'number_of_stocks': 5,
            'max_client_processing_time': 5
        }
