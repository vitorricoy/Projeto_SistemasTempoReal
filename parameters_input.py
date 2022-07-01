import eel
import threading


class ParametersInput:

    def __init__(self):
        self.parameters = {}

    def new_read_parameters(self):
        eel.init('parameters_interface')

        @eel.expose
        def set_values(values):
            self.parameters = values

        def close_callback(route, websockets):
            if not websockets:
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
