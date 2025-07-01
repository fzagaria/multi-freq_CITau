import sys
sys.path.append('/data/discsim2/fz258/casa/analysis_scripts')
import analysisUtils as au
from uvplot import export_uvtable

execfile('/data/discsim2/fz258/casa/reduction_utils.py')

LB_cont_ap0_weights = 'CI_Tau_LB_contap0_weights.ms'

split(
	vis = LB_cont_ap0_weights,
	outputvis = 'export_uvtable_SBs_lsb.ms',
	spw = '8~9',
	width = [6,6],
	datacolumn = 'DATA',
	timebin = '30s',
)

listobs(
	vis = 'export_uvtable_SBs_lsb.ms',
	listfile = 'export_uvtable_SBs_lsb.ms.listobs.txt',
	overwrite = True
)

split(
	vis = LB_cont_ap0_weights,
	outputvis = 'export_uvtable_SBs_usb.ms',
	spw = '10~11',
	width = [6,6],
	datacolumn = 'DATA',
	timebin = '30s',
)

listobs(
	vis = 'export_uvtable_SBs_usb.ms',
	listfile = 'export_uvtable_SBs_usb.ms.listobs.txt',
	overwrite = True
)

split(
	vis = LB_cont_ap0_weights,
	outputvis = 'export_uvtable_LBs_lsb.ms',
	spw = '0~1,4~5',
	width = [32,32,32,32],
	datacolumn = 'DATA',
	timebin = '30s',
)

listobs(
	vis = 'export_uvtable_LBs_lsb.ms',
	listfile = 'export_uvtable_LBs_lsb.ms.listobs.txt',
	overwrite = True
)

split(
	vis = LB_cont_ap0_weights,
	outputvis = 'export_uvtable_LBs_usb.ms',
	spw = '2~3,6~7',
	width = [32,32,32,32],
	datacolumn = 'DATA',
	timebin = '30s',
)

listobs(
	vis = 'export_uvtable_LBs_usb.ms',
	listfile = 'export_uvtable_LBs_usb.ms.listobs.txt',
	overwrite = True
)

concat(
	vis = ['export_uvtable_SBs_lsb.ms','export_uvtable_SBs_usb.ms',
           'export_uvtable_LBs_lsb.ms','export_uvtable_LBs_usb.ms'],
	concatvis = 'export_uvtable.ms',
	dirtol = '0.1arcsec',
	copypointing = False,
)
#2023-04-12 19:51:35	WARN	MSConcat::concatenate (file casacore/ms/MSOper/MSConcat.cc, line 996)	Zero or negative scan numbers in MS. May lead to duplicate scan numbers in concatenated MS.
#2023-04-12 19:51:38	WARN	MSConcat::concatenate (file casacore/ms/MSOper/MSConcat.cc, line 996)	Zero or negative scan numbers in MS. May lead to duplicate scan numbers in concatenated MS.

listobs(
	vis = 'export_uvtable.ms',
	listfile = 'export_uvtable.ms.listobs.txt',
	overwrite = True
)

export_uvtable(
	'uvtable_CI_Tau_B3.txt',
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
#Warning: the MS table mstable_tmp.ms has 12 spectral windows. By default all of them are exported. To choose which spws to export, provide split_args with the spw parameter.
#Exporting 4 channels per spw.
#Exporting visibilities to uvtable_CI_Tau_B3.txt...done.
#Removing temporary MS table mstable_tmp.ms

concat(
	vis = ['export_uvtable_SBs_lsb.ms','export_uvtable_LBs_lsb.ms'],
	concatvis = 'export_uvtable_lsb.ms',
	dirtol = '0.1arcsec',
	copypointing = False,
)
#2023-04-12 19:52:12	WARN	MSConcat::concatenate (file casacore/ms/MSOper/MSConcat.cc, line 996)	Zero or negative scan numbers in MS. May lead to duplicate scan numbers in concatenated MS.

listobs(
	vis = 'export_uvtable_lsb.ms',
	listfile = 'export_uvtable_lsb.ms.listobs.txt',
	overwrite = True
)

export_uvtable(
	'uvtable_CI_Tau_B3_lsb.txt',
	tb,
	channel = 'all',
	split = split,
	split_args = {'vis':'export_uvtable_lsb.ms',
                  'keepflags':False,
                  'datacolumn':'DATA'},
	verbose = True,
)
#Applying split. Creating temporary MS table mstable_tmp.ms from original MS table export_uvtable_lsb.ms
#datacolumn has been changed from "CORRECTED_DATA" to "DATA" in order to operate on the new ms
#Reading mstable_tmp.ms
#Warning: the MS table mstable_tmp.ms has 6 spectral windows. By default all of them are exported. To choose which spws to export, provide split_args with the spw parameter.
#Exporting 4 channels per spw.
#Exporting visibilities to uvtable_CI_Tau_B3_lsb.txt...done.
#Removing temporary MS table mstable_tmp.ms

concat(
	vis = ['export_uvtable_SBs_usb.ms','export_uvtable_LBs_usb.ms'],
	concatvis = 'export_uvtable_usb.ms',
	dirtol = '0.1arcsec',
	copypointing = False,
)
#2023-04-12 19:52:36	WARN	MSConcat::concatenate (file casacore/ms/MSOper/MSConcat.cc, line 996)	Zero or negative scan numbers in MS. May lead to duplicate scan numbers in concatenated MS.

listobs(
	vis = 'export_uvtable_usb.ms',
	listfile = 'export_uvtable_usb.ms.listobs.txt',
	overwrite = True
)

export_uvtable(
	'uvtable_CI_Tau_B3_usb.txt',
	tb,
	channel = 'all',
	split = split,
	split_args = {'vis':'export_uvtable_usb.ms',
                  'keepflags':False,
                  'datacolumn':'DATA'},
	verbose = True,
)
#Applying split. Creating temporary MS table mstable_tmp.ms from original MS table export_uvtable_usb.ms
#datacolumn has been changed from "CORRECTED_DATA" to "DATA" in order to operate on the new ms
#Reading mstable_tmp.ms
#Warning: the MS table mstable_tmp.ms has 6 spectral windows. By default all of them are exported. To choose which spws to export, provide split_args with the spw parameter.
#Exporting 4 channels per spw.
#Exporting visibilities to uvtable_CI_Tau_B3_usb.txt...done.
#Removing temporary MS table mstable_tmp.ms
