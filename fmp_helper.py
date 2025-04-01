import requests
import json

class FMPAPI:
    """Fetches multiple financial data points for a given stock symbol from the FMP API."""

    def __init__(self, api_key):
        self.api_key = api_key
        self.yearly_urls = {
            "key_metrics": "https://financialmodelingprep.com/stable/key-metrics",
            "ratios": "https://financialmodelingprep.com/stable/ratios",
            "income_statement": "https://financialmodelingprep.com/stable/income-statement",
            "balance_sheet": "https://financialmodelingprep.com/stable/balance-sheet-statement",
            "cash_flow": "https://financialmodelingprep.com/stable/cash-flow-statement"
        }
        self.profile_urls = {
            "profile": "https://financialmodelingprep.com/stable/profile",
            "dcf": "https://financialmodelingprep.com/stable/discounted-cash-flow",
        }
        self.news_url = "https://financialmodelingprep.com/stable/news/general-latest"


    def fetch_data(self, symbol, save=False):
        try:
            params = {
                "symbol": symbol,
                "apikey": self.api_key
            }

            yearly_data = {}
            profile_data = {}
            news_data = [
                {
                    "symbol": "AAPL",
                    "publishedDate": "2025-02-03 23:51:37",
                    "publisher": "CNBC",
                    "title": "Asia tech stocks rise after Trump pauses tariffs on China and Mexico",
                    "image": "https://images.financialmodelingprep.com/news/asia-tech-stocks-rise-after-trump-pauses-tariffs-on-20250203.jpg",
                    "site": "cnbc.com",
                    "text": "Gains in Asian tech companies were broad-based, with stocks in Japan, South Korea and Hong Kong advancing. Semiconductor players Advantest and Lasertec led gains among Japanese tech stocks.",
                    "url": "https://www.cnbc.com/2025/02/04/asia-tech-stocks-rise-after-trump-pauses-tariffs-on-china-and-mexico.html"
                }
            ]
            
            latest_yearly_data = {}

            # Fetch yearly data
            for key, url in self.yearly_urls.items():
                response = requests.get(url, params=params)
                response.raise_for_status()
                response = response.json()

                latest_yearly_data.update(response[0])

                data = {}
                for report in response:
                    year = report["date"].split("-")[0]

                    del report["date"]
                    del report["symbol"]
                    data[year] = report

                    if year in yearly_data:
                        yearly_data[year].update(report)
                    else:
                        yearly_data[year] = report

                    if ("revenue" in yearly_data[year]):
                        yearly_data[year]["NetIncomeMargin"] = yearly_data[year]["netIncome"] / yearly_data[year]["revenue"] if yearly_data[year]["revenue"] != 0 else 0
                    if ("interestExpense" in yearly_data[year]):
                        yearly_data[year]["IntrestCoverage"] = yearly_data[year]["ebit"] / yearly_data[year]["interestExpense"] if yearly_data[year]["interestExpense"] != 0 else 0
                    if ("totalEquity" in yearly_data[year]):
                        yearly_data[year]["DebtToEquity"] = yearly_data[year]["totalDebt"] / yearly_data[year]["totalEquity"]
                    if ("totalAssets" in yearly_data[year]):
                        yearly_data[year]["DebtToAssets"] = yearly_data[year]["totalDebt"] / yearly_data[year]["totalAssets"]
                    if ("totalEquity" in yearly_data[year]):
                        yearly_data[year]["ReturnOnEquity"] = yearly_data[year]["netIncome"] / yearly_data[year]["totalEquity"]
                    if ("weightedAverageShsOut" in yearly_data[year]):
                        yearly_data[year]["EarningsPerShare"] = yearly_data[year]["netIncome"] / latest_yearly_data["weightedAverageShsOut"] if latest_yearly_data["weightedAverageShsOut"] != 0 else 0
                    if ("priceToEarningsGrowthRatio" in yearly_data[year]):
                        yearly_data[year]["PEG"] = yearly_data[year]["priceToEarningsGrowthRatio"]
            
            for key, url in self.profile_urls.items():
                response = requests.get(url, params=params)
                response.raise_for_status()
                response = response.json()[0]

                response.update({
                    "dividendYield": latest_yearly_data["dividendYield"],
                    "weightedAverageShsOut": latest_yearly_data["weightedAverageShsOut"],
                    "evToSales": latest_yearly_data["evToSales"],
                    "evToRevenue": latest_yearly_data["enterpriseValue"] / latest_yearly_data["revenue"] if latest_yearly_data["revenue"] != 0 else 0,
                    "evToEBIT": latest_yearly_data["enterpriseValue"] / latest_yearly_data["ebit"] if latest_yearly_data["ebit"] != 0 else 0,
                    "evToEBITDA": latest_yearly_data["evToEBITDA"],
                    "priceToEarningsRatio": latest_yearly_data["priceToEarningsRatio"]
                })
                profile_data.update(response)
            
            #response = requests.get(self.news_url, params=params)
            #response.raise_for_status()
            response = [] #response.json()
            news_data = response + news_data

            if (save):
                file_path = 'test.json'
                with open(file_path, 'w') as json_file:
                    json.dump([yearly_data, profile_data], json_file, indent=4)

            return (yearly_data, profile_data, news_data)
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

