import pandas as pd

df1 = pd.read_excel('data/2022Oct_output1_1k.xlsx')
df2 = pd.read_excel('data/2022Oct_output1_2k.xlsx')
df3 = pd.read_excel('data/2022Oct_output1_3k.xlsx')
df4 = pd.read_excel('data/2022Oct_output1_4k.xlsx')

join = [df1,df2,df3,df4]

concat_df = pd.concat(join)

concat_df.columns.values[0] = 'SCRIP NAME'

temp_df = pd.read_csv('data/BSE_Equity_download_2022Oct.csv', sep=',', encoding='unicode_escape', usecols=["Security Id", "Security Name", "Group", "Face Value", "Industry", "Sector Name"],index_col=False)

df5 = temp_df[["Security Id", "Security Name", "Group", "Face Value", "Industry", "Sector Name"]]

df5.rename(columns= {'Security Id' : 'SCRIP NAME', 'Group' : 'GROUP', 'Face Value' : 'FACE VALUE', 'Industry' : 'INDUSTRY',  'Sector Name' : 'SECTOR'}, inplace=True)

merge = pd.merge(df5, concat_df, on="SCRIP NAME")

merge.to_csv('data/stockdata_2022Oct_ready.csv',index=False)