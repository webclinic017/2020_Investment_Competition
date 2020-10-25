import csv
import json
import finnhub
from metrics import *

def write_financials(input_file_path, output_file_path):

    # Setup client
    finnhub_client = finnhub.Client(api_key="btts0j748v6ojt2hie60")

    input_csv = open(input_file_path, "r", newline = '')
    output_csv = open(output_file_path, "w", newline = '')

    ticker_reader = csv.reader(input_csv, delimiter=' ', quotechar='|')
    csv_writer = csv.writer(output_csv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    # Writing headers of CSV file 
    csv_writer.writerow(
        [SYMBOL,
        YEAR,
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

    for ticker in ticker_reader:
        json_data = finnhub_client.financials(ticker, 'bs', 'annual')
        ticker = json_data["symbol"]
        try:
        
            for year in json_data["financials"]:
                
                csv_writer.writerow(
                    [ticker,
                    getValue(year, YEAR),
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
                

def getValue(list, metric):
    try:
        return list[metric]
    except:
        return None


if __name__ == "__main__":
    write_financials("Input/tickers.csv", "aapl_fundamental_test.csv")
