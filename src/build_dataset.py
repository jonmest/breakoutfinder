import pandas as pd
import os
import yfinance as yf

def get_price_history(ticker):
  return (yf.download(ticker, interval="1d", period="max", progress=False, debug=False))
  
def download_data(indices):
  for index in indices:
    df = pd.read_csv('listed/{}.csv'.format(index), delimiter=',')
    for i, ticker in enumerate(df['Symbol'].values):  
      if os.path.exists('{}/{}.csv'.format(index, ticker)):
        pass
      else:
        d = get_price_history(ticker)
        if df.empty:
          df.drop(i)
        d.to_csv('{}/{}.csv'.format(index, ticker))
    df.to_csv('listed/{}.csv'.format(index))