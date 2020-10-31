from helper_functions import get_us_tickers, write_financials, write_estimates, write_basic_financials
import finnhub

key1 = 'bucae7f48v6oa2u4ng20'
key2 = 'btts0j748v6ojt2hie60'

finnhub_client = finnhub.Client(api_key=key2)

#print(finnhub_client.financials('TEVA', 'bs', 'annual'))

sector = 'staples'

#=== TICKERS ===#
#get_us_tickers("Input/{}.csv".format(sector), "US_Tickers/{}.csv".format(sector))

#=== DATA ===#
write_financials(finnhub_client, "US_Tickers/{}.csv".format(sector), "Data/{}_income_annual.csv".format(sector), 'ic', 'annual')
#write_financials(finnhub_client, "US_Tickers/{}.csv".format(sector), "Data/{}_income_ttm.csv".format(sector), 'ic', 'annual')

#write_financials(finnhub_client, "US_Tickers/{}.csv".format(sector), "Data/{}_cashflows_annual.csv".format(sector), 'cf', 'annual')
#write_financials(finnhub_client, "US_Tickers/{}.csv".format(sector), "Data/{}_cashflows_ttm.csv".format(sector), 'cf', 'annual')

#write_basic_financials(finnhub_client, "US_Tickers/{}.csv".format(sector), "Data/{}_basic_financials.csv".format(sector))
#write_financials(finnhub_client, "US_Tickers/{}.csv".format(sector), "Data/{}_balance_annual.csv".format(sector), 'bs', 'annual')
#write_estimates(finnhub_client, "US_Tickers/{}.csv".format(sector), "Data/{}_estimates.csv".format(sector), "annual")
