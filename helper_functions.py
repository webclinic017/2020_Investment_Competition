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




def write_financials(client, input_file_path, output_file_path, data = 'bs', time = 'annual'):

    # Setup client
    finnhub_client = client

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
                for section in json_data["financials"]:
                    csv_writer.writerow([
                        ticker,
                        getValue(section, YEAR),
                        getValue(section, PERIOD),
                        getValue(section, ACCOUTNS_PAYABLE),
                        getValue(section, ACCOUNTS_RECEIVABLES),
                        getValue(section, ACCRUED_LIABILITY),
                        getValue(section, ACCUMULATED_DEPRECIATION),
                        getValue(section, CASH_EQUIVALENTS),
                        getValue(section, CASH_SHORT_TERM_INVESTMENTS),
                        getValue(section, COMMON_STOCK),
                        getValue(section, CURRENT_ASSETS),
                        getValue(section, CURRENT_LIABILITIES),
                        getValue(section, CURRENT_PORTION_LONG_TERM_DEBT),
                        getValue(section, DEFERRED_INCOME_TAX),
                        getValue(section, GOODWILL),
                        getValue(section, INTANGIBLES_ASSETS),
                        getValue(section, INVENTORY),
                        getValue(section, LIABILITIES_SHAREHOLDERS_EQUITY),
                        getValue(section, LONG_TERM_DEBT),
                        getValue(section, LONG_TERM_INVESTMENTS),
                        getValue(section, OTHER_CURRENT_ASSETS),
                        getValue(section, OTHER_CURRENT_LIABILITIES),
                        getValue(section, OTHER_EQUITY),
                        getValue(section, OTHER_LIABILITIES),
                        getValue(section, OTHER_LONG_TERM_ASSETS),
                        getValue(section, OTHER_RECEIVABLES),
                        getValue(section, PERIOD),
                        getValue(section, PROPERTY_PLANT_EQUIPMENT),
                        getValue(section, RETAINED_EARNINGS),
                        getValue(section, SHARES_OUTSTANDING),
                        getValue(section, SHORT_TERM_DEBT),
                        getValue(section, SHORT_TERM_INVESTMENTS),
                        getValue(section, TANGIBLE_BOOK_VALUE_PERSHARE),
                        getValue(section, TOTAL_ASSETS),
                        getValue(section, TOTAL_DEBT),
                        getValue(section, TOTAL_EQUITY),
                        getValue(section, TOTAL_LIABILITIES),
                        getValue(section, TOTAL_LONG_TERM_DEBT),
                        getValue(section, TOTAL_RECEIVABLES),
                        getValue(section, TREASURY_STOCK)
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

def write_estimates(client, input_file_path, output_file_path, frequency = 'annual'):
    
    # Setup client
    finnhub_client = client

    input_csv = open(input_file_path, "r", newline = '')
    output_csv = open(output_file_path, "w", newline = '')

    ticker_reader = csv.reader(input_csv, delimiter=' ', quotechar='|')
    csv_writer = csv.writer(output_csv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    # Writing headers of CSV file 
    csv_writer.writerow([
        SYMBOL,
        PERIOD,
        NUMBER_ANALYSTS,
        REVENUE_AVG,
        REVENUE_HIGH,
        REVENUE_LOW
    ]) 

    # writing down companeis listed in input ticker csv file
    for ticker in ticker_reader:
        json_data = finnhub_client.company_revenue_estimates(ticker, frequency) # obtaining data from Finnhub API
        ticker = json_data[SYMBOL] # getting ticker
        
        # check if ticker is contained in database
        try:
            for section in json_data["data"]:
                csv_writer.writerow([
                    ticker,
                    getValue(section, PERIOD),
                    getValue(section, NUMBER_ANALYSTS),
                    getValue(section, REVENUE_AVG),
                    getValue(section, REVENUE_HIGH),
                    getValue(section, REVENUE_LOW)
                ])
        except:
            print(ticker, ", not found")

def write_basic_financials(client, input_file_path, output_file_path):
    
    # Setup client
    finnhub_client = client

    input_csv = open(input_file_path, "r", newline = '')
    output_csv = open(output_file_path, "w", newline = '')

    ticker_reader = csv.reader(input_csv, delimiter=' ', quotechar='|')
    csv_writer = csv.writer(output_csv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    # Writing headers of CSV file 
    csv_writer.writerow([
        SYMBOL,
        PE_BASIC_EXCL_EXTRA_TTM,
        PE_EXCL_EXTRA_ANNUAL,
        PE_EXCL_EXTRA_HIGH_TTM,
        PE_EXCL_EXTRA_TTM,
        PE_EXCL_LOW_TTM,
        PE_INCL_EXTRA_TTM,
        PE_NORMALIZED_ANNUAL
    ]) 

    # writing down companeis listed in input ticker csv file
    for ticker in ticker_reader:
        json_data = finnhub_client.company_basic_financials(ticker, 'all') # obtaining data from Finnhub API
        ticker = json_data[SYMBOL] # getting ticker
        section = json_data['metric']
        try:
            csv_writer.writerow([
                ticker,
                getValue(section, PE_BASIC_EXCL_EXTRA_TTM),
                getValue(section, PE_EXCL_EXTRA_ANNUAL),
                getValue(section, PE_EXCL_EXTRA_HIGH_TTM),
                getValue(section, PE_EXCL_EXTRA_TTM),
                getValue(section, PE_EXCL_LOW_TTM),
                getValue(section, PE_INCL_EXTRA_TTM),
                getValue(section, PE_NORMALIZED_ANNUAL)
            ])
        except:
            print(ticker, ", not found")


def getValue(list, metric):
    try:
        return list[metric]
    except:
        return None


