# 1 — Key parameters (suggested defaults)

initial_price = 15.0  # USD
float_shares = 70_000_000  # shares available
short_interest_ratio = 1.2  # 120% of float shorted
short_shares = float_shares * short_interest_ratio
liquidity = 100_000  # shares; larger → less price move for same net demand
price_impact_k = 0.01  # impact constant used in log-price model
tick_duration = 1  # unit time, e.g., 1 minute
simulation_ticks = 1000  # run length
retail_base_arrival_rate = 80.0  # expected buys per tick baseline
media_amplification_factor = 4.0  # multiplier to retail rate when media hype is on
hedge_cover_threshold_pct = 0.05  # hedges begin to cover after 5% loss of collateral
platform_volatility_threshold = 0.10  # 10% realized volatility over short window → restrict buys
fomo_threshold_price_increase = 0.05  # 5% price increase in short window triggers FOMO entry surge