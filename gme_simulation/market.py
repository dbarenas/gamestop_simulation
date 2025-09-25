import asyncio
import math
from collections import deque
import config

class Order:
    def __init__(self, actor_id, side, size):
        self.actor_id = actor_id
        self.side = side  # 'buy', 'sell', or 'cover'
        self.size = size  # shares

class Market:
    def __init__(self):
        self.price = config.initial_price
        self.liquidity = config.liquidity
        self.k = config.price_impact_k
        self.order_queue = asyncio.Queue()
        self.price_history = []
        self.volume_history = []
        self.short_interest_history = []
        self.actor_pnl = {}
        self.return_window = deque(maxlen=50)
        self.buy_allowed = True
        self.time = 0
        self.short_shares = config.short_shares
        self.available_float = config.float_shares

    async def run_tick(self):
        buy_volume = 0
        sell_volume = 0
        orders = []

        while not self.order_queue.empty():
            order = self.order_queue.get_nowait()
            if order.side == 'buy' and not self.buy_allowed:
                continue
            orders.append(order)
            if order.side == 'buy' or order.side == 'cover':
                buy_volume += order.size
                if order.side == 'cover':
                    self.short_shares -= order.size
            else:
                sell_volume += order.size

        net_vol = buy_volume - sell_volume
        # print(f"Net volume: {net_vol}")
        log_return = self.k * (net_vol / self.liquidity)
        old_price = self.price
        self.price = self.price * math.exp(log_return)
        ret = math.log(self.price / old_price) if old_price > 0 else 0
        self.return_window.append(ret)

        # Log data for this tick
        self.price_history.append(self.price)
        self.volume_history.append({'buy': buy_volume, 'sell': sell_volume})
        self.short_interest_history.append(self.short_shares)

        self.time += 1

        return {'price': self.price, 'net_vol': net_vol, 'buys': buy_volume, 'sells': sell_volume}

    def get_realized_volatility(self):
        if len(self.return_window) < 2:
            return 0.0
        return (sum([(r)**2 for r in self.return_window]) / len(self.return_window))**0.5