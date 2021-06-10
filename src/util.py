import pandas as pd
from datetime import datetime
from .BreakoutScanner import  BreakoutScanner
import glob
import os
import sys
import traceback
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from rich.progress import track
from rich.console import Console

console = Console()
    
def walk_through_directories (directories, config, callbacks):
  with console.status("[bold green]Looking for breakouts...") as status:
    for directory in directories:
      for file in glob.glob("{}/*.csv".format(directory)):
        fileName_absolute = os.path.basename(file)
        ticker = fileName_absolute.replace('.csv', '')
        
        try:
          df = pd.read_csv(
            file, 
            index_col='Date', 
            parse_dates=True
            )
        except Exception as e:
          print("Failed to read file:", file, "\nSkipping.")
        
        if df.empty:
          os.remove(file)
          print("Found corrupted file:", file, "\nSkipping.")
          continue
        
        bs = BreakoutScanner(df, 
                            config['min_breakout_hold'], 
                            config['min_consolidation_period'],
                            config['maximum_consolidation_range'], 
                            config['min_increase_from_range'], 
                            config['n_preceeding_days'])
        breakouts = bs.get_breakouts(5, 10, 5)
        
        for i, breakout in enumerate(breakouts):
          if breakout.empty:
            continue

          for callback in callbacks:
            callback(breakout, ticker, i)
        console.log("Done with {}.".format(ticker),)