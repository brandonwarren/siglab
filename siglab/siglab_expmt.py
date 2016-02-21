#!/usr/bin/env python

# another example of using signal_lab

import matplotlib.pyplot as plt
import signal_lab

path = 'zf3017_42337.39741472_11_29_11_2_21_motif_1.wav'
data = signal_lab.SignalLab(path)
#data.plot_time(offset_time=0.0)

N = 1024

offset = 0.57 # nice harmonic stack at this location
title = 'nice stack'
#data.plot_time(offset_time=offset, num_points=N, title=title)
data.power_spectrum(offset_time=offset, blocksize=N, plot_it=False, title=title)
#data.autocorrelation(N/2, title=title)
goodness_of_pitch, pitch = data.cepstrum(N/2, title=title)
print '{}: goodness = {:.2f} pitch = {:.1f}'.format(title,
                                                    goodness_of_pitch, pitch)

offset = 0.0367 # no stack here
title = 'lame stack'
#data.plot_time(offset_time=offset, num_points=N, title=title)
data.power_spectrum(offset_time=offset, blocksize=N, plot_it=False, title=title)
#data.autocorrelation(N/2, title=title)
goodness_of_pitch, pitch = data.cepstrum(N/2, title=title)
print '{}: goodness = {:.2f} pitch = {:.1f}'.format(title,
                                                    goodness_of_pitch, pitch)

offset = 0.381
title = 'best stack'
#data.plot_time(offset_time=offset, num_points=N, title=title)
data.power_spectrum(offset_time=offset, blocksize=N, plot_it=False, title=title)
#data.autocorrelation(N/2, title=title)
goodness_of_pitch, pitch = data.cepstrum(N/2, title=title)
print '{}: goodness = {:.2f} pitch = {:.1f}'.format(title,
                                                    goodness_of_pitch, pitch)

plt.show() # shows plots and waits for user to close them all
