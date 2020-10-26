import csv
from metrics import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


with open("Input/utilities_fundamentals.csv", "r", newline = '') as input_csv:

    utilities_df = pd.read_csv(input_csv)

    utilities_df.set_index([SYMBOL,YEAR], inplace=True)

    dd = utilities_df.loc[("CPB",2018)]


    projected_years = 5
    initial_sales = sales
    depr_percent
    sales_growth_rate
    ebitda_margin
    nwc_percent
    tax_rate

    WACC
    tgr

    interations = 1000
    sales_std_dev = 0.01
    ebitda_std_dev = 0.02
    nwc_std_dev = 0.01