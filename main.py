# Importing QuantConnect Algorithm framework
from AlgorithmImports import *

class TrendFollowingAlgorithm(QCAlgorithm):
    
    def Initialize(self):
        # Set the start and end date for backtest
        self.SetStartDate(2020, 1, 1)  # Set start date
        self.SetEndDate(2023, 1, 1)    # Set end date

        # Set cash to trade
        self.SetCash(100000)  # Starting cash balance

        # Use higher data resolution for more frequent signals
        self.symbol = self.AddEquity("TSLA", Resolution.Hour).Symbol

        # Define parameters for moving averages (shortened for more signals)
        self.short_window = 10  # Shorter-term EMA for faster signals
        self.long_window = 50  # Long-term EMA to capture overall trend

        # Create exponential moving average indicators
        self.short_ema = self.EMA(self.symbol, self.short_window, Resolution.Hour)
        self.long_ema = self.EMA(self.symbol, self.long_window, Resolution.Hour)

        # Define thresholds for scaling positions
        self.initial_allocation = 0.2  # Start with 20% allocation
        self.max_allocation = 1  # Maximum allocation 100%
        self.step_allocation = 0.2  # Increase by 20% on each confirmation

        # Set flag to track position state
        self.invested = False

    def OnData(self, data):
        # Ensure we have price data and moving averages are ready
        if not data.ContainsKey(self.symbol) or not self.short_ema.IsReady or not self.long_ema.IsReady:
            return

        # Check if TSLA data is available
        tsla_data = data[self.symbol]
        if tsla_data is None or not tsla_data.Close:
            return  # Skip if no data is available

        # Get the current short and long moving average values
        short_ema_value = self.short_ema.Current.Value
        long_ema_value = self.long_ema.Current.Value
        price = tsla_data.Close  # Get the current price

        # Trading Logic:
        current_allocation = self.Portfolio[self.symbol].Invested  # Get current portfolio allocation for TSLA

        # Buy/Increase position if price > short-term EMA and short-term EMA > long-term EMA (trend strengthening)
        if price > short_ema_value and short_ema_value > long_ema_value:
            if current_allocation < self.max_allocation:
                # Increase allocation gradually (step by 20%)
                new_allocation = min(current_allocation + self.step_allocation, self.max_allocation)
                self.SetHoldings(self.symbol, new_allocation)
                self.invested = True
                self.Debug(f"BUY/INCREASE TSLA: {self.Time} Short EMA: {short_ema_value}, Long EMA: {long_ema_value}, Price: {price}")

        # Sell/Reduce position if short-term EMA < long-term EMA or price drops below short-term EMA
        elif price < short_ema_value or short_ema_value < long_ema_value:
            if current_allocation > 0:
                # Gradually decrease allocation (step by 20%)
                new_allocation = max(current_allocation - self.step_allocation, 0)
                self.SetHoldings(self.symbol, new_allocation)
                if new_allocation == 0:
                    self.invested = False
                self.Debug(f"SELL/DECREASE TSLA: {self.Time} Short EMA: {short_ema_value}, Long EMA: {long_ema_value}, Price: {price}")
    
    def OnEndOfDay(self, symbol):
        # End of day logging for analysis
        self.Debug(f"End of Day: {self.Time}, Holdings: {self.Portfolio[self.symbol].Quantity}")
