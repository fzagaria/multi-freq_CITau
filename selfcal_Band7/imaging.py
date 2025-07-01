import sys
sys.path.append('/data/discsim2/fz258/casa/analysis_scripts')
import analysisUtils as au

execfile('/data/discsim2/fz258/casa/reduction_utils.py')
execfile('/data/discsim2/fz258/casa/apply_JvMcorr.py')

prefix = 'CI_Tau'

LB_cont_ap0 = 'CI_Tau_LB_contap0.ms'

# Final cleaning with different imaging parameters

mask_pa  = 11.28 # position angle of mask in degrees from Cathie's paper
mask_maj = 1.5   # semimajor axis of mask in arcsec
mask_min = 0.9   # semiminor axis of mask in arcsec
mask_ra  = '04h33m52.026630s' #new_J2000_center
mask_dec = '22d50m29.773008s' #new_J2000_center
mask = 'ellipse[[%s, %s], [%.1farcsec, %.1farcsec], %.1fdeg]' % \
           (mask_ra, mask_dec, mask_maj, mask_min, mask_pa)
noise_annulus = "annulus[[%s, %s],['%.2farcsec', '6.arcsec']]" % \
                (mask_ra, mask_dec, 1.5*mask_maj)

# In Multi-Scale CLEAN, the selection of scale sizes to evaluate over is
# admittedly ill-defined but usually not too crucial. Too fine a range such
# as an arithmetic progression wastes compute time, and too coarse can lead
# to poor convergence. We have generally chosen a geometric progress
# terminating at or below the largest scale expected (Cornwell, 2008)
# La cosa migliore di fare e’ creare due immagini per ogni robust.
# Una in cui fai un cleaning fino a 1 sigma, stando attento a non fare una
# maschera troppo grande. Una in cui fai un cleaning fino a 3.5/4 sigma invece.
# In questo modo quindi puoi applicare la cosiddetta JvM correction,
# che devi fare per non avere una scala sbagliata nei residui
# (vedi Czekala+2021, MAPS II). Per poterla applicare, meglio fare cleaning
# fino a 4 sigma, per evitare un fenomeno chiamato “stippling” (S.F. priv.comm.)
# Scales are always point, beam 2 or 3 beam (Andrews+18), rings and outer edge.

LB_scales = {
	-1.0:[0, 8, 16, 25, 53, 138, 214],
	-0.5:[0, 8, 16, 24, 51, 133, 203],
	 0.0:[0, 8, 16, 22, 48, 119, 185],
	 0.5:[0, 8, 16, 20, 40, 101, 156],
	 1.0:[0, 8, 16, 36, 86, 130],
	 1.5:[0, 8, 16, 32, 78, 120],
}

cellsizes = {
	-1.0:0.056/8.,
	-0.5:0.059/8.,
	 0.0:0.065/8.,
	 0.5:0.077/8.,
	 1.0:0.092/8.,
	 1.5:0.100/8.,
}

rmses = {
	-1.0:1.05e-01,
	-0.5:7.30e-02,
	 0.0:5.15e-02,
	 0.5:4.15e-02,
	 1.0:3.95e-02,
	 1.5:4.10e-02,
}

for robust in [-1.0,-0.5,0.0,0.5,1.0,1.5]:

    LB_ima_ap0 = prefix + '_LB_{}robust_1.0sigma'.format(robust)

    print('CLEANing {}'.format(LB_ima_ap0))
    
    os.system('rm -rf ' + LB_ima_ap0 + '.*')
    tclean_wrapper_b3(
		vis = LB_cont_ap0,
        imagename = LB_ima_ap0,
        mask = mask,
        scales = LB_scales[robust],
        threshold = '{}mJy'.format(rmses[robust]),  # 1 rms contap0
        savemodel = 'none',
        imsize = 2400,
        cellsize = '{}arcsec'.format(cellsizes[robust]),  # 1/8 min_ax
        gain = 0.1,
        robust = robust,
        interactive = False
	)

    estimate_SNR(
		LB_ima_ap0 + '.image.tt0',
        disk_mask = mask,
        noise_mask = noise_annulus
	)

    exportfits(
		imagename = LB_ima_ap0 + '.image.tt0',
		fitsimage = LB_ima_ap0 + '.image.tt0.fits',
		overwrite = True
	)

#CI_Tau_LB_-1.0robust_1.0sigma.image.tt0
#Beam 0.086 arcsec x 0.056 arcsec (-33.20 deg)
#Flux inside disk mask: 410.16 mJy
#Peak intensity of source: 12.55 mJy/beam
#rms: 1.05e-01 mJy/beam
#Peak SNR: 119.48

#CI_Tau_LB_-0.5robust_1.0sigma.image.tt0
#Beam 0.088 arcsec x 0.059 arcsec (-33.09 deg)
#Flux inside disk mask: 413.80 mJy
#Peak intensity of source: 13.02 mJy/beam
#rms: 7.30e-02 mJy/beam
#Peak SNR: 178.27

#CI_Tau_LB_0.0robust_1.0sigma.image.tt0
#Beam 0.096 arcsec x 0.065 arcsec (-32.94 deg)
#Flux inside disk mask: 417.51 mJy
#Peak intensity of source: 14.32 mJy/beam
#rms: 5.15e-02 mJy/beam
#Peak SNR: 278.00

#CI_Tau_LB_0.5robust_1.0sigma.image.tt0
#Beam 0.111 arcsec x 0.077 arcsec (-33.69 deg)
#Flux inside disk mask: 416.02 mJy
#Peak intensity of source: 16.77 mJy/beam
#rms: 4.14e-02 mJy/beam
#Peak SNR: 404.76

#CI_Tau_LB_1.0robust_1.0sigma.image.tt0
#Beam 0.133 arcsec x 0.092 arcsec (-34.67 deg)
#Flux inside disk mask: 418.27 mJy
#Peak intensity of source: 19.94 mJy/beam
#rms: 3.95e-02 mJy/beam
#Peak SNR: 505.03

#CI_Tau_LB_1.5robust_1.0sigma.image.tt0
#Beam 0.145 arcsec x 0.100 arcsec (-34.90 deg)
#Flux inside disk mask: 418.98 mJy
#Peak intensity of source: 21.71 mJy/beam
#rms: 4.12e-02 mJy/beam
#Peak SNR: 526.90

for robust in [-1.0,-0.5,0.0,0.5,1.0,1.5]:

    LB_ima_ap0 = prefix + '_LB_{}robust_4.0sigma'.format(robust)

    print('CLEANing {}'.format(LB_ima_ap0))
    
    os.system('rm -rf ' + LB_ima_ap0 + '.*')
    tclean_wrapper_b3(
		vis = LB_cont_ap0,
        imagename = LB_ima_ap0,
        mask = mask,
        scales = LB_scales[robust],
        threshold = '{}mJy'.format(4.*rmses[robust]),  # 4 rms contap0
        savemodel = 'none',
        imsize = 2400,
        cellsize = '{}arcsec'.format(cellsizes[robust]),  # 1/8 min_ax
        gain = 0.1,
        robust = robust,
        interactive = False
	)

    estimate_SNR(
		LB_ima_ap0 + '.image.tt0',
        disk_mask = mask,
        noise_mask = noise_annulus
	)

    exportfits(
		imagename = LB_ima_ap0 + '.image.tt0',
		fitsimage = LB_ima_ap0 + '.image.tt0.fits',
		overwrite = True
	)

#CI_Tau_LB_-1.0robust_4.0sigma.image.tt0
#Beam 0.086 arcsec x 0.056 arcsec (-33.20 deg)
#Flux inside disk mask: 391.03 mJy
#Peak intensity of source: 12.61 mJy/beam
#rms: 1.09e-01 mJy/beam
#Peak SNR: 115.55

#CI_Tau_LB_-0.5robust_4.0sigma.image.tt0
#Beam 0.088 arcsec x 0.059 arcsec (-33.09 deg)
#Flux inside disk mask: 401.26 mJy
#Peak intensity of source: 13.06 mJy/beam
#rms: 7.55e-02 mJy/beam
#Peak SNR: 173.03

#CI_Tau_LB_0.0robust_4.0sigma.image.tt0
#Beam 0.096 arcsec x 0.065 arcsec (-32.94 deg)
#Flux inside disk mask: 410.76 mJy
#Peak intensity of source: 14.34 mJy/beam
#rms: 5.30e-02 mJy/beam
#Peak SNR: 270.36

#CI_Tau_LB_0.5robust_4.0sigma.image.tt0
#Beam 0.111 arcsec x 0.077 arcsec (-33.69 deg)
#Flux inside disk mask: 413.81 mJy
#Peak intensity of source: 16.78 mJy/beam
#rms: 4.27e-02 mJy/beam
#Peak SNR: 392.59

#CI_Tau_LB_1.0robust_4.0sigma.image.tt0
#Beam 0.133 arcsec x 0.092 arcsec (-34.67 deg)
#Flux inside disk mask: 419.18 mJy
#Peak intensity of source: 19.91 mJy/beam
#rms: 4.11e-02 mJy/beam
#Peak SNR: 484.20

#CI_Tau_LB_1.5robust_4.0sigma.image.tt0
#Beam 0.145 arcsec x 0.100 arcsec (-34.90 deg)
#Flux inside disk mask: 421.15 mJy
#Peak intensity of source: 21.68 mJy/beam
#rms: 4.33e-02 mJy/beam
#Peak SNR: 500.35

for robust in [-1.0,-0.5,0.0,0.5,1.0,1.5]:

    LB_ima_ap0 = prefix+'_LB_{}robust_4.0sigma'.format(robust)

    print('JvM correcting {}.image.tt0'.format(LB_ima_ap0))
    
    do_JvM_correction_and_get_epsilon(LB_ima_ap0)

    estimate_SNR(LB_ima_ap0 + '.JvMcorr.image',
             disk_mask = mask,
             noise_mask = noise_annulus
	)    

    exportfits(imagename = LB_ima_ap0 + '.JvMcorr.image',
               fitsimage = LB_ima_ap0 + '.JvMcorr.image.fits',
               overwrite = True
	)

#The CASA fitted beam is 0.08606630563735962x0.05612698942422867" at -33.20088195800781deg
#Epsilon = 0.8045970474350508

#CI_Tau_LB_-1.0robust_4.0sigma.JvMcorr.image
#Beam 0.086 arcsec x 0.056 arcsec (-33.20 deg)
#Flux inside disk mask: 387.02 mJy
#Peak intensity of source: 12.56 mJy/beam
#rms: 8.78e-02 mJy/beam
#Peak SNR: 143.08

#The CASA fitted beam is 0.08824115246534348x0.058714475482702255" at -33.08661651611328deg
#Epsilon = 0.7991047145406154

#CI_Tau_LB_-0.5robust_4.0sigma.JvMcorr.image
#Beam 0.088 arcsec x 0.059 arcsec (-33.09 deg)
#Flux inside disk mask: 398.69 mJy
#Peak intensity of source: 13.04 mJy/beam
#rms: 6.04e-02 mJy/beam
#Peak SNR: 215.93

#The CASA fitted beam is 0.09558525681495667x0.06539589166641235" at -32.93501281738281deg
#Epsilon = 0.7800885608559485

#CI_Tau_LB_0.0robust_4.0sigma.JvMcorr.image
#Beam 0.096 arcsec x 0.065 arcsec (-32.94 deg)
#Flux inside disk mask: 408.76 mJy
#Peak intensity of source: 14.33 mJy/beam
#rms: 4.15e-02 mJy/beam
#Peak SNR: 345.36

#The CASA fitted beam is 0.11138258129358292x0.07717371731996536" at -33.692710876464844deg
#Epsilon = 0.5537973958038287

#CI_Tau_LB_0.5robust_4.0sigma.JvMcorr.image
#Beam 0.111 arcsec x 0.077 arcsec (-33.69 deg)
#Flux inside disk mask: 410.03 mJy
#Peak intensity of source: 16.79 mJy/beam
#rms: 2.38e-02 mJy/beam
#Peak SNR: 704.23

#The CASA fitted beam is 0.13323818147182465x0.09216275066137314" at -34.66798400878906deg
#Epsilon = 0.31926762144586496

#CI_Tau_LB_1.0robust_4.0sigma.JvMcorr.image
#Beam 0.133 arcsec x 0.092 arcsec (-34.67 deg)
#Flux inside disk mask: 414.00 mJy
#Peak intensity of source: 19.91 mJy/beam
#rms: 1.30e-02 mJy/beam
#Peak SNR: 1528.99

#The CASA fitted beam is 0.14504171907901764x0.10017908364534378" at -34.90468978881836deg
#Epsilon = 0.24086437211067943

#CI_Tau_LB_1.5robust_4.0sigma.JvMcorr.image
#Beam 0.145 arcsec x 0.100 arcsec (-34.90 deg)
#Flux inside disk mask: 415.38 mJy
#Peak intensity of source: 21.66 mJy/beam
#rms: 1.00e-02 mJy/beam
#Peak SNR: 2160.78
