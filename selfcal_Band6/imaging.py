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
mask_ra  = '04h33m52.026900s'
mask_dec = '22d50m29.780037s'
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
	-1.0:[0, 8, 16, 56, 146, 361, 572],
	-0.5:[0, 8, 16, 53, 136, 341, 546],
	 0.0:[0, 8, 16, 51, 126, 301, 480],
	 0.5:[0, 8, 16, 37,  96, 241, 375],
	 1.0:[0, 8, 16, 33,  76, 181, 280],
	 1.5:[0, 8, 16, 30,  66, 161, 245],
}

cellsizes = {
	-1.0:0.021/8.,
	-0.5:0.022/8.,
	 0.0:0.025/8.,
	 0.5:0.032/8.,
	 1.0:0.043/8.,
	 1.5:0.049/8.,
}

rmses = {
	-1.0:2.89e-02,
	-0.5:2.05e-02,
	 0.0:1.45e-02,
	 0.5:1.10e-02,
	 1.0:9.79e-03,
	 1.5:9.61e-03,
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
        threshold = '{}mJy'.format(rmses[robust]),        # 1 rms contap0
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
#Beam 0.033 arcsec x 0.021 arcsec (7.95 deg)
#Flux inside disk mask: 147.06 mJy
#Peak intensity of source: 1.73 mJy/beam
#rms: 2.89e-02 mJy/beam
#Peak SNR: 59.74

#CI_Tau_LB_-0.5robust_1.0sigma.image.tt0
#Beam 0.034 arcsec x 0.022 arcsec (7.94 deg)
#Flux inside disk mask: 147.07 mJy
#Peak intensity of source: 1.80 mJy/beam
#rms: 2.05e-02 mJy/beam
#Peak SNR: 88.09

#CI_Tau_LB_0.0robust_1.0sigma.image.tt0
#Beam 0.037 arcsec x 0.025 arcsec (7.51 deg)
#Flux inside disk mask: 147.08 mJy
#Peak intensity of source: 2.05 mJy/beam
#rms: 1.45e-02 mJy/beam
#Peak SNR: 141.19

#CI_Tau_LB_0.5robust_1.0sigma.image.tt0
#Beam 0.044 arcsec x 0.032 arcsec (8.74 deg)
#Flux inside disk mask: 147.47 mJy
#Peak intensity of source: 2.66 mJy/beam
#rms: 1.10e-02 mJy/beam
#Peak SNR: 241.03

#CI_Tau_LB_1.0robust_1.0sigma.image.tt0
#Beam 0.062 arcsec x 0.043 arcsec (29.99 deg)
#Flux inside disk mask: 147.49 mJy
#Peak intensity of source: 3.84 mJy/beam
#rms: 9.79e-03 mJy/beam
#Peak SNR: 392.22

#CI_Tau_LB_1.5robust_1.0sigma.image.tt0
#Beam 0.070 arcsec x 0.049 arcsec (35.61 deg)
#Flux inside disk mask: 147.68 mJy
#Peak intensity of source: 4.44 mJy/beam
#rms: 9.61e-03 mJy/beam
#Peak SNR: 462.12

for robust in [-1.0,-0.5,0.0,0.5,1.0,1.5]:

    LB_ima_ap0 = prefix + '_LB_{}robust_4.0sigma'.format(robust)

    print('CLEANing {}'.format(LB_ima_ap0))
    
    os.system('rm -rf ' + LB_ima_ap0 + '.*')
    tclean_wrapper_b3(
		vis = LB_cont_ap0,
        imagename = LB_ima_ap0,
        mask = mask,
        scales = LB_scales[robust],
        threshold = '{}mJy'.format(4.*rmses[robust]),     # 4 rms contap0
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
#Beam 0.033 arcsec x 0.021 arcsec (7.95 deg)
#Flux inside disk mask: 150.96 mJy
#Peak intensity of source: 1.78 mJy/beam
#rms: 3.15e-02 mJy/beam
#Peak SNR: 56.44

#CI_Tau_LB_-0.5robust_4.0sigma.image.tt0
#Beam 0.034 arcsec x 0.022 arcsec (7.94 deg)
#Flux inside disk mask: 149.31 mJy
#Peak intensity of source: 1.86 mJy/beam
#rms: 2.17e-02 mJy/beam
#Peak SNR: 85.40

#CI_Tau_LB_0.0robust_4.0sigma.image.tt0
#Beam 0.037 arcsec x 0.025 arcsec (7.51 deg)
#Flux inside disk mask: 148.56 mJy
#Peak intensity of source: 2.09 mJy/beam
#rms: 1.51e-02 mJy/beam
#Peak SNR: 138.05

#CI_Tau_LB_0.5robust_4.0sigma.image.tt0
#Beam 0.044 arcsec x 0.032 arcsec (8.74 deg)
#Flux inside disk mask: 149.26 mJy
#Peak intensity of source: 2.69 mJy/beam
#rms: 1.15e-02 mJy/beam
#Peak SNR: 234.81

#CI_Tau_LB_1.0robust_4.0sigma.image.tt0
#Beam 0.062 arcsec x 0.043 arcsec (29.99 deg)
#Flux inside disk mask: 148.75 mJy
#Peak intensity of source: 3.84 mJy/beam
#rms: 1.02e-02 mJy/beam
#Peak SNR: 375.29

#CI_Tau_LB_1.5robust_4.0sigma.image.tt0
#Beam 0.070 arcsec x 0.049 arcsec (35.61 deg)
#Flux inside disk mask: 148.96 mJy
#Peak intensity of source: 4.41 mJy/beam
#rms: 1.01e-02 mJy/beam
#Peak SNR: 435.17

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

#The CASA fitted beam is 0.03337464854121208x0.02068297564983368" at 7.9491729736328125deg
#Epsilon = 0.7307945257366176

#CI_Tau_LB_-1.0robust_4.0sigma.JvMcorr.image
#Beam 0.033 arcsec x 0.021 arcsec (7.95 deg)
#Flux inside disk mask: 141.37 mJy
#Peak intensity of source: 1.75 mJy/beam
#rms: 2.26e-02 mJy/beam
#Peak SNR: 77.72

#The CASA fitted beam is 0.03414563089609146x0.021619895473122597" at 7.942779541015625deg
#Epsilon = 0.7394484937048242

#CI_Tau_LB_-0.5robust_4.0sigma.JvMcorr.image
#Beam 0.034 arcsec x 0.022 arcsec (7.94 deg)
#Flux inside disk mask: 143.92 mJy
#Peak intensity of source: 1.84 mJy/beam
#rms: 1.55e-02 mJy/beam
#Peak SNR: 118.46

#The CASA fitted beam is 0.03688677400350571x0.02490628883242607" at 7.50665283203125deg
#Epsilon = 0.6996386503166396

#CI_Tau_LB_0.0robust_4.0sigma.JvMcorr.image
#Beam 0.037 arcsec x 0.025 arcsec (7.51 deg)
#Flux inside disk mask: 146.01 mJy
#Peak intensity of source: 2.08 mJy/beam
#rms: 1.02e-02 mJy/beam
#Peak SNR: 204.31

#The CASA fitted beam is 0.04414024204015732x0.03222673758864403" at 8.743194580078125deg
#Epsilon = 0.5377702412839922

#CI_Tau_LB_0.5robust_4.0sigma.JvMcorr.image
#Beam 0.044 arcsec x 0.032 arcsec (8.74 deg)
#Flux inside disk mask: 147.50 mJy
#Peak intensity of source: 2.68 mJy/beam
#rms: 5.91e-03 mJy/beam
#Peak SNR: 452.90

#The CASA fitted beam is 0.06156514212489128x0.04287024959921837" at 29.98807144165039deg
#Epsilon = 0.38742683839674324

#CI_Tau_LB_1.0robust_4.0sigma.JvMcorr.image
#Beam 0.062 arcsec x 0.043 arcsec (29.99 deg)
#Flux inside disk mask: 147.62 mJy
#Peak intensity of source: 3.82 mJy/beam
#rms: 3.81e-03 mJy/beam
#Peak SNR: 1001.58

#The CASA fitted beam is 0.07040822505950928x0.04893125593662262" at 35.60769271850586deg
#Epsilon = 0.33569425057578584

#CI_Tau_LB_1.5robust_4.0sigma.JvMcorr.image
#Beam 0.070 arcsec x 0.049 arcsec (35.61 deg)
#Flux inside disk mask: 148.04 mJy
#Peak intensity of source: 4.39 mJy/beam
#rms: 3.28e-03 mJy/beam
#Peak SNR: 1339.37
