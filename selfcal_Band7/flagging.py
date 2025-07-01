import sys
sys.path.append('/data/discsim2/fz258/casa/analysis_scripts')
import analysisUtils as au

execfile('/data/discsim2/fz258/casa/reduction_utils.py')

path   = '/data/discsim2/fz258/CI_Tau_B7/'

prefix = 'CI_Tau'

name_LB_EB0 = 'uid___A002_Xc7bfc7_X4b6d.ms.split.cal'

name_LB_EB1 = 'uid___A002_Xc7bfc7_X4113.ms.split.cal'

data_params = {
	'LB_EB0' : {
		'vis'       : 'CI_Tau_LB_EB0.ms',
		'name'      : 'LB_EB0',
    	'field'     : 'CI_Tau',
    	'line_spws' : np.array([25,27,29]),
    	'line_freqs': np.array([3.305880e11,3.428829e11,3.457960e11]),
	},

	'LB_EB1' : {
		'vis'       : 'CI_Tau_LB_EB1.ms',
		'name'      : 'LB_EB1',
    	'field'     : 'CI_Tau',
    	'line_spws' : np.array([25,27,29]),
    	'line_freqs': np.array([3.305880e11,3.428829e11,3.457960e11]),
	},
}

listobs(
	vis = path + name_LB_EB0,
    listfile = name_LB_EB0 + '.listobs.txt',
    overwrite = True
)
# field: CI_Tau; spws: 19,25,27,29; pos: 04:33:52.002664 +22.50.29.88035 ICRS

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

plotms('CI_Tau_LB_EB0.ms',xaxis='vel',yaxis='amp',showgui=False,avgtime='1e8',avgscan=True,
	yselfscale=True,transform=True,freqframe='LSRK',restfreq='330.5880GHz',
	spw='25',plotrange=[-50,50,0,4],plotfile='CI_Tau_LB_EB0_Spw25_13CO.png',overwrite=True)

plotms('CI_Tau_LB_EB0.ms',xaxis='vel',yaxis='amp',showgui=False,avgtime='1e8',avgscan=True,
	yselfscale=True,transform=True,freqframe='LSRK',restfreq='342.8829GHz',
	spw='27',plotrange=[-50,50,0,4],plotfile='CI_Tau_LB_EB0_Spw27_CS.png',overwrite=True)

plotms('CI_Tau_LB_EB0.ms',xaxis='vel',yaxis='amp',showgui=False,avgtime='1e8',avgscan=True,
	yselfscale=True,transform=True,freqframe='LSRK',restfreq='345.7960GHz',
	spw='29',plotrange=[-50,50,0,4],plotfile='CI_Tau_LB_EB0_Spw29_12CO.png',overwrite=True)

LB_EB0_flagchannels_string = get_flagchannels(
	data_params['LB_EB0'], 
	output_prefix = 'CI_Tau', 
	velocity_range = np.array([-5.0,15.0]))
# Flagchannels input string for LB_EB0: '25:1268~1313, 27:697~744, 29:1095~1142'

# Flag lines and average to reasonable channel width to avoid bandwidth smearing
# au.getBaselineLengths(LB_EB0['vis'])
# LB_EB0 have max baselines of 3320.964792m, hence channels of less than 283.950MHz
# Channel width of MHz average [16,240,240,240] channels

avg_cont(
	data_params['LB_EB0'], 
	output_prefix = 'CI_Tau_flagtest', 
	flagchannels = LB_EB0_flagchannels_string,
	contspws = '19,25,27,29',
	width_array = [1,1,1,1],
)

plotms('CI_Tau_flagtest_LB_EB0_initcont.ms',xaxis='freq',yaxis='amp',showgui=False,avgtime='1e8',avgscan=True,
	showatm=True,iteraxis='spw',yselfscale=True,transform=True,freqframe='LSRK',
	plotfile='CI_Tau_LB_EB0_flagged.png',exprange='all',overwrite=True) 

os.system('rm -rf CI_Tau_LB_EB0_initcont.ms.flagversions')
os.system('rm -rf CI_Tau_LB_EB0_initcont.ms')
avg_cont(
	data_params['LB_EB0'], 
	output_prefix = 'CI_Tau', 
	flagchannels = LB_EB0_flagchannels_string,
	contspws = '19,25,27,29',
	width_array = [16,240,240,240],
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
# field: CI_Tau; spws: 19,25,27,29; pos: 04:33:52.002664 +22.50.29.88035 ICRS

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

plotms('CI_Tau_LB_EB1.ms',xaxis='vel',yaxis='amp',showgui=False,avgtime='1e8',avgscan=True,
	yselfscale=True,transform=True,freqframe='LSRK',restfreq='330.5880GHz',
	spw='25',plotrange=[-50,50,0,4],plotfile='CI_Tau_LB_EB1_Spw25_13CO.png',overwrite=True)

plotms('CI_Tau_LB_EB1.ms',xaxis='vel',yaxis='amp',showgui=False,avgtime='1e8',avgscan=True,
	yselfscale=True,transform=True,freqframe='LSRK',restfreq='342.8829GHz',
	spw='27',plotrange=[-50,50,0,4],plotfile='CI_Tau_LB_EB1_Spw27_CS.png',overwrite=True)

plotms('CI_Tau_LB_EB1.ms',xaxis='vel',yaxis='amp',showgui=False,avgtime='1e8',avgscan=True,
	yselfscale=True,transform=True,freqframe='LSRK',restfreq='345.7960GHz',
	spw='29',plotrange=[-50,50,0,4],plotfile='CI_Tau_LB_EB1_Spw29_12CO.png',overwrite=True)

LB_EB1_flagchannels_string = get_flagchannels(
	data_params['LB_EB1'], 
	output_prefix = 'CI_Tau', 
	velocity_range = np.array([-5.0,15.0]))
# Flagchannels input string for LB_EB1: '25:1268~1313, 27:697~744, 29:1095~1142'

# Flag lines and average to reasonable channel width to avoid bandwidth smearing
# au.getBaselineLengths(LB_EB1['vis'])
# LB_EB1 have max baselines of 3320.964792m, hence channels of less than 283.950MHz
# Channel width of MHz average [16,240,240,240] channels

avg_cont(
	data_params['LB_EB1'], 
	output_prefix = 'CI_Tau_flagtest', 
	flagchannels = LB_EB1_flagchannels_string,
	contspws = '19,25,27,29',
	width_array = [1,1,1,1],
)

plotms('CI_Tau_flagtest_LB_EB1_initcont.ms',xaxis='freq',yaxis='amp',showgui=False,avgtime='1e8',avgscan=True,
	showatm=True,iteraxis='spw',yselfscale=True,transform=True,freqframe='LSRK',
	plotfile='CI_Tau_LB_EB1_flagged.png',exprange='all',overwrite=True) 

os.system('rm -rf CI_Tau_LB_EB1_initcont.ms.flagversions')
os.system('rm -rf CI_Tau_LB_EB1_initcont.ms')
avg_cont(
	data_params['LB_EB1'], 
	output_prefix = 'CI_Tau', 
	flagchannels = LB_EB1_flagchannels_string,
	contspws = '19,25,27,29',
	width_array = [16,240,240,240],
)
#Averaged continuum dataset saved to CI_Tau_LB_EB1_initcont.ms

listobs(
	vis = 'CI_Tau_LB_EB1_initcont.ms',
    listfile = 'CI_Tau_LB_EB1_initcont.ms.listobs.txt',
    overwrite = True
)