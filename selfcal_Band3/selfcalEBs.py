#Both calmode = G and T do not improve the LBs SNR much.

import sys
sys.path.append('/data/discsim2/fz258/casa/analysis_scripts')
import analysisUtils as au

execfile('/data/discsim2/fz258/casa/reduction_utils.py')

prefix = 'CI_Tau'

LB_EB0 = 'CI_Tau_LB_EB0_initcont.ms'

# cont. sens.: 0.0097 mJy/beam, ang. res.: 0.052 arcsec

# select reference antennas for LB_EB0: DV12, PM02, DV08, DA65, ...

# get_station_numbers('CI_Tau_LB_EB0_initcont.ms','PM02')
# Observation ID 0: PM02@A135

LB_EB0_refant = 'PM02@A135'

mask_pa  = 11.28 # position angle of mask in degrees from Cathie's paper
mask_maj = 2.    # semimajor axis of mask in arcsec
mask_min = 1.25  # semiminor axis of mask in arcsec
mask_ra  = '04h33m52.026951s'   
mask_dec = '22d50m29.760440s'
mask = 'ellipse[[%s, %s], [%.1farcsec, %.1farcsec], %.1fdeg]' % \
           (mask_ra, mask_dec, mask_maj, mask_min, mask_pa)
noise_annulus = "annulus[[%s, %s],['%.2farcsec', '6.arcsec']]" % \
                (mask_ra, mask_dec, 1.5*mask_maj)

contspws = '0~3'

LB_EB0_scales = [0, 8, 20, 50, 100, 300]

LB_EB0_p0 = prefix + '_LB_EB0_p0'
os.system('rm -rf ' + LB_EB0_p0 + '.*')
tclean_wrapper_b3(
	vis = LB_EB0,
    imagename = LB_EB0_p0,
    mask = mask,
    scales = LB_EB0_scales,
    threshold = '0.029mJy',    # 3 const. sens.
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0052arcsec', # 1/10 ang. res.
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_EB0_p0 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_EB0_p0.image.tt0
#Beam 0.095 arcsec x 0.058 arcsec (16.71 deg)
#Flux inside disk mask: 16.47 mJy
#Peak intensity of source: 1.13 mJy/beam
#rms: 1.14e-02 mJy/beam
#Peak SNR: 98.81

LB_EB0_p1 = prefix + '_LB_EB0.p1'
os.system('rm -rf ' + LB_EB0_p1)
gaincal(
	vis = LB_EB0,
    caltable = LB_EB0_p1,
    gaintype = 'G',
    combine = 'scan',
    spw = contspws, 
    refant = LB_EB0_refant,
    calmode = 'p',
    solint = 'inf',
    minsnr = 4.0,
    minblperant = 4
)

plotms('CI_Tau_LB_EB0.p1',xaxis='time',yaxis='phase',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_LB_EB0.p1.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

# Check solution by antenna:
# plotms('CI_Tau_LB_EB0.p1',xaxis='time',yaxis='phase',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

applycal(
	vis = LB_EB0,
    spw = contspws,
    spwmap = [0,1,2,3],
    gaintable = [LB_EB0_p1],
    calwt = True,
    interp = 'linear',
    applymode = 'calonly'
)
         
LB_EB0_cont_p1 = prefix + '_LB_EB0_contp1.ms'
os.system('rm -rf ' + LB_EB0_cont_p1)
os.system('rm -rf ' + LB_EB0_cont_p1 + '.flagversions')
split(
	vis = LB_EB0,
    outputvis = LB_EB0_cont_p1,
    datacolumn = 'corrected'
)

LB_EB0_ima_p1 = prefix + '_LB_EB0_initcont_p1'
os.system('rm -rf ' + LB_EB0_ima_p1 + '.*')
tclean_wrapper_b3(
	vis = LB_EB0_cont_p1,
    imagename = LB_EB0_ima_p1,
    mask = mask,
    scales = LB_EB0_scales,
    threshold = '0.029mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0052arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_EB0_ima_p1 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_EB0_initcont_p1.image.tt0
#Beam 0.095 arcsec x 0.058 arcsec (16.71 deg)
#Flux inside disk mask: 16.66 mJy
#Peak intensity of source: 1.14 mJy/beam
#rms: 1.13e-02 mJy/beam
#Peak SNR: 100.90

LB_EB1 = 'CI_Tau_LB_EB1_initcont.ms'

# cont. sens.: 0.0097 mJy/beam, ang. res.: 0.052 arcsec

# select reference antennas for LB_EB1: PM02, PM04, DV08, DV18, ...

# get_station_numbers('CI_Tau_LB_EB1_initcont.ms','PM02')
# Observation ID 1: PM02@A135

LB_EB1_refant = 'PM02@A135'

mask_pa  = 11.28 # position angle of mask in degrees from Cathie's paper
mask_maj = 2.    # semimajor axis of mask in arcsec
mask_min = 1.25  # semiminor axis of mask in arcsec
mask_ra  = '04h33m52.026963s'  
mask_dec = '22d50m29.760110s'
mask = 'ellipse[[%s, %s], [%.1farcsec, %.1farcsec], %.1fdeg]' % \
           (mask_ra, mask_dec, mask_maj, mask_min, mask_pa)
noise_annulus = "annulus[[%s, %s],['%.2farcsec', '6.arcsec']]" % \
                (mask_ra, mask_dec, 1.5*mask_maj)

contspws = '0~3'

LB_EB1_scales = [0, 8, 20, 50, 100, 300]

LB_EB1_p0 = prefix + '_LB_EB1_p0'
os.system('rm -rf ' + LB_EB1_p0 + '.*')
tclean_wrapper_b3(
	vis = LB_EB1,
    imagename = LB_EB1_p0,
    mask = mask,
    scales = LB_EB1_scales,
    threshold = '0.029mJy',    # 3 const. sens.
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0052arcsec', # 1/10 ang. res.
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_EB1_p0 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#Beam 0.075 arcsec x 0.052 arcsec (-11.36 deg)
#Flux inside disk mask: 16.97 mJy
#Peak intensity of source: 0.89 mJy/beam
#rms: 9.18e-03 mJy/beam
#Peak SNR: 97.11
            
LB_EB1_p1 = prefix + '_LB_EB1.p1'
os.system('rm -rf ' + LB_EB1_p1)
gaincal(
	vis = LB_EB1,
    caltable = LB_EB1_p1,
    gaintype = 'G',
    combine = 'scan',
    spw = contspws, 
    refant = LB_EB1_refant,
    calmode = 'p',
    solint = 'inf',
    minsnr = 4.0,
    minblperant = 4
)

plotms('CI_Tau_LB_EB1.p1',xaxis='time',yaxis='phase',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_LB_EB1.p1.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

# Check solution by antenna:
# plotms('CI_Tau_LB_EB1.p1',xaxis='time',yaxis='phase',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

applycal(
	vis = LB_EB1,
    spw = contspws,
    spwmap = [0,1,2,3],
    gaintable = [LB_EB1_p1],
    calwt = True,
    interp = 'linear',
    applymode = 'calonly'
)
         
LB_EB1_cont_p1 = prefix + '_LB_EB1_contp1.ms'
os.system('rm -rf ' + LB_EB1_cont_p1)
os.system('rm -rf ' + LB_EB1_cont_p1 + '.flagversions')
split(
	vis = LB_EB1,
    outputvis = LB_EB1_cont_p1,
    datacolumn = 'corrected'
)

LB_EB1_ima_p1 = prefix + '_LB_EB1_initcont_p1'
os.system('rm -rf ' + LB_EB1_ima_p1 + '.*')
tclean_wrapper_b3(
	vis = LB_EB1_cont_p1,
    imagename = LB_EB1_ima_p1,
    mask = mask,
    scales = LB_EB1_scales,
    threshold = '0.029mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0052arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_EB1_ima_p1 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_EB1_initcont_p1.image.tt0
#Beam 0.075 arcsec x 0.052 arcsec (-11.36 deg)
#Flux inside disk mask: 17.00 mJy
#Peak intensity of source: 0.90 mJy/beam
#rms: 9.14e-03 mJy/beam
#Peak SNR: 98.82