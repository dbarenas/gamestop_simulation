import asyncio
from collections import deque
import config

class Media:
    def __init__(self, market):
        self.market = market
        self.hype = False
        self.hype_ticks = 0
        self.threshold = config.fomo_threshold_price_increase # Using fomo threshold for hype detection
        self.window = deque(maxlen=30) # Window of 30 ticks to check for hype

    async def run(self):
        while True:
            self.window.append(self.market.price)
            if len(self.window) >= 3:
                # Check for significant price increase
                if (self.window[-1] - self.window[0]) / (self.window[0] + 1e-9) > self.threshold:
                    self.hype = True
                    self.hype_ticks = 150 # Hype lasts for 150 ticks

            if self.hype and self.hype_ticks > 0:
                self.hype_ticks -= 1
            else:
                self.hype = False

            await asyncio.sleep(0.01)

    def is_hype(self):
        return self.hype