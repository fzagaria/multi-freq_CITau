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
mask_ra  = '04h33m52.027880s'
mask_dec = '22d50m29.748318s'
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
	-1.0:[0, 8, 16, 34, 89, 229, 353],
	-0.5:[0, 8, 16, 36, 84, 211, 325],
	 0.0:[0, 8, 16, 34, 71, 181, 273],
	 0.5:[0, 8, 16, 28, 56, 146, 218],
	 1.0:[0, 8, 16, 23, 46, 121, 182],
	 1.5:[0, 8, 16, 20, 41, 106, 156],
}

cellsizes = {
	-1.0:0.034/8.,
	-0.5:0.037/8.,
	 0.0:0.044/8.,
	 0.5:0.055/8.,
	 1.0:0.066/8.,
	 1.5:0.077/8.,
}

rmses = {
	-1.0:1.44e-02,
	-0.5:1.04e-02,
	 0.0:7.54e-03,
	 0.5:6.26e-03,
	 1.0:5.66e-03,
	 1.5:5.50e-03,
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
#Beam 0.050 arcsec x 0.034 arcsec (-11.22 deg)
#Flux inside disk mask: 15.94 mJy
#Peak intensity of source: 0.60 mJy/beam
#rms: 1.44e-02 mJy/beam
#Peak SNR: 41.51

#CI_Tau_LB_-0.5robust_1.0sigma.image.tt0
#Beam 0.054 arcsec x 0.037 arcsec (-10.25 deg)
#Flux inside disk mask: 16.16 mJy
#Peak intensity of source: 0.66 mJy/beam
#rms: 1.04e-02 mJy/beam
#Peak SNR: 63.36

#CI_Tau_LB_0.0robust_1.0sigma.image.tt0
#Beam 0.064 arcsec x 0.044 arcsec (-6.22 deg)
#Flux inside disk mask: 16.42 mJy
#Peak intensity of source: 0.79 mJy/beam
#rms: 7.55e-03 mJy/beam
#Peak SNR: 104.85

#CI_Tau_LB_0.5robust_1.0sigma.image.tt0
#Beam 0.081 arcsec x 0.055 arcsec (3.21 deg)
#Flux inside disk mask: 16.41 mJy
#Peak intensity of source: 0.97 mJy/beam
#rms: 6.26e-03 mJy/beam
#Peak SNR: 155.14

#CI_Tau_LB_1.0robust_1.0sigma.image.tt0
#Beam 0.137 arcsec x 0.066 arcsec (22.34 deg)
#Flux inside disk mask: 16.35 mJy
#Peak intensity of source: 1.25 mJy/beam
#rms: 5.66e-03 mJy/beam
#Peak SNR: 220.42

#CI_Tau_LB_1.5robust_1.0sigma.image.tt0
#Beam 0.173 arcsec x 0.077 arcsec (27.84 deg)
#Flux inside disk mask: 16.33 mJy
#Peak intensity of source: 1.43 mJy/beam
#rms: 5.50e-03 mJy/beam
#Peak SNR: 260.64

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
#Beam 0.050 arcsec x 0.034 arcsec (-11.22 deg)
#Flux inside disk mask: 14.80 mJy
#Peak intensity of source: 0.61 mJy/beam
#rms: 1.46e-02 mJy/beam
#Peak SNR: 41.54

#CI_Tau_LB_-0.5robust_4.0sigma.image.tt0
#Beam 0.054 arcsec x 0.037 arcsec (-10.25 deg)
#Flux inside disk mask: 15.66 mJy
#Peak intensity of source: 0.66 mJy/beam
#rms: 1.05e-02 mJy/beam
#Peak SNR: 63.25

#CI_Tau_LB_0.0robust_4.0sigma.image.tt0
#Beam 0.064 arcsec x 0.044 arcsec (-6.22 deg)
#Flux inside disk mask: 17.12 mJy
#Peak intensity of source: 0.80 mJy/beam
#rms: 7.60e-03 mJy/beam
#Peak SNR: 104.77

#CI_Tau_LB_0.5robust_4.0sigma.image.tt0
#Beam 0.081 arcsec x 0.055 arcsec (3.21 deg)
#Flux inside disk mask: 18.13 mJy
#Peak intensity of source: 0.96 mJy/beam
#rms: 6.32e-03 mJy/beam
#Peak SNR: 152.11

#CI_Tau_LB_1.0robust_4.0sigma.image.tt0
#Beam 0.137 arcsec x 0.066 arcsec (22.34 deg)
#Flux inside disk mask: 17.59 mJy
#Peak intensity of source: 1.22 mJy/beam
#rms: 5.75e-03 mJy/beam
#Peak SNR: 212.52

#CI_Tau_LB_1.5robust_4.0sigma.image.tt0
#Beam 0.173 arcsec x 0.077 arcsec (27.84 deg)
#Flux inside disk mask: 17.25 mJy
#Peak intensity of source: 1.41 mJy/beam
#rms: 5.61e-03 mJy/beam
#Peak SNR: 250.58

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

#The CASA fitted beam is 0.0499173179268837x0.033634718507528305" at -11.21826171875deg
#Epsilon = 0.9566981109594672

#CI_Tau_LB_-1.0robust_4.0sigma.JvMcorr.image
#Beam 0.050 arcsec x 0.034 arcsec (-11.22 deg)
#Flux inside disk mask: 14.65 mJy
#Peak intensity of source: 0.61 mJy/beam
#rms: 1.41e-02 mJy/beam
#Peak SNR: 42.83

#The CASA fitted beam is 0.05405379831790924x0.03674154356122017" at -10.247218132019043deg
#Epsilon = 0.9730354716231565

#CI_Tau_LB_-0.5robust_4.0sigma.JvMcorr.image
#Beam 0.054 arcsec x 0.037 arcsec (-10.25 deg)
#Flux inside disk mask: 15.60 mJy
#Peak intensity of source: 0.66 mJy/beam
#rms: 1.02e-02 mJy/beam
#Peak SNR: 64.69

#The CASA fitted beam is 0.06398829817771912x0.04423379525542259" at -6.21917724609375deg
#Epsilon = 0.8100229150918377

#CI_Tau_LB_0.0robust_4.0sigma.JvMcorr.image
#Beam 0.064 arcsec x 0.044 arcsec (-6.22 deg)
#Flux inside disk mask: 16.62 mJy
#Peak intensity of source: 0.79 mJy/beam
#rms: 6.16e-03 mJy/beam
#Peak SNR: 128.48

#The CASA fitted beam is 0.08076183497905731x0.055060528218746185" at 3.210540771484375deg
#Epsilon = 0.24590642679252522

#CI_Tau_LB_0.5robust_4.0sigma.JvMcorr.image
#Beam 0.081 arcsec x 0.055 arcsec (3.21 deg)
#Flux inside disk mask: 16.28 mJy
#Peak intensity of source: 0.94 mJy/beam
#rms: 1.56e-03 mJy/beam
#Peak SNR: 607.12

#The CASA fitted beam is 0.1370481550693512x0.0659472644329071" at 22.33892822265625deg
#Epsilon = 0.09629908827134454

#CI_Tau_LB_1.0robust_4.0sigma.JvMcorr.image
#Beam 0.137 arcsec x 0.066 arcsec (22.34 deg)
#Flux inside disk mask: 16.24 mJy
#Peak intensity of source: 1.20 mJy/beam
#rms: 5.54e-04 mJy/beam
#Peak SNR: 2174.20

#The CASA fitted beam is 0.17325085401535034x0.07735392451286316" at 27.841659545898438deg
#Epsilon = 0.0608831492285845

#CI_Tau_LB_1.5robust_4.0sigma.JvMcorr.image
#Beam 0.173 arcsec x 0.077 arcsec (27.84 deg)
#Flux inside disk mask: 16.24 mJy
#Peak intensity of source: 1.39 mJy/beam
#rms: 3.41e-04 mJy/beam
#Peak SNR: 4063.07

#The CASA fitted beam is 0.17325085401535034x0.07735392451286316" at 27.841659545898438deg
#Epsilon = 0.20069453804969428
#CI_Tau_LB_1.5robust_4.0sigma_copyw201pix.JvMcorr.image
#Beam 0.173 arcsec x 0.077 arcsec (27.84 deg)
#Flux inside disk mask: 16.39 mJy
#Peak intensity of source: 1.39 mJy/beam
#rms: 1.13e-03 mJy/beam
#Peak SNR: 1234.97
