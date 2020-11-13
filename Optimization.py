from helper_functions import get_eod_prices
import pandas as pd
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier


tickers = ['TSN', 'VZ', 'AMGN']
output_file_path = "Output/prices.csv"
token = "949f9442cbdff3e5ad488d93280c0b92ef042449"


get_eod_prices(tickers, output_file_path, token)

with open(output_file_path, "r", newline = '') as price_sheet:
    prices_df = pd.read_csv(price_sheet)
    prices_df.set_index(['date'], inplace=True)

    mu = mean_historical_return(prices_df)
    S = CovarianceShrinkage(prices_df).ledoit_wolf()

    ef = EfficientFrontier(mu, S)
    weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    ef.save_weights_to_file("weights.txt")  # saves to file

    print(cleaned_weights)

    ef.portfolio_performance(verbose=True)