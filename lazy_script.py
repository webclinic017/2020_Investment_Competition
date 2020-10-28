from helper_functions import write_financials, write_estimates
import finnhub

finnhub_client = finnhub.Client(api_key="bucae7f48v6oa2u4ng20")
print(finnhub_client.quote("AAPL")["c"])
#print(finnhub_client.company_basic_financials('AAPL', 'cashRatio'))
#print(finnhub_client.company_revenue_estimates('TSLA', freq='annual'))

#=== Cyclicals ===#
#write_financials("Input/cyclicals.csv", "Data/cyclicals_income_annual.csv", 'ic', 'annual')
#write_financials("Input/cyclicals.csv", "Data/cyclicals_income_ttm.csv", 'ic', 'annual')

#write_financials("Input/cyclicals.csv", "Data/cyclicals_cashflows_annual.csv", 'cf', 'annual')
#write_financials("Input/cyclicals.csv", "Data/cyclicals_cashflows_ttm.csv", 'cf', 'annual')

#write_financials("Input/cyclicals.csv", "Data/cyclicals_balance_annual.csv", 'bs', 'annual')
#write_estimates("Input/cyclicals.csv", "Data/cyclicals_estimates.csv", "annual")

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
