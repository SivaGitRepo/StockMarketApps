import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import csv

data_month = st.sidebar.selectbox("Choose the required report:", ('July-2022','Oct-2022'))

#stocks_df = pd.read_csv("data/stocks.csv",index_col="SCRIP NAME")
if data_month == 'July-2022':
    st.write("""
    # Simple Stock Price App
    Shown are the stock prices downloaded from BSE on JULY 2022!
    """)
    stocks_df = pd.read_csv("data/stockdata_ready.csv",index_col="SCRIP NAME")
    watchlist_file = 'data/StockWatchList.csv'
elif data_month == 'Oct-2022':
    st.write("""
    # Simple Stock Price App
    Shown are the stock prices downloaded from BSE on October 2022!
    """)
    stocks_df = pd.read_csv("data/stockdata_2022Oct_ready.csv", index_col="SCRIP NAME")
    watchlist_file = 'data/StockWatchList_2022Oct.csv'

stocks_df["PE"] = stocks_df["PE"].replace(["-","Z "],np.nan)
stocks_df["PE"] = stocks_df["PE"].astype(float)

stocks_df["PB"] = stocks_df["PB"].replace(["-"],np.nan)
stocks_df["PB"] = stocks_df["PB"].astype(float)

stocks_df["Mcap Full (Cr.)"] = stocks_df["Mcap Full (Cr.)"].replace("-",np.nan)
stocks_df["Mcap Full (Cr.)"] = stocks_df["Mcap Full (Cr.)"].astype(float)

stocks_df["Mcap FF (Cr.)"] = stocks_df["Mcap FF (Cr.)"].replace("-",np.nan)
stocks_df["Mcap FF (Cr.)"] = stocks_df["Mcap FF (Cr.)"].astype(float)

stocks_df["ROE"] = stocks_df["ROE"].replace("-",np.nan)
stocks_df["ROE"] = stocks_df["ROE"].astype(float)

st.sidebar.header("Stock filter v.2.0")
option = st.sidebar.selectbox("Choose the filter criteria:", ('PE / PB Filter',
                                                              'Turnover > Mcap',
                                                              'Stock Filter',
                                                              'Sector Filter',
                                                              'Top 20',
                                                              'Best Stocks to Invest',
                                                              "Watchlist",
                                                              'Date Filter'))

st.header(option)

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

if option == "PE / PB Filter":
    PE_PB_Select = st.sidebar.radio("PE / PB",("PE","PB"))
    if PE_PB_Select == "PE":
        PE_from = st.sidebar.slider('PE From', 0.0, 100.0, 0.0)
        PE_to = st.sidebar.slider('PE To', 0.0, 100.0, 0.0)
        if PE_to > 0:
            if PE_to < PE_from:
                st.write("PE_To value should be greater than PE_From value")
            else:
                st.write(stocks_df.loc[(stocks_df["PE"] > PE_from) & (stocks_df["PE"] < PE_to),
                                       ["Security Name","SECTOR","Open","52 Wk High", "52 Wk Low",
                                        "Turnover (Cr.)","Mcap Full (Cr.)","PE","PB","ROE"]]
                        )
    if PE_PB_Select == "PB":
        PB_from = st.sidebar.slider('PB From', 0.0, 100.0, 0.0)
        PB_to = st.sidebar.slider('PB To', 0.0, 100.0, 0.0)
        if PB_to > 0:
            if PB_to < PB_from:
                st.write("PB_To value should be greater than PB_From value")
            else:
                st.write(stocks_df.loc[(stocks_df["PB"] > PB_from) & (stocks_df["PB"] < PB_to),
                                       ["Security Name", "SECTOR", "Open", "52 Wk High", "52 Wk Low",
                                        "Turnover (Cr.)", "Mcap Full (Cr.)", "PE", "PB", "ROE"]]
                        )
