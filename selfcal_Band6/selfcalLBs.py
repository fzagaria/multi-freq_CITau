# Go for T instead of G for p1, because the gain phase solutions are less extreme (but no big difference from p2 onwards)
# Keep the ap0 step: the SNR slightly decreses but the noise structure improve substantially. No ap1.

import sys
sys.path.append('/data/discsim2/fz258/casa/analysis_scripts')
import analysisUtils as au

execfile('/data/discsim2/fz258/casa/reduction_utils.py')

prefix = 'CI_Tau'

cont_LB_p0 = prefix + '_LB_initcont_conc.ms'

# cont. sens.: 0.0159 mJy/beam, ang. res.: 0.035 arcsec

# select reference antennas for SB_EB0: DA49, DA41, DV20, DV22, ...

# select reference antennas for LB_EB0: DV09, DA61, DV24, DV20, ...

# select reference antennas for LB_EB1: DA61, DA57, DV24, DV09, ...

# get_station_numbers('CI_Tau_LB_initcont_conc.ms','DA49')
# Observation ID 0: DA49@A002

# get_station_numbers('CI_Tau_LB_initcont_conc.ms','DA61')
# Observation ID 1: DA61@A015

LB_refant = 'DA49@A002,DA61@A015'

mask_pa  = 11.28 # position angle of mask in degrees from Cathie's paper
mask_maj = 2.    # semimajor axis of mask in arcsec
mask_min = 1.25  # semiminor axis of mask in arcsec
mask_ra  = '04h33m52.026900s'
mask_dec = '22d50m29.780037s'
mask = 'ellipse[[%s, %s], [%.1farcsec, %.1farcsec], %.1fdeg]' % \
           (mask_ra, mask_dec, mask_maj, mask_min, mask_pa)
noise_annulus = "annulus[[%s, %s],['%.2farcsec', '6.arcsec']]" % \
                (mask_ra, mask_dec, 1.5*mask_maj)

contspws = '0~7'

LB_scales = [0, 8, 20, 50, 100, 300]

spw_mapping = [0, 0, 0, 0,
               4, 4, 4, 4]

