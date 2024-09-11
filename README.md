Project Description: Trend-Following Algorithm for TSLA

This project implements a Trend-Following Algorithm for trading Tesla (TSLA) stock using the QuantConnect platform. The strategy employs a dual Exponential Moving Average (EMA) approach to capture trend signals and trade accordingly.
Key Features:

    Stock: The algorithm focuses on TSLA.
    Moving Averages:
        Short-term EMA: 10-period window.
        Long-term EMA: 50-period window.
    Data Resolution: The algorithm uses hourly data for more frequent trade signals.
    Trade Logic:
        Buy Signals: The algorithm opens or increases positions when the stock price is above the short-term EMA, and the short-term EMA is above the long-term EMA.
        Sell Signals: The algorithm reduces or closes positions if the stock price falls below the short-term EMA or if the short-term EMA falls below the long-term EMA.
    Position Scaling: Trades are incrementally adjusted with a step allocation of 20% to scale up or down based on trend confirmation.

Performance:

The strategy is designed to capture upward trends in TSLA stock while avoiding market downturns by exiting positions during bearish signals. The use of EMAs allows the algorithm to follow the overall market trend without relying on short-term price fluctuations.

This project is a foundation for exploring trend-following strategies and can be further optimized by adjusting parameters such as EMA windows, position scaling, and risk management rules.
