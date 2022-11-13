from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import queue as Queue
import threading
import openpyxl
from openpyxl import *
from openpyxl.styles import NamedStyle
from openpyxl import load_workbook

opts = webdriver.ChromeOptions()
opts.headless =True

cols_required = ['Previous Close',
                 'Open',
                 'High',
                 'Low',
                 'VWAP',
                 '52 Wk High',
                 '52 Wk Low',
                 'Upper Price Band',
                 'Lower Price Band',
                 '2W Avg Qty`(Lakh)',
                 'TTQ (Lakh)',
                 'Turnover (Cr.)',
                 'Turnover (Lakh)',
                 'Mcap Full (Cr.)',
                 'Mcap FF (Cr.)',
                 'Face Value',
                 'EPS (TTM) ',
                 'CEPS (TTM)',
                 'PE',
                 'PB',
                 'ROE']

class myThread(threading.Thread):
    def __init__(self, name, q):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q

    def run(self):
        while 1:
            try:
                things_to_be_done(self.name, self.q)
            except Queue.Empty:
                break

def things_to_be_done(name, q):
    dict = {}
    target_url = q.get(timeout=1)
    time.sleep(1)
    driver = webdriver.Chrome('./chromedriver',options=opts)
    driver.get(target_url)
    # this is just to ensure that the page is loaded
    time.sleep(5)

    html_content = driver.page_source

    soup = BeautifulSoup(html_content, features="html.parser")

    table_rows = soup.find_all('tr')
    for row in table_rows:
        table_cols = row.find_all('td')
        process = "N"
        label = "N"
        for col in table_cols:
            if process == "Y":
                label = "N"
            elif col.text in cols_required:
                 process = "Y"
                 label = "Y"

            if process == "Y":
                 if label == "Y":
                     label_name = col.text
                 else:
                     try:
                         label_value = float((col.text).replace(',', ''))
                     except:
                         label_value = col.text
                     else:
                         label_value = float((col.text).replace(',', ''))
                     finally:
                         dict.update({label_name:label_value})
    global COUNTER
    COUNTER += 1
    global stock_dict
    s_name = target_url.split("/",6)[5]
    # debug
    print(f'Stock # {COUNTER} >> {s_name}')
    stock_dict.setdefault(s_name, dict)
    dict = {}
    df1 = pd.DataFrame.from_dict(stock_dict)
    df1_transposed = df1.T
    #print(df1_transposed)
    try:
        df1_transposed.to_excel('data/2022Oct_output1_4k.xlsx', "a")
    except:
        df1_transposed.to_excel('data/2022Oct_output2_4k.xlsx', "a")

def main(df, no_of_threads):

    thread_list = [str(n) for n in range(no_of_threads)]
    length = len(df)
    queue = Queue.Queue(length)

    threads = []
    for index, d_row in df.iterrows():
        #URL = f'https://www.google.com/search?q=site%3Amoneycontrol.com+{d_row["Security Name"]}&oq=site%3Amoneycontrol.com&aqs=chrome.1.69i57j69i59l2j69i58.2517j0j7&sourceid=chrome&ie=UTF-8'
        URL = d_row["URL"]
        queue.put(URL)

    for name in thread_list:
        thread = myThread(name, queue)
        thread.start()
        threads.append(thread)

if __name__ == '__main__':
    NO_OF_WORKERS = 6
    COUNTER = 0
    stock_dict = {}
    df = pd.read_csv('data/stock_list_2022Oct_4k.csv', sep=',', encoding='unicode_escape', usecols=['Stock', 'URL'])
    #df["Security Name"] = df["Security Name"].str.replace(" ", "+")
    #df["Security Name"] = df["Security Name"].str.replace("&", "%26")
    main(df, NO_OF_WORKERS)