# breakoutfinder
This is a very primitive script to find breakouts in the historical data for stocks traded on the NYSE and Nasdaq. It automatically finds breakouts conforming to specified criteria and saves them as (1) static images, (2) interactive charts and (3) CSV files. Please note, that doing this for all of the NYSE and Nasdaq listed stocks means scouring through a LOT of data. It's tens of thousands of years of time series. Moreover, I haven't really spent time trying to optimize the speed of the analysis and in its current state it's quite brute force. I tried using Numpy only, as opposed to Pandas, but the speed improvement appeared to be so small I stuck with Pandas to keep the code more readable. Also, there are some duplicates, meaning that the script will find one breakout, and then consider the next day another breakout. But I find this good enough to get some learning materials.

As of now, the criteria for a breakout are defined "config.yaml". There are some comments trying to explain what each option means, but hit me up if something's unclear.

# Requirements
Python 3.8 - It might work with older Python 3 versions, but not tested.
Pip

The script has only been tested on Ubuntu, but feel free to test it on other distros or Windows/MacOS and tell me how it works.



## Quick Start
1. Enter directory of this repo in command line
2. `pip install -r requirements.txt`
3. `python .`