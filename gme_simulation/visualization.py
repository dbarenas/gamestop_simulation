import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import config

class LiveChart:
    def __init__(self, market):
        self.market = market
        self.fig, self.axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
        self.fig.suptitle('GameStop Short Squeeze Simulation')

        self.axs[0].set_ylabel('Price (USD)')
        self.axs[1].set_ylabel('Volume')
        self.axs[2].set_ylabel('Short Interest')
        self.axs[2].set_xlabel('Time (Ticks)')

        self.price_line, = self.axs[0].plot([], [], 'b-')
        self.buy_vol_bar = self.axs[1].bar([], [], color='g', alpha=0.6, label='Buy Volume')
        self.sell_vol_bar = self.axs[1].bar([], [], color='r', alpha=0.6, label='Sell Volume')
        self.short_int_line, = self.axs[2].plot([], [], 'k-')

        for ax in self.axs:
            ax.grid(True)
        self.axs[1].legend()

    def update(self, frame):
        ticks = range(len(self.market.price_history))
        prices = self.market.price_history

        buy_volumes = [v['buy'] for v in self.market.volume_history]
        sell_volumes = [v['sell'] for v in self.market.volume_history]

        short_interest = self.market.short_interest_history

        self.price_line.set_data(ticks, prices)

        # For bar charts, we need to re-create them
        self.axs[1].clear()
        self.axs[1].bar(ticks, buy_volumes, color='g', alpha=0.6, label='Buy Volume')
        self.axs[1].bar(ticks, [-s for s in sell_volumes], color='r', alpha=0.6, label='Sell Volume')
        self.axs[1].set_ylabel('Volume')
        self.axs[1].legend()

        self.short_int_line.set_data(ticks, short_interest)

        for ax in self.axs:
            ax.relim()
            ax.autoscale_view()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        return self.price_line, self.buy_vol_bar, self.sell_vol_bar, self.short_int_line

    def show(self):
        self.ani = animation.FuncAnimation(self.fig, self.update, blit=False, interval=100, save_count=config.simulation_ticks)
        plt.show(block=False)

    def non_blocking_show(self):
        plt.ion()
        plt.show()

    def update_final(self):
        self.update(None)
        plt.ioff()
        plt.show()