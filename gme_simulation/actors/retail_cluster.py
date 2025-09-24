import asyncio
import random
from market import Order
import config

class RetailCluster:
    def __init__(self, market, id, media_hype_func):
        self.market = market
        self.id = id
        self.base_rate = config.retail_base_arrival_rate
        self.media_hype_func = media_hype_func
        self.holdings = []
        self.pnl = 0

    async def run(self):
        while True:
            # Current arrival rate is amplified by media hype
            current_arrival_rate = self.base_rate
            if self.media_hype_func():
                current_arrival_rate *= config.media_amplification_factor

            # FOMO effect if price is rising sharply
            if len(self.market.price_history) > 20:
                recent_prices = self.market.price_history[-20:]
                if self.market.price > recent_prices[0] * (1 + config.fomo_threshold_price_increase):
                     current_arrival_rate *= 2 # Double down on FOMO

            # Poisson process for buy orders
            if random.random() < (current_arrival_rate / 100.0):
                size = random.randint(1, 10)
                await self.market.order_queue.put(Order(self.id, 'buy', size))
                self.holdings.append({'entry_price': self.market.price, 'size': size})

            # Profit taking and stop loss
            for h in list(self.holdings):
                # Simple take profit / stop loss logic
                if self.market.price >= h['entry_price'] * 1.5: # 50% profit
                    await self.market.order_queue.put(Order(self.id, 'sell', h['size']))
                    self.pnl += (self.market.price - h['entry_price']) * h['size']
                    self.holdings.remove(h)
                elif self.market.price <= h['entry_price'] * 0.8: # 20% stop-loss
                    await self.market.order_queue.put(Order(self.id, 'sell', h['size']))
                    self.pnl += (self.market.price - h['entry_price']) * h['size']
                    self.holdings.remove(h)

            await asyncio.sleep(config.tick_duration)