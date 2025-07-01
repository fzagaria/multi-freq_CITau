import sys
sys.path.append('/data/discsim2/fz258/casa/analysis_scripts')
import analysisUtils as au

execfile('/data/discsim2/fz258/casa/reduction_utils.py')

path   = '/data/discsim2/fz258/CI_Tau_B3/'

prefix = 'CI_Tau'

name_SB_EB0 = 'uid___A002_Xed9025_X1a19.ms.split.cal'

name_LB_EB0 = 'uid___A002_Xde2e20_X1745.ms.split.cal'

name_LB_EB1 = 'uid___A002_Xde63ab_X1d88.ms.split.cal'

data_params = {
	'SB_EB0' : {
		'vis'  : 'CI_Tau_SB_EB0.ms',
		'name' : 'SB_EB0',
   		'field': 'CI_Tau',
	},

	'LB_EB0' : {
		'vis'  : 'CI_Tau_LB_EB0.ms',
		'name' : 'LB_EB0',
    	'field': 'CI_Tau',
	},

	'LB_EB1' : {
		'vis'  : 'CI_Tau_LB_EB1.ms',
		'name' : 'LB_EB1',
    	'field': 'CI_Tau',
	},
}

listobs(
	vis = path + name_SB_EB0,
    listfile = name_SB_EB0 + '.listobs.txt',
    overwrite = True
)
# field: CI_Tau; spws: 23,25,27,29; pos: 04:33:52.028250 +22.50.29.72601 ICRS

os.system('rm -rf ' + data_params['SB_EB0']['vis'])
split(
	vis = path + name_SB_EB0,
    outputvis = data_params['SB_EB0']['vis'],
    datacolumn = 'data',
    field = data_params['SB_EB0']['field'],
	intent = 'OBSERVE_TARGET#ON_SOURCE',
    keepflags = False
)

listobs(
	vis = data_params['SB_EB0']['vis'],
    listfile = data_params['SB_EB0']['vis'] + '.listobs.txt',
    overwrite = True
)

plotms('CI_Tau_SB_EB0.ms',xaxis='freq',yaxis='amp',showgui=False,avgtime='1e8',avgscan=True,
	showatm=True,iteraxis='spw',yselfscale=True,transform=True,freqframe='LSRK',
	plotfile='CI_Tau_SB_EB0.png',exprange='all',overwrite=True) 

# Average to reasonable channel width to avoid bandwidth smearing
# au.getBaselineLengths(data_params['SB_EB0']['vis'])
# SB_EB0 have max baselines of 2386.147763 m, hence channels of less than 107.389171362 MHz
# Channel width of MHz average [80,80,80,80] channels (78.12496MHz width)

avg_cont(
	data_params['SB_EB0'], 
	output_prefix = 'CI_Tau', 
	flagchannels = '',
	contspws = '23,25,27,29',
	width_array = [80,80,80,80],
)
#WARN MSTransformManager::checkCorrelatorPreaveraging The data has already been preaveraged by the correlator but further smoothing or averaging has been requested. Preaveraged SPWs are: 23 25 27 29
#Averaged continuum dataset saved to CI_Tau_SB_EB0_initcont.ms

listobs(
	vis = 'CI_Tau_SB_EB0_initcont.ms',
    listfile = 'CI_Tau_SB_EB0_initcont.ms.listobs.txt',
    overwrite = True
)

listobs(
	vis = path + name_LB_EB0,
    listfile = name_LB_EB0 + '.listobs.txt',
    overwrite = True
)
# field: CI_Tau; spws: 23,25,27,29; pos: 04:33:52.026951 +22.50.29.76044 ICRS

os.system('rm -rf ' + data_params['LB_EB0']['vis'])
split(
	vis = path + name_LB_EB0,
    outputvis = data_params['LB_EB0']['vis'],
    datacolumn = 'data',
    field = data_params['LB_EB0']['field'],
	intent = 'OBSERVE_TARGET#ON_SOURCE',
    keepflags = False
)

listobs(
	vis = data_params['LB_EB0']['vis'],
    listfile = data_params['LB_EB0']['vis'] + '.listobs.txt',
    overwrite = True
)

plotms('CI_Tau_LB_EB0.ms',xaxis='freq',yaxis='amp',showgui=False,avgtime='1e8',avgscan=True,
	showatm=True,iteraxis='spw',yselfscale=True,transform=True,freqframe='LSRK',
	plotfile='CI_Tau_LB_EB0.png',exprange='all',overwrite=True)

# Average to reasonable channel width to avoid bandwidth smearing
# au.getBaselineLengths(data_params['LB_EB0']['vis'])
# LB_EB0 have max baselines of 16196.309961 m, hence channels of less than 15.821284702 MHz
# Channel width of MHz average [15,15,15,15] channels (14.648MHz width)

avg_cont(
	data_params['LB_EB0'], 
	output_prefix = 'CI_Tau', 
	flagchannels = '',
	contspws = '23,25,27,29',
	width_array = [15,15,15,15],
)
#Averaged continuum dataset saved to CI_Tau_LB_EB0_initcont.ms

listobs(
	vis = 'CI_Tau_LB_EB0_initcont.ms',
    listfile = 'CI_Tau_LB_EB0_initcont.ms.listobs.txt',
    overwrite = True
)

listobs(
	vis = path + name_LB_EB1,
    listfile = name_LB_EB1 + '.listobs.txt',
    overwrite = True
)
# field: CI_Tau; spws: 23,25,27,29; pos: 04:33:52.026963 +22.50.29.76011 ICRS

os.system('rm -rf ' + data_params['LB_EB1']['vis'])
split(
	vis = path + name_LB_EB1,
    outputvis = data_params['LB_EB1']['vis'],
    datacolumn = 'data',
    field = data_params['LB_EB1']['field'],
	intent = 'OBSERVE_TARGET#ON_SOURCE',
    keepflags = False
)

listobs(
	vis = data_params['LB_EB1']['vis'],
    listfile = data_params['LB_EB1']['vis'] + '.listobs.txt',
    overwrite = True
)

plotms('CI_Tau_LB_EB1.ms',xaxis='freq',yaxis='amp',showgui=False,avgtime='1e8',avgscan=True,
	showatm=True,iteraxis='spw',yselfscale=True,transform=True,freqframe='LSRK',
	plotfile='CI_Tau_LB_EB1.png',exprange='all',overwrite=True)

# Average to reasonable channel width to avoid bandwidth smearing
# au.getBaselineLengths(data_params['LB_EB1']['vis'])
# LB_EB1 have max baselines of 16196.309961 m, hence channels of less than 15.821284702 MHz
# Channel width of MHz average [15,15,15,15] channels (14.648MHz width)

avg_cont(
	data_params['LB_EB1'], 
	output_prefix = 'CI_Tau', 
	flagchannels = '',
	contspws = '23,25,27,29',
	width_array = [15,15,15,15],
)
#Averaged continuum dataset saved to CI_Tau_LB_EB1_initcont.ms

listobs(
	vis = 'CI_Tau_LB_EB1_initcont.ms',
    listfile = 'CI_Tau_LB_EB1_initcont.ms.listobs.txt',
    overwrite = True
)