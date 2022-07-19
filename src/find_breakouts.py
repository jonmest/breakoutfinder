from multiprocessing import Process

import pandas as pd
import glob
import os

from src.BreakoutScanner import BreakoutScanner


def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

def read_filelist_and_run_breakoutfinder(file_list, config, callbacks, console):
    for file in file_list:
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
            continue

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


def find_breakouts(console, directories, config, callbacks):
    with console.status("[bold green]Looking for breakouts...") as status:
        processes = []
        for directory in directories:
            file_list_of_lists = chunkIt(glob.glob("{}/*.csv".format(directory)), config.get("procs"))
            for list in file_list_of_lists:
                p = Process(target=read_filelist_and_run_breakoutfinder, args=(list, config, callbacks, console))
                p.start()
                processes.append(p)

        while len(processes) > 0:
            for p in processes:
                if not p.is_alive():
                    processes.remove(p)

    console.log("Done!")
