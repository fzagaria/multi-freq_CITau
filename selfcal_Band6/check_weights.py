import sys
sys.path.append('/data/discsim2/fz258/casa/analysis_scripts')
import analysisUtils as au

execfile('/data/discsim2/fz258/casa/reduction_utils.py')

mask_pa  = 11.28 # position angle of mask in degrees from Cathie's paper
mask_maj = 2.    # semimajor axis of mask in arcsec
mask_min = 1.25  # semiminor axis of mask in arcsec
mask_ra  = '04h33m52.026900s'
mask_dec = '22d50m29.780037s'
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
    threshold = '0.00978mJy',
    savemodel = 'modelcolumn',
    imsize = 2400,
    cellsize = '0.0035arcsec',
    robust = 1.0,
    interactive = False
)

estimate_SNR(
    LB_ima_ap0_weights + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_initcont_ap0_weights.image.tt0
#Beam 0.063 arcsec x 0.043 arcsec (31.44 deg)
#Flux inside disk mask: 148.50 mJy
#Peak intensity of source: 3.90 mJy/beam
#rms: 9.62e-03 mJy/beam
#Peak SNR: 405.69

#CI_Tau_LB_initcont_ap0.image.tt0
#Beam 0.061 arcsec x 0.043 arcsec (29.67 deg)
#Flux inside disk mask: 149.11 mJy
#Peak intensity of source: 3.82 mJy/beam
#rms: 9.51e-03 mJy/beam
#Peak SNR: 402.06