if option == "Turnover > Mcap":
    stocks_df["Turnover-Mcap-Diff"] = stocks_df["Turnover (Cr.)"] - stocks_df["Mcap Full (Cr.)"]
    st.write(stocks_df.loc[stocks_df["Turnover (Cr.)"] > stocks_df["Mcap Full (Cr.)"],
                           ["Security Name", "SECTOR", "Open", "52 Wk High", "52 Wk Low",
                            "Turnover (Cr.)", "Mcap Full (Cr.)", "PE", "PB", "ROE","Turnover-Mcap-Diff"]
             ])
if option == "Stock Filter":
    stock_input = st.sidebar.text_input("Enter stock name",max_chars=10).lower()
    st.write(stocks_df.loc[(stocks_df["Security Name"].str.lower()).str.contains(stock_input),
                           ["Security Name", "SECTOR", "Open", "52 Wk High", "52 Wk Low",
                            "Turnover (Cr.)", "Mcap Full (Cr.)", "PE", "PB", "ROE"]])
if option == "Sector Filter":
    Sec_Ind_Select = st.sidebar.radio("Sector / Industry", ("By Sector", "By Industry"))
    # if Sec_Ind_Select == "By Sector":
    #     sector_input = st.sidebar.selectbox("Select Sector",options=(stocks_df["SECTOR"].unique()))
    #     st.write(stocks_df.loc[stocks_df["SECTOR"] == sector_input,
    #                            ["Security Name", "SECTOR", "Open", "52 Wk High", "52 Wk Low",
    #                             "Turnover (Cr.)", "Mcap Full (Cr.)", "PE", "PB", "ROE"]])
    if Sec_Ind_Select == "By Sector":
        sector_input = st.sidebar.selectbox("Select Sector", options=(stocks_df["SECTOR"].unique()))
        sub_filter_PB =  st.sidebar.radio("Use PB Filter?", ("Yes", "No"))
        if sub_filter_PB == "Yes":
            PB_from = st.sidebar.slider('PB From', 0.0, 10.0, 0.0)
            PB_to = st.sidebar.slider('PB To', 0.0, 10.0, 0.0)
            st.write(stocks_df.loc[(stocks_df["SECTOR"] == sector_input) & (stocks_df["PB"] > PB_from) & (stocks_df["PB"] < PB_to),
                                   ["Security Name", "INDUSTRY", "Open", "52 Wk High", "52 Wk Low",
                                    "Turnover (Cr.)", "Mcap Full (Cr.)", "PE", "PB", "ROE"]])
        else:
            st.write(stocks_df.loc[stocks_df["SECTOR"] == sector_input,
                                   ["Security Name", "INDUSTRY", "Open", "52 Wk High", "52 Wk Low",
                                    "Turnover (Cr.)", "Mcap Full (Cr.)", "PE", "PB", "ROE"]])
    if Sec_Ind_Select == "By Industry":
        sector_input = st.sidebar.selectbox("Select Industry", options=(stocks_df["INDUSTRY"].unique()))
        sub_filter_PE =  st.sidebar.radio("Use PE Filter?", ("Yes", "No"))
        if sub_filter_PE == "Yes":
            PE_from = st.sidebar.slider('PE From', 0.0, 100.0, 0.0)
            PE_to = st.sidebar.slider('PE To', 0.0, 100.0, 0.0)
            st.write(stocks_df.loc[(stocks_df["INDUSTRY"] == sector_input) & (stocks_df["PE"] > PE_from) & (stocks_df["PE"] < PE_to),
                                   ["Security Name", "INDUSTRY", "Open", "52 Wk High", "52 Wk Low",
                                    "Turnover (Cr.)", "Mcap Full (Cr.)", "PE", "PB", "ROE"]])
        else:
            st.write(stocks_df.loc[stocks_df["INDUSTRY"] == sector_input,
                                   ["Security Name", "INDUSTRY", "Open", "52 Wk High", "52 Wk Low",
                                    "Turnover (Cr.)", "Mcap Full (Cr.)", "PE", "PB", "ROE"]])
