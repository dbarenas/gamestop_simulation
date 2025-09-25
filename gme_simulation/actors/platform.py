import asyncio
import config

class Platform:
    def __init__(self, market):
        self.market = market
        self.volatility_threshold = config.platform_volatility_threshold

    async def run(self):
        while True:
            volatility = self.market.get_realized_volatility()
            if volatility > self.volatility_threshold:
                self.market.buy_allowed = False
            else:
                # Restriction is lifted once volatility subsides
                self.market.buy_allowed = True

            await asyncio.sleep(0.01)