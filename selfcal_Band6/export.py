import sys
sys.path.append('/data/discsim2/fz258/casa/analysis_scripts')
import analysisUtils as au
from uvplot import export_uvtable

execfile('/data/discsim2/fz258/casa/reduction_utils.py')

LB_cont_ap0_weights = 'CI_Tau_LB_contap0_weights.ms'

split(
	vis = LB_cont_ap0_weights,
	outputvis = 'export_uvtable_SBs.ms',
	spw = '0~3',
	width = [2,2,2,2],
	datacolumn = 'DATA',
	timebin = '30s',
)

listobs(
	vis = 'export_uvtable_SBs.ms',
	listfile = 'export_uvtable_SBs.ms.listobs.txt',
	overwrite = True
)

split(
	vis = LB_cont_ap0_weights,
	outputvis = 'export_uvtable_LBs.ms',
	spw = '4~7',
	width = [32,32,32,32],
	datacolumn = 'DATA',
	timebin = '30s',
)

listobs(
	vis = 'export_uvtable_LBs.ms',
	listfile = 'export_uvtable_LBs.ms.listobs.txt',
	overwrite = True
)

concat(
	vis = ['export_uvtable_SBs.ms','export_uvtable_LBs.ms'],
	concatvis = 'export_uvtable.ms',
	dirtol = '0.1arcsec',
	copypointing = False,
)

listobs(
	vis = 'export_uvtable.ms',
	listfile = 'export_uvtable.ms.listobs.txt',
	overwrite = True
)

export_uvtable(
	'uvtable_CI_Tau_B6.txt',
	tb,
	channel = 'all',
	split = split,
	split_args = {'vis':'export_uvtable.ms',
                  'keepflags':False,
                  'datacolumn':'DATA'},
	verbose = True,
)

#Applying split. Creating temporary MS table mstable_tmp.ms from original MS table export_uvtable.ms
#datacolumn has been changed from "CORRECTED_DATA" to "DATA" in order to operate on the new ms
#Reading mstable_tmp.ms
#Warning: the MS table mstable_tmp.ms has 8 spectral windows. By default all of them are exported. To choose which spws to export, provide split_args with the spw parameter.
#Exporting 2 channels per spw.
#Exporting visibilities to uvtable_CI_Tau_B6.txt...done.
#Removing temporary MS table mstable_tmp.ms
