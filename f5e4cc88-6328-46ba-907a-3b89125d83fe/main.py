from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "AAPL"  # The asset to trade
        self.lookback_period = 30  # The SMA lookback period

    @property
    def assets(self):
        # Defines the assets this strategy is interested in
        return [self.ticker]

    @property
    def interval(self):
        # Data interval for price fetching; can adjust based on strategy requirements
        return "1day"

    def run(self, data):
        """
        Core logic of the trading strategy: compares the asset's latest price against its SMA.
        
        :param data: The data provided for the asset including price, volume etc.
        :return: TargetAllocation object with the desired asset allocation based on the strategy
        """
        # Calculate the SMA for the specified lookback period
        sma_values = SMA(self.ticker, data["ohlcv"], self.lookback_period)
        if sma_values is None:
            return TargetAllocation({})
        
        latest_close_price = data["ohlcv"][-1][self.ticker]["close"]
        latest_sma_value = sma_values[-1]
        
        allocation = 0
        # If the latest close price is above the SMA, we consider buying (allocation = 1),
        # otherwise, do not allocate funds to this asset (allocation = 0).
        if latest_close_price > latest_sma_value:
            allocation = 1  # signifies a buy decision
        else:
            allocation = 0  # signifies a sell or no-buy decision

        # Construct and return the allocation decision
        return TargetAllocation({self.ticker: allocation})