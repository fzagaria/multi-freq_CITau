# Jump fifth phase calibration run. Residuals are best after p4 but only marginally.
# T or G in the first step gives negligible changes in the ap0. No ap1

import sys
sys.path.append('/data/discsim2/fz258/casa/analysis_scripts')
import analysisUtils as au

execfile('/data/discsim2/fz258/casa/reduction_utils.py')

prefix = 'CI_Tau'

cont_LB_p0 = prefix + '_LB_initcont_conc.ms'

# cont. sens.: 0.0097 mJy/beam, ang. res.: 0.052 arcsec

# select reference antennas for SB_EB0: DA65, DA43, DV06, DV17, ...

# select reference antennas for LB_EB0: DV12, PM02, DV08, DA65, ...

# select reference antennas for LB_EB1: PM02, PM04, DV08, DV18, ...

# get_station_numbers('CI_Tau_LB_initcont_conc.ms','DA65')
# Observation ID 0: DA65@A040

# get_station_numbers('CI_Tau_LB_initcont_conc.ms','PM02')
# Observation ID 0: PM02@A135

LB_refant = 'PM02@A135,DA65@A040'

mask_pa  = 11.28 # position angle of mask in degrees from Cathie's paper
mask_maj = 2.    # semimajor axis of mask in arcsec
mask_min = 1.25  # semiminor axis of mask in arcsec
mask_ra  = '04h33m52.027880s'
mask_dec = '22d50m29.748318s'
mask = 'ellipse[[%s, %s], [%.1farcsec, %.1farcsec], %.1fdeg]' % \
           (mask_ra, mask_dec, mask_maj, mask_min, mask_pa)
noise_annulus = "annulus[[%s, %s],['%.2farcsec', '6.arcsec']]" % \
                (mask_ra, mask_dec, 1.5*mask_maj)

contspws = '0~11'

LB_scales = [0, 8, 20, 50, 100, 300]

spw_mapping = [0, 0, 0, 0,
               4, 4, 4, 4,
			   8, 8, 8, 8]

LB_p0 = prefix + '_LB_p0'
os.system('rm -rf ' + LB_p0 + '.*')
tclean_wrapper_b3(
	vis = cont_LB_p0,
    imagename = LB_p0,
    mask = mask,
    scales = LB_scales,
    threshold = '0.018mJy',    # 3 const. sens.
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0052arcsec', # 1/10 ang. res.
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_p0 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
             
#CI_Tau_LB_p0.image.tt0
#Beam 0.151 arcsec x 0.071 arcsec (25.47 deg)
#Flux inside disk mask: 17.07 mJy
#Peak intensity of source: 1.31 mJy/beam
#rms: 5.97e-03 mJy/beam
#Peak SNR: 219.29

LB_p1 = prefix + '_LB.p1'
os.system('rm -rf ' + LB_p1)
gaincal(
	vis = cont_LB_p0,
    caltable = LB_p1,
    gaintype = 'G',
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
    spwmap = [0,1,2,3,4,5,6,7,8,9,10,11],
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
    threshold = '0.018mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0052arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_p1 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
             
#CI_Tau_LB_initcont_p1.image.tt0
#Beam 0.151 arcsec x 0.071 arcsec (25.47 deg)
#Flux inside disk mask: 17.05 mJy
#Peak intensity of source: 1.31 mJy/beam
#rms: 5.97e-03 mJy/beam
#Peak SNR: 219.02

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
    threshold = '0.018mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0052arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_p2 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
            
#CI_Tau_LB_initcont_p2.image.tt0
#Beam 0.151 arcsec x 0.071 arcsec (25.47 deg)
#Flux inside disk mask: 17.11 mJy
#Peak intensity of source: 1.32 mJy/beam
#rms: 5.98e-03 mJy/beam
#Peak SNR: 220.85

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
    threshold = '0.018mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0052arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_p3 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_initcont_p3.image.tt0
#Beam 0.151 arcsec x 0.071 arcsec (25.47 deg)
#Flux inside disk mask: 16.99 mJy
#Peak intensity of source: 1.32 mJy/beam
#rms: 5.98e-03 mJy/beam
#Peak SNR: 219.90

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
    threshold = '0.018mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0052arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_p4 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_initcont_p4.image.tt0
#Beam 0.151 arcsec x 0.071 arcsec (25.47 deg)
#Flux inside disk mask: 17.02 mJy
#Peak intensity of source: 1.33 mJy/beam
#rms: 5.96e-03 mJy/beam
#Peak SNR: 222.71
'''
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
    threshold = '0.018mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0052arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_p5 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_initcont_p5.image.tt0
#Beam 0.151 arcsec x 0.071 arcsec (25.47 deg)
#Flux inside disk mask: 16.97 mJy
#Peak intensity of source: 1.25 mJy/beam
#rms: 6.15e-03 mJy/beam
#Peak SNR: 203.01
'''
# Clean deeper before amplitude self-cal
os.system('rm -rf ' + LB_ima_p4 + '.*')
tclean_wrapper_b3(
	vis = LB_cont_p4,
    imagename = LB_ima_p4,
    mask = mask, 
    scales = LB_scales,
    threshold = '0.006mJy',    # 1 cont. sens.
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0052arcsec', # 1/10 ang. res.
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_p4 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
             
#CI_Tau_LB_initcont_p4.image.tt0
#Beam 0.151 arcsec x 0.071 arcsec (25.47 deg)
#Flux inside disk mask: 16.52 mJy
#Peak intensity of source: 1.36 mJy/beam
#rms: 5.90e-03 mJy/beam
#Peak SNR: 229.55

LB_ap0 = prefix + '_LB.ap0'
os.system('rm -rf ' + LB_ap0 + '*')
gaincal(
	vis = LB_cont_p4,
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
	vis = LB_cont_p4,
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
	vis = LB_cont_p4,
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
    threshold = '0.006mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0052arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_ap0 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
             
#CI_Tau_LB_initcont_ap0.image.tt0
#Beam 0.136 arcsec x 0.066 arcsec (22.89 deg)
#Flux inside disk mask: 16.48 mJy
#Peak intensity of source: 1.24 mJy/beam
#rms: 5.66e-03 mJy/beam
#Peak SNR: 218.75
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
    threshold = '0.006mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0052arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_ap1 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
             
#CI_Tau_LB_initcont_ap1.image.tt0
#Beam 0.135 arcsec x 0.065 arcsec (22.56 deg)
#Flux inside disk mask: 16.48 mJy
#Peak intensity of source: 1.23 mJy/beam
#rms: 5.63e-03 mJy/beam
#Peak SNR: 217.82
'''