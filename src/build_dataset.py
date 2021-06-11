import pandas as pd
import os
import yfinance as yf
import asyncio
import zipfile
import gdown

def get_price_history(ticker):
  return (yf.download(ticker, interval="1d", period="max", progress=False, debug=False))
  
def download_data(indices):
  for index in indices:
    df = pd.read_csv('listed/{}.csv'.format(index), delimiter=',')
    for i, ticker in enumerate(df['Symbol'].values):  
          res = asyncio.run(get_data(ticker, index))
    df.to_csv('listed/{}.csv'.format(index))
    
    
async def get_data(ticker, index):
  if os.path.exists('{}/{}.csv'.format(index, ticker)):
        pass
  else:
    d = get_price_history(ticker)
    d.to_csv('{}/{}.csv'.format(index, ticker))
    
    
def download_zips (exchanges):
  for exchange in exchanges:
    if exchange == 'nasdaq':
      url = 'https://drive.google.com/uc?id=1Te_B2dIChh3WFXPGz4iCq94G8LI1xxgp'
    elif exchange == 'nyse':
      url = 'https://drive.google.com/uc?id=17KCevcvfp4eA6KhOXRQSY0Mc-Vd8URtO'
      
    output = '{}.zip'.format(exchange)
    gdown.download(url, output, quiet=False)
    
def unzip_data(exchanges):
  for exchange in exchanges:
    with zipfile.ZipFile('{}.zip'.format(exchange), 'r') as zip_ref:
      zip_ref.extractall('')