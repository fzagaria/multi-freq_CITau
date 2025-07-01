# No flagging and substuntial (> 20 per cent) SNR increase make G a good choice.
# No need to test behaviour with T.

import sys
sys.path.append('/data/discsim2/fz258/casa/analysis_scripts')
import analysisUtils as au

execfile('/data/discsim2/fz258/casa/reduction_utils.py')

prefix = 'CI_Tau'

LB_EB0 = 'CI_Tau_LB_EB0_initcont.ms'

# cont. sens.: 0.0516 mJy/beam, ang. res.: 0.088 arcsec

# select reference antennas for LB_EB0: DV08, DV05, DV01, DV06, ...

# get_station_numbers('CI_Tau_LB_EB0_initcont.ms','DV08')
# Observation ID 0: DV08@A042

LB_EB0_refant = 'DV08@A042'

mask_pa  = 11.28 # position angle of mask in degrees from Cathie's paper
mask_maj = 2.    # semimajor axis of mask in arcsec
mask_min = 1.25  # semiminor axis of mask in arcsec
mask_ra  = '04h33m52.002664s'
mask_dec = '22d50m29.880350s'
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
    threshold = '0.155mJy',    # 3 const. sens.
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0088arcsec', # 1/10 ang. res.
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_EB0_p0 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
             
#CI_Tau_LB_EB0_p0.image.tt0
#Beam 0.162 arcsec x 0.088 arcsec (-44.07 deg)
#Flux inside disk mask: 404.82 mJy
#Peak intensity of source: 19.06 mJy/beam
#rms: 1.02e-01 mJy/beam
#Peak SNR: 187.67

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
    threshold = '0.155mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0088arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_EB0_ima_p1 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
             
#CI_Tau_LB_EB0_initcont_p1.image.tt0
#Beam 0.162 arcsec x 0.088 arcsec (-44.07 deg)
#Flux inside disk mask: 410.82 mJy
#Peak intensity of source: 19.22 mJy/beam
#rms: 8.54e-02 mJy/beam
#Peak SNR: 224.90

LB_EB1 = 'CI_Tau_LB_EB1_initcont.ms'

# cont. sens.: 0.0516 mJy/beam, ang. res.: 0.088 arcsec

# select reference antennas for LB_EB1: DA60, DA64, DV08, DV05, ...

# get_station_numbers('CI_Tau_LB_EB1_initcont.ms','DV08')
# Observation ID 1: DV08@A042

LB_EB1_refant = 'DV08@A042'

mask_pa  = 11.28 # position angle of mask in degrees from Cathie's paper
mask_maj = 2.    # semimajor axis of mask in arcsec
mask_min = 1.25  # semiminor axis of mask in arcsec
mask_ra  = '04h33m52.002664s'  
mask_dec = '22d50m29.880350s'
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
    threshold = '0.155mJy',    # 3 const. sens.
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0088arcsec', # 1/10 ang. res.
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_EB1_p0 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
             
#CI_Tau_LB_EB1_p0.image.tt0
#Beam 0.127 arcsec x 0.094 arcsec (-26.62 deg)
#Flux inside disk mask: 423.15 mJy
#Peak intensity of source: 19.39 mJy/beam
#rms: 8.44e-02 mJy/beam
#Peak SNR: 229.83

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
    threshold = '0.155mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0088arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_EB1_ima_p1 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
             
#CI_Tau_LB_EB1_initcont_p1.image.tt0
#Beam 0.127 arcsec x 0.094 arcsec (-26.61 deg)
#Flux inside disk mask: 430.12 mJy
#Peak intensity of source: 19.42 mJy/beam
#rms: 6.94e-02 mJy/beam
#Peak SNR: 279.89