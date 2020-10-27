import Analysis_Finnhub as analysis
import csv
from docx import Document
from docx.shared import Inches
import matplotlib.pyplot as plt

document = Document()
document.add_heading('Monte-Carlo Discounted Cash Flow Models', 0)

with open("Input/utilities_tickers.csv", "r", newline = '') as ticker_file:
    
    ticker_reader = csv.reader(ticker_file, delimiter=' ', quotechar='|')
    ana = analysis.Analysis_Finnhub("utilities_balance.csv", "utilities_income.csv", "utilities_cashflows.csv", "utilities_estimates.csv")  

    for row in ticker_reader:

        ticker = row[0]
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