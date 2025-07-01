import sys
sys.path.append('/data/discsim2/fz258/casa/analysis_scripts')
import analysisUtils as au

execfile('/data/discsim2/fz258/casa/reduction_utils.py')

""" Find centers of emission using simple gaussian fitting in image plane """

mask_fit_center_pa  = 11.28  # position angle of mask in degrees
mask_fit_center_maj = 0.1    # semimajor axis of mask in arcsec
mask_fit_center_min = 0.065  # semiminor axis of mask in arcsec
mask_fit_center_ra  = '04h33m52.028s' #from imview
mask_fit_center_dec = '22d50m29.737s' #from imview
mask_fit_center = 'ellipse[[%s, %s], [%.1farcsec, %.1farcsec], %.1fdeg]' % \
           (mask_fit_center_ra, mask_fit_center_dec, mask_fit_center_maj, mask_fit_center_min, mask_fit_center_pa)

fit_gaussian('CI_Tau_SB_initcont_ap0.image.tt0', region = mask_fit_center, dooff = True)

#04h33m52.028170s +22d50m29.72218s
#Peak of Gaussian component identified with imfit: ICRS 04h33m52.028170s +22d50m29.72218s
#04:33:52.028170 +22:50:29.72218
#Separation: radian = 7.2873e-08, degrees = 0.000004 = 4.17531e-06, arcsec = 0.015031 = 0.0150311
#Peak in J2000 coordinates: 04:33:52.02878, +022:50:29.709737
#PA of Gaussian component: 13.58 deg
#Inclination of Gaussian component: 46.91 deg
#Pixel coordinates of peak: x = 250.025 y = 249.912

fit_gaussian('CI_Tau_LB_EB0_initcont_p1.image.tt0', region = mask_fit_center, dooff = True)

#04h33m52.027189s +22d50m29.76076s
#Peak of Gaussian component identified with imfit: ICRS 04h33m52.027189s +22d50m29.76076s
#04:33:52.027189 +22:50:29.76076
#Separation: radian = 7.29066e-08, degrees = 0.000004 = 4.17724e-06, arcsec = 0.015038 = 0.0150381
#Peak in J2000 coordinates: 04:33:52.02780, +022:50:29.748318
#PA of Gaussian component: 17.42 deg
#Inclination of Gaussian component: 45.44 deg
#Pixel coordinates of peak: x = 1199.367 y = 1200.061

fit_gaussian('CI_Tau_LB_EB1_initcont_p1.image.tt0', region = mask_fit_center, dooff = True)

#04h33m52.027368s +22d50m29.76229s
#Peak of Gaussian component identified with imfit: ICRS 04h33m52.027368s +22d50m29.76229s
#04:33:52.027368 +22:50:29.76229
#Separation: radian = 7.29442e-08, degrees = 0.000004 = 4.1794e-06, arcsec = 0.015046 = 0.0150458
#Peak in J2000 coordinates: 04:33:52.02798, +022:50:29.749848
#PA of Gaussian component: 27.56 deg
#Inclination of Gaussian component: 53.89 deg
#Pixel coordinates of peak: x = 1198.924 y = 1200.418

""" Re-Centering: center the disc on the phase center """

SB_EB0_ICRS_new_phase_center = 'ICRS 04h33m52.028170s +22d50m29.72218s'
LB_EB0_ICRS_new_phase_center = 'ICRS 04h33m52.027189s +22d50m29.76076s'
LB_EB1_ICRS_new_phase_center = 'ICRS 04h33m52.027368s +22d50m29.76229s'

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

new_J2000_center = 'J2000 04h33m52.02780s +22d50m29.748318s'
                                   
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
mask_ra  = '04h33m52.027800s'
mask_dec = '22d50m29.748318s'
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
    threshold = '0.012mJy',    # 1 cont. sens.
    savemodel = 'none',
    imsize = 500,
    cellsize = '0.0437arcsec', # 1/10 ang. res.
    robust = 0.5,
    interactive = False
)

estimate_SNR(
	SB_EB0_initcont_check_centered + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_SB_EB0_initcont_cent.ms.image.tt0
#Beam 0.544 arcsec x 0.353 arcsec (48.76 deg)
#Flux inside disk mask: 16.02 mJy
#Peak intensity of source: 5.06 mJy/beam
#rms: 1.15e-02 mJy/beam
#Peak SNR: 440.69

tclean_wrapper_b3(
	vis = LB_EB0_initcont_check_centered,
    imagename = LB_EB0_initcont_check_centered,
    mask = mask, 
    scales = LB_scales,
    threshold = '0.029mJy',    # 3 cont. sens.
    savemodel = 'none',
    imsize = 2400,
    cellsize = '0.0052arcsec', # 1/10 ang. res.
    robust = 1.0,
    interactive = False
)

estimate_SNR(
	LB_EB0_initcont_check_centered + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_EB0_initcont_cent.ms.image.tt0
#Beam 0.095 arcsec x 0.058 arcsec (16.71 deg)
#Flux inside disk mask: 16.51 mJy
#Peak intensity of source: 1.14 mJy/beam
#rms: 1.13e-02 mJy/beam
#Peak SNR: 101.09

tclean_wrapper_b3(
	vis = LB_EB1_initcont_check_centered,
    imagename = LB_EB1_initcont_check_centered,
    mask = mask, 
    scales = LB_scales,
    threshold = '0.029mJy',    # 3 cont. sens.
    savemodel = 'none',
    imsize = 2400,
    cellsize = '0.0052arcsec', # 1/10 ang. res.
    robust = 1.0,
    interactive = False
)

estimate_SNR(
	LB_EB1_initcont_check_centered + '.image.tt0',
    disk_mask = mask,
    noise_mask = noise_annulus
)

#CI_Tau_LB_EB1_initcont_cent.ms.image.tt0
#Beam 0.075 arcsec x 0.052 arcsec (-11.36 deg)
#Flux inside disk mask: 17.00 mJy
#Peak intensity of source: 0.90 mJy/beam
#rms: 9.10e-03 mJy/beam
#Peak SNR: 99.37

mask_fit_center_pa  = 11.28  # position angle of mask in degrees
mask_fit_center_maj = 0.1    # semimajor axis of mask in arcsec
mask_fit_center_min = 0.065  # semiminor axis of mask in arcsec
mask_fit_center_ra  = '04h33m52.027800s' #new_J2000_center
mask_fit_center_dec = '22d50m29.748318s' #new_J2000_center
mask_fit_center = 'ellipse[[%s, %s], [%.1farcsec, %.1farcsec], %.1fdeg]' % \
           (mask_fit_center_ra, mask_fit_center_dec, mask_fit_center_maj, mask_fit_center_min, mask_fit_center_pa)

fit_gaussian(SB_EB0_initcont_check_centered + '.image.tt0', region = mask_fit_center, dooff = True)

#04h33m52.027800s +22d50m29.74837s
#Peak of Gaussian component identified with imfit: J2000 04h33m52.027800s +22d50m29.74837s
#PA of Gaussian component: 10.51 deg
#Inclination of Gaussian component: 48.47 deg
#Pixel coordinates of peak: x = 250.000 y = 250.001

fit_gaussian(LB_EB0_initcont_check_centered + '.image.tt0', region = mask_fit_center, dooff = True)

#04h33m52.027791s +22d50m29.74814s
#Peak of Gaussian component identified with imfit: J2000 04h33m52.027791s +22d50m29.74814s
#PA of Gaussian component: 16.05 deg
#Inclination of Gaussian component: 45.93 deg
#Pixel coordinates of peak: x = 1200.023 y = 1199.966

fit_gaussian(LB_EB1_initcont_check_centered + '.image.tt0', region = mask_fit_center, dooff = True)

#04h33m52.027796s +22d50m29.74826s
#Peak of Gaussian component identified with imfit: J2000 04h33m52.027796s +22d50m29.74826s
#PA of Gaussian component: 26.46 deg
#Inclination of Gaussian component: 52.83 deg
#Pixel coordinates of peak: x = 1200.009 y = 1199.989

#SB_EB0 04h33m52.027800s +22d50m29.748370s
#LB_EB0 04h33m52.027791s +22d50m29.748140s
#LB_EB1 04h33m52.027796s +22d50m29.748260s
#J2000  04h33m52.027800s +22d50m29.748318s

""" Check flux calibrators """

# SB_EB0 -- uid___A002_Xed9025_X1a19.ms.split.cal
# Flux in QA2 for J0237+2848 is 1.345 Jy @90.508 GHz
#                               1.328834 +- 0.024533 Jy
# Diff is 1.2019% of QA2
au.getALMAFlux('J0237+2848', frequency = '90.508GHz',  date = '2021/07/03')
"""
  Closest Band 3 measurement: 1.220 +- 0.030 (age=-4 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 1.320 +- 0.030 (age=-4 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 0.590 +- 0.060 (age=-3 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age -3.5 days from 2021/07/03, with age separation of 1 days
  2021/07/07 -- 2021/07/08: freqs=[103.5, 91.47, 343.48], fluxes=[1.22, 1.32, 0.59], errors=[0.03, 0.03, 0.06]
Median Monte-Carlo result for 90.508000 = 1.326366 +- 0.024533 (scaled MAD = 0.024265)
Result using spectral index of -0.609814 for 90.508 GHz from 1.270 Jy at 97.485 GHz = 1.328834 +- 0.024533 Jy
"""
# Flux in QA2 for J0237+2848 is 1.327 Jy @92.500 GHz
#                               1.311309 +- 0.023164 Jy
# Diff is 1.1824% of QA2
au.getALMAFlux('J0237+2848', frequency = '92.500GHz',  date = '2021/07/03')
"""
  Closest Band 3 measurement: 1.220 +- 0.030 (age=-4 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 1.320 +- 0.030 (age=-4 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 0.590 +- 0.060 (age=-3 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age -3.5 days from 2021/07/03, with age separation of 1 days
  2021/07/07 -- 2021/07/08: freqs=[103.5, 91.47, 343.48], fluxes=[1.22, 1.32, 0.59], errors=[0.03, 0.03, 0.06]
Median Monte-Carlo result for 92.500000 = 1.309084 +- 0.023164 (scaled MAD = 0.023230)
Result using spectral index of -0.609814 for 92.500 GHz from 1.270 Jy at 97.485 GHz = 1.311309 +- 0.023164 Jy
"""
# Flux in QA2 for J0237+2848 is 1.245 Jy @102.612 GHz
#                               1.230918 +- 0.020509 Jy
# Diff is 1.1311% of QA2
au.getALMAFlux('J0237+2848', frequency = '102.612GHz', date = '2021/07/03')
"""
  Closest Band 3 measurement: 1.220 +- 0.030 (age=-4 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 1.320 +- 0.030 (age=-4 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 0.590 +- 0.060 (age=-3 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age -3.5 days from 2021/07/03, with age separation of 1 days
  2021/07/07 -- 2021/07/08: freqs=[103.5, 91.47, 343.48], fluxes=[1.22, 1.32, 0.59], errors=[0.03, 0.03, 0.06]
Median Monte-Carlo result for 102.612000 = 1.228360 +- 0.020509 (scaled MAD = 0.020535)
Result using spectral index of -0.609814 for 102.612 GHz from 1.270 Jy at 97.485 GHz = 1.230918 +- 0.020509 Jy
"""
# Flux in QA2 for J0237+2848 is 1.232 Jy @104.500 GHz
#                               1.217310 +- 0.020334 Jy
# Diff is 1.1924% of QA2
au.getALMAFlux('J0237+2848', frequency = '104.500GHz', date = '2021/07/03')
"""
  Closest Band 3 measurement: 1.220 +- 0.030 (age=-4 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 1.320 +- 0.030 (age=-4 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 0.590 +- 0.060 (age=-3 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age -3.5 days from 2021/07/03, with age separation of 1 days
  2021/07/07 -- 2021/07/08: freqs=[103.5, 91.47, 343.48], fluxes=[1.22, 1.32, 0.59], errors=[0.03, 0.03, 0.06]
Median Monte-Carlo result for 104.499730 = 1.215120 +- 0.020334 (scaled MAD = 0.020039)
Result using spectral index of -0.609814 for 104.500 GHz from 1.270 Jy at 97.485 GHz = 1.217310 +- 0.020334 Jy
"""

# LB_EB0 -- uid___A002_Xde2e20_X1745.ms.split.cal
# Flux in QA2 for J0423-0120 is 4.278 Jy @90.519 GHz
#                               4.278012 +- 0.057973 Jy
# Diff is 0.0003% of QA2
au.getALMAFlux('J0423-0120', frequency = '90.519GHZ',  date = '2019/06/27')
"""
  Closest Band 3 measurement: 3.970 +- 0.070 (age=+5 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 4.240 +- 0.080 (age=+5 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 2.030 +- 0.050 (age=+5 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +5.0 days from 2019/06/27, with age separation of 0 days
  2019/06/22: freqs=[103.49, 91.46, 343.48], fluxes=[3.97, 4.24, 2.03], errors=[0.07, 0.08, 0.05]
Median Monte-Carlo result for 90.519000 = 4.271830 +- 0.057973 (scaled MAD = 0.058228)
Result using spectral index of -0.557601 for 90.519 GHz from 4.105 Jy at 97.475 GHz = 4.278012 +- 0.057973 Jy
"""
# Flux in QA2 for J0423-0120 is 4.227 Jy @92.503 GHz
#                               4.226604 +- 0.056840 Jy
# Diff is 0.009% of QA2
au.getALMAFlux('J0423-0120', frequency = '92.503GHz',  date = '2019/06/27')
"""
  Closest Band 3 measurement: 3.970 +- 0.070 (age=+5 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 4.240 +- 0.080 (age=+5 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 2.030 +- 0.050 (age=+5 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +5.0 days from 2019/06/27, with age separation of 0 days
  2019/06/22: freqs=[103.49, 91.46, 343.48], fluxes=[3.97, 4.24, 2.03], errors=[0.07, 0.08, 0.05]
Median Monte-Carlo result for 92.503000 = 4.219576 +- 0.056840 (scaled MAD = 0.056361)
Result using spectral index of -0.557601 for 92.503 GHz from 4.105 Jy at 97.475 GHz = 4.226604 +- 0.056840 Jy
"""
# Flux in QA2 for J0423-0120 is 3.990 Jy @102.586 GHz
#                               3.989673 +- 0.049163 Jy
# Diff is 0.008% of QA2
au.getALMAFlux('J0423-0120', frequency = '102.586GHz', date = '2019/06/27')
"""
  Closest Band 3 measurement: 3.970 +- 0.070 (age=+5 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 4.240 +- 0.080 (age=+5 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 2.030 +- 0.050 (age=+5 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +5.0 days from 2019/06/27, with age separation of 0 days
  2019/06/22: freqs=[103.49, 91.46, 343.48], fluxes=[3.97, 4.24, 2.03], errors=[0.07, 0.08, 0.05]
Median Monte-Carlo result for 102.586000 = 3.983685 +- 0.049163 (scaled MAD = 0.048893)
Result using spectral index of -0.557601 for 102.586 GHz from 4.105 Jy at 97.475 GHz = 3.989673 +- 0.049163 Jy
"""
# Flux in QA2 for J0423-0120 is 3.949 Jy @104.503 GHz
#                               3.948697 +- 0.047778 Jy
# Diff is 0.008% of QA2
au.getALMAFlux('J0423-0120', frequency = '104.503GHz', date = '2019/06/27')
"""
  Closest Band 3 measurement: 3.970 +- 0.070 (age=+5 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 4.240 +- 0.080 (age=+5 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 2.030 +- 0.050 (age=+5 days) 343.5 GHz 
number of measurements used in low/high bands = 2 / 1
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +5.0 days from 2019/06/27, with age separation of 0 days
  2019/06/22: freqs=[103.49, 91.46, 343.48], fluxes=[3.97, 4.24, 2.03], errors=[0.07, 0.08, 0.05]
Median Monte-Carlo result for 104.503000 = 3.941352 +- 0.047778 (scaled MAD = 0.047679)
Result using spectral index of -0.557601 for 104.503 GHz from 4.105 Jy at 97.475 GHz = 3.948697 +- 0.047778 Jy
"""

# LB_EB1 -- uid___A002_Xde63ab_X1d88.ms.split.cal
# Flux in QA2 for J0510+1800 is 2.855 Jy @90.520 GHz
#                               2.855406 +- 0.028651 Jy
# Diff is 0.014% of QA2
au.getALMAFlux('J0510+1800', frequency = '90.520GHz',  date = '2019/07/04')
"""
  Closest Band 3 measurement: 2.640 +- 0.040 (age=+0 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.840 +- 0.060 (age=+0 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.820 +- 0.060 (age=+0 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.630 +- 0.050 (age=+0 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.290 +- 0.040 (age=+0 days) 343.5 GHz 
  Closest Band 7 measurement: 1.340 +- 0.040 (age=+0 days) 343.5 GHz 
number of measurements used in low/high bands = 4 / 2
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +0.0 days from 2019/07/04, with age separation of 0 days
  2019/07/04: freqs=[103.49, 91.46, 91.46, 103.49, 343.48], fluxes=[2.64, 2.84, 2.82, 2.63, 1.29], errors=[0.04, 0.06, 0.06, 0.05, 0.04]
Median Monte-Carlo result for 90.520000 = 2.851550 +- 0.028651 (scaled MAD = 0.029195)
Result using spectral index of -0.594355 for 90.520 GHz from 2.732 Jy at 97.475 GHz = 2.855406 +- 0.028651 Jy
"""
# Flux in QA2 for J0510+1800 is 2.819 Jy @92.504 GHz
#                               2.818847 +- 0.027662 Jy
# Diff is 0.005% of QA2
au.getALMAFlux('J0510+1800', frequency = '92.504GHz',  date = '2019/07/04')
"""
  Closest Band 3 measurement: 2.640 +- 0.040 (age=+0 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.840 +- 0.060 (age=+0 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.820 +- 0.060 (age=+0 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.630 +- 0.050 (age=+0 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.290 +- 0.040 (age=+0 days) 343.5 GHz 
  Closest Band 7 measurement: 1.340 +- 0.040 (age=+0 days) 343.5 GHz 
number of measurements used in low/high bands = 4 / 2
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +0.0 days from 2019/07/04, with age separation of 0 days
  2019/07/04: freqs=[103.49, 91.46, 91.46, 103.49, 343.48], fluxes=[2.64, 2.84, 2.82, 2.63, 1.29], errors=[0.04, 0.06, 0.06, 0.05, 0.04]
Median Monte-Carlo result for 92.504000 = 2.814896 +- 0.027662 (scaled MAD = 0.027742)
Result using spectral index of -0.594355 for 92.504 GHz from 2.732 Jy at 97.475 GHz = 2.818847 +- 0.027662 Jy
"""
# Flux in QA2 for J0510+1800 is 2.651 Jy @102.587 GHz
#                               2.650733 +- 0.023821 Jy
# Diff is 0.008% of QA2
au.getALMAFlux('J0510+1800', frequency = '102.587GHz', date = '2019/07/04')
"""
  Closest Band 3 measurement: 2.640 +- 0.040 (age=+0 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.840 +- 0.060 (age=+0 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.820 +- 0.060 (age=+0 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.630 +- 0.050 (age=+0 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.290 +- 0.040 (age=+0 days) 343.5 GHz 
  Closest Band 7 measurement: 1.340 +- 0.040 (age=+0 days) 343.5 GHz 
number of measurements used in low/high bands = 4 / 2
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +0.0 days from 2019/07/04, with age separation of 0 days
  2019/07/04: freqs=[103.49, 91.46, 91.46, 103.49, 343.48], fluxes=[2.64, 2.84, 2.82, 2.63, 1.29], errors=[0.04, 0.06, 0.06, 0.05, 0.04]
Median Monte-Carlo result for 102.587000 = 2.646803 +- 0.023821 (scaled MAD = 0.023722)
Result using spectral index of -0.594355 for 102.587 GHz from 2.732 Jy at 97.475 GHz = 2.650733 +- 0.023821 Jy
"""
# Flux in QA2 for J0510+1800 is 2.622 Jy @104.504 GHz
#                               2.621725 +- 0.023274 Jy
# Diff is 0.01% of QA2
au.getALMAFlux('J0510+1800', frequency = '104.504GHz', date = '2019/07/04')
"""
  Closest Band 3 measurement: 2.640 +- 0.040 (age=+0 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.840 +- 0.060 (age=+0 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.820 +- 0.060 (age=+0 days) 91.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 3 measurement: 2.630 +- 0.050 (age=+0 days) 103.5 GHz (will extrapolate from this datum using spectral index)
  Closest Band 7 measurement: 1.290 +- 0.040 (age=+0 days) 343.5 GHz 
  Closest Band 7 measurement: 1.340 +- 0.040 (age=+0 days) 343.5 GHz 
number of measurements used in low/high bands = 4 / 2
getALMAFluxCSV(Cycle6): Fitting for spectral index with 1 measurement pair of age +0.0 days from 2019/07/04, with age separation of 0 days
  2019/07/04: freqs=[103.49, 91.46, 91.46, 103.49, 343.48], fluxes=[2.64, 2.84, 2.82, 2.63, 1.29], errors=[0.04, 0.06, 0.06, 0.05, 0.04]
Median Monte-Carlo result for 104.504000 = 2.618015 +- 0.023274 (scaled MAD = 0.023299)
Result using spectral index of -0.594355 for 104.504 GHz from 2.732 Jy at 97.475 GHz = 2.621725 +- 0.023274 Jy
"""

""" Flux scales and concatenation """

PA   = 11.28 #from Cathie's paper
incl = 49.24 #from Cathie's paper

for msfile in [
	SB_EB0_initcont_check_centered,	
	LB_EB0_initcont_check_centered, 
	LB_EB1_initcont_check_centered]:

    export_MS(msfile)

#2022-10-20 01:54:55	WARN	MSTransformManager::checkCorrelatorPreaveragingThe data has already been preaveraged by the correlator but further smoothing or averaging has been requested. Preaveraged SPWs are: 0 1 2 3
#Measurement set exported to CI_Tau_SB_EB0_initcont_cent.vis.npz

#Measurement set exported to CI_Tau_LB_EB0_initcont_cent.vis.npz

#Measurement set exported to CI_Tau_LB_EB1_initcont_cent.vis.npz

estimate_flux_scale(
	reference  = 'CI_Tau_LB_EB1_initcont_cent.vis.npz', #because this was observed the same day of the tabulated calibrators and so flux is known most certainly
    comparison = 'CI_Tau_SB_EB0_initcont_cent.vis.npz',
    incl = incl,
    PA = PA
)

#The ratio of the fluxes of CI_Tau_SB_EB0_initcont_cent.vis.npz to CI_Tau_LB_EB1_initcont_cent.vis.npz is 0.97190
#The scaling factor for gencal is 0.986 for your comparison measurement
#The error on the weighted mean ratio is 3.363e-03, although it's likely that the weights in the measurement sets are off by some constant factor

estimate_flux_scale(
	reference  = 'CI_Tau_LB_EB1_initcont_cent.vis.npz', 
    comparison = 'CI_Tau_LB_EB0_initcont_cent.vis.npz',
    incl = incl,
    PA = PA
)

#The ratio of the fluxes of CI_Tau_LB_EB0_initcont_cent.vis.npz to CI_Tau_LB_EB1_initcont_cent.vis.npz is 1.02945
#The scaling factor for gencal is 1.015 for your comparison measurement
#The error on the weighted mean ratio is 4.912e-03, although it's likely that the weights in the measurement sets are off by some constant factor

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

rescale_flux(SB_EB0_initcont_check_centered, [0.986])

rescale_flux(LB_EB0_initcont_check_centered, [1.015])

#2022-10-20 02:05:13	WARN	MSTransformManager::checkCorrelatorPreaveragingThe data has already been preaveraged by the correlator but further smoothing or averaging has been requested. Preaveraged SPWs are: 0 1 2 3
#Splitting out rescaled values into new MS: CI_Tau_SB_EB0_initcont_cent_rescaled.ms

#Splitting out rescaled values into new MS: CI_Tau LB_EB0_initcont_cent_rescaled.ms

export_MS('CI_Tau_SB_EB0_initcont_cent_rescaled.ms')

export_MS('CI_Tau_LB_EB0_initcont_cent_rescaled.ms')

#Measurement set exported to CI_Tau_SB_EB0_initcont_cent_rescaled.vis.npz

#Measurement set exported to CI_Tau_LB_EB0_initcont_cent_rescaled.vis.npz

estimate_flux_scale(
	reference  = 'CI_Tau_LB_EB1_initcont_cent.vis.npz', 
    comparison = 'CI_Tau_SB_EB0_initcont_cent_rescaled.vis.npz',
    incl = incl,
    PA = PA
)

#The ratio of the fluxes of CI_Tau_SB_EB0_initcont_cent_rescaled.vis.npz to CI_Tau_LB_EB1_initcont_cent.vis.npz is 0.99970
#The scaling factor for gencal is 1.000 for your comparison measurement
#The error on the weighted mean ratio is 3.459e-03, although it's likely that the weights in the measurement sets are off by some constant factor

estimate_flux_scale(
	reference  = 'CI_Tau_LB_EB1_initcont_cent.vis.npz', 
    comparison = 'CI_Tau_LB_EB0_initcont_cent_rescaled.vis.npz',
    incl = incl,
    PA = PA
)                    

#The ratio of the fluxes of CI_Tau_LB_EB0_initcont_cent_rescaled.vis.npz to CI_Tau_LB_EB1_initcont_cent.vis.npz is 0.99925
#The scaling factor for gencal is 1.000 for your comparison measurement
#The error on the weighted mean ratio is 4.768e-03, although it's likely that the weights in the measurement sets are off by some constant factor

plot_deprojected([
		'CI_Tau_SB_EB0_initcont_cent_rescaled.vis.npz',
	    'CI_Tau_LB_EB0_initcont_cent_rescaled.vis.npz',
	    'CI_Tau_LB_EB1_initcont_cent.vis.npz'
	],
    fluxscale = [1.0,1.0,1.0],
    PA = PA,
    incl = incl,
    show_err = True
)

listobs(
	vis = 'CI_Tau_SB_EB0_initcont_cent_rescaled.ms',
    listfile = 'CI_Tau_SB_EB0_initcont_cent_rescaled.ms.listobs.txt',
    overwrite = True
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
concat(vis = ['CI_Tau_SB_EB0_initcont_cent_rescaled.ms',
              'CI_Tau_LB_EB0_initcont_cent_rescaled.ms',
              'CI_Tau_LB_EB1_initcont_cent.ms'],
       concatvis = cont_LB_p0,
       dirtol = '0.1arcsec',
       copypointing = False
)

listobs(
	vis = cont_LB_p0,
    listfile = cont_LB_p0 + '.listobs.txt',
    overwrite = True
)