if option == "Top 20":
    Top_20 = st.sidebar.selectbox("Choose one:",('ROE', 'PE', 'PB', 'Mcap Full (Cr.)', 'Turnover (Cr.)'))

    st.write(stocks_df[["Security Name", "SECTOR", "Open", "52 Wk High", "52 Wk Low",
                        "Turnover (Cr.)", "Mcap Full (Cr.)", "PE", "PB", "ROE"]].sort_values(Top_20,ascending=False).head(20))
    st.bar_chart(stocks_df[[Top_20]].sort_values(Top_20, ascending=False).head(20))
if option == "Best Stocks to Invest":
    PB_from = st.sidebar.slider('PB From', 0.0, 1.0, 0.0)
    PB_to = st.sidebar.slider('PB To', 0.0, 1.0, 0.0)
    PE_from = st.sidebar.slider('PE From', 0.0, 5.0, 0.0)
    PE_to = st.sidebar.slider('PE To', 0.0, 5.0, 0.0)
    Best_Stocks_df = stocks_df.loc[(stocks_df["PB"] > PB_from) & (stocks_df["PB"] < PB_to) &
                                   (stocks_df["PE"] > PE_from) & (stocks_df["PE"] < PE_to),
                                   ["Security Name", "SECTOR", "Open", "52 Wk High", "52 Wk Low",
                                    "Turnover (Cr.)", "Mcap Full (Cr.)", "PE", "PB", "ROE"]]
    Best_stocks_order = st.sidebar.selectbox("Order stocks by:", ('ROE', 'Mcap Full (Cr.)', 'Turnover (Cr.)'))
    st.write(Best_Stocks_df[["Security Name", "SECTOR", "Open", "52 Wk High", "52 Wk Low",
                             "Turnover (Cr.)", "Mcap Full (Cr.)", "PE", "PB", "ROE"]
                           ].sort_values(Best_stocks_order,ascending=False).head(10))
    st.bar_chart(Best_Stocks_df[[Best_stocks_order]].sort_values(Best_stocks_order, ascending=False).head(10))
if option == "Watchlist":
    opt_Add_View_WL = st.sidebar.radio("Add / View / Delete", ("Add", "View", "Delete"))
    if opt_Add_View_WL == "Add":
        stock_input = st.sidebar.text_input("Enter stock name", max_chars=10).lower()
        Add_WL_df = stocks_df.loc[(stocks_df["Security Name"].str.lower()).str.contains(stock_input),
                               ["Security Name", "SECTOR", "Open", "52 Wk High", "52 Wk Low",
                                "Turnover (Cr.)", "Mcap Full (Cr.)", "PE", "PB", "ROE"]]
        st.write (Add_WL_df)
        if st.sidebar.button("Add"):
            try:
                WL_df = pd.read_csv(watchlist_file, index_col="SCRIP NAME")
                Add_WL_df.to_csv(watchlist_file,mode='a',header=False)
            except:
                Add_WL_df.to_csv(watchlist_file)
            finally:
                st.write("Added successfully")
    if opt_Add_View_WL == "View":
        try:
            WL_df = pd.read_csv(watchlist_file,index_col="SCRIP NAME")
            st.write(WL_df)
        except:
            st.write("Watchlist is empty, first add before viewing")
    if opt_Add_View_WL == "Delete":
        try:
            WL_df = pd.read_csv(watchlist_file,index_col="SCRIP NAME")
            st.write(WL_df)
            stock_to_del = st.sidebar.text_input("Enter stock index to delete").upper()
            if st.sidebar.button("Delete"):
                try:
                    WL_df_del = WL_df.drop(stock_to_del)
                    WL_df_del.to_csv(watchlist_file)
                    st.write("Deleted successfully")
                except:
                    st.write("Stock could not be deleted")
        except:
            st.write("Watchlist is empty, first add before deleting")
if option == "Date Filter":
    st.subheader("Work in progress")
    #from_date = st.sidebar.date_input("From Date")
    #to_date = st.sidebar.date_input("To Date")