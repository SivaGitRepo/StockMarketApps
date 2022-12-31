import nsepy as nse
from nsepy import get_history
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
from functools import reduce

stocks_list = ["USDINR"]
start_date = date(2021,1,1)
end_date = date(2022,12,30)
dataframe_list = []

def get_forex_data(exchange_currency):
    if exchange_currency == "USD":
       forex_data = nse.get_rbi_ref_history(start=start_date, end=end_date)
       forex_data = forex_data.reset_index()
       forex_data = forex_data.rename(columns={"1 USD": "USDINR"})
       forex_data = forex_data[["Date", "USDINR"]]
       forex_data.rename_axis(None)
       return forex_data

for stock in stocks_list:
    if stock == "USDINR":
        forex_data = get_forex_data("USD")
        dataframe_list.append(forex_data[["Date", stock]])
    else:
        if stock == "NIFTY":
            market_data = get_history(symbol="NIFTY 50", start=start_date, end=end_date, index=True)
        else:
            market_data = get_history(symbol=stock,start=start_date,end=end_date)
        dataframe = market_data.reset_index()
        dataframe.rename_axis(None)
        dataframe = dataframe.rename(columns={"Close": stock})
        dataframe_list.append(dataframe[["Date", stock]])

all_together = reduce(lambda  left,right: pd.merge(left,right,on=['Date'],
                                            how='outer'), dataframe_list)

all_together_corr = all_together.corr()
print(all_together.corr())

#fig, axes = plt.subplots(figsize=(12,4))
#all_together.plot.line(ax=axes)
#axes.set_ylabel("STOCKS")
all_together.plot.scatter(x="USDINR",y="Date",alpha=0.5)
plt.show()