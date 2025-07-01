import sys
sys.path.append('/data/discsim2/fz258/casa/analysis_scripts')
import analysisUtils as au

execfile('/data/discsim2/fz258/casa/reduction_utils.py')

""" Find centers of emission using simple gaussian fitting in image plane """

mask_fit_center_pa  = 11.28  # position angle of mask in degrees
mask_fit_center_maj = 0.1    # semimajor axis of mask in arcsec
mask_fit_center_min = 0.065  # semiminor axis of mask in arcsec
mask_fit_center_ra  = '04h33m52.026s' #from imview
mask_fit_center_dec = '22d50m29.801s' #from imview
mask_fit_center = 'ellipse[[%s, %s], [%.1farcsec, %.1farcsec], %.1fdeg]' % \
           (mask_fit_center_ra, mask_fit_center_dec, mask_fit_center_maj, mask_fit_center_min, mask_fit_center_pa)

fit_gaussian('CI_Tau_LB_EB0_initcont_p1.image.tt0', region = mask_fit_center, dooff = True)

#04h33m52.025496s +22d50m29.79382s
#Peak of Gaussian component identified with imfit: ICRS 04h33m52.025496s +22d50m29.79382s
#04:33:52.025496 +22:50:29.79382
#Separation: radian = 7.30197e-08, degrees = 0.000004 = 4.18372e-06, arcsec = 0.015061 = 0.0150614
#Peak in J2000 coordinates: 04:33:52.02611, +022:50:29.781378
#PA of Gaussian component: 123.72 deg
#Inclination of Gaussian component: 31.75 deg
#Pixel coordinates of peak: x = 1164.133 y = 1190.167

fit_gaussian('CI_Tau_LB_EB1_initcont_p1.image.tt0', region = mask_fit_center, dooff = True)

#04h33m52.026016s +22d50m29.78545s
#Peak of Gaussian component identified with imfit: ICRS 04h33m52.026016s +22d50m29.78545s
#04:33:52.026016 +22:50:29.78545
#Separation: radian = 7.30197e-08, degrees = 0.000004 = 4.18372e-06, arcsec = 0.015061 = 0.0150614
#Peak in J2000 coordinates: 04:33:52.02663, +022:50:29.773008
#PA of Gaussian component: 108.36 deg
#Inclination of Gaussian component: 39.59 deg
#Pixel coordinates of peak: x = 1163.316 y = 1189.216

""" Re-Centering: center the disc on the phase center """

LB_EB0_ICRS_new_phase_center = 'ICRS 04h33m52.025496s +22d50m29.79382s'
LB_EB1_ICRS_new_phase_center = 'ICRS 04h33m52.026016s +22d50m29.78545s'

LB_EB0_initcont_check_centered = 'CI_Tau_LB_EB0_initcont_cent.ms'
LB_EB1_initcont_check_centered = 'CI_Tau_LB_EB1_initcont_cent.ms'

os.system('rm -rf ' + LB_EB0_initcont_check_centered)
os.system('rm -rf ' + LB_EB0_initcont_check_centered + '.flagversions')
phaseshift(
    vis = 'CI_Tau_LB_EB0_contp1.ms',
    outputvis = LB_EB0_initcont_check_centered,
    field = 'CI_Tau',
    phasecenter = LB_EB0_ICRS_new_phase_center
)

os.system('rm -rf ' + LB_EB1_initcont_check_centered)
os.system('rm -rf ' + LB_EB1_initcont_check_centered + '.flagversions')
phaseshift(
    vis = 'CI_Tau_LB_EB1_contp1.ms',
    outputvis = LB_EB1_initcont_check_centered,
    field = 'CI_Tau',
    phasecenter = LB_EB1_ICRS_new_phase_center
)

""" Re-Centering: update the phase center to match across .ms """ 

new_J2000_center = 'J2000 04h33m52.02663s +22d50m29.773008s'
                       
fixplanets(
    vis = LB_EB0_initcont_check_centered,
    field = 'CI_Tau',
    direction = new_J2000_center
)

listobs(
    vis = LB_EB0_initcont_check_centered,
    listfile = LB_EB0_initcont_check_centered + '.listobs.txt',
    overwrite = True,
)

fixplanets(
    vis = LB_EB1_initcont_check_centered,
    field = 'CI_Tau',
    direction = new_J2000_center
)

listobs(
    vis = LB_EB1_initcont_check_centered,
    listfile = LB_EB1_initcont_check_centered + '.listobs.txt',
    overwrite = True,
)

""" Check centers """

mask_pa  = 11.28 # position angle of mask in degrees from Cathie's paper
mask_maj = 2.    # semimajor axis of mask in arcsec
mask_min = 1.25  # semiminor axis of mask in arcsec
mask_ra  = '04h33m52.026630s' #new_J2000_center
mask_dec = '22d50m29.773008s' #new_J2000_center
mask = 'ellipse[[%s, %s], [%.1farcsec, %.1farcsec], %.1fdeg]' % \
           (mask_ra, mask_dec, mask_maj, mask_min, mask_pa)
noise_annulus = "annulus[[%s, %s],['%.2farcsec', '4.25arcsec']]" % \
                (mask_ra, mask_dec, 1.5*mask_maj)

LB_scales = [0, 8, 20, 50, 100, 300]

tclean_wrapper_b3(
	vis = LB_EB0_initcont_check_centered,
    imagename = LB_EB0_initcont_check_centered,
    mask = mask, 
    scales = LB_scales,
    threshold = '0.155mJy',    # 3 cont. sens.
    savemodel = 'none',
    imsize = 2400,
    cellsize = '0.0088arcsec', # 1/10 ang. res.
    robust = 1.0,
    interactive = False
)

estimate_SNR(
	LB_EB0_initcont_check_centered + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_EB0_initcont_cent.ms.image.tt0
#Beam 0.162 arcsec x 0.088 arcsec (-44.07 deg)
#Flux inside disk mask: 415.89 mJy
#Peak intensity of source: 19.21 mJy/beam
#rms: 8.04e-02 mJy/beam
#Peak SNR: 238.89

tclean_wrapper_b3(
	vis = LB_EB1_initcont_check_centered,
    imagename = LB_EB1_initcont_check_centered,
    mask = mask, 
    scales = LB_scales,
    threshold = '0.155mJy',    # 3 cont. sens.
    savemodel = 'none',
    imsize = 2400,
    cellsize = '0.0088arcsec', # 1/10 ang. res.
    robust = 1.0,
    interactive = False
)

estimate_SNR(
	LB_EB1_initcont_check_centered + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_EB1_initcont_cent.ms.image.tt0
#Beam 0.127 arcsec x 0.094 arcsec (-26.61 deg)
#Flux inside disk mask: 438.17 mJy
#Peak intensity of source: 19.45 mJy/beam
#rms: 7.14e-02 mJy/beam
#Peak SNR: 272.35

mask_fit_center_pa  = 11.28  # position angle of mask in degrees
mask_fit_center_maj = 0.1    # semimajor axis of mask in arcsec
mask_fit_center_min = 0.065  # semiminor axis of mask in arcsec
mask_fit_center_ra  = '04h33m52.026630s' #new_J2000_center
mask_fit_center_dec = '22d50m29.773008s' #new_J2000_center
mask_fit_center = 'ellipse[[%s, %s], [%.1farcsec, %.1farcsec], %.1fdeg]' % \
           (mask_fit_center_ra, mask_fit_center_dec, mask_fit_center_maj, mask_fit_center_min, mask_fit_center_pa)

fit_gaussian(LB_EB0_initcont_check_centered + '.image.tt0', region = mask_fit_center, dooff = True)

#04h33m52.026630s +22d50m29.77297s
#Peak of Gaussian component identified with imfit: J2000 04h33m52.026630s +22d50m29.77297s
#PA of Gaussian component: 99.87 deg
#Inclination of Gaussian component: 31.42 deg
#Pixel coordinates of peak: x = 1200.001 y = 1199.996

fit_gaussian(LB_EB1_initcont_check_centered + '.image.tt0', region = mask_fit_center, dooff = True)

#04h33m52.026622s +22d50m29.77305s
#Peak of Gaussian component identified with imfit: J2000 04h33m52.026622s +22d50m29.77305s
#PA of Gaussian component: 100.96 deg
#Inclination of Gaussian component: 43.80 deg
#Pixel coordinates of peak: x = 1200.012 y = 1200.004

#EB0   04h33m52.026630s +22d50m29.77297s
#EB1   04h33m52.026622s +22d50m29.77305s
#J2000 04h33m52.026630s +22d50m29.77301s

""" Check flux calibrators """

# EB0 -- uid___A002_Xc7bfc7_X4b6d.ms
# Flux in QA2 for J0510+1800 is 1.356 Jy @333.173 GHz
#                               1.272174 +- 0.076398 Jy
# Diff is 6.1816% of QA2
au.getALMAFlux('J0510+1800', frequency = '333.173GHz', date = '2017/12/11')
"""
  Closest Band 3 measurement: 2.140 +- 0.050 (age=+3 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.250 +- 0.040 (age=+3 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.250 +- 0.080 (age=+2 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +2.5 days from 2017/12/11, with age separation of 1 days
  2017/12/08 -- 2017/12/09: freqs=[103.49, 91.46, 343.48], fluxes=[2.14, 2.25, 1.25], errors=[0.05, 0.04, 0.08]
Median Monte-Carlo result for 333.173000 = 1.269734 +- 0.076398 (scaled MAD = 0.075522)
Result using spectral index of -0.443796 for 333.173 GHz from 2.195 Jy at 97.475 GHz = 1.272174 +- 0.076398 Jy
"""
# Flux in QA2 for J0510+1800 is 1.360 Jy @330.727 GHz
#                               1.276342 +- 0.078323 Jy
# Diff is 6.1513% of QA2
au.getALMAFlux('J0510+1800', frequency = '330.727GHz', date = '2017/12/11')
"""
  Closest Band 3 measurement: 2.140 +- 0.050 (age=+3 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.250 +- 0.040 (age=+3 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.250 +- 0.080 (age=+2 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +2.5 days from 2017/12/11, with age separation of 1 days
  2017/12/08 -- 2017/12/09: freqs=[103.49, 91.46, 343.48], fluxes=[2.14, 2.25, 1.25], errors=[0.05, 0.04, 0.08]
Median Monte-Carlo result for 330.727000 = 1.272587 +- 0.077919 (scaled MAD = 0.077439)
Result using spectral index of -0.443796 for 330.727 GHz from 2.195 Jy at 97.475 GHz = 1.276342 +- 0.077919 Jy
"""
# Flux in QA2 for J0510+1800 is 1.340 Jy @342.976 GHz
#                               1.255907 +- 0.079484 Jy
# Diff is 6.2709% of QA2
au.getALMAFlux('J0510+1800', frequency = '342.976GHz', date = '2017/12/11')
"""
  Closest Band 3 measurement: 2.140 +- 0.050 (age=+3 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.250 +- 0.040 (age=+3 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.250 +- 0.080 (age=+2 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +2.5 days from 2017/12/11, with age separation of 1 days
  2017/12/08 -- 2017/12/09: freqs=[103.49, 91.46, 343.48], fluxes=[2.14, 2.25, 1.25], errors=[0.05, 0.04, 0.08]
Median Monte-Carlo result for 342.976000 = 1.253626 +- 0.079484 (scaled MAD = 0.078725)
Result using spectral index of -0.443796 for 342.976 GHz from 2.195 Jy at 97.475 GHz = 1.255907 +- 0.079484 Jy
"""
# Flux in QA2 for J0510+1800 is 1.336 Jy @345.694 GHz
#                               1.251515 +- 0.078582 Jy
# Diff is 6.3237% of QA2
au.getALMAFlux('J0510+1800', frequency = '345.694GHz', date = '2017/12/11')
"""
  Closest Band 3 measurement: 2.140 +- 0.050 (age=+3 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.250 +- 0.040 (age=+3 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.250 +- 0.080 (age=+2 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +2.5 days from 2017/12/11, with age separation of 1 days
  2017/12/08 -- 2017/12/09: freqs=[103.49, 91.46, 343.48], fluxes=[2.14, 2.25, 1.25], errors=[0.05, 0.04, 0.08]
Median Monte-Carlo result for 345.694000 = 1.248913 +- 0.078582 (scaled MAD = 0.077782)
Result using spectral index of -0.443796 for 345.694 GHz from 2.195 Jy at 97.475 GHz = 1.251515 +- 0.078582 Jy
"""

# EB1 -- uid___A002_Xc7bfc7_X4113.ms
# Flux in QA2 for J0510+1800 is 1.356 Jy @333.173 GHz
#                               1.272174 +- 0.077680 Jy
# Diff is 6.1816% of QA2
au.getALMAFlux('J0510+1800', frequency = '333.173GHz', date = '2017/12/11')
"""
  Closest Band 3 measurement: 2.140 +- 0.050 (age=+3 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.250 +- 0.040 (age=+3 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.250 +- 0.080 (age=+2 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +2.5 days from 2017/12/11, with age separation of 1 days
  2017/12/08 -- 2017/12/09: freqs=[103.49, 91.46, 343.48], fluxes=[2.14, 2.25, 1.25], errors=[0.05, 0.04, 0.08]
Median Monte-Carlo result for 333.173000 = 1.270016 +- 0.077680 (scaled MAD = 0.077533)
Result using spectral index of -0.443796 for 333.173 GHz from 2.195 Jy at 97.475 GHz = 1.272174 +- 0.077680 Jy
"""
# Flux in QA2 for J0510+1800 is 1.360 Jy @330.727 GHz
#                               1.276342 +- 0.078216 Jy
# Diff is 6.1513% of QA2
au.getALMAFlux('J0510+1800', frequency = '330.727GHz', date = '2017/12/11')
"""
  Closest Band 3 measurement: 2.140 +- 0.050 (age=+3 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.250 +- 0.040 (age=+3 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.250 +- 0.080 (age=+2 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +2.5 days from 2017/12/11, with age separation of 1 days
  2017/12/08 -- 2017/12/09: freqs=[103.49, 91.46, 343.48], fluxes=[2.14, 2.25, 1.25], errors=[0.05, 0.04, 0.08]
Median Monte-Carlo result for 330.727000 = 1.274930 +- 0.078216 (scaled MAD = 0.077968)
Result using spectral index of -0.443796 for 330.727 GHz from 2.195 Jy at 97.475 GHz = 1.276342 +- 0.078216 Jy
"""
# Flux in QA2 for J0510+1800 is 1.340 Jy @342.976 GHz
#                               1.255907 +- 0.079388 Jy
# Diff is 6.2709% of QA2
au.getALMAFlux('J0510+1800', frequency = '342.976GHz', date = '2017/12/11')
"""
  Closest Band 3 measurement: 2.140 +- 0.050 (age=+3 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.250 +- 0.040 (age=+3 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.250 +- 0.080 (age=+2 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +2.5 days from 2017/12/11, with age separation of 1 days
  2017/12/08 -- 2017/12/09: freqs=[103.49, 91.46, 343.48], fluxes=[2.14, 2.25, 1.25], errors=[0.05, 0.04, 0.08]
Median Monte-Carlo result for 342.976000 = 1.253691 +- 0.079388 (scaled MAD = 0.079221)
Result using spectral index of -0.443796 for 342.976 GHz from 2.195 Jy at 97.475 GHz = 1.255907 +- 0.079388 Jy
"""
# Flux in QA2 for J0510+1800 is 1.336 Jy @345.694 GHz
#                               1.251515 +- 0.077387 Jy
# Diff is 6.3237% of QA2
au.getALMAFlux('J0510+1800', frequency = '345.694GHz', date = '2017/12/11')
"""
  Closest Band 3 measurement: 2.140 +- 0.050 (age=+3 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.250 +- 0.040 (age=+3 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.250 +- 0.080 (age=+2 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +2.5 days from 2017/12/11, with age separation of 1 days
  2017/12/08 -- 2017/12/09: freqs=[103.49, 91.46, 343.48], fluxes=[2.14, 2.25, 1.25], errors=[0.05, 0.04, 0.08]
Median Monte-Carlo result for 345.694000 = 1.249209 +- 0.077387 (scaled MAD = 0.077041)
Result using spectral index of -0.443796 for 345.694 GHz from 2.195 Jy at 97.475 GHz = 1.251515 +- 0.077387 Jy
"""

""" Flux scales and concatenation """

PA   = 11.28 #from Cathie's paper
incl = 49.24 #from Cathie's paper

for msfile in [LB_EB0_initcont_check_centered, LB_EB1_initcont_check_centered]:
    export_MS(msfile)

#Measurement set exported to CI_Tau_LB_EB0_initcont_cent.vis.npz

#Measurement set exported to CI_Tau_LB_EB1_initcont_cent.vis.npz

estimate_flux_scale(
	reference  = 'CI_Tau_LB_EB0_initcont_cent.vis.npz', 
    comparison = 'CI_Tau_LB_EB1_initcont_cent.vis.npz',
    incl = incl,
    PA = PA
)

#The ratio of the fluxes of CI_Tau_LB_EB1_initcont_cent.vis.npz to CI_Tau_LB_EB0_initcont_cent.vis.npz is 1.03281
#The scaling factor for gencal is 1.016 for your comparison measurement
#The error on the weighted mean ratio is 7.513e-04, although it's likely that the weights in the measurement sets are off by some constant factor

plot_deprojected(['CI_Tau_LB_EB0_initcont_cent.vis.npz','CI_Tau_LB_EB1_initcont_cent.vis.npz'],
                 fluxscale = [1.0,1.0],
                 PA = PA,
                 incl = incl,
                 show_err = True)

rescale_flux(LB_EB1_initcont_check_centered, [1.016])

#Splitting out rescaled values into new MS: CI_Tau_LB_EB1_initcont_cent_rescaled.ms

export_MS('CI_Tau_LB_EB1_initcont_cent_rescaled.ms')

#Measurement set exported to CI_Tau_LB_EB1_initcont_cent_rescaled.vis.npz

estimate_flux_scale(
	reference  = 'CI_Tau_LB_EB0_initcont_cent.vis.npz', 
    comparison = 'CI_Tau_LB_EB1_initcont_cent_rescaled.vis.npz',
    incl = incl,
    PA = PA
)                    

#The ratio of the fluxes of CI_Tau_LB_EB1_initcont_cent_rescaled.vis.npz to CI_Tau_LB_EB0_initcont_cent.vis.npz is 1.00054
#The scaling factor for gencal is 1.000 for your comparison measurement
#The error on the weighted mean ratio is 7.278e-04, although it's likely that the weights in the measurement sets are off by some constant factor

plot_deprojected(['CI_Tau_LB_EB0_initcont_cent.vis.npz','CI_Tau_LB_EB1_initcont_cent_rescaled.vis.npz'],
                 fluxscale = [1.0,1.0],
                 PA = PA,
                 incl = incl,
                 show_err=True)

listobs(
	vis = 'CI_Tau_LB_EB1_initcont_cent_rescaled.ms',
    listfile = 'CI_Tau_LB_EB1_initcont_cent_rescaled.ms.listobs.txt',
    overwrite = True
)

""" Concatenate EBs """

prefix = 'CI_Tau'

cont_LB_p0 = prefix + '_LB_initcont_conc.ms'

os.system('rm -rf ' + cont_LB_p0)
concat(vis = ['CI_Tau_LB_EB0_initcont_cent.ms',
              'CI_Tau_LB_EB1_initcont_cent_rescaled.ms'],
       concatvis = cont_LB_p0,
       dirtol = '0.1arcsec',
       copypointing = False
)

listobs(
	vis = cont_LB_p0,
    listfile = cont_LB_p0 + '.listobs.txt',
    overwrite = True
)