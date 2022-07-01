import PySimpleGUI as sg

class ParametersInput:
    def read_parameters(self):
        # FIXME: Hard coded parameters to make debugging easier
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
