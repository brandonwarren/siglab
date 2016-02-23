#!/usr/bin/env python

# another example of using signal_lab
# plot goodness-of-pitch and pitch over time

import numpy
import matplotlib.pyplot as plt
import signal_lab

N = 1024
overlap = .5 #0.50 # as a fraction - .25 is 25%
window_it = True
max_pitch_freq = 4.2e3

path = 'zf3017_42337.39741472_11_29_11_2_21_motif_1.wav'
data = signal_lab.SignalLab(path, max_pitch_freq=max_pitch_freq)
print('_n_cepstrum_points_to_skip_for_pitch = {0}, max pitch freq = {1:.1f}kHz'.format(
    data._n_cepstrum_points_to_skip_for_pitch, data.max_pitch_freq))
#data.plot_time(offset_time=0.0)

dur_of_N = data.sample_times[N] # how much time N represents
end_time = data.sample_times[data.n_wav_samps-1]

inc_t = dur_of_N - overlap*dur_of_N

# Because we may be using overlap, the number of measurements
# is not obvious. Since the actual number is small, just use lists.
time = []
goodness_of_pitch = []
pitch = []

offset = 0.0
#end_time = 0.1 # TEMP
while offset+dur_of_N < end_time:
    data.power_spectrum(offset_time=offset, blocksize=N, window_it=window_it,
                        plot_it=False)
    good, p = data.cepstrum(N/2, plot_it=False)

    time.append(offset)
    goodness_of_pitch.append(good)
    pitch.append(p)

    # print 'offset = {0:.3f} goodness = {1:.2f} pitch = {2:.1f}'.format(offset, good, p)
    offset += inc_t

# http://matplotlib.org/examples/api/two_scales.html#api-two-scales
fig, ax1 = plt.subplots(figsize=(10.0, 4.0), dpi=80)
ax1.plot(time, pitch, 'b.')
ax1.set_ylabel('pitch', color='b')
for tlab in ax1.get_yticklabels():
    tlab.set_color('b')

plt.grid(True)

ax2 = ax1.twinx()
ax2.plot(time, goodness_of_pitch, 'r')
ax2.set_xlabel('Seconds')
ax2.set_ylabel('goodness', color='r')
for tlab in ax2.get_yticklabels():
    tlab.set_color('r')

plt.title('Max pitch={0:.1f}kHz N={1} overlap={2}%'.format(1e-3*data.max_pitch_freq,
                                                     N, int(overlap*100)))


offset = 0.546 # 0.035
title = 'nice stack, offset={0:.3f} sec'.format(offset)
#data.plot_time(offset_time=offset, num_points=N, title=title)
data.power_spectrum(offset_time=offset, blocksize=N, window_it=window_it,
                    plot_it=False, title=title)
#data.autocorrelation(N/2, title=title)
goodness_of_pitch, pitch = data.cepstrum(N/2, title=title)
print '{0}: goodness = {1:.2f} pitch = {2:.1f}'.format(title,
                                                    goodness_of_pitch, pitch)

offset = 0.210
title = 'lame stack, offset={0:.3f} sec'.format(offset)
#data.plot_time(offset_time=offset, num_points=N, title=title)
data.power_spectrum(offset_time=offset, blocksize=N, window_it=window_it,
                    plot_it=False, title=title)
#data.autocorrelation(N/2, title=title)
goodness_of_pitch, pitch = data.cepstrum(N/2, title=title)
print '{0}: goodness = {1:.2f} pitch = {2:.1f}'.format(title,
                                                    goodness_of_pitch, pitch)



plt.show() # shows plots and waits for user to close them all
