from helper_functions import write_financials, write_estimates
import finnhub

finnhub_client = finnhub.Client(api_key="bucae7f48v6oa2u4ng20")

print(finnhub_client.company_basic_financials('AAPL', 'cashRatio'))
#print(finnhub_client.company_revenue_estimates('TSLA', freq='annual'))

#write_financials("Input/cyclicals_tickers.csv", "utilities_income_annual.csv", 'ic', 'annual')
#write_financials("Input/cyclicals_tickers.csv", "utilities_income_ttm.csv", 'ic', 'annual')

#write_financials("Input/cyclicals_tickers.csv", "utilities_cashflows_annual.csv", 'cf', 'annual')
#write_financials("Input/cyclicals_tickers.csv", "utilities_cashflows_ttm.csv", 'cf', 'annual')

#write_financials("Input/cyclicals_tickers.csv", "utilities_balance_annual.csv", 'bs', 'annual')
#write_estimates("Input/cyclicals_tickers.csv", "utilities_estimates.csv", "annual")


