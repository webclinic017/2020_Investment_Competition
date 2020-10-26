from helper_functions import write_financials
import finnhub

#finnhub_client = finnhub.Client(api_key="btts0j748v6ojt2hie60")
#print(finnhub_client.financials('AAPL', 'bs', 'ttm'))

#write_financials("Input/utilities_tickers.csv", "utilities_income.csv", 'ic', 'ttm')
#write_financials("Input/utilities_tickers.csv", "utilities_cashflows.csv", 'cf', 'ttm')
write_financials("Input/utilities_tickers.csv", "utilities_balance.csv", 'bs', 'annual')

