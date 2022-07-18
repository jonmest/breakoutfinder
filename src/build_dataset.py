from pathlib import Path
from typing import List

import pandas as pd
import os
import yfinance as yf
import asyncio
import zipfile
import gdown


class Downloader:
    exchanges: List[str]
    config: dict

    def __init__(self, exchanges: List[str], config):
        self.exchanges = exchanges
        self.config = config
        self.stock_data_path = config.get("stock_data_dir")
        Path(self.stock_data_path).mkdir(parents=True, exist_ok=True)
        for exchange in exchanges:
            dir_path = os.path.join(self.stock_data_path, exchange)
            Path(dir_path).mkdir(parents=True, exist_ok=True)

    def unzip_data(self, exchanges):
        for exchange in exchanges:
            with zipfile.ZipFile('{}.zip'.format(exchange), 'r') as zip_ref:
                zip_ref.extractall('')

    def get_price_history(self, ticker):
        return yf.download(ticker, interval="1d", period="max", progress=False, debug=False)

    def download_data(self, indices):
        for index in indices:
            df = pd.read_csv('listed/{}.csv'.format(index), delimiter=',')
            for i, ticker in enumerate(df['Symbol'].values):
                asyncio.run(self.get_yahoo_data(ticker, index))
            df.to_csv('listed/{}.csv'.format(index))

    async def get_yahoo_data(self, ticker, index):
        file_path = os.path.join(self.stock_data_path, index, ticker)
        if not os.path.exists(file_path):
            d = self.get_price_history(ticker)
            d.to_csv(file_path)

    def download_zips(self, exchanges):
        url = 'https://drive.google.com/uc?id=1Te_B2dIChh3WFXPGz4iCq94G8LI1xxgp'  # Default to NASDAQ
        for exchange in exchanges:
            output_zip_path = os.path.join(self.stock_data_path, "{}.zip".format(exchange))
            if os.path.isfile(output_zip_path):
                continue

            final_output_path = os.path.join(self.stock_data_path, exchange)
            if exchange == 'nasdaq':
                url = 'https://drive.google.com/uc?id=1Te_B2dIChh3WFXPGz4iCq94G8LI1xxgp'
            elif exchange == 'nyse':
                url = 'https://drive.google.com/uc?id=17KCevcvfp4eA6KhOXRQSY0Mc-Vd8URtO'
            gdown.download(url=url, output=output_zip_path, quiet=False)
            with zipfile.ZipFile(output_zip_path, 'r') as zip_ref:
                zip_ref.extractall(final_output_path)
