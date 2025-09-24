import asyncio
import random
from market import Order
import config

class HedgeFund:
    def __init__(self, market):
        self.market = market
        self.short_shares = config.short_shares
        self.entry_price = config.initial_price
        self.cover_threshold = config.hedge_cover_threshold_pct
        self.pnl = 0

    async def run(self):
        while True:
            unrealized_loss = (self.market.price - self.entry_price) * self.short_shares
            # A simple way to estimate collateral, could be more complex
            collateral = self.entry_price * self.short_shares
            loss_frac = unrealized_loss / (collateral + 1e-9)

            if loss_frac > self.cover_threshold:
                # Cover a fraction proportional to the loss severity
                cover_size = int(self.short_shares * min(0.05 + loss_frac, 0.2))
                if cover_size > 0:
                    await self.market.order_queue.put(Order('hedge', 'buy', cover_size))
                    # P&L is realized on covering
                    self.pnl -= (self.market.price - self.entry_price) * cover_size
                    self.short_shares -= cover_size


            await asyncio.sleep(config.tick_duration)