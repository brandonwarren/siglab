#!/usr/bin/env python

# another example of using signal_lab
# plot goodness-of-pitch and pitch over time

import numpy
import matplotlib.pyplot as plt
import signal_lab

path = 'zf3017_42337.39741472_11_29_11_2_21_motif_1.wav'
data = signal_lab.SignalLab(path)
data.plot_time(offset_time=0.0)

N = 1024
dur_of_N = data.sample_times[N] # how much time N represents
end_time = data.sample_times[data.n_wav_samps-1]

overlap = 0.50 # as a fraction - .25 is 25%
inc_t = dur_of_N - overlap*dur_of_N

# Because we may be using overlap, the number of measurements
# is not obvious. Since the actual number is small, just use lists.
time = []
goodness_of_pitch = []
pitch = []

offset = 0.0
while offset+dur_of_N < end_time:
    data.power_spectrum(offset_time=offset, blocksize=N, plot_it=False)
    good, p = data.cepstrum(N/2, plot_it=False)

    time.append(offset)
    goodness_of_pitch.append(good)
    pitch.append(p)

    print 'offset = {:.3f} goodness = {:.2f} pitch = {:.1f}'.format(offset, good, p)
    offset += inc_t

# http://matplotlib.org/examples/api/two_scales.html#api-two-scales
fig, ax1 = plt.subplots()
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

plt.title('N={} overlap={}%'.format(N, int(overlap*100)))

plt.show() # shows plots and waits for user to close them all
