import pandas as pd
import glob
import os

from src.BreakoutScanner import BreakoutScanner


def find_breakouts(console, directories, config, callbacks):
    with console.status("[bold green]Looking for breakouts...") as status:
        for directory in directories:
            for file in glob.glob("{}/*.csv".format(directory)):
                file_name_absolute = os.path.basename(file)
                ticker = file_name_absolute.replace('.csv', '')

                try:
                    df = pd.read_csv(
                        file,
                        index_col='Date',
                        parse_dates=True
                    )
                except Exception as e:
                    console.log("Failed to read file:", file, "- Skipping.")

                if df.empty:
                    os.remove(file)
                    console.log("Found empty file:", file, "- Skipping.")
                    continue

                bs = BreakoutScanner(df,
                                     config['min_breakout_hold'],
                                     config['min_consolidation_period'],
                                     config['maximum_consolidation_range'],
                                     config['min_increase_from_range'],
                                     config['n_preceeding_days'])
                breakouts = bs.get_breakouts()

                for i, breakout in enumerate(breakouts):
                    if breakout.empty:
                        continue

                    for callback in callbacks:
                        callback(breakout, ticker, i)
                console.log("Done with {}.".format(ticker), )

    console.log("Done!")