from os import path
import mplfinance as mpf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yaml
from pathlib import Path


class Exporter:
    img_folder: str
    interactive_folder: str
    csv_folder: str

    def __init__(self, config):
        self.img_folder = path.join(config["breakout_data_dir"], config['imgFolder'])
        self.interactive_folder = path.join(config["breakout_data_dir"], config['interactiveChartFolder'])
        self.csv_folder = path.join(config["breakout_data_dir"], config['csvFolder'])

        Path(self.csv_folder).mkdir(parents=True, exist_ok=True)
        Path(self.img_folder).mkdir(parents=True, exist_ok=True)
        Path(self.interactive_folder).mkdir(parents=True, exist_ok=True)

    def export_csv(self, df, ticker, breakout_number):
        df.to_csv("{}/{}-{}.csv".format(self.csv_folder, ticker, breakout_number), header=True)

    def export_static_chart(self, df, ticker, breakout_number, dpi=250):
        mpf.plot(df, type='candle', volume=True,
                 savefig=dict(fname="{}/{}-{}.png".format(self.img_folder, ticker, breakout_number),
                              dpi=dpi, pad_inches=0.25), title="{} {}".format(ticker, df.index[0]))

    def export_interactive(self, df, ticker, breakout_number):
        fig = make_subplots(rows=2, cols=1,
                            row_heights=[0.8, 0.2], shared_xaxes=True,
                            subplot_titles=(ticker, "Volume"))
        fig.add_trace(
            go.Candlestick(x=df.index,
                           open=df['Open'],
                           high=df['High'],
                           low=df['Low'],
                           close=df['Close']),
            row=1, col=1
        )

        fig.add_trace(
            go.Bar(x=df.index, y=df['Volume']),
            row=2, col=1
        )
        fig.update_xaxes(
            rangebreaks=[
                dict(bounds=["sat", "mon"]),  # hide weekends
            ]
        )
        fig.write_html("{}/{}-{}.html".format(self.interactive_folder, ticker, breakout_number))
