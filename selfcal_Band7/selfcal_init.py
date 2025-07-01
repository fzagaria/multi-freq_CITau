"""
This script was written for CASA 6.4.3.27

Datasets calibrated (in order of date observed):
LBs: 2017.A.00014.S PI: G. P. Rosotti
     Observed 11 Dec 2017 (2 execution blocks)

Reducer: F. Zagaria
See logfile at selfcal_init.log
"""

import sys
sys.path.append('/data/discsim2/fz258/casa/analysis_scripts')
import analysisUtils as au

execfile('/data/discsim2/fz258/casa/reduction_utils.py')

execfile('flagging.py')
execfile('selfcalEBs.py')
execfile('concatEBs.py')
execfile('selfcal.py')