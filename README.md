AnonymousReserve
================

The script is set up to run two bidder experimentation (~6.5 hours). Simply run "python utils.py" in the directory and the appropriate files and pdfs will be generated.

pdfs will be created in /data and the csv files generated in ./ contain a summary of the data (opt, ratio, max reserve, datapoints etc...)

Note: output files are named using numerical codes. In the two bidder case the first two numbers are codes for the distributions involved in the auction and the final number is the experiment number. The distributions numbers can be traced back to their entity through the utils script that generates them (getRegularDistributions).
