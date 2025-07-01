# Stop after first amplitude calibration run

import sys
sys.path.append('/data/discsim2/fz258/casa/analysis_scripts')
import analysisUtils as au

execfile('/data/discsim2/fz258/casa/reduction_utils.py')

prefix = 'CI_Tau'

cont_LB_p0 = prefix + '_LB_initcont_conc.ms'

# cont. sens.: 0.0516 mJy/beam, ang. res.: 0.088 arcsec

# get_station_numbers('CI_Tau_LB_initcont_conc.ms','DV08')
# Observation ID 0: DV08@A042

LB_refant = 'DV08@A042'

mask_pa  = 11.28 # position angle of mask in degrees from Cathie's paper
mask_maj = 2.    # semimajor axis of mask in arcsec
mask_min = 1.25  # semiminor axis of mask in arcsec
mask_ra  = '04h33m52.026630s' #new_J2000_center
mask_dec = '22d50m29.773008s' #new_J2000_center
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
    threshold = '0.155mJy',    # 3 const. sens.
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0088arcsec', # 1/10 ang. res.
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_p0 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
             
#CI_Tau_LB_p0.image.tt0
#Beam 0.135 arcsec x 0.092 arcsec (-35.43 deg)
#Flux inside disk mask: 420.80 mJy
#Peak intensity of source: 18.84 mJy/beam
#rms: 5.79e-02 mJy/beam
#Peak SNR: 325.62

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
    threshold = '0.155mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0088arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_p1 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
             
#CI_Tau_LB_initcont_p1.image.tt0
#Beam 0.135 arcsec x 0.092 arcsec (-35.43 deg)
#Flux inside disk mask: 421.40 mJy
#Peak intensity of source: 18.85 mJy/beam
#rms: 5.48e-02 mJy/beam
#Peak SNR: 343.74

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
    threshold = '0.155mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0088arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_p2 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
             
#CI_Tau_LB_initcont_p2.image.tt0
#Beam 0.135 arcsec x 0.092 arcsec (-35.43 deg)
#Flux inside disk mask: 420.38 mJy
#Peak intensity of source: 19.03 mJy/beam
#rms: 5.63e-02 mJy/beam
#Peak SNR: 338.13

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
    threshold = '0.155mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0088arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_p3 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_initcont_p3.image.tt0
#Beam 0.135 arcsec x 0.092 arcsec (-35.43 deg)
#Flux inside disk mask: 423.24 mJy
#Peak intensity of source: 19.41 mJy/beam
#rms: 5.26e-02 mJy/beam
#Peak SNR: 368.80

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
    threshold = '0.155mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0088arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_p4 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_initcont_p4.image.tt0
#Beam 0.135 arcsec x 0.092 arcsec (-35.43 deg)
#Flux inside disk mask: 425.62 mJy
#Peak intensity of source: 19.90 mJy/beam
#rms: 5.01e-02 mJy/beam
#Peak SNR: 397.06

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
    threshold = '0.155mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0088arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_p5 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_initcont_p5.image.tt0
#Beam 0.135 arcsec x 0.092 arcsec (-35.43 deg)
#Flux inside disk mask: 428.31 mJy
#Peak intensity of source: 20.07 mJy/beam
#rms: 4.95e-02 mJy/beam
#Peak SNR: 405.51

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
    threshold = '0.155mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0088arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_p6 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_initcont_p6.image.tt0
#Beam 0.135 arcsec x 0.092 arcsec (-35.43 deg)
#Flux inside disk mask: 430.34 mJy
#Peak intensity of source: 20.19 mJy/beam
#rms: 4.93e-02 mJy/beam
#Peak SNR: 409.43

# Clean deeper before amplitude self-cal
os.system('rm -rf ' + LB_ima_p6 + '.*')
tclean_wrapper_b3(
	vis = LB_cont_p6,
    imagename = LB_ima_p6,
    mask = mask, 
    scales = LB_scales,
    threshold = '0.050mJy',    # 1 cont. sens.
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0088arcsec', # 1/10 ang. res.
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_p6 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
             
#CI_Tau_LB_initcont_p6.image.tt0
#Beam 0.135 arcsec x 0.092 arcsec (-35.43 deg)
#Flux inside disk mask: 431.77 mJy
#Peak intensity of source: 20.16 mJy/beam
#rms: 4.78e-02 mJy/beam
#Peak SNR: 421.98

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
    threshold = '0.050mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0088arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_ap0 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
             
#CI_Tau_LB_initcont_ap0.image.tt0
#Beam 0.133 arcsec x 0.092 arcsec (-34.67 deg)
#Flux inside disk mask: 429.45 mJy
#Peak intensity of source: 19.90 mJy/beam
#rms: 3.91e-02 mJy/beam
#Peak SNR: 508.44
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
    threshold = '0.050mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0088arcsec',
    robust = 1.0,
    interactive = False
)
                  
estimate_SNR(
	LB_ima_ap1 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
             
#CI_Tau_LB_initcont_ap1.image.tt0
#Beam 0.131 arcsec x 0.091 arcsec (-34.12 deg)
#Flux inside disk mask: 427.51 mJy
#Peak intensity of source: 19.50 mJy/beam
#rms: 4.32e-02 mJy/beam
#Peak SNR: 451.80
'''
