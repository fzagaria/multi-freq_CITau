import sys
sys.path.append('/data/discsim2/fz258/casa/analysis_scripts')
import analysisUtils as au

execfile('/data/discsim2/fz258/casa/reduction_utils.py')

SB_EB0 = 'CI_Tau_SB_EB0_initcont.ms'

# cont. sens.: 0.0124 mJy/beam, ang. res.: 0.437 arcsec

# select reference antennas for SB_EB0: DA65, DA43, DV06, DV17, ...

# get_station_numbers('CI_Tau_SB_EB0_initcont.ms','DA65')
# Observation ID 0: DA65@A040

SB_refant = 'DA65@A040'

mask_pa  = 11.28 # position angle of mask in degrees from Cathie's paper
mask_maj = 2.    # semimajor axis of mask in arcsec
mask_min = 1.25  # semiminor axis of mask in arcsec
mask_ra  = '04h33m52.028250s'  
mask_dec = '22d50m29.726010s'
mask = 'ellipse[[%s, %s], [%.1farcsec, %.1farcsec], %.1fdeg]' % \
           (mask_ra, mask_dec, mask_maj, mask_min, mask_pa)
noise_annulus = "annulus[[%s, %s],['%.2farcsec', '6.arcsec']]" % \
                (mask_ra, mask_dec, 1.5*mask_maj)

SB_scales = [0, 10, 20, 30, 50]

contspws  = '0~3'

prefix    = 'CI_Tau'

SB_p0 = 'CI_Tau_SB_p0'
os.system('rm -rf ' + SB_p0 + '.*')
tclean_wrapper_b3(
	vis = SB_EB0,
    imagename = SB_p0,
    mask = mask,
    scales = SB_scales,
    threshold = '0.037mJy',    # 3 cont. sens.
    savemodel = 'modelcolumn',
    imsize = 500,
    cellsize = '0.0437arcsec', # 1/10 ang. res.
    robust = 0.5,
    interactive = False
)

estimate_SNR(
	SB_p0 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_SB_p0.image.tt0
#Beam 0.546 arcsec x 0.354 arcsec (49.36 deg)
#Flux inside disk mask: 16.04 mJy
#Peak intensity of source: 4.83 mJy/beam
#rms: 1.47e-02 mJy/beam
#Peak SNR: 327.89

SB_p1 = prefix + '_SB.p1'
os.system('rm -rf ' + SB_p1)
gaincal(
	vis = SB_EB0,
    caltable = SB_p1,
    gaintype = 'G',
    combine = 'scan',
    spw = contspws,
    refant = SB_refant,
    calmode = 'p',
    solint = 'inf',
    minsnr = 4.0,
    minblperant = 4
)

plotms('CI_Tau_SB.p1',xaxis='time',yaxis='phase',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_SB.p1.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

# Check solution by antenna:
# plotms('CI_Tau_SB.p1',xaxis='time',yaxis='phase',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

applycal(
	vis = SB_EB0,
    spw = contspws,
    spwmap = [0,1,2,3],
    gaintable = [SB_p1],
    calwt = True,
    interp = 'linear',
	applymode = 'calonly'
)
         
SB_cont_p1 = prefix + '_SB_contp1.ms'
os.system('rm -rf ' + SB_cont_p1)
os.system('rm -rf ' + SB_cont_p1 + '.flagversions')
split(
	vis = SB_EB0,
    outputvis = SB_cont_p1,
    datacolumn = 'corrected'
)

SB_ima_p1 = prefix + '_SB_initcont_p1'
os.system('rm -rf ' + SB_ima_p1 + '.*')
tclean_wrapper_b3(
	vis = SB_cont_p1,
    imagename = SB_ima_p1,
    mask = mask,
    scales = SB_scales,
    threshold = '0.037mJy',
    savemodel = 'modelcolumn',
    imsize = 500,
    cellsize = '0.0437arcsec',
    robust = 0.5,
    interactive = False
)
                  
estimate_SNR(
	SB_ima_p1 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)
             
#CI_Tau_SB_initcont_p1.image.tt0
#Beam 0.546 arcsec x 0.354 arcsec (49.36 deg)
#Flux inside disk mask: 16.05 mJy
#Peak intensity of source: 4.83 mJy/beam
#rms: 1.44e-02 mJy/beam
#Peak SNR: 335.56

SB_p2 = prefix + '_SB.p2'
os.system('rm -rf ' + SB_p2)
gaincal(
	vis = SB_cont_p1,
    caltable = SB_p2,
    gaintype = 'T',
    combine = 'scan,spw',
    spw = contspws,
    refant = SB_refant,
    calmode = 'p',
    solint = '240s',
    minsnr = 4.0,
    minblperant = 4
)

plotms('CI_Tau_SB.p2',xaxis='time',yaxis='phase',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_SB.p2.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

# Check solution by antenna:
# plotms('CI_Tau_SB.p2',xaxis='time',yaxis='phase',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

applycal(
	vis = SB_cont_p1,
    spw = contspws,
    spwmap = [0,0,0,0],
    gaintable = [SB_p2],
    calwt = True,
    interp = 'linearPD',
	applymode = 'calonly'
)

SB_cont_p2 = prefix + '_SB_contp2.ms'
os.system('rm -rf ' + SB_cont_p2)
os.system('rm -rf ' + SB_cont_p2 + '.flagversions')
split(
	vis = SB_cont_p1,
    outputvis = SB_cont_p2,
    datacolumn = 'corrected'
)

SB_ima_p2 = prefix + '_SB_initcont_p2'
os.system('rm -rf ' + SB_ima_p2 + '.*')
tclean_wrapper_b3(
	vis = SB_cont_p2,
    imagename = SB_ima_p2,
    mask = mask,
    scales = SB_scales,
    threshold = '0.037mJy',
    savemodel = 'modelcolumn',
    imsize = 500,
    cellsize = '0.0437arcsec',
    robust = 0.5,
    interactive = False
)

estimate_SNR(
	SB_ima_p2 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_SB_initcont_p2.image.tt0
#Beam 0.546 arcsec x 0.354 arcsec (49.36 deg)
#Flux inside disk mask: 16.05 mJy
#Peak intensity of source: 5.02 mJy/beam
#rms: 1.22e-02 mJy/beam
#Peak SNR: 410.46

SB_p3 = prefix + '_SB.p3'
os.system('rm -rf ' + SB_p3)
gaincal(
	vis = SB_cont_p2,
    caltable = SB_p3,
    gaintype = 'T',
    combine = 'scan,spw',
    spw = contspws,
    refant = SB_refant,
    calmode = 'p',
    solint = '120s',
    minsnr = 4.0,
    minblperant = 4
)

plotms('CI_Tau_SB.p3',xaxis='time',yaxis='phase',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_SB.p3.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

# Check solution by antenna:
# plotms('CI_Tau_SB.p3',xaxis='time',yaxis='phase',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

applycal(
	vis = SB_cont_p2,
    spw = contspws,
    spwmap = [0,0,0,0],
    gaintable = [SB_p3],
    calwt = True,
    interp = 'linearPD',
    applymode = 'calonly'
)

SB_cont_p3 = prefix + '_SB_contp3.ms'
os.system('rm -rf ' + SB_cont_p3)
os.system('rm -rf ' + SB_cont_p3 + '.flagversions')
split(
	vis = SB_cont_p2,
    outputvis = SB_cont_p3,
    datacolumn = 'corrected'
)

SB_ima_p3 = prefix + '_SB_initcont_p3'
os.system('rm -rf ' + SB_ima_p3 + '.*')
tclean_wrapper_b3(
	vis = SB_cont_p3,
    imagename = SB_ima_p3,
    mask = mask,
    scales = SB_scales,
    threshold = '0.037mJy',
    savemodel = 'modelcolumn',
    imsize = 500,
    cellsize = '0.0437arcsec',
    robust = 0.5,
    interactive = False
)

estimate_SNR(
	SB_ima_p3 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_SB_initcont_p3.image.tt0
#Beam 0.546 arcsec x 0.354 arcsec (49.36 deg)
#Flux inside disk mask: 16.06 mJy
#Peak intensity of source: 5.04 mJy/beam
#rms: 1.22e-02 mJy/beam
#Peak SNR: 412.58

SB_p4 = prefix + '_SB.p4'
os.system('rm -rf ' + SB_p4)
gaincal(
	vis = SB_cont_p3,
    caltable = SB_p4,
    gaintype = 'T',
    combine = 'scan,spw',
    spw = contspws,
    refant = SB_refant,
    calmode = 'p',
    solint = '60s',
    minsnr = 4.0,
    minblperant = 4
)

plotms('CI_Tau_SB.p4',xaxis='time',yaxis='phase',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_SB.p4.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

# Check solution by antenna:
# plotms('CI_Tau_SB.p4',xaxis='time',yaxis='phase',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

applycal(
	vis = SB_cont_p3,
    spw = contspws,
    spwmap = [0,0,0,0],
    gaintable = [SB_p4],
    calwt = True,
    interp = 'linearPD',
    applymode = 'calonly'
)

SB_cont_p4 = prefix + '_SB_contp4.ms'
os.system('rm -rf ' + SB_cont_p4)
os.system('rm -rf ' + SB_cont_p4 + '.flagversions')
split(
	vis = SB_cont_p3,
    outputvis = SB_cont_p4,
    datacolumn = 'corrected'
)

SB_ima_p4 = prefix + '_SB_initcont_p4'
os.system('rm -rf ' + SB_ima_p4 + '.*')
tclean_wrapper_b3(
	vis=SB_cont_p4,
    imagename = SB_ima_p4,
    mask = mask,
    scales = SB_scales,
    threshold = '0.037mJy',
    savemodel = 'modelcolumn',
    imsize = 500,
    cellsize = '0.0437arcsec',
    robust = 0.5,
    interactive = False
)

estimate_SNR(
	SB_ima_p4 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_SB_initcont_p4.image.tt0
#Beam 0.546 arcsec x 0.354 arcsec (49.36 deg)
#Flux inside disk mask: 16.06 mJy
#Peak intensity of source: 5.05 mJy/beam
#rms: 1.22e-02 mJy/beam
#Peak SNR: 414.74

SB_p5 = prefix + '_SB.p5'
os.system('rm -rf ' + SB_p5)
gaincal(
	vis = SB_cont_p4,
    caltable = SB_p5,
    gaintype = 'T',
    combine = 'scan,spw',
    spw = contspws,
    refant = SB_refant,
    calmode = 'p',
    solint = '30s',
    minsnr = 4.0,
    minblperant = 4
)

plotms('CI_Tau_SB.p5',xaxis='time',yaxis='phase',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_SB.p5.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

# Check solution by antenna:
# plotms('CI_Tau_SB.p5',xaxis='time',yaxis='phase',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

applycal(
	vis = SB_cont_p4,
    spw = contspws,
    spwmap = [0,0,0,0],
    gaintable = [SB_p5],
    calwt = True,
    interp = 'linearPD',
    applymode = 'calonly'
)

SB_cont_p5 = prefix + '_SB_contp5.ms'
os.system('rm -rf ' + SB_cont_p5)
os.system('rm -rf ' + SB_cont_p5 + '.flagversions')
split(
	vis = SB_cont_p4,
    outputvis = SB_cont_p5,
    datacolumn = 'corrected'
)

SB_ima_p5 = prefix + '_SB_initcont_p5'
os.system('rm -rf ' + SB_ima_p5 + '.*')
tclean_wrapper_b3(
	vis = SB_cont_p5,
    imagename = SB_ima_p5,
    mask = mask,
    scales = SB_scales,
    threshold = '0.037mJy',
    savemodel = 'modelcolumn',
    imsize = 500,
    cellsize = '0.0437arcsec',
    robust = 0.5,
    interactive = False
)

estimate_SNR(
	SB_ima_p5 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_SB_initcont_p5.image.tt0
#Beam 0.546 arcsec x 0.354 arcsec (49.36 deg)
#Flux inside disk mask: 16.06 mJy
#Peak intensity of source: 5.06 mJy/beam
#rms: 1.21e-02 mJy/beam
#Peak SNR: 417.08

SB_p6 = prefix + '_SB.p6'
os.system('rm -rf ' + SB_p6)
gaincal(
	vis = SB_cont_p5,
    caltable = SB_p6,
    gaintype = 'T',
    combine = 'scan,spw',
    spw = contspws,
    refant = SB_refant,
    calmode = 'p',
    solint = '15s',
    minsnr = 4.0,
    minblperant = 4
)

plotms('CI_Tau_SB.p6',xaxis='time',yaxis='phase',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_SB.p6.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

# Check solution by antenna:
# plotms('CI_Tau_SB.p6',xaxis='time',yaxis='phase',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

applycal(
	vis = SB_cont_p5,
    spw = contspws,
    spwmap = [0,0,0,0],
    gaintable = [SB_p6],
    calwt = True,
    interp = 'linearPD',
    applymode = 'calonly'
)

SB_cont_p6 = prefix + '_SB_contp6.ms'
os.system('rm -rf ' + SB_cont_p6)
os.system('rm -rf ' + SB_cont_p6 + '.flagversions')
split(
	vis = SB_cont_p5,
    outputvis = SB_cont_p6,
    datacolumn = 'corrected'
)

SB_ima_p6 = prefix + '_SB_initcont_p6'
os.system('rm -rf ' + SB_ima_p6 + '.*')
tclean_wrapper_b3(
	vis = SB_cont_p6,
    imagename = SB_ima_p6,
    mask = mask,
    scales = SB_scales,
    threshold = '0.037mJy',
    savemodel = 'modelcolumn',
    imsize = 500,
    cellsize = '0.0437arcsec',
    robust = 0.5,
    interactive = False
)

estimate_SNR(
	SB_ima_p6 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_SB_initcont_p6.image.tt0
#Beam 0.546 arcsec x 0.354 arcsec (49.36 deg)
#Flux inside disk mask: 16.07 mJy
#Peak intensity of source: 5.07 mJy/beam
#rms: 1.21e-02 mJy/beam
#Peak SNR: 418.50

# Clean deeper before amplitude self-cal
os.system('rm -rf ' + SB_ima_p6 + '.*')
tclean_wrapper_b3(
	vis = SB_cont_p6,
    imagename = SB_ima_p6,
    mask = mask,
    scales = SB_scales,
    threshold = '0.012mJy',    # 1 cont. sens.
    savemodel = 'modelcolumn',
    imsize = 500,
    cellsize = '0.0437arcsec', # 1/10 ang. res.
    robust = 0.5,
    interactive = False
)

estimate_SNR(
	SB_ima_p6 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_SB_initcont_p6.image.tt0
#Beam 0.546 arcsec x 0.354 arcsec (49.36 deg)
#Flux inside disk mask: 16.05 mJy
#Peak intensity of source: 5.08 mJy/beam
#rms: 1.19e-02 mJy/beam
#Peak SNR: 427.25

SB_ap0 = prefix + '_SB.ap0'
os.system('rm -rf ' + SB_ap0+'*')
gaincal(
	vis = SB_cont_p6,
    caltable = SB_ap0,
    gaintype = 'T',
    combine = 'spw,scan',
    spw = contspws,
    refant = SB_refant,
    calmode = 'ap',
    solint = 'inf',
    minsnr = 4.0,
    minblperant = 4
)

plotms('CI_Tau_SB.ap0',xaxis='time',yaxis='phase',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_SB.ap0_phase.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

plotms('CI_Tau_SB.ap0',xaxis='time',yaxis='amp',iteraxis='spw',yselfscale=True,
	showgui=False,plotfile='CI_Tau_SB.ap0_amp.png',exprange='all',overwrite=True,
	customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

# Check solution by antenna:
# plotms('CI_Tau_SB.ap0',xaxis='time',yaxis='phase',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')
# plotms('CI_Tau_SB.ap0',xaxis='time',yaxis='amp',iteraxis='antenna',yselfscale=True,
#	showgui=True,overwrite=True,customsymbol=True,customflaggedsymbol=True,flaggedsymbolshape='autoscaling')

applycal(
	vis = SB_cont_p6,
    spw = contspws,
    spwmap = [0,0,0,0],
    gaintable = [SB_ap0],
    calwt = True,
    interp = 'linearPD',
	applymode = 'calonly'
)

SB_cont_ap0 = prefix + '_SB_contap0.ms'
os.system('rm -rf ' + SB_cont_ap0)
os.system('rm -rf ' + SB_cont_ap0 + '.flagversions')
split(
	vis = SB_cont_p6,
    outputvis = SB_cont_ap0,
    datacolumn = 'corrected'
)

SB_ima_ap0 = prefix + '_SB_initcont_ap0'
os.system('rm -rf ' + SB_ima_ap0 + '.*')
tclean_wrapper_b3(
	vis = SB_cont_ap0,
    imagename = SB_ima_ap0,
    mask = mask,
    scales = SB_scales,
    threshold = '0.012mJy',
    savemodel = 'modelcolumn',
    imsize = 500,
    cellsize = '0.0437arcsec',
    robust = 0.5,
    interactive = False
)

estimate_SNR(
	SB_ima_ap0 + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_SB_initcont_ap0.image.tt0
#Beam 0.544 arcsec x 0.353 arcsec (48.76 deg)
#Flux inside disk mask: 16.03 mJy
#Peak intensity of source: 5.06 mJy/beam
#rms: 1.19e-02 mJy/beam
#Peak SNR: 426.07