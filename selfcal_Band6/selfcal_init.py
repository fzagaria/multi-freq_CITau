"""
This script was written for CASA 6.4.3.27

Datasets calibrated (in order of date observed):

SBs: 2015.1.01207.S PI: H. Nomura
     Observed 27 August 2016 (1 execution block)
    
LBs: 2016.1.01370.S PI: C. J. Clarke
     Observed 23 and 24 September 2017 (2 execution blocks)
     
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
