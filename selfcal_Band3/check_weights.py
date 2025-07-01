import sys
sys.path.append('/data/discsim2/fz258/casa/analysis_scripts')
import analysisUtils as au

execfile('/data/discsim2/fz258/casa/reduction_utils.py')

mask_pa  = 11.28 # position angle of mask in degrees from Cathie's paper
mask_maj = 2.    # semimajor axis of mask in arcsec
mask_min = 1.25  # semiminor axis of mask in arcsec
mask_ra  = '04h33m52.027880s'
mask_dec = '22d50m29.748318s'
mask = 'ellipse[[%s, %s], [%.1farcsec, %.1farcsec], %.1fdeg]' % \
           (mask_ra, mask_dec, mask_maj, mask_min, mask_pa)
noise_annulus = "annulus[[%s, %s],['%.2farcsec', '6.arcsec']]" % \
                (mask_ra, mask_dec, 1.5*mask_maj)

LB_scales = [0, 8, 20, 50, 100, 300]

prefix = 'CI_Tau'

LB_cont_ap0 = prefix + '_LB_contap0.ms'

LB_cont_ap0_weights = prefix + '_LB_contap0_weights.ms'

split(
    vis = LB_cont_ap0,
    outputvis = LB_cont_ap0_weights,
    datacolumn = 'DATA'
)

statwt(
    vis = LB_cont_ap0_weights,
    datacolumn = 'DATA'
)

listobs(
    vis = LB_cont_ap0_weights,
    listfile = LB_cont_ap0_weights + '.listobs.txt',
    overwrite = True
)

LB_ima_ap0_weights = prefix + '_LB_initcont_ap0_weights'
os.system('rm -rf ' + LB_ima_ap0_weights + '.*')
tclean_wrapper_b3(
    vis = LB_cont_ap0_weights,
    imagename = LB_ima_ap0_weights,
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
    LB_ima_ap0_weights + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_initcont_ap0_weights.image.tt0
#Beam 0.139 arcsec x 0.067 arcsec (23.39 deg)
#Flux inside disk mask: 16.52 mJy
#Peak intensity of source: 1.25 mJy/beam
#rms: 5.66e-03 mJy/beam
#Peak SNR: 221.22

#CI_Tau_LB_initcont_ap0.image.tt0
#Beam 0.136 arcsec x 0.066 arcsec (22.89 deg)
#Flux inside disk mask: 16.48 mJy
#Peak intensity of source: 1.24 mJy/beam
#rms: 5.66e-03 mJy/beam
#Peak SNR: 218.75
