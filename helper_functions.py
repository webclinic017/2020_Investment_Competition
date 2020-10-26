import csv
import json
import finnhub
from metrics import *



def get_us_tickers(input_file_path, output_file_path):
    input_csv = open(input_file_path, "r", newline = '')
    output_csv = open(output_file_path, "w", newline = '')

    ticker_reader = csv.reader(input_csv, delimiter=' ', quotechar='|')
    ticker_writer = csv.writer(output_csv, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for row in ticker_reader:

        ticker_list = row[0].split(",")
        
        if(ticker_list[1] == '"New' or ticker_list[1] == "Nasdaq"):

            ticker_writer.writerow([ticker_list[0]])  




def write_financials(input_file_path, output_file_path, data = 'bs', time = 'annual'):

    # Setup client
    finnhub_client = finnhub.Client(api_key="btts0j748v6ojt2hie60")

    input_csv = open(input_file_path, "r", newline = '')
    output_csv = open(output_file_path, "w", newline = '')

    ticker_reader = csv.reader(input_csv, delimiter=' ', quotechar='|')
    csv_writer = csv.writer(output_csv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    if data == 'bs':
        
        # Writing headers of CSV file 
        csv_writer.writerow([
            SYMBOL,
            YEAR,
            PERIOD,
            ACCOUTNS_PAYABLE,
            ACCOUNTS_RECEIVABLES,
            ACCRUED_LIABILITY,
            ACCUMULATED_DEPRECIATION,
            CASH_EQUIVALENTS,
            CASH_SHORT_TERM_INVESTMENTS ,
            COMMON_STOCK,
            CURRENT_ASSETS,
            CURRENT_LIABILITIES,
            CURRENT_PORTION_LONG_TERM_DEBT,
            DEFERRED_INCOME_TAX,
            GOODWILL,
            INTANGIBLES_ASSETS,
            INVENTORY,
            LIABILITIES_SHAREHOLDERS_EQUITY,
            LONG_TERM_DEBT,
            LONG_TERM_INVESTMENTS,
            OTHER_CURRENT_ASSETS,
            OTHER_CURRENT_LIABILITIES,
            OTHER_EQUITY,
            OTHER_LIABILITIES,
            OTHER_LONG_TERM_ASSETS,
            OTHER_RECEIVABLES,
            PERIOD,
            PROPERTY_PLANT_EQUIPMENT,
            RETAINED_EARNINGS,
            SHARES_OUTSTANDING,
            SHORT_TERM_DEBT,
            SHORT_TERM_INVESTMENTS,
            TANGIBLE_BOOK_VALUE_PERSHARE,
            TOTAL_ASSETS,
            TOTAL_DEBT,
            TOTAL_EQUITY,
            TOTAL_LIABILITIES,
            TOTAL_LONG_TERM_DEBT,
            TOTAL_RECEIVABLES,
            TREASURY_STOCK
        ]) 

        # writing down companeis listed in input ticker csv file
        for ticker in ticker_reader:
            json_data = finnhub_client.financials(ticker, 'bs', time) # obtaining data from Finnhub API
            ticker = json_data[SYMBOL] # getting ticker
            
            # check if ticker is contained in database
            try:
                for year in json_data["financials"]:
                    csv_writer.writerow([
                        ticker,
                        getValue(year, YEAR),
                        getValue(year, PERIOD),
                        getValue(year, ACCOUTNS_PAYABLE),
                        getValue(year, ACCOUNTS_RECEIVABLES),
                        getValue(year, ACCRUED_LIABILITY),
                        getValue(year, ACCUMULATED_DEPRECIATION),
                        getValue(year, CASH_EQUIVALENTS),
                        getValue(year, CASH_SHORT_TERM_INVESTMENTS),
                        getValue(year, COMMON_STOCK),
                        getValue(year, CURRENT_ASSETS),
                        getValue(year, CURRENT_LIABILITIES),
                        getValue(year, CURRENT_PORTION_LONG_TERM_DEBT),
                        getValue(year, DEFERRED_INCOME_TAX),
                        getValue(year, GOODWILL),
                        getValue(year, INTANGIBLES_ASSETS),
                        getValue(year, INVENTORY),
                        getValue(year, LIABILITIES_SHAREHOLDERS_EQUITY),
                        getValue(year, LONG_TERM_DEBT),
                        getValue(year, LONG_TERM_INVESTMENTS),
                        getValue(year, OTHER_CURRENT_ASSETS),
                        getValue(year, OTHER_CURRENT_LIABILITIES),
                        getValue(year, OTHER_EQUITY),
                        getValue(year, OTHER_LIABILITIES),
                        getValue(year, OTHER_LONG_TERM_ASSETS),
                        getValue(year, OTHER_RECEIVABLES),
                        getValue(year, PERIOD),
                        getValue(year, PROPERTY_PLANT_EQUIPMENT),
                        getValue(year, RETAINED_EARNINGS),
                        getValue(year, SHARES_OUTSTANDING),
                        getValue(year, SHORT_TERM_DEBT),
                        getValue(year, SHORT_TERM_INVESTMENTS),
                        getValue(year, TANGIBLE_BOOK_VALUE_PERSHARE),
                        getValue(year, TOTAL_ASSETS),
                        getValue(year, TOTAL_DEBT),
                        getValue(year, TOTAL_EQUITY),
                        getValue(year, TOTAL_LIABILITIES),
                        getValue(year, TOTAL_LONG_TERM_DEBT),
                        getValue(year, TOTAL_RECEIVABLES),
                        getValue(year, TREASURY_STOCK)
                        ])
            except:
                print(ticker, ", not found")
    
    elif data == 'ic':
        
        # Writing headers of CSV file 
        csv_writer.writerow([
            SYMBOL,
            YEAR,
            PERIOD,
            COST_OF_GOODS_SOLD,
            DILUTED_AVERAGE_SHARES_OUTSTANDING,
            DILUTED_EPS,
            EBIT,
            GROSS_INCOME,
            INTEREST_INCOME_EXPENSE,
            NET_INCOME,
            NET_INCOME_AFTER_TAXES,
            PERIOD,
            PRETAX_INCOME,
            PROVISION_FOR_INCOME_TAXES,
            RESEARCH_DEVELOPMENT,
            REVENUE,
            SGA_EXPENSE,
            TOTAL_OPERATING_EXPENSE,
            TOTAL_OTHER_INCOME_EXPENSE_NET
        ])

        for ticker in ticker_reader:
            json_data = finnhub_client.financials(ticker, 'ic', time) # obtaining data from Finnhub API
            ticker = json_data[SYMBOL] # getting ticker
            
            # check if ticker is contained in database
            try:
                for section in json_data["financials"]:
                    csv_writer.writerow(
                        [ticker,
                        getValue(section, YEAR),
                        getValue(section, PERIOD),
                        getValue(section, COST_OF_GOODS_SOLD),
                        getValue(section, DILUTED_AVERAGE_SHARES_OUTSTANDING),
                        getValue(section, DILUTED_EPS),
                        getValue(section, EBIT),
                        getValue(section, GROSS_INCOME),
                        getValue(section, INTEREST_INCOME_EXPENSE),
                        getValue(section, NET_INCOME),
                        getValue(section, NET_INCOME_AFTER_TAXES),
                        getValue(section, PERIOD),
                        getValue(section, PRETAX_INCOME),
                        getValue(section, PROVISION_FOR_INCOME_TAXES),
                        getValue(section, RESEARCH_DEVELOPMENT),
                        getValue(section, REVENUE),
                        getValue(section, SGA_EXPENSE),
                        getValue(section, TOTAL_OPERATING_EXPENSE),
                        getValue(section, TOTAL_OTHER_INCOME_EXPENSE_NET)
                        ])
            except:
                print(ticker, ", not found")

    else:

        # Writing headers of CSV file 
        csv_writer.writerow([
            SYMBOL,
            YEAR,
            PERIOD,
            CAPEX,
            CASH_DIVIDENDS_PAID,
            CASH_INTEREST_PAID,
            CASH_TAXES_PAID,
            CHANGE_IN_CASH,
            CHANGES_IN_WORKING_CAPITAL,
            DEFERRED_TAXES_INVESTMENT_TAX_CREDIT,
            DEPRECIATION_AMORTIZATION,
            FOREIGN_EXCHANGE_EFFECTS,
            ISSUANCE_REDUCTION_CAPITAL_STOCK,
            ISSUANCE_REDUCTION_DEBT_NET,
            NET_CASH_FINANCING_ACTIVITIES,
            NET_INCOME_STARTING_LINE,
            NET_INVESTING_CASH_FLOW,
            NET_OPERATING_CASH_FLOW,
            OTHER_FUNDS_FINANCING_ITEMS,
            OTHER_FUNDS_NON_CASH_ITEMS,
            OTHER_INVESTING_CASH_FLOW_ITEMS_TOTAL
        ])

        for ticker in ticker_reader:
            json_data = finnhub_client.financials(ticker, 'cf', time) # obtaining data from Finnhub API
            ticker = json_data[SYMBOL] # getting ticker
            
            # check if ticker is contained in database
            try:
                for section in json_data["financials"]:
                    csv_writer.writerow(
                        [ticker,
                        getValue(section, YEAR),
                        getValue(section, PERIOD),
                        getValue(section, CAPEX),
                        getValue(section, CASH_DIVIDENDS_PAID),
                        getValue(section, CASH_INTEREST_PAID),
                        getValue(section, CASH_TAXES_PAID),
                        getValue(section, CHANGE_IN_CASH),
                        getValue(section, CHANGES_IN_WORKING_CAPITAL),
                        getValue(section, DEFERRED_TAXES_INVESTMENT_TAX_CREDIT),
                        getValue(section, DEPRECIATION_AMORTIZATION),
                        getValue(section, FOREIGN_EXCHANGE_EFFECTS),
                        getValue(section, ISSUANCE_REDUCTION_CAPITAL_STOCK),
                        getValue(section, ISSUANCE_REDUCTION_DEBT_NET),
                        getValue(section, NET_CASH_FINANCING_ACTIVITIES),
                        getValue(section, NET_INCOME_STARTING_LINE),
                        getValue(section, NET_INVESTING_CASH_FLOW),
                        getValue(section, NET_OPERATING_CASH_FLOW),
                        getValue(section, OTHER_FUNDS_FINANCING_ITEMS),
                        getValue(section, OTHER_FUNDS_NON_CASH_ITEMS),
                        getValue(section, OTHER_INVESTING_CASH_FLOW_ITEMS_TOTAL)
                    ])
            except:
                print(ticker, ", not found")



def getValue(list, metric):
    try:
        return list[metric]
    except:
        return None


