from helper_functions import write_financials, write_estimates, write_basic_financials
import finnhub

finnhub_client = finnhub.Client(api_key="bucae7f48v6oa2u4ng20")

#print(finnhub_client.quote("AAPL")["c"])
#print(finnhub_client.company_basic_financials('AAPL', 'all')['metric'])
#print(finnhub_client.company_revenue_estimates('TSLA', freq='annual'))

sector = 'staples'

#=== Cyclicals ===#
#write_financials(finnhub_client, "US_Tickers/{}.csv".format(sector), "Data/{}_income_annual.csv".format(sector), 'ic', 'annual')
#write_financials(finnhub_client, "US_Tickers/{}.csv".format(sector), "Data/{}_income_ttm.csv".format(sector), 'ic', 'annual')

#write_financials(finnhub_client, "US_Tickers/{}.csv".format(sector), "Data/{}_cashflows_annual.csv".format(sector), 'cf', 'annual')
#write_financials(finnhub_client, "US_Tickers/{}.csv".format(sector), "Data/{}_cashflows_ttm.csv".format(sector), 'cf', 'annual')

write_basic_financials(finnhub_client, "US_Tickers/{}.csv".format(sector), "Data/{}_basic_financials.csv".format(sector))
#write_financials(finnhub_client, "US_Tickers/{}.csv".format(sector), "Data/{}_balance_annual.csv".format(sector), 'bs', 'annual')
#write_estimates(finnhub_client, "US_Tickers/{}csv".format(sector), "Data/{}_estimates.csv".format(sector), "annual")


#=== Healthcare ===#
#write_financials("Input/healthcare.csv", "Data/healthcare_income_annual.csv", 'ic', 'annual')
#write_financials("Input/healthcare.csv", "Data/healthcare_income_ttm.csv", 'ic', 'annual')

#write_financials("Input/healthcare.csv", "Data/healthcare_cashflows_annual.csv", 'cf', 'annual')
#write_financials("Input/healthcare.csv", "Data/healthcare_cashflows_ttm.csv", 'cf', 'annual')

#write_financials("Input/healthcare.csv", "Data/healthcare_balance_annual.csv", 'bs', 'annual')
#write_estimates("Input/healthcare.csv", "Data/healthcare_estimates.csv", "annual")

#=== Technology ===#
#write_financials("Input/technology.csv", "Data/technology_income_annual.csv", 'ic', 'annual')
#write_financials("Input/technology.csv", "Data/technology_income_ttm.csv", 'ic', 'annual')

#write_financials("Input/technology.csv", "Data/technology_cashflows_annual.csv", 'cf', 'annual')
#write_financials("Input/technology.csv", "Data/technology_cashflows_ttm.csv", 'cf', 'annual')

#write_financials("Input/technology.csv", "Data/technology_balance_annual.csv", 'bs', 'annual')
#write_estimates("Input/technology.csv", "Data/technology_estimates.csv", "annual")

#=== Utilities===#
#write_financials("Input/utilities.csv", "Data/utilities_income_annual.csv", 'ic', 'annual')
#write_financials("Input/utilities.csv", "Data/utilities_income_ttm.csv", 'ic', 'annual')

#write_financials("Input/utilities.csv", "Data/utilities_cashflows_annual.csv", 'cf', 'annual')
#write_financials("Input/utilities.csv", "Data/utilities_cashflows_ttm.csv", 'cf', 'annual')

#write_financials("Input/utilities.csv", "Data/utilities_balance_annual.csv", 'bs', 'annual')
#write_estimates("Input/utilities.csv", "Data/utilities_estimates.csv", "annual")
