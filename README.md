# GameStop (GME) Short Squeeze Simulation

This project is a Python-based simulation of the GameStop (GME) short squeeze event of early 2021. It uses an asynchronous, actor-based model to simulate the interactions between different market participants and the resulting price dynamics.

The simulation is for educational and research purposes to understand the mechanics of a short squeeze, feedback loops in financial markets, and the impact of platform interventions.

## Features

*   **Actor-Based Model:** Simulates different market participants with distinct behaviors:
    *   **Hedge Funds:** Start with a large short position and cover based on losses.
    *   **Retail Clusters:** Buy shares based on baseline rates, media hype, and FOMO.
    *   **Media/Social Media:** Amplifies retail interest when it detects strong price momentum.
    *   **Trading Platform:** Can halt buying activity based on extreme market volatility.
*   **Log-Price Impact Model:** Market price is updated based on net order volume, creating realistic, multiplicative price movements.
*   **Live Visualization:** Generates a real-time chart showing the price, trading volume, and short interest throughout the simulation.
*   **Configurable Parameters:** Easily tune the simulation's initial conditions and actor behaviors in a central `config.py` file.

## How It Works

The simulation runs in discrete time steps ("ticks"). At each tick, the actors (Hedge Funds, Retail Clusters, etc.) can submit buy or sell orders to a central `Market`. The market collects all orders, calculates the net volume, and updates the stock price using a price impact model.

Key events that drive the simulation:
1.  **Initial State:** Hedge funds hold a large short position.
2.  **Retail Buying:** Retail investors begin buying shares, causing the price to gradually increase.
3.  **Media Hype:** As the price momentum builds, a "media" actor triggers a hype cycle, dramatically increasing the rate of retail buying.
4.  **The Squeeze:** The rising price puts pressure on the short-selling hedge funds. As their losses mount, they are forced to buy back shares to cover their positions, pushing the price up even faster.
5.  **Platform Intervention:** The extreme price volatility triggers a "platform" actor to restrict buy orders.
6.  **Reversion:** With buying pressure removed, the price rapidly declines as investors sell their positions.

## Getting Started

Follow these instructions to get the simulation running on your local machine.

### Prerequisites

You will need Python 3.7+ and the following libraries:

*   `matplotlib`
*   `numpy`

You can install them using pip:

```bash
pip install matplotlib numpy
```

### Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd gme-simulation
    ```

### Running the Simulation

To run the simulation, simply execute the `simulation.py` script:

```bash
python gme_simulation/simulation.py
```

A window will appear showing the live-updating chart of the simulation. The console will print progress updates every 100 ticks.

## Output

The simulation produces a real-time plot with three charts:

1.  **Price (USD):** The market price of the stock over time.
2.  **Volume:** The number of shares bought (green) and sold (red) at each tick.
3.  **Short Interest:** The total number of shares held short by hedge funds.

![Simulation Chart Placeholder](httpsgme_simulation_chart.png)
*(Note: This is a placeholder image. Running the simulation will generate a live chart.)*

## Configuration

You can modify the simulation's parameters by editing the `gme_simulation/config.py` file. This file contains all the key variables, such as initial price, number of shares, actor behavior thresholds, and more.

```python
# gme_simulation/config.py

initial_price = 15.0
float_shares = 70_000_000
short_interest_ratio = 1.2
...
```

Feel free to experiment with these values to see how they affect the simulation's outcome.

## Disclaimer

This model is a stylized representation of market dynamics and omits many complexities of real-world financial markets. It is intended for educational purposes only and should not be considered financial advice.