import sys
sys.path.append('/data/discsim2/fz258/casa/analysis_scripts')
import analysisUtils as au

execfile('/data/discsim2/fz258/casa/reduction_utils.py')

""" Find centers of emission using simple gaussian fitting in image plane """

mask_fit_center_pa  = 11.28  # position angle of mask in degrees
mask_fit_center_maj = 0.1    # semimajor axis of mask in arcsec
mask_fit_center_min = 0.065  # semiminor axis of mask in arcsec
mask_fit_center_ra  = '04h33m52.027s' #from imview
mask_fit_center_dec = '22d50m29.852s' #from imview
mask_fit_center = 'ellipse[[%s, %s], [%.1farcsec, %.1farcsec], %.1fdeg]' % \
           (mask_fit_center_ra, mask_fit_center_dec, mask_fit_center_maj, mask_fit_center_min, mask_fit_center_pa)

fit_gaussian('CI_Tau_SB_initcont_ap0.image.tt0', region = mask_fit_center, dooff = True)

#04h33m52.028080s +22d50m29.85607s
#Peak of Gaussian component identified with imfit: ICRS 04h33m52.028080s +22d50m29.85607s
#04:33:52.028080 +22:50:29.85607
#Separation: radian = 7.2873e-08, degrees = 0.000004 = 4.17531e-06, arcsec = 0.015031 = 0.0150311
#Peak in J2000 coordinates: 04:33:52.02869, +022:50:29.843627
#PA of Gaussian component: 15.13 deg
#Inclination of Gaussian component: 47.06 deg
#Pixel coordinates of peak: x = 242.088 y = 241.710

mask_fit_center_pa  = 11.28  # position angle of mask in degrees
mask_fit_center_maj = 0.1    # semimajor axis of mask in arcsec
mask_fit_center_min = 0.065  # semiminor axis of mask in arcsec
mask_fit_center_ra  = '04h33m52.026s' #from imview
mask_fit_center_dec = '22d50m29.795s' #from imview
mask_fit_center = 'ellipse[[%s, %s], [%.1farcsec, %.1farcsec], %.1fdeg]' % \
           (mask_fit_center_ra, mask_fit_center_dec, mask_fit_center_maj, mask_fit_center_min, mask_fit_center_pa)

fit_gaussian('CI_Tau_LB_EB0_initcont_p1.image.tt0', region = mask_fit_center, dooff = True)

#04h33m52.026283s +22d50m29.79260s
#Peak of Gaussian component identified with imfit: ICRS 04h33m52.026283s +22d50m29.79260s
#04:33:52.026283 +22:50:29.79260
#Separation: radian = 7.27563e-08, degrees = 0.000004 = 4.16863e-06, arcsec = 0.015007 = 0.0150071
#Peak in J2000 coordinates: 04:33:52.02689, +022:50:29.780158
#PA of Gaussian component: 22.62 deg
#Inclination of Gaussian component: 38.16 deg
#Pixel coordinates of peak: x = 1105.402 y = 1173.556

fit_gaussian('CI_Tau_LB_EB1_initcont_p1.image.tt0', region = mask_fit_center, dooff = True)

#04h33m52.026289s +22d50m29.79248s
#Peak of Gaussian component identified with imfit: ICRS 04h33m52.026289s +22d50m29.79248s
#04:33:52.026289 +22:50:29.79248
#Separation: radian = 7.29106e-08, degrees = 0.000004 = 4.17747e-06, arcsec = 0.015039 = 0.0150389
#Peak in J2000 coordinates: 04:33:52.02690, +022:50:29.780037
#PA of Gaussian component: 1.72 deg
#Inclination of Gaussian component: 38.40 deg
#Pixel coordinates of peak: x = 1105.375 y = 1173.534

""" Re-Centering: center the disc on the phase center """

SB_EB0_ICRS_new_phase_center = 'ICRS 04h33m52.028080s +22d50m29.85607s'
LB_EB0_ICRS_new_phase_center = 'ICRS 04h33m52.026283s +22d50m29.79260s'
LB_EB1_ICRS_new_phase_center = 'ICRS 04h33m52.026289s +22d50m29.79248s'

SB_EB0_initcont_check_centered = 'CI_Tau_SB_EB0_initcont_cent.ms'
LB_EB0_initcont_check_centered = 'CI_Tau_LB_EB0_initcont_cent.ms'
LB_EB1_initcont_check_centered = 'CI_Tau_LB_EB1_initcont_cent.ms'

os.system('rm -rf ' + SB_EB0_initcont_check_centered)
os.system('rm -rf ' + SB_EB0_initcont_check_centered + '.flagversions')
phaseshift(
    vis = 'CI_Tau_SB_contap0.ms',
    outputvis = SB_EB0_initcont_check_centered,
    field = 'CI_Tau',
    phasecenter = SB_EB0_ICRS_new_phase_center
)

os.system('rm -rf ' + LB_EB0_initcont_check_centered)
os.system('rm -rf ' + LB_EB0_initcont_check_centered + '.flagversions')
phaseshift(
    vis = 'CI_Tau_LB_EB0_contp1.ms',
    outputvis = LB_EB0_initcont_check_centered,
    field = 'ci_tau',
    phasecenter = LB_EB0_ICRS_new_phase_center
)

os.system('rm -rf ' + LB_EB1_initcont_check_centered)
os.system('rm -rf ' + LB_EB1_initcont_check_centered + '.flagversions')
phaseshift(
    vis = 'CI_Tau_LB_EB1_contp1.ms',
    outputvis = LB_EB1_initcont_check_centered,
    field = 'ci_tau',
    phasecenter = LB_EB1_ICRS_new_phase_center
)

""" Re-Centering: update the phase center to match across .ms """

new_J2000_center = 'J2000 04h33m52.02690s +22d50m29.780037s'

fixplanets(
    vis = SB_EB0_initcont_check_centered,
    field = 'CI_Tau',
    direction = new_J2000_center
)

listobs(
    vis = SB_EB0_initcont_check_centered,
    listfile = SB_EB0_initcont_check_centered + '.listobs.txt',
    overwrite = True,
)

fixplanets(
    vis = LB_EB0_initcont_check_centered,
    field = 'ci_tau',
    direction = new_J2000_center
)

listobs(
    vis = LB_EB0_initcont_check_centered,
    listfile = LB_EB0_initcont_check_centered + '.listobs.txt',
    overwrite = True,
)

fixplanets(
    vis = LB_EB1_initcont_check_centered,
    field = 'ci_tau',
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
mask_ra  = '04h33m52.026900s'
mask_dec = '22d50m29.780037s'
mask = 'ellipse[[%s, %s], [%.1farcsec, %.1farcsec], %.1fdeg]' % \
           (mask_ra, mask_dec, mask_maj, mask_min, mask_pa)
noise_annulus = "annulus[[%s, %s],['%.2farcsec', '4.25arcsec']]" % \
                (mask_ra, mask_dec, 1.5*mask_maj)

SB_scales = [0, 10, 20, 30, 50]

LB_scales = [0, 8, 20, 50, 100, 300]

tclean_wrapper_b3(
	vis = SB_EB0_initcont_check_centered,
    imagename = SB_EB0_initcont_check_centered,
    mask = mask, 
    scales = SB_scales,
    threshold = '0.0627mJy',   # 1 cont. sens.
    savemodel = 'none',
    imsize = 500,
    cellsize = '0.0246arcsec', # 1/10 ang. res.
    robust = 0.5,
    interactive = False
)

estimate_SNR(
	SB_EB0_initcont_check_centered + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_SB_EB0_initcont_cent.ms.image.tt0
#Beam 0.303 arcsec x 0.202 arcsec (1.17 deg)
#Flux inside disk mask: 140.46 mJy
#Peak intensity of source: 18.58 mJy/beam
#rms: 6.73e-02 mJy/beam
#Peak SNR: 275.98

tclean_wrapper_b3(
	vis = LB_EB0_initcont_check_centered,
    imagename = LB_EB0_initcont_check_centered,
    mask = mask, 
    scales = LB_scales,
    threshold = '0.048mJy',    # 3 cont. sens.
    savemodel = 'none',
    imsize = 2400,
    cellsize = '0.0035arcsec', # 1/10 ang. res.
    robust = 1.0,
    interactive = False
)

estimate_SNR(
	LB_EB0_initcont_check_centered + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_EB0_initcont_cent.ms.image.tt0
#Beam 0.060 arcsec x 0.048 arcsec (25.43 deg)
#Flux inside disk mask: 175.55 mJy
#Peak intensity of source: 3.89 mJy/beam
#rms: 1.72e-02 mJy/beam
#Peak SNR: 226.57

tclean_wrapper_b3(
	vis = LB_EB1_initcont_check_centered,
    imagename = LB_EB1_initcont_check_centered,
    mask = mask, 
    scales = LB_scales,
    threshold = '0.048mJy',    # 3 cont. sens.
    savemodel = 'none',
    imsize = 2400,
    cellsize = '0.0035arcsec', # 1/10 ang. res.
    robust = 1.0,
    interactive = False
)

estimate_SNR(
	LB_EB1_initcont_check_centered + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_EB1_initcont_cent.ms.image.tt0
#Beam 0.077 arcsec x 0.037 arcsec (36.16 deg)
#Flux inside disk mask: 155.63 mJy
#Peak intensity of source: 3.83 mJy/beam
#rms: 1.51e-02 mJy/beam
#Peak SNR: 253.61

mask_fit_center_pa  = 11.28  # position angle of mask in degrees
mask_fit_center_maj = 0.1    # semimajor axis of mask in arcsec
mask_fit_center_min = 0.065  # semiminor axis of mask in arcsec
mask_fit_center_ra  = '04h33m52.026900s' #new_J2000_center
mask_fit_center_dec = '22d50m29.780037s' #new_J2000_center
mask_fit_center = 'ellipse[[%s, %s], [%.1farcsec, %.1farcsec], %.1fdeg]' % \
           (mask_fit_center_ra, mask_fit_center_dec, mask_fit_center_maj, mask_fit_center_min, mask_fit_center_pa)

fit_gaussian(SB_EB0_initcont_check_centered + '.image.tt0', region = mask_fit_center, dooff = True)

#04h33m52.026895s +22d50m29.77969s
#Peak of Gaussian component identified with imfit: J2000 04h33m52.026895s +22d50m29.77969s
#PA of Gaussian component: 15.45 deg
#Inclination of Gaussian component: 46.59 deg
#Pixel coordinates of peak: x = 250.003 y = 249.986

fit_gaussian(LB_EB0_initcont_check_centered + '.image.tt0', region = mask_fit_center, dooff = True)

#04h33m52.026898s +22d50m29.77994s
#Peak of Gaussian component identified with imfit: J2000 04h33m52.026898s +22d50m29.77994s
#PA of Gaussian component: 23.60 deg
#Inclination of Gaussian component: 37.37 deg
#Pixel coordinates of peak: x = 1200.008 y = 1199.973

fit_gaussian(LB_EB1_initcont_check_centered + '.image.tt0', region = mask_fit_center, dooff = True)

#04h33m52.026898s +22d50m29.78005s
#Peak of Gaussian component identified with imfit: J2000 04h33m52.026898s +22d50m29.78005s
#PA of Gaussian component: 2.93 deg
#Inclination of Gaussian component: 37.55 deg
#Pixel coordinates of peak: x = 1200.006 y = 1200.003

#SB_EB0 04h33m52.026895s +22d50m29.77969s
#LB_EB0 04h33m52.026898s +22d50m29.77994s
#LB_EB1 04h33m52.026898s +22d50m29.78005s
#J2000  04h33m52.026900s +22d50m29.78004s

""" Check flux calibrators """

# Check quasars used for flux-calibration. From listobs.txt select observational date.
# To check the QA2 report open weblogs at hif_setmodels or hif_setjy

# SB_EB0 -- uid___A002_Xb74a0f_X166a.ms.split.cal
# Flux in QA2 for J0510+1800 is 1.852 Jy @219.959 GHz
#                               1.940918 +- 0.046100 Jy
# Diff is 4.801% of QA2
au.getALMAFlux('J0510+1800', frequency = '219.959GHz',  date = '2016/08/27')
"""
  Closest Band 3 measurement: 2.650 +- 0.060 (age=-7 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.680 +- 0.060 (age=-7 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.740 +- 0.090 (age=-7 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.450 +- 0.060 (age=+6 days) 343.5 GHz 
number of measurements used in low/high bands = 3 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +7.0 days from 2016/08/27, with age separation of 2 days
  2016/08/19 -- 2016/08/21: freqs=[91.46, 103.49, 343.48], fluxes=[2.42, 2.38, 1.45], errors=[0.04, 0.04, 0.06]
Median Monte-Carlo result for 219.959000 = 1.742692 +- 0.046100 (scaled MAD = 0.046077)
Result using spectral index of -0.391048 for 219.959 GHz from 2.690 Jy at 95.470 GHz = 1.940918 +- 0.046100 Jy
"""
# Flux in QA2 for J0510+1800 is 1.865 Jy @216.720 GHz
#                               1.952210 +- 0.045420 Jy
# Diff is 4.676% of QA2
au.getALMAFlux('J0510+1800', frequency = '216.720GHz',  date = '2016/08/27')
"""
  Closest Band 3 measurement: 2.650 +- 0.060 (age=-7 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.680 +- 0.060 (age=-7 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.740 +- 0.090 (age=-7 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.450 +- 0.060 (age=+6 days) 343.5 GHz 
number of measurements used in low/high bands = 3 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +7.0 days from 2016/08/27, with age separation of 2 days
  2016/08/19 -- 2016/08/21: freqs=[91.46, 103.49, 343.48], fluxes=[2.42, 2.38, 1.45], errors=[0.04, 0.04, 0.06]
Median Monte-Carlo result for 216.720000 = 1.752428 +- 0.045420 (scaled MAD = 0.044704)
Result using spectral index of -0.391048 for 216.720 GHz from 2.690 Jy at 95.470 GHz = 1.952210 +- 0.045420 Jy
"""
# Flux in QA2 for J0510+1800 is 1.809 Jy @231.231 GHz
#                               1.903354 +- 0.048302 Jy
# Diff is 5.215% of QA2
au.getALMAFlux('J0510+1800', frequency = '231.231GHz', date = '2016/08/27')
"""
  Closest Band 3 measurement: 2.650 +- 0.060 (age=-7 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.680 +- 0.060 (age=-7 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.740 +- 0.090 (age=-7 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.450 +- 0.060 (age=+6 days) 343.5 GHz 
number of measurements used in low/high bands = 3 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +7.0 days from 2016/08/27, with age separation of 2 days
  2016/08/19 -- 2016/08/21: freqs=[91.46, 103.49, 343.48], fluxes=[2.42, 2.38, 1.45], errors=[0.04, 0.04, 0.06]
Median Monte-Carlo result for 231.231000 = 1.708570 +- 0.048302 (scaled MAD = 0.048552)
Result using spectral index of -0.391048 for 231.231 GHz from 2.690 Jy at 95.470 GHz = 1.903354 +- 0.048302 Jy
"""
# Flux in QA2 for J0510+1800 is 1.797 Jy @234.432 GHz
#                               1.893149 +- 0.049030 Jy
# Diff is 5.350% of QA2
au.getALMAFlux('J0510+1800', frequency = '234.432GHz', date = '2016/08/27')
"""
  Closest Band 3 measurement: 2.650 +- 0.060 (age=-7 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.680 +- 0.060 (age=-7 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.740 +- 0.090 (age=-7 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.450 +- 0.060 (age=+6 days) 343.5 GHz 
number of measurements used in low/high bands = 3 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +7.0 days from 2016/08/27, with age separation of 2 days
  2016/08/19 -- 2016/08/21: freqs=[91.46, 103.49, 343.48], fluxes=[2.42, 2.38, 1.45], errors=[0.04, 0.04, 0.06]
Median Monte-Carlo result for 234.432000 = 1.700925 +- 0.049030 (scaled MAD = 0.048463)
Result using spectral index of -0.391048 for 234.432 GHz from 2.690 Jy at 95.470 GHz = 1.893149 +- 0.049030 Jy
"""

# LB_EB0 -- uid___A002_Xc4bcba_X1f20.ms.split.cal
# Flux in QA2 for J0510+1800 is 1.683 Jy @224.000 GHz
#                               1.682651 +- 0.055693 Jy
# Diff is 0.021% of QA2
au.getALMAFlux('J0510+1800', frequency = '224.000GHZ',  date = '2017/09/23')
"""
  Closest Band 3 measurement: 2.280 +- 0.060 (age=+6 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.400 +- 0.050 (age=+6 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.120 +- 0.070 (age=-4 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +6.0 days from 2017/09/23, with age separation of 0 days
  2017/09/17: freqs=[103.49, 91.46, 343.48], fluxes=[2.28, 2.4, 1.42], errors=[0.06, 0.05, 0.07]
Median Monte-Carlo result for 224.000000 = 1.680786 +- 0.055693 (scaled MAD = 0.055674)
Result using spectral index of -0.396347 for 224.000 GHz from 2.340 Jy at 97.475 GHz = 1.682651 +- 0.055693 Jy
"""
# Flux in QA2 for J0510+1800 is 1.677 Jy @226.000 GHz
#                               1.676733 +- 0.056602 Jy
# Diff is 0.016% of QA2
au.getALMAFlux('J0510+1800', frequency = '226.000GHz',  date = '2017/09/23')
"""
  Closest Band 3 measurement: 2.280 +- 0.060 (age=+6 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.400 +- 0.050 (age=+6 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.120 +- 0.070 (age=-4 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +6.0 days from 2017/09/23, with age separation of 0 days
  2017/09/17: freqs=[103.49, 91.46, 343.48], fluxes=[2.28, 2.4, 1.42], errors=[0.06, 0.05, 0.07]
Median Monte-Carlo result for 226.000000 = 1.675169 +- 0.056602 (scaled MAD = 0.055742)
Result using spectral index of -0.396347 for 226.000 GHz from 2.340 Jy at 97.475 GHz = 1.676733 +- 0.056602 Jy
"""
# Flux in QA2 for J0510+1800 is 1.637 Jy @240.000 GHz
#                               1.637262 +- 0.058368 Jy
# Diff is 0.016% of QA2
au.getALMAFlux('J0510+1800', frequency = '240.000GHz', date = '2017/09/23')
"""
  Closest Band 3 measurement: 2.280 +- 0.060 (age=+6 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.400 +- 0.050 (age=+6 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.120 +- 0.070 (age=-4 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +6.0 days from 2017/09/23, with age separation of 0 days
  2017/09/17: freqs=[103.49, 91.46, 343.48], fluxes=[2.28, 2.4, 1.42], errors=[0.06, 0.05, 0.07]
Median Monte-Carlo result for 240.000000 = 1.635168 +- 0.058368 (scaled MAD = 0.058827)
Result using spectral index of -0.396347 for 240.000 GHz from 2.340 Jy at 97.475 GHz = 1.637262 +- 0.058368 Jy
"""
# Flux in QA2 for J0510+1800 is 1.632 Jy @242.000 GHz
#                               1.631886 +- 0.057487 Jy
# Diff is 0.007% of QA2
au.getALMAFlux('J0510+1800', frequency = '242.000GHz', date = '2017/09/23')
"""
  Closest Band 3 measurement: 2.280 +- 0.060 (age=+6 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.400 +- 0.050 (age=+6 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.120 +- 0.070 (age=-4 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +6.0 days from 2017/09/23, with age separation of 0 days
  2017/09/17: freqs=[103.49, 91.46, 343.48], fluxes=[2.28, 2.4, 1.42], errors=[0.06, 0.05, 0.07]
Median Monte-Carlo result for 242.000000 = 1.630951 +- 0.057487 (scaled MAD = 0.057796)
Result using spectral index of -0.396347 for 242.000 GHz from 2.340 Jy at 97.475 GHz = 1.631886 +- 0.057487 Jy
"""

# LB_EB1 -- uid___A002_Xc4c2da_X2903.ms.split.cal
# Flux in QA2 for J0510+1800 is 1.510 Jy @224.000 GHz
#                               1.682651 +- 0.055215 Jy
# Diff is 11.4349% of QA2
au.getALMAFlux('J0510+1800', frequency = '224.000GHz',  date = '2017/09/24')
"""
  Closest Band 3 measurement: 2.280 +- 0.060 (age=+7 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.400 +- 0.050 (age=+7 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.120 +- 0.070 (age=-3 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +7.0 days from 2017/09/24, with age separation of 0 days
  2017/09/17: freqs=[103.49, 91.46, 343.48], fluxes=[2.28, 2.4, 1.42], errors=[0.06, 0.05, 0.07]
Median Monte-Carlo result for 224.000000 = 1.680486 +- 0.055215 (scaled MAD = 0.054601)
Result using spectral index of -0.396347 for 224.000 GHz from 2.340 Jy at 97.475 GHz = 1.682651 +- 0.055215 Jy
"""
# Flux in QA2 for J0510+1800 is 1.505 Jy @226.000 GHz
#                               1.676733 +- 0.055483 Jy
# Diff is 11.411% of QA2
au.getALMAFlux('J0510+1800', frequency = '226.000GHz',  date = '2017/09/24')
"""
  Closest Band 3 measurement: 2.280 +- 0.060 (age=+7 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.400 +- 0.050 (age=+7 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.120 +- 0.070 (age=-3 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +7.0 days from 2017/09/24, with age separation of 0 days
  2017/09/17: freqs=[103.49, 91.46, 343.48], fluxes=[2.28, 2.4, 1.42], errors=[0.06, 0.05, 0.07]
Median Monte-Carlo result for 226.000000 = 1.675608 +- 0.055483 (scaled MAD = 0.055017)
Result using spectral index of -0.396347 for 226.000 GHz from 2.340 Jy at 97.475 GHz = 1.676733 +- 0.055483 Jy
"""
# Flux in QA2 for J0510+1800 is 1.469 Jy @240.000 GHz
#                               1.637262 +- 0.057128 Jy
# Diff is 11.454% of QA2
au.getALMAFlux('J0510+1800', frequency = '240.000GHz', date = '2017/09/24')
"""
  Closest Band 3 measurement: 2.280 +- 0.060 (age=+7 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.400 +- 0.050 (age=+7 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.120 +- 0.070 (age=-3 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +7.0 days from 2017/09/24, with age separation of 0 days
  2017/09/17: freqs=[103.49, 91.46, 343.48], fluxes=[2.28, 2.4, 1.42], errors=[0.06, 0.05, 0.07]
Median Monte-Carlo result for 240.000000 = 1.636473 +- 0.057128 (scaled MAD = 0.056904)
Result using spectral index of -0.396347 for 240.000 GHz from 2.340 Jy at 97.475 GHz = 1.637262 +- 0.057128 Jy
"""
# Flux in QA2 for J0510+1800 is 1.464 Jy @242.000 GHz
#                               1.631886 +- 0.058159 Jy
# Diff is 11.467% of QA2
au.getALMAFlux('J0510+1800', frequency = '242.000GHz', date = '2017/09/24')
"""
  Closest Band 3 measurement: 2.280 +- 0.060 (age=+7 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.400 +- 0.050 (age=+7 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.120 +- 0.070 (age=-3 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +7.0 days from 2017/09/24, with age separation of 0 days
  2017/09/17: freqs=[103.49, 91.46, 343.48], fluxes=[2.28, 2.4, 1.42], errors=[0.06, 0.05, 0.07]
Median Monte-Carlo result for 242.000000 = 1.629462 +- 0.058159 (scaled MAD = 0.057402)
Result using spectral index of -0.396347 for 242.000 GHz from 2.340 Jy at 97.475 GHz = 1.631886 +- 0.058159 Jy
"""

""" Flux scales and concatenation """

PA   = 11.28 #from Cathie's paper
incl = 49.24 #from Cathie's paper

for msfile in [SB_EB0_initcont_check_centered,
               LB_EB0_initcont_check_centered,
               LB_EB1_initcont_check_centered]:
    export_MS(msfile)

#Measurement set exported to CI_Tau_SB_EB0_initcont_cent.vis.npz

#Measurement set exported to CI_Tau_LB_EB0_initcont_cent.vis.npz

#Measurement set exported to CI_Tau_LB_EB1_initcont_cent.vis.npz

estimate_flux_scale(
	reference  = 'CI_Tau_SB_EB0_initcont_cent.vis.npz', #because this was observed closest to the tabulated calibrators and so flux is known most certainly
    comparison = 'CI_Tau_LB_EB0_initcont_cent.vis.npz',
    incl = incl,
    PA = PA
)

#The ratio of the fluxes of CI_Tau_LB_EB0_initcont_cent.vis.npz to CI_Tau_SB_EB0_initcont_cent.vis.npz is 1.19594
#The scaling factor for gencal is 1.094 for your comparison measurement
#The error on the weighted mean ratio is 1.962e-03, although it's likely that the weights in the measurement sets are off by some constant factor

estimate_flux_scale(
	reference  = 'CI_Tau_SB_EB0_initcont_cent.vis.npz', 
    comparison = 'CI_Tau_LB_EB1_initcont_cent.vis.npz',
    incl = incl,
    PA = PA
)

#The ratio of the fluxes of CI_Tau_LB_EB1_initcont_cent.vis.npz to CI_Tau_SB_EB0_initcont_cent.vis.npz is 1.06877
#The scaling factor for gencal is 1.034 for your comparison measurement
#The error on the weighted mean ratio is 1.551e-03, although it's likely that the weights in the measurement sets are off by some constant factor

estimate_flux_scale(
	reference  = 'CI_Tau_LB_EB1_initcont_cent.vis.npz', # Because the flux of this EB is consistent with the spectral index between SB (whose flux is in agreement with that of Long+18, measured the same day of a calibrator) and Band 7. The other EB is clearly too bright.
    comparison = 'CI_Tau_LB_EB0_initcont_cent.vis.npz',
    incl = incl,
    PA = PA
)

#The ratio of the fluxes of CI_Tau_LB_EB0_initcont_cent.vis.npz to CI_Tau_LB_EB1_initcont_cent.vis.npz is 1.11864
#The scaling factor for gencal is 1.058 for your comparison measurement
#The error on the weighted mean ratio is 1.231e-03, although it's likely that the weights in the measurement sets are off by some constant factor

plot_deprojected([
		'CI_Tau_SB_EB0_initcont_cent.vis.npz',
        'CI_Tau_LB_EB0_initcont_cent.vis.npz',
        'CI_Tau_LB_EB1_initcont_cent.vis.npz'
	],
    fluxscale = [1.0,1.0,1.0],
    PA = PA,
    incl = incl,
    show_err = True
)

#Only rescale LBs because, even though the SB flux is reliable, its reference frequency is different!
rescale_flux(LB_EB0_initcont_check_centered, [1.058])

#Splitting out rescaled values into new MS: CI_Tau_LB_EB0_initcont_cent_rescaled.ms

export_MS('CI_Tau_LB_EB0_initcont_cent_rescaled.ms')

#Measurement set exported to CI_Tau_LB_EB0_initcont_cent_rescaled.vis.npz

estimate_flux_scale(
	reference  = 'CI_Tau_LB_EB1_initcont_cent.vis.npz', 
    comparison = 'CI_Tau_LB_EB0_initcont_cent_rescaled.vis.npz',
    incl = incl,
    PA = PA
)

#The ratio of the fluxes of CI_Tau_LB_EB0_initcont_cent_rescaled.vis.npz to CI_Tau_LB_EB1_initcont_cent.vis.npz is 0.99935
#The scaling factor for gencal is 1.000 for your comparison measurement
#The error on the weighted mean ratio is 1.100e-03, although it's likely that the weights in the measurement sets are off by some constant factor

plot_deprojected([
		'CI_Tau_SB_EB0_initcont_cent.vis.npz',
        'CI_Tau_LB_EB0_initcont_cent_rescaled.vis.npz',
        'CI_Tau_LB_EB1_initcont_cent.vis.npz'
	],
    fluxscale = [1.0,1.0,1.0],
    PA = PA,
    incl = incl,
    show_err = True
)

listobs(
	vis = 'CI_Tau_LB_EB0_initcont_cent_rescaled.ms',
    listfile = 'CI_Tau_LB_EB0_initcont_cent_rescaled.ms.listobs.txt',
    overwrite = True
)

""" Concatenate EBs """

prefix = 'CI_Tau'

cont_LB_p0 = prefix + '_LB_initcont_conc.ms'

os.system('rm -rf ' + cont_LB_p0)
concat(vis = ['CI_Tau_SB_EB0_initcont_cent.ms',
              'CI_Tau_LB_EB0_initcont_cent_rescaled.ms',
              'CI_Tau_LB_EB1_initcont_cent.ms'],
       concatvis = cont_LB_p0,
       dirtol = '0.1arcsec',
       copypointing = False
)

#2022-09-22 10:07:10	WARN	MSConcat::copySysCal	/data/discsim2/fz258/scienceB6_05-09-22/CI_Tau_LB_initcont_conc.ms does not have a valid syscal table,
#2022-09-22 10:07:10	WARN	MSConcat::copySysCal+	  the MS to be appended, however, has one. Result won't have one.
#2022-09-22 10:07:10	WARN	MSConcat::concatenate (file casacore/ms/MSOper/MSConcat.cc, line 996)	Could not merge SysCal subtables 

#2022-09-22 10:11:19	WARN	MSConcat::copySysCal	/data/discsim2/fz258/scienceB6_05-09-22/CI_Tau_LB_initcont_conc.ms does not have a valid syscal table,
#2022-09-22 10:11:19	WARN	MSConcat::copySysCal+	  the MS to be appended, however, has one. Result won't have one.
#2022-09-22 10:11:19	WARN	MSConcat::concatenate (file casacore/ms/MSOper/MSConcat.cc, line 996)	Could not merge SysCal subtables

listobs(
	vis = cont_LB_p0,
    listfile = cont_LB_p0 + '.listobs.txt',
    overwrite = True
)
