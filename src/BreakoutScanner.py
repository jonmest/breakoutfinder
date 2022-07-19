from multiprocessing import Queue, Process
from queue import Empty

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from breakout import breakout


def find_breakouts_wrapper(queue, df):
    res = breakout(df["Close"],
             min_size=30,  # minimum observations between breakouts
             method='multi',  # multi or amoc (at most one change)
             degree=1,  # degree of the penalization polynomial (multi only)
             beta=0.002,  # penalization term (multi only)
             percent=None,  # minimum percent change in goodness of fit statistic (multi only)
             alpha=2,  # weight of the distance between observations (amoc only)
             exact=True  # exact or approximate median (amoc only)
             )
    queue.put(res)

class BreakoutScanner:
    def __init__(self, df,
                 min_breakout_hold=5,
                 min_consolidation_period=9,
                 maximum_consolidation_range=5,
                 min_increase_from_range=10,
                 n_preceeding_days=65,
                 n_succeeding_days=10
                 ):
        self.history = df
        self.min_breakout_hold = min_breakout_hold
        self.min_consolidation_period = min_consolidation_period
        self.maximum_consolidation_range = maximum_consolidation_range
        self.min_increase_from_range = min_increase_from_range
        self.n_preceeding_days = n_preceeding_days
        self.n_succeeding_days = n_succeeding_days

    def is_consolidating(self, current_df):
        recent_candlesticks = current_df[-self.min_consolidation_period:]

        max_close = recent_candlesticks['Close'].max()
        min_close = recent_candlesticks['Close'].min()

        treshold = 1 - (self.maximum_consolidation_range / 100)
        if min_close > (max_close * treshold):
            return True

        return False

    def is_breaking_out(self, current_df, ahead_df):
        last_close = ahead_df[['Close']].mean()[0]

        treshold = 1 + (self.min_increase_from_range / 100)
        if self.is_consolidating(current_df[:-1]):
            recent_closes = current_df
            if last_close > (recent_closes['Close'].max() * treshold):
                return True

        return False

    def get_breakouts(self):
        df = self.history
        to_return = []

        # We're starting a new process here, which you may consider
        # exceptionally stupid. Yes, but it's a way to get around occasional
        # SIGABRT signals by the breakout-detector library.
        queue = Queue()
        p = Process(target=find_breakouts_wrapper, args=(queue, df))
        p.start()
        try:
            breakouts_indices = queue.get(True, 60)
        except Empty:
            breakouts_indices = []
        p.join()
        if p.is_alive():
            p.kill()
        #breakouts_indices = find_breakouts_wrapper(df)
        # this blocks until the process terminates

        for breakout_index in breakouts_indices:
            to_return.append(
                df[['Close', 'Open', 'Low', 'High', 'Volume']][
                  breakout_index - self.n_preceeding_days: breakout_index + self.n_succeeding_days]
            )
        # for i in range((self.min_consolidation_period + 1), len(df)):
        #   current_window = df[i-self.min_consolidation_period:i-1]
        #   ahead_window = df[i:i+self.min_breakout_hold]
        #
        #   if self.is_breaking_out(current_window, ahead_window):
        #     breakout_day = df[['Close']].iloc[[i-1]].values[0][0]
        #     preceding_day = df[['Close']].iloc[[i-2]].values[0][0]
        #
        #     to_return.append(
        #         df[['Close', 'Open', 'Low', 'High', 'Volume']][i-self.n_preceeding_days:i+self.n_succeeding_days]
        #       )
        #
        return to_return
