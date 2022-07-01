from matplotlib import pyplot as plt
import matplotlib
from matplotlib.animation import FuncAnimation
import time

class Graphics:
    def plot_graph(self, global_state, period, companies_list, clients_list):
        cmap = matplotlib.cm.get_cmap('Spectral')
        total = 3 + len(companies_list) + len(clients_list)

        x_data = []
        y00_data = []
        y01_data = []
        y02_data = []
        y10_data = []
        y11_data = []
        y12_data = []
        y20_data = []
        y21_data = []
        y22_data = []

        for _ in clients_list:
            y00_data.append([])
            y01_data.append([])
            y02_data.append([])
            y10_data.append([])
        
        for _ in companies_list:
            y20_data.append([])
            y21_data.append([])
        starting_time = round(time.time())

        x_upper_lim = 20
        x_lower_lim = 0
        
        fig, ax = plt.subplots(3, 3)

        ax[0,0].set_xlim(x_lower_lim, x_upper_lim)
        ax[0,1].set_xlim(x_lower_lim, x_upper_lim)
        ax[0,2].set_xlim(x_lower_lim, x_upper_lim)
        ax[1,0].set_xlim(x_lower_lim, x_upper_lim)
        ax[1,1].set_xlim(x_lower_lim, x_upper_lim)
        ax[1,2].set_xlim(x_lower_lim, x_upper_lim)
        ax[2,0].set_xlim(x_lower_lim, x_upper_lim)
        ax[2,1].set_xlim(x_lower_lim, x_upper_lim)
        ax[2,2].set_xlim(x_lower_lim, x_upper_lim)

        for i, client in enumerate(clients_list):
            ax[0,0].plot(0, 0, label=client, color=cmap(i/total))
            ax[0,1].plot(0, 0, label=client, color=cmap(i/total))
            ax[0,2].plot(0, 0, label=client, color=cmap(i/total))
            ax[1,0].plot(0, 0, label=client, color=cmap(i/total))
        ax[2,2].plot(0, 0, color=cmap(0))

        ax[1,1].plot(0, 0, color=cmap(total-1))
        ax[1,2].plot(0, 0, color=cmap(total-2))
        for i, company in enumerate(companies_list):
            ax[2,0].plot(0, 0, label=company, color=cmap((len(clients_list) + i)/total))
            ax[2,1].plot(0, 0, label=company, color=cmap((len(clients_list) + i)/total))

        ax[0,0].set_title("Balance")
        ax[0,1].set_title("Portfolio Value")
        ax[0,2].set_title("Wealth")
        ax[1,0].set_title("Client Lost Deadlines")
        ax[1,1].set_title("Buy Orders")
        ax[1,2].set_title("Sell Orders")
        ax[2,0].set_title("Stock Prices")
        ax[2,1].set_title("Stock Values")
        ax[2,2].set_title("Server Lost Deadlines")

        ax[0,0].legend(loc="upper right")
        ax[0,1].legend(loc="upper right")
        ax[0,2].legend(loc="upper right")
        ax[1,0].legend(loc="upper right")
        ax[1,1].legend(loc="upper right")
        ax[1,2].legend(loc="upper right")
        ax[2,0].legend(loc="upper right")
        ax[2,1].legend(loc="upper right")

        def animation_frame(i):
            nonlocal x_upper_lim, x_lower_lim
            x_data.append(time.time() - starting_time)

            y22_data.append(0 if len(global_state.statistics.lost_server_deadlines) == 0 else global_state.statistics.lost_server_deadlines[-1])

            for i, client in enumerate(clients_list):
                balance = 0 if len(global_state.statistics.clients_data) == 0 else global_state.statistics.clients_data[-1][client].balance
                portfolio = 0 if len(global_state.statistics.clients_data) == 0 else sum([global_state.statistics.stock_prices[-1][stock] for stock in global_state.statistics.clients_data[-1][client].portfolio])
                lost_deadline = 0 if len(global_state.statistics.clients_data) == 0 else global_state.statistics.clients_data[-1][client].lost_deadline

                # balance
                y00_data[i].append(balance)
                
                # porfolio total value
                y01_data[i].append(portfolio)
                
                # total wealth
                y02_data[i].append(balance + portfolio)

                # lost deadlines
                y10_data[i].append(lost_deadline)
            
            # buy orders
            y11_data.append(0 if len(global_state.statistics.buy_orders) == 0 else global_state.statistics.buy_orders[-1])
            
            # sell orders
            y12_data.append(0 if len(global_state.statistics.sell_orders) == 0 else global_state.statistics.sell_orders[-1])
            
            for i, company in enumerate(companies_list):
                # stock prices
                y20_data[i].append(0 if len(global_state.statistics.stock_prices) == 0 else global_state.statistics.stock_prices[-1][company])
                
                # stock values
                y21_data[i].append(0 if len(global_state.statistics.stock_values) == 0 else global_state.statistics.stock_values[-1][company])

            if(len(x_data) > 0 and x_data[-1] >= x_upper_lim):
                x_upper_lim += (period / 1000)
                x_lower_lim += (period / 1000)
                ax[0,0].set_xlim(x_lower_lim, x_upper_lim)
                ax[0,1].set_xlim(x_lower_lim, x_upper_lim)
                ax[0,2].set_xlim(x_lower_lim, x_upper_lim)
                ax[1,0].set_xlim(x_lower_lim, x_upper_lim)
                ax[1,1].set_xlim(x_lower_lim, x_upper_lim)
                ax[1,2].set_xlim(x_lower_lim, x_upper_lim)
                ax[2,0].set_xlim(x_lower_lim, x_upper_lim)
                ax[2,1].set_xlim(x_lower_lim, x_upper_lim)

            for i, client in enumerate(clients_list):
                ax[0,0].plot(x_data, y00_data[i], label=client, color=cmap(i/total))    
                ax[0,1].plot(x_data, y01_data[i], label=client, color=cmap(i/total))    
                ax[0,2].plot(x_data, y02_data[i], label=client, color=cmap(i/total))    
                ax[1,0].plot(x_data, y10_data[i], label=client, color=cmap(i/total))    
                
            ax[1,1].plot(x_data, y11_data, color=cmap(total-1))
            ax[1,2].plot(x_data, y12_data, color=cmap(total-2))
            for i, company in enumerate(companies_list):
                ax[2,0].plot(x_data, y20_data[i], label=company, color=cmap((len(clients_list) + i)/total))    
                ax[2,1].plot(x_data, y21_data[i], label=company, color=cmap((len(clients_list) + i)/total))
            ax[2,2].plot(x_data, y22_data, color=cmap(0))

        anim = FuncAnimation(fig, animation_frame, interval = period, repeat = False, blit = False)
        plt.show()