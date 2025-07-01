import sys
sys.path.append('/data/discsim2/fz258/casa/analysis_scripts')
import analysisUtils as au

execfile('/data/discsim2/fz258/casa/reduction_utils.py')

path   = '/data/discsim2/fz258/CI_Tau_B6/'

prefix = 'CI_Tau'

name_SB_EB0 = 'uid___A002_Xb74a0f_X166a.ms.split.cal'

name_LB_EB0 = 'uid___A002_Xc4bcba_X1f20.ms.split.cal'

name_LB_EB1 = 'uid___A002_Xc4c2da_X2903.ms.split.cal'

data_params = {
	'SB_EB0' : {
		'vis'  : 'CI_Tau_SB_EB0.ms',
		'name' : 'SB_EB0',
   		'field': 'CI_Tau',
	},

	'LB_EB0' : {
		'vis'  : 'CI_Tau_LB_EB0.ms',
		'name' : 'LB_EB0',
    	'field': 'ci_tau',
	},

	'LB_EB1' : {
		'vis'  : 'CI_Tau_LB_EB1.ms',
		'name' : 'LB_EB1',
    	'field': 'ci_tau',
	},
}

listobs(
	vis = path + name_SB_EB0,
    listfile = name_SB_EB0 + '.listobs.txt',
    overwrite = True
)
# field: CI_Tau; spws: 0,1,2,3;     pos: 04:33:52.014000 +22.50.30.06000 ICRS

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
# au.getBaselineLengths(SB_EB0['vis'])
# SB_EB0 have max baselines of ~ 1604.860989 m, hence channels of less than 398.638 MHz
# Channel width of MHz average [120,480,480,240] channels (234.37488MHz width)

avg_cont(
	data_params['SB_EB0'], 
	output_prefix = 'CI_Tau', 
	flagchannels = '',
	contspws = '0~3',
	width_array = [120,480,480,240],
)
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
# field: ci_tau; spws: 17,19,21,23; pos: 04:33:52.002332 +22.50.29.88515 ICRS

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
# LB_EB0 have max baselines of ~ 12145.220747 m, hence channels of less than 52.5119 MHz
# Channel width of MHz average [2,2,2,2] channels (31.250MHz width)

avg_cont(
	data_params['LB_EB0'], 
	output_prefix = 'CI_Tau', 
	flagchannels = '',
	contspws = '17,19,21,23',
	width_array = [2,2,2,2],
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
# field: ci_tau; spws: 17,19,21,23; pos: 04:33:52.002331 +22.50.29.88511 ICRS

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
# LB_EB0 have max baselines of ~ 12145.220747 m, hence channels of less than 52.5119 MHz
# Channel width of MHz average [2,2,2,2] channels (31.250MHz width)

avg_cont(
	data_params['LB_EB1'], 
	output_prefix = 'CI_Tau', 
	flagchannels = '',
	contspws = '17,19,21,23',
	width_array = [2,2,2,2],
)
#Averaged continuum dataset saved to CI_Tau_LB_EB1_initcont.ms

listobs(
	vis = 'CI_Tau_LB_EB1_initcont.ms',
    listfile = 'CI_Tau_LB_EB1_initcont.ms.listobs.txt',
    overwrite = True
)
