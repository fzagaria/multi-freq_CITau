"""
This script was written for CASA 6.4.3.27

Datasets calibrated (in order of date observed):

SBs: 2018.1.00900.S PI: M. Tazzari
     Observed 03 July 2021 (1 execution block)
    
LBs: 2018.1.00900.S PI: M. Tazzari
     Observed 27 June 2019 and 04 July 2019 (2 execution blocks)
     
Reducer: F. Zagaria
See logfile at selfcal_init.log for results
"""

import sys
sys.path.append('/data/discsim2/fz258/casa/analysis_scripts')
import analysisUtils as au

execfile('/data/discsim2/fz258/casa/reduction_utils.py')

execfile('flagging.py')
execfile('selfcalEBs.py')
execfile('selfcalSBs.py')
execfile('concatEBs.py')
execfile('selfcalLBs.py')