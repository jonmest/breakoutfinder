from src.util import walk_through_directories
from src.export import export_interactive, export_static_chart, export_csv

# The minimimum period the breakout should
# Hold without falling
min_breakout_hold = 5

# Minimum consolidation period
# For how many days should it stay within range?
min_consolidation_period = 9

# During consolidation, what is the
# Maximum percent difference between
# The highest and lowest bar?
maximum_consolidation_range = 5

# On the day of a breakout,
# How high above the upper range during consolidation
# Does the close need to be? Percent.
min_increase_from_range = 10

# Number of days before breakout
# That should be included in chart
n_preceeding_days = 65


config = {
    'min_breakout_hold': min_breakout_hold,
    'min_consolidation_period': min_consolidation_period,
    'maximum_consolidation_range': maximum_consolidation_range,
    'min_increase_from_range': min_increase_from_range,
    'n_preceeding_days': n_preceeding_days
}

def find_breakouts(directories, config, callbacks):
    walk_through_directories(directories, config, callbacks)
