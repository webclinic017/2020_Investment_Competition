import csv
import math
import finnhub
import datetime
from metrics import *
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

class Analysis_Finnhub:
    def __init__(self, client, balance, income_ttm, income_annual, cashflows_ttm, cashflows_annual, estimates):
        
        self.finnhub_client = client
        
        with open(balance, "r", newline = '') as csv_balance:
            self.balance_df = pd.read_csv(csv_balance)
            self.balance_df.set_index([SYMBOL], inplace=True)

        with open(income_ttm, "r", newline = '') as csv_income:
            self.income_ttm_df = pd.read_csv(csv_income)
            self.income_ttm_df.set_index([SYMBOL], inplace=True)

        with open(income_annual, "r", newline = '') as csv_income:
            self.income_annual_df = pd.read_csv(csv_income)
            self.income_annual_df.set_index([SYMBOL], inplace=True)

        with open(cashflows_ttm, "r", newline = '') as csv_cashflows:
            self.cashflows_ttm_df = pd.read_csv(csv_cashflows)
            self.cashflows_ttm_df.set_index([SYMBOL], inplace=True)

        with open(cashflows_annual, "r", newline = '') as csv_cashflows:
            self.cashflows_annual_df = pd.read_csv(csv_cashflows)
            self.cashflows_annual_df.set_index([SYMBOL], inplace=True)

        with open(estimates, "r", newline = '') as csv_estimate:
            self.estimates_df = pd.read_csv(csv_estimate)
            self.estimates_df.set_index([SYMBOL], inplace=True)

        

    def monte_carlo_DCF(self, ticker):

        #===== Company Balances =====#
        company_balance_df = self.balance_df.loc[ticker]
        period = company_balance_df.iloc[0][PERIOD]  # important to get the time period of the company
        company_balance_df.set_index(PERIOD, inplace=True)

        #===== Company Incomes =====#
        company_income_df = self.income_ttm_df.loc[ticker]
        company_income_df.set_index(PERIOD, inplace=True)
        
        #===== Company Cashflows =====#
        company_cashflow_df = self.cashflows_ttm_df.loc[ticker]
        company_cashflow_df.set_index(PERIOD, inplace=True)

        #===== Company Estimates =====#
        company_estimates_df = self.estimates_df.loc[ticker]


        #===== Dictionary for projected revenues =====#
        years = ['2020A', '2021B', '2022P', '2023P', '2024P', '2025P']
        sales = pd.Series(index = years, dtype='float64') # generate dataframe

        #===== YEARS of PROJECTION =====#
        projected_years = 5 # unused variable...

        #===== INITIAL SALES =====#
        initial_sales = sales['2020A'] = company_income_df.loc[period][REVENUE] # DONE

        #===== DEPRECIATION RATE =====#
        depr_percent = capex_percent = 0.032 #depr_percent: depreication rate / capex_percent: Capital Expenditure rate

        #===== SALES GROWTH RATE =====#
        sales_growth_rate = 0 
        growth_rate_sum = 0
        for i in range(5):
            try:
                revenue1 = company_estimates_df.iloc[i][REVENUE_AVG]
                revenue2 = company_estimates_df.iloc[i+1][REVENUE_AVG]
                growth_rate_sum += (revenue1 / revenue2)
            except:
                print("Error - check revenue growth function")
        sales_growth_rate = growth_rate_sum / 5 # DONE
                
        #===== EBITDA MARGIN =====#
        ebitda_margin = (company_income_df.loc[period][EBIT] + 
            company_cashflow_df.loc[period][DEPRECIATION_AMORTIZATION]) / initial_sales # DONE

        #===== NET WORKING CAPITAL RATE =====#
        nwc_percent = (company_balance_df.loc[period][CURRENT_ASSETS] - 
            company_balance_df.loc[period][CURRENT_LIABILITIES]) / initial_sales # DONE

        #===== CORPORATE INCOME TAX RATE =====#
        tax_rate = 0.25 #DONE

        #===== WACC & Terminal Growth Rate in the DCF Model =====#
        WACC = 0.12 #weighted average cost of capital

        total_debt = company_balance_df.loc[period][TOTAL_DEBT]
        total_equity = company_balance_df.loc[period][TOTAL_EQUITY]
        enterprise_value = total_equity + total_debt
        wd = total_debt / enterprise_value
        rd = .04 # arbitrary
        wp = 0
        rp = 0
        we = total_equity / enterprise_value
        de = .10 # need to use CAPM for this value

        WACC = wd * rd * (1-tax_rate) + wp * rp + we * de

        tgr = 0.02 #terminal growth rate of the company: for a mature company, the value maintains between 0.2-0.3%(long-term inflation rate) to 0.4-0.5%(History GDP growth rate)

        #===== Monte-Carlo Simulation Parameters =====#
        iterations = 1000 #simulate 1000 times
        sales_std_dev = 0.01
        ebitda_std_dev = 0.02 
        nwc_std_dev = 0.01

        
        #=============== DCF CALCULATION ===============#

        #Generate randomized input for probability distributions
        sales_growth_dist = np.random.normal(loc = sales_growth_rate, scale = sales_std_dev, size = iterations)
        ebitda_margin_dist = np.random.normal(loc = ebitda_margin, scale = ebitda_std_dev, size = iterations)
        nwc_percent_dist = np.random.normal(loc = nwc_percent, scale = nwc_std_dev, size = iterations)
        
        #Calculate the Free Cash Flow, denoted as FCF
        output_dcfDistribution = []
        for i in range(iterations):
            for year in range(1, len(years)):
                sales[year] = sales[year - 1] * (1 + sales_growth_dist[0]) # project sales per year
            
            ebitda = sales * ebitda_margin_dist[i] # earnings before interest, tax, depreciation, and ammortization
            
            depreciation = (sales * depr_percent) # depreciation
            
            ebit = ebitda - depreciation # earnings before interest and tax
            
            nwc = sales * nwc_percent_dist[i] # net working capital
            
            change_in_nwc = nwc.shift(1) - nwc 
            
            capex = -(sales * capex_percent) # capital expenditures
            
            tax_payment = -ebit * tax_rate # tax payment
            
            tax_payment = tax_payment.apply(lambda x: min(x, 0)) 
            
            FCF = ebit + depreciation + tax_payment + capex + change_in_nwc # free cash flow
        
            # Implementing the DCF Formula with WACC & Terminal_Growth_Rate to get the DCF values
            terminal_value = (FCF[-1] * (1 + tgr)) / (WACC - tgr)
            FCF[-1] += terminal_value
            discount_factors = [(1 / (1 + WACC)) ** i for i in range (1,6)]        
            dcf_value = sum(FCF[1:] * discount_factors )
            output_dcfDistribution.append(dcf_value)
        
        return output_dcfDistribution


    def buffett(self, ticker):
        try:
            #===== Company Balances =====# 
            company_balance_df = self.balance_df.loc[ticker]
            company_balance_df.set_index(YEAR, inplace=True)

            #===== Company Incomes =====#
            company_income_df = self.income_annual_df.loc[ticker]
            company_income_df.set_index(YEAR, inplace=True)
            
            #===== Company Cashflows =====#
            company_cashflow_df = self.cashflows_annual_df.loc[ticker]
            company_cashflow_df.set_index(YEAR, inplace=True)

            #===== Company Estimates =====#
            company_estimates_df = self.estimates_df.loc[ticker]


            #===== Company ROE =====#
            roe_array = []
            roe_df = company_income_df[NET_INCOME] / company_balance_df[TOTAL_EQUITY]
            roe_df = roe_df.dropna() # drop NaN values
            for i in range(10):
                try:
                    roe_array = roe_df.to_numpy()[0:i]
                except:
                    print("ROE too short")

            #===== Company EPS =====#
            eps_array = []
            eps_df = company_income_df[NET_INCOME] / company_balance_df[SHARES_OUTSTANDING]
            eps_df = eps_df.dropna() # drop NaN values
            for i in range(10):
                try:
                    eps_array = eps_df.to_numpy()[0:i]
                except:
                    print("EPS too short")

            #===== PLACEHOLDER ARRAY =====#
            placeholder_array = []
            for i in range(len(roe_array)):
                placeholder_array.append(i)
            # put placeholder array in a numpy array
            count_array = np.array(placeholder_array).reshape(-1, 1)

            #===== MIN & MAX PE RATIOS =====#
            #get pe ratio min max 10 years
            pe_min = 10
            pe_max = 30

            #===== CURRENT PRICE =====#
            cur_price = self.finnhub_client.quote(ticker)["c"] # 'c' for current price
            

            #=============== ANALYSIS ===============#

            # create linear regression models
            model_roe = LinearRegression()
            model_eps = LinearRegression()
            # fit lines from given values
            model_roe.fit(count_array, roe_array)
            model_eps.fit(count_array, eps_array)
            # obtain r values from coefficient of determinations
            r_value_roe = math.sqrt(model_roe.score(count_array, roe_array))
            r_value_eps = math.sqrt(model_eps.score(count_array, eps_array))

            #===== EPS INDEXING =====#
            a = len(eps_array) - 1 # count for EPS 1 position
            b = 0 # count for EPS 2 position
            eps1 = eps_array[a]
            eps2 = eps_array[b]
            # find the earliest positive eps and set position accordingly             
            while(eps1 <= 0):
                a -= 1
                try:
                    eps1 = eps_array[a]
                except IndexError:
                    #print(ticker, "eps 1 out of bounds")
                    break
            # find the latest positive eps and set position accordingly  
            while(eps2 <= 0):
                b += 1
                try:
                    eps2 = eps_array[b]
                except IndexError:
                    #print(ticker, "eps 2 out of bounds")
                    break
            length = a - b + 1 # find differences in position between EPS

            #===== EPS AGR =====#
            cagr_eps = math.pow(eps1 / eps2, 1 / length) - 1
            
            #===== PROJECTED VALUE AND GROWTH =====#
            projected_n = 10

            projected_eps = eps2 * math.pow(1 + cagr_eps, projected_n)
            
            projected_price_min = projected_eps * pe_min
            projected_price_max = projected_eps * pe_max

            try:
                p_agr_min = 100 * (math.pow(projected_price_min/cur_price, 1 / projected_n) - 1)
                p_agr_max = 100 * (math.pow(projected_price_max/cur_price, 1 / projected_n) - 1)
            except ValueError:
                print("value error")
                p_agr_min = -10101
                p_agr_max = -10101
            
            #correlation
            if(r_value_roe >= 0.3 and r_value_eps >= 0.3):
                """
                a = len(eps_array) - 1 # count for EPS 1 position
                b = 0 # count for EPS 2 position
                eps1 = eps_array[a]
                eps2 = eps_array[b]
                # find the earliest positive eps and set position accordingly             
                while(eps1 <= 0):
                    a -= 1
                    try:
                        eps1 = eps_array[a]
                    except IndexError:
                        #print(ticker, "eps 1 out of bounds")
                        break
                # find the latest positive eps and set position accordingly  
                while(eps2 <= 0):
                    b += 1
                    try:
                        eps2 = eps_array[b]
                    except IndexError:
                        #print(ticker, "eps 2 out of bounds")
                        break
                length = a - b + 1 # find differences in position between EPS
                """

                # find CAGR of EPS 1, EPS 2, and length
                if(eps1 > 0 and eps2 > 0 and length > 2):
                    """
                    cagr_eps = math.pow(eps1 / eps2, 1 / length) - 1
                    """
                    # perform further analysis if CAGR is greater than 0%
                    if(cagr_eps > 0):
                        """
                        projected_n = 10

                        projected_eps = eps2 * math.pow(1 + cagr_eps, projected_n)
                        
                        projected_price_min = projected_eps * pe_min
                        projected_price_max = projected_eps * pe_max

                        p_agr_min = 100 * (math.pow(projected_price_min/cur_price, 1 / projected_n) - 1)
                        p_agr_max = 100 * (math.pow(projected_price_max/cur_price, 1 / projected_n) - 1)
                        """
                        print(ticker, "- Projected growth max:", p_agr_max)
                        
                    else:
                        print(ticker, "- CAGR is negative")

                else:
                    print(ticker, "- EPS is negative or n is 2 or less")

            else:
                print(ticker, "- no strong correlation")

            return [ticker, length, cagr_eps, pe_min, pe_max, p_agr_min, p_agr_max]
            
        except KeyError:
            print(ticker, "- not found")

if __name__ == "__main__":
    client = finnhub.Client(api_key="bucae7f48v6oa2u4ng20")
    sector = "staples"
    analysis = Analysis_Finnhub(client, "Data/{}_balance_annual.csv".format(sector), 
                                        "Data/{}_income_ttm.csv".format(sector), 
                                        "Data/{}_income_annual.csv".format(sector),
                                        "Data/{}_cashflows_ttm.csv".format(sector), 
                                        "Data/{}_cashflows_annual.csv".format(sector), 
                                        "Data/{}_estimates.csv".format(sector))
    analysis.buffett('JJSF')
