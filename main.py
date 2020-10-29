import Analysis_Finnhub as analysis
import helper_functions as hf
import csv
import matplotlib.pyplot as plt
import finnhub
from docx import Document
from docx.shared import Inches

#===== INPUT PARAMETERS =====#
sector = 'staples'
key = "bucae7f48v6oa2u4ng20"

buffett_url = "/Users/ezzatsuhaime/Desktop/dcf_{}.csv".format(sector)
dcf_url = "/Users/ezzatsuhaime/Desktop/dcf_{}.docx".format(sector)


#===== FINNHUB CLIENT =====#
finnhub_client = finnhub.Client(api_key=key)

#===== US COMPANIES =====#
us_tickers = "US_Tickers/{}.csv".format(sector) # file path name
hf.get_us_tickers("Input/{}.csv".format(sector), us_tickers)

#===== FILES =====#
output_f = open(buffett_url, 'w', newline = '')
csv_writer = csv.writer(output_f)

document = Document()
document.add_heading('Monte-Carlo Discounted Cash Flow Models', 0)

#===== ANALYSIS CLASS =====#
ana = analysis.Analysis_Finnhub(finnhub_client, "Data/{}_balance_annual.csv".format(sector), 
                                        "Data/{}_income_ttm.csv".format(sector), 
                                        "Data/{}_income_annual.csv".format(sector),
                                        "Data/{}_cashflows_ttm.csv".format(sector), 
                                        "Data/{}_cashflows_annual.csv".format(sector), 
                                        "Data/{}_basic_financials.csv".format(sector),
                                        "Data/{}_estimates.csv".format(sector))


#=============== ANALYSIS ===============#
with open(us_tickers, "r", newline = '') as ticker_file:
    ticker_reader = csv.reader(ticker_file, delimiter=' ', quotechar='|')
    
    csv_writer.writerow(["Ticker", "N", "R-COEFF ROE", 'R-COEFF EPS', "EPS 1", "EPS 2", "CAGR EPS", "PE MIN", "PE MAX", "P AGR MIN", "P AGR MAX"])

    for row in ticker_reader:   
        ticker = row[0] # ticker
        
        data_array = ana.buffett(ticker) # get Buffett analysis
        
        if(data_array is not None):
            
            if(data_array[9] > 0):
                document.add_heading("TICKER: {}".format(ticker), level=1)
                csv_writer.writerow(data_array)
                
                try:
                    plt.hist(ana.monte_carlo_DCF(ticker), bins = 30, density = True, color = "r")
                    image_path = "Images/{}.png".format(ticker)
                    plt.savefig(image_path)
                    document.add_picture(image_path, width=Inches(3.00))
                    document.add_paragraph("\n\n")
                    plt.clf()

                except Exception as e:
                    print(ticker, " : Error - ", e)
                    #print(ticker"Something happened with", ticker)
                    document.add_paragraph("Something wrong happened")
                    plt.clf()

document.save(dcf_url)
ticker_file.close()
