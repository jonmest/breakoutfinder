import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import mplfinance as mpf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

IMG_FOLDER = 'img'
INTERACTIVE_FOLDER = 'interactive'
CSV_FOLDER = 'csv'

def export_csv (df, ticker, breakout_number):
  breakout.to_csv("{}/{}-{}.csv".format(CSV_FOLDER, ticker, breakout_number), header=True)

def export_static_chart (df, ticker, breakout_number, dpi=250):
  mpf.plot(df,type='candle', volume=True, 
           savefig=dict(fname="{}/{}-{}.png".format(IMG_FOLDER, ticker, breakout_number),
           dpi=dpi,pad_inches=0.25))
  
def export_interactive(df, ticker, breakout_number):
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
          dict(bounds=["sat", "mon"]), #hide weekends
      ]
  )
  fig.write_html("{}/{}-{}.html".format(INTERACTIVE_FOLDER, ticker, breakout_number))