LB_p0 = prefix + '_LB_p0'
os.system('rm -rf ' + LB_p0 + '.*')
tclean_wrapper_b3(
	vis = cont_LB_p0,
    imagename = LB_p0,
    mask = mask,
    scales = LB_scales,
    threshold = '0.032mJy',    # 3 const. sens.
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0035arcsec', # 1/10 ang. res.
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_p0 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
             
#CI_Tau_LB_p0.image.tt0
#Beam 0.065 arcsec x 0.043 arcsec (31.10 deg)
#Flux inside disk mask: 150.46 mJy
#Peak intensity of source: 3.54 mJy/beam
#rms: 1.11e-02 mJy/beam
#Peak SNR: 319.42

LB_p1 = prefix + '_LB.p1'
os.system('rm -rf ' + LB_p1)
gaincal(
	vis = cont_LB_p0,
    caltable = LB_p1,
    gaintype = 'T',
    combine = 'scan',
    spw = contspws, 
    refant = LB_refant,
    calmode = 'p',
    solint = 'inf',
    minsnr = 4.0,
    minblperant = 4
)

plotms('CI_Tau_LB.p1',xaxis='time',yaxis='phase',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_LB.p1.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

# Check solution by antenna:
# plotms('CI_Tau_LB.p1',xaxis='time',yaxis='phase',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

applycal(
	vis = cont_LB_p0,
    spw = contspws,
    spwmap = [0,1,2,3,4,5,6,7],
    gaintable = [LB_p1],
    calwt = True,
    interp = 'linear',
    applymode = 'calonly'
)
         
LB_cont_p1 = prefix + '_LB_contp1.ms'
os.system('rm -rf ' + LB_cont_p1)
os.system('rm -rf ' + LB_cont_p1 + '.flagversions')
split(
	vis = cont_LB_p0,
    outputvis = LB_cont_p1,
    datacolumn = 'corrected'
)

LB_ima_p1 = prefix + '_LB_initcont_p1'
os.system('rm -rf ' + LB_ima_p1 + '.*')
tclean_wrapper_b3(
	vis = LB_cont_p1,
    imagename = LB_ima_p1,
    mask = mask,
    scales = LB_scales,
    threshold = '0.032mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0035arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_p1 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
         
#CI_Tau_LB_initcont_p1.image.tt0
#Beam 0.065 arcsec x 0.043 arcsec (31.10 deg)
#Flux inside disk mask: 151.21 mJy
#Peak intensity of source: 3.55 mJy/beam
#rms: 1.10e-02 mJy/beam
#Peak SNR: 323.82

LB_p2 = prefix + '_LB.p2'
os.system('rm -rf ' + LB_p2)
gaincal(
	vis = LB_cont_p1,
    caltable = LB_p2,
    gaintype = 'T',
    combine = 'scan,spw',
    spw = contspws,
    refant = LB_refant,
    calmode = 'p',
    solint = '360s',
    minsnr = 4.0,
    minblperant = 4
)

plotms('CI_Tau_LB.p2',xaxis='time',yaxis='phase',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_LB.p2.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

# Check solution by antenna:
# plotms('CI_Tau_LB.p2',xaxis='time',yaxis='phase',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

applycal(
	vis = LB_cont_p1,
    spw = contspws,
    spwmap = spw_mapping,
    gaintable = [LB_p2],
    calwt = True,
    interp = 'linearPD',
    applymode = 'calonly'
)
         
LB_cont_p2 = prefix + '_LB_contp2.ms'
os.system('rm -rf ' + LB_cont_p2)
os.system('rm -rf ' + LB_cont_p2 + '.flagversions')
split(
	vis = LB_cont_p1,
    outputvis = LB_cont_p2,
    datacolumn = 'corrected'
)

LB_ima_p2 = prefix + '_LB_initcont_p2'
os.system('rm -rf ' + LB_ima_p2 + '.*')
tclean_wrapper_b3(
	vis = LB_cont_p2,
    imagename = LB_ima_p2,
    mask = mask, 
    scales = LB_scales,
    threshold = '0.032mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0035arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_p2 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
             
#CI_Tau_LB_initcont_p2.image.tt0
#Beam 0.065 arcsec x 0.043 arcsec (31.10 deg)
#Flux inside disk mask: 151.02 mJy
#Peak intensity of source: 3.57 mJy/beam
#rms: 1.07e-02 mJy/beam
#Peak SNR: 332.36

LB_p3 = prefix + '_LB.p3'
os.system('rm -rf ' + LB_p3)
gaincal(
	vis = LB_cont_p2,
    caltable = LB_p3,
    gaintype = 'T',
    combine = 'scan,spw',
    spw = contspws,
    refant = LB_refant,
    calmode = 'p',
    solint = '180s',
    minsnr = 4.0,
    minblperant = 4
)

plotms('CI_Tau_LB.p3',xaxis='time',yaxis='phase',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_LB.p3.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

# Check solution by antenna:
# plotms('CI_Tau_LB.p3',xaxis='time',yaxis='phase',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

applycal(
	vis = LB_cont_p2,
    spw = contspws,
    spwmap = spw_mapping,
    gaintable = [LB_p3],
    calwt = True,
    interp = 'linearPD',
    applymode = 'calonly'
)
         
LB_cont_p3 = prefix + '_LB_contp3.ms'
os.system('rm -rf ' + LB_cont_p3)
os.system('rm -rf ' + LB_cont_p3 + '.flagversions')
split(
	vis = LB_cont_p2,
    outputvis = LB_cont_p3,
    datacolumn = 'corrected'
)

LB_ima_p3 = prefix + '_LB_initcont_p3'
os.system('rm -rf ' + LB_ima_p3 + '.*')
tclean_wrapper_b3(
	vis = LB_cont_p3,
    imagename = LB_ima_p3,
    mask = mask, 
    scales = LB_scales,
    threshold = '0.032mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0035arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_p3 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_initcont_p3.image.tt0
#Beam 0.065 arcsec x 0.043 arcsec (31.10 deg)
#Flux inside disk mask: 150.42 mJy
#Peak intensity of source: 3.64 mJy/beam
#rms: 1.09e-02 mJy/beam
#Peak SNR: 333.76

LB_p4 = prefix + '_LB.p4'
os.system('rm -rf ' + LB_p4)
gaincal(
	vis = LB_cont_p3,
    caltable = LB_p4,
    gaintype = 'T',
    combine = 'scan,spw',
    spw = contspws,
    refant = LB_refant,
    calmode = 'p',
    solint = '60s',
    minsnr = 4.0,
    minblperant = 4
)

plotms('CI_Tau_LB.p4',xaxis='time',yaxis='phase',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_LB.p4.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

# Check solution by antenna:
# plotms('CI_Tau_LB.p4',xaxis='time',yaxis='phase',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

applycal(
	vis = LB_cont_p3,
    spw = contspws,
    spwmap = spw_mapping,
    gaintable = [LB_p4],
    calwt = True,
    interp = 'linearPD',
    applymode = 'calonly'
)
         
LB_cont_p4 = prefix + '_LB_contp4.ms'
os.system('rm -rf ' + LB_cont_p4)
os.system('rm -rf ' + LB_cont_p4 + '.flagversions')
split(
	vis = LB_cont_p3,
    outputvis = LB_cont_p4,
    datacolumn = 'corrected'
)

LB_ima_p4 = prefix + '_LB_initcont_p4'
os.system('rm -rf ' + LB_ima_p4 + '.*')
tclean_wrapper_b3(
	vis = LB_cont_p4,
    imagename = LB_ima_p4,
    mask = mask, 
    scales = LB_scales,
    threshold = '0.032mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0035arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_p4 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_initcont_p4.image.tt0
#Beam 0.065 arcsec x 0.043 arcsec (31.10 deg)
#Flux inside disk mask: 151.30 mJy
#Peak intensity of source: 3.88 mJy/beam
#rms: 1.04e-02 mJy/beam
#Peak SNR: 373.49

LB_p5 = prefix + '_LB.p5'
os.system('rm -rf ' + LB_p5)
gaincal(
	vis = LB_cont_p4,
    caltable = LB_p5,
    gaintype = 'T',
    combine = 'scan,spw',
    spw = contspws,
    refant = LB_refant,
    calmode = 'p',
    solint = '30s',
    minsnr = 4.0,
    minblperant = 4
)

plotms('CI_Tau_LB.p5',xaxis='time',yaxis='phase',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_LB.p5.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

# Check solution by antenna:
# plotms('CI_Tau_LB.p5',xaxis='time',yaxis='phase',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

applycal(
	vis = LB_cont_p4,
    spw = contspws,
    spwmap = spw_mapping,
    gaintable = [LB_p5],
    calwt = True,
    interp = 'linearPD',
    applymode = 'calonly'
)
         
LB_cont_p5 = prefix + '_LB_contp5.ms'
os.system('rm -rf ' + LB_cont_p5)
os.system('rm -rf ' + LB_cont_p5 + '.flagversions')
split(
	vis = LB_cont_p4,
    outputvis = LB_cont_p5,
    datacolumn = 'corrected'
)

LB_ima_p5 = prefix + '_LB_initcont_p5'
os.system('rm -rf ' + LB_ima_p5 + '.*')
tclean_wrapper_b3(
	vis = LB_cont_p5,
    imagename = LB_ima_p5,
    mask = mask, 
    scales = LB_scales,
    threshold = '0.032mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0035arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_p5 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_initcont_p5.image.tt0
#Beam 0.065 arcsec x 0.043 arcsec (31.10 deg)
#Flux inside disk mask: 150.95 mJy
#Peak intensity of source: 3.97 mJy/beam
#rms: 1.04e-02 mJy/beam
#Peak SNR: 383.05

LB_p6 = prefix + '_LB.p6'
os.system('rm -rf ' + LB_p6)
gaincal(
	vis = LB_cont_p5,
    caltable = LB_p6,
    gaintype = 'T',
    combine = 'scan,spw',
    spw = contspws,
    refant = LB_refant,
    calmode = 'p',
    solint = '15s',
    minsnr = 4.0,
    minblperant = 4
)

plotms('CI_Tau_LB.p6',xaxis='time',yaxis='phase',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_LB.p6.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

# Check solution by antenna:
# plotms('CI_Tau_LB.p6',xaxis='time',yaxis='phase',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

applycal(
	vis = LB_cont_p5,
    spw = contspws,
    spwmap = spw_mapping,
    gaintable = [LB_p6],
    calwt = True,
    interp = 'linearPD',
    applymode = 'calonly'
)
         
LB_cont_p6 = prefix + '_LB_contp6.ms'
os.system('rm -rf ' + LB_cont_p6)
os.system('rm -rf ' + LB_cont_p6 + '.flagversions')
split(
	vis = LB_cont_p5,
    outputvis = LB_cont_p6,
    datacolumn = 'corrected'
)

LB_ima_p6 = prefix + '_LB_initcont_p6'
os.system('rm -rf ' + LB_ima_p6 + '.*')
tclean_wrapper_b3(
	vis = LB_cont_p6,
    imagename = LB_ima_p6,
    mask = mask, 
    scales = LB_scales,
    threshold = '0.032mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0035arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_p6 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_initcont_p6.image.tt0
#Beam 0.065 arcsec x 0.043 arcsec (31.10 deg)
#Flux inside disk mask: 150.60 mJy
#Peak intensity of source: 4.01 mJy/beam
#rms: 1.04e-02 mJy/beam
#Peak SNR: 385.79

# Clean deeper before amplitude self-cal
os.system('rm -rf ' + LB_ima_p6 + '.*')
tclean_wrapper_b3(
	vis = LB_cont_p6,
    imagename = LB_ima_p6,
    mask = mask, 
    scales = LB_scales,
    threshold = '0.00978mJy',   # 1 cont. sens.
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0035arcsec', # 1/10 ang. res.
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_p6 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
             
#CI_Tau_LB_initcont_p6.image.tt0
#Beam 0.065 arcsec x 0.043 arcsec (31.10 deg)
#Flux inside disk mask: 148.12 mJy
#Peak intensity of source: 4.01 mJy/beam
#rms: 9.79e-03 mJy/beam
#Peak SNR: 409.80

LB_ap0 = prefix + '_LB.ap0'
os.system('rm -rf ' + LB_ap0 + '*')
gaincal(
	vis = LB_cont_p6,
    caltable = LB_ap0,
    gaintype = 'T',
    combine = 'spw,scan',
    spw = contspws,
    refant = LB_refant,
    calmode = 'ap',
    solint = 'inf',
    minsnr = 4.0, 
    minblperant = 4
)

plotms('CI_Tau_LB.ap0',xaxis='time',yaxis='phase',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_LB.ap0_phase.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

plotms('CI_Tau_LB.ap0',xaxis='time',yaxis='amp',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_LB.ap0_amp.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

# Check solution by antenna:
# plotms('CI_Tau_LB.ap0',xaxis='time',yaxis='phase',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')
# plotms('CI_Tau_LB.ap0',xaxis='time',yaxis='amp',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

flagdata(
	vis = LB_ap0,
	mode = 'clip',
	clipminmax = [0.8,1.2],
	clipoutside = True,
	datacolumn = 'CPARAM'
)

plotms('CI_Tau_LB.ap0',xaxis='time',yaxis='phase',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_LB.ap0_phase_flagged.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

plotms('CI_Tau_LB.ap0',xaxis='time',yaxis='amp',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_LB.ap0_amp_flagged.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

# Check solution by antenna:
# plotms('CI_Tau_LB.ap0',xaxis='time',yaxis='phase',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')
# plotms('CI_Tau_LB.ap0',xaxis='time',yaxis='amp',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

applycal(
	vis = LB_cont_p6,
    spw = contspws,
    spwmap = spw_mapping,
    gaintable = [LB_ap0],
    calwt = True,
    interp = 'linearPD',
    applymode = 'calonly'
)
         
LB_cont_ap0 = prefix + '_LB_contap0.ms'
os.system('rm -rf ' + LB_cont_ap0)
os.system('rm -rf ' + LB_cont_ap0 + '.flagversions')
split(
	vis = LB_cont_p6,
    outputvis = LB_cont_ap0,
    datacolumn = 'corrected'
)

LB_ima_ap0 = prefix + '_LB_initcont_ap0'
os.system('rm -rf ' + LB_ima_ap0 + '.*')
tclean_wrapper_b3(
	vis = LB_cont_ap0,
    imagename = LB_ima_ap0,
    mask = mask,
    scales = LB_scales,
    threshold = '0.00978mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0035arcsec',
    robust = 1.0,
    interactive = False
)
               
estimate_SNR(
	LB_ima_ap0 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_initcont_ap0.image.tt0
#Beam 0.061 arcsec x 0.043 arcsec (29.67 deg)
#Flux inside disk mask: 149.11 mJy
#Peak intensity of source: 3.82 mJy/beam
#rms: 9.51e-03 mJy/beam
#Peak SNR: 402.06
'''
LB_ap1 = prefix + '_LB.ap1'
os.system('rm -rf ' + LB_ap1 + '*')
gaincal(
	vis = LB_cont_ap0,
    caltable = LB_ap1,
    gaintype = 'T',
    combine = 'spw,scan',
    spw = contspws,
    refant = LB_refant,
    calmode = 'ap',
    solint = '360s',
    minsnr = 4.0, 
    minblperant = 4
)

plotms('CI_Tau_LB.ap1',xaxis='time',yaxis='phase',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_LB.ap1_phase.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

plotms('CI_Tau_LB.ap1',xaxis='time',yaxis='amp',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_LB.ap1_amp.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

# Check solution by antenna:
# plotms('CI_Tau_LB.ap1',xaxis='time',yaxis='phase',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')
# plotms('CI_Tau_LB.ap1',xaxis='time',yaxis='amp',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

flagdata(
	vis = LB_ap1,
	mode = 'clip',
	clipminmax = [0.8,1.2],
	clipoutside = True,
	datacolumn = 'CPARAM'
)

plotms('CI_Tau_LB.ap1',xaxis='time',yaxis='phase',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_LB.ap1_phase_flagged.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

plotms('CI_Tau_LB.ap1',xaxis='time',yaxis='amp',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_LB.ap1_amp_flagged.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

# Check solution by antenna:
# plotms('CI_Tau_LB.ap1',xaxis='time',yaxis='phase',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')
# plotms('CI_Tau_LB.ap1',xaxis='time',yaxis='amp',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

applycal(
	vis = LB_cont_ap0,
    spw = contspws,
    spwmap = spw_mapping,
    gaintable = [LB_ap1],
    calwt = True,
    interp = 'linearPD',
    applymode = 'calonly'
)
         
LB_cont_ap1 = prefix + '_LB_contap1.ms'
os.system('rm -rf ' + LB_cont_ap1)
os.system('rm -rf ' + LB_cont_ap1 + '.flagversions')
split(
	vis = LB_cont_ap0,
    outputvis = LB_cont_ap1,
    datacolumn = 'corrected'
)

LB_ima_ap1 = prefix + '_LB_initcont_ap1'
os.system('rm -rf ' + LB_ima_ap1 + '.*')
tclean_wrapper_b3(
	vis = LB_cont_ap1,
    imagename = LB_ima_ap1,
    mask = mask,
    scales = LB_scales,
    threshold = '0.0095mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0035arcsec',
    robust = 1.0,
    interactive = False
)
               
estimate_SNR(
	LB_ima_ap1 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
             
#CI_Tau_LB_initcont_ap1.image.tt0
#Beam 0.060 arcsec x 0.043 arcsec (28.74 deg)
#Flux inside disk mask: 149.47 mJy
#Peak intensity of source: 3.71 mJy/beam
#rms: 9.30e-03 mJy/beam
#Peak SNR: 398.37
'''
