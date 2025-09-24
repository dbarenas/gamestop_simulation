import asyncio
import matplotlib.pyplot as plt
import config
from market import Market
from actors.hedge_fund import HedgeFund
from actors.retail_cluster import RetailCluster
from actors.media import Media
from actors.platform import Platform
from visualization import LiveChart

async def market_engine(market, ticks):
    for i in range(ticks):
        if i % 100 == 0: # Print progress
            print(f"Tick {i}/{ticks}, Price: ${market.price:.2f}")
        await market.run_tick()
        await asyncio.sleep(0.01) # A small delay to allow UI to update

async def main():
    market = Market()
    media = Media(market)

    # Actors
    hedge_fund = HedgeFund(market)
    retail_clusters = [RetailCluster(market, f"retail_{i}", media.is_hype) for i in range(10)] # 10 retail clusters
    platform = Platform(market)

    # Visualization
    chart = LiveChart(market)
    chart.non_blocking_show()

    # Spawn actor tasks
    actor_tasks = [
        asyncio.create_task(hedge_fund.run()),
        asyncio.create_task(media.run()),
        asyncio.create_task(platform.run()),
    ]
    for retail in retail_clusters:
        actor_tasks.append(asyncio.create_task(retail.run()))

    # Run the market engine
    engine_task = asyncio.create_task(market_engine(market, config.simulation_ticks))

    # Let the simulation run
    while not engine_task.done():
        chart.update(None)
        plt.pause(0.1) # Pause to allow plot to update
        await asyncio.sleep(0.1)

    # Cancel actor tasks once the simulation is done
    for task in actor_tasks:
        task.cancel()

    print("Simulation finished.")
    chart.update_final()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Simulation stopped by user.")