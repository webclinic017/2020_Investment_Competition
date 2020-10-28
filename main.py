import Analysis_Finnhub as analysis
import helper_functions as hf
import csv
import matplotlib.pyplot as plt
import finnhub
from docx import Document
from docx.shared import Inches


sector = 'staples'
key = "bucae7f48v6oa2u4ng20"

#===== FINNHUB CLIENT =====#
finnhub_client = finnhub.Client(api_key=key)

#===== US COMPANIES =====#
us_tickers = "US_Tickers/{}.csv".format(sector) # file path name
hf.get_us_tickers("Input/{}.csv".format(sector), us_tickers)

#document = Document()
#document.add_heading('Monte-Carlo Discounted Cash Flow Models', 0)

ana = analysis.Analysis_Finnhub(finnhub_client, "Data/{}_balance_annual.csv".format(sector), 
                                        "Data/{}_income_ttm.csv".format(sector), 
                                        "Data/{}_income_annual.csv".format(sector),
                                        "Data/{}_cashflows_ttm.csv".format(sector), 
                                        "Data/{}_cashflows_annual.csv".format(sector), 
                                        "Data/{}_estimates.csv".format(sector))

#=============== ANALYSIS ===============#
with open(us_tickers, "r", newline = '') as ticker_file:
    ticker_reader = csv.reader(ticker_file, delimiter=' ', quotechar='|')

    for row in ticker_reader:
        ticker = row[0]

        ana.buffett(ticker, "Output/output.csv")

"""
    document.add_heading("TICKER: {}".format(ticker), level=1)
    
    try:
        plt.hist(ana.monte_carlo_DCF(ticker), bins = 30, density = True, color = "r")
        image_path = "Images/{}.png".format(ticker)
        plt.savefig(image_path)
        document.add_picture(image_path, width=Inches(3.00))
        document.add_paragraph("\n\n")
        plt.clf()
    
    except:
        print("Something happened with", ticker)
        document.add_paragraph("Something wrong happened")
        plt.clf()

document.save("/Users/ezzatsuhaime/Desktop/dcf_monte_carlo.docx")

ticker_file.close()
"""