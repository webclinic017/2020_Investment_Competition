import csv


def get_us_tickers(input_file_path, output_file_path):
    input_csv = open(input_file_path, "r", newline = '')
    output_csv = open(output_file_path, "w", newline = '')

    ticker_reader = csv.reader(input_csv, delimiter=' ', quotechar='|')
    ticker_writer = csv.writer(output_csv, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for row in ticker_reader:

        ticker_list = row[0].split(",")
        
        if(ticker_list[1] == '"New' or ticker_list[1] == "Nasdaq"):

            ticker_writer.writerow([ticker_list[0]])        
        



if __name__ == "__main__":
    get_us_tickers("Input/consumer_stapes.csv", "tickers.csv")

