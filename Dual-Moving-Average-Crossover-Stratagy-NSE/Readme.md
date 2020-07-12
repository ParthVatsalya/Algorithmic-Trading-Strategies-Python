# **Introduction**

The Dual Moving Average Crossover trading system uses two moving averages, one short and one long. The system trades when the short moving average crosses the long moving average.


# **How It Works**
The system optionally uses a stop based on Average True Range (ATR). If the ATR stop is used, the system will exit the market when that stop is hit.

If the ATR stop is not used, the Dual Moving Average Crossover system does not have an explicit stop and will always be in the market, making it a reversal system. It will exit a position only when the moving averages cross. At that point, it will exit and enter a new position in the opposite direction. In this case, the positions are sized based only on ATR using a custom money manager.

If an ATR stop is not used, then the entry risk is essentially infinite. This will cause the R-Multiples relatively meaningless since all gains will be less than the infinite risk of entering without any stop.
"""
