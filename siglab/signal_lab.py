#!/usr/bin/env python

"""Class to make playing around with wav files easy and fun.

See code at bottom for example usage.

Written Feb 2016 by Brandon Warren (bwarren@uw.edu)

"""

import wave
import numpy
import matplotlib.pyplot as plt

# Max cepstrum freq of interest: keep 1st point above this freq and
# all the ones below.
# this should be set by user (caller), and the actual number should be computed
# and shown (e.g. if this is set to 10kHz, show 11kHz) self.top_cepstrum_freq
UPPER_CEPSTRUM_FREQ = 4.5e3# 4.5e3

class SignalLab(object):
    """Class for opening, plotting, and analyzing sound files (only wav for now).

    Attributes:
        path (str): full path of opened file
        sample_rate (float) : sample rate of opened file in Hz
        n_wav_samps (int): number of samples
        sound_data (numpy int16 array): the raw sound data
        delta_t (float): 1/sample_rate
        sample_times (numpy float array): time of each sample, first time is zero
    """

    def __init__(self, path):
        """This just opens, reads, and closes the wav file.

        Args:
            path (str): full path of file to open
        """
        try:
            snd = wave.open(path, 'r')
            self.path = path
            if snd.getsampwidth() != 2:
                raise TypeError('{} has {}-byte samples. Expecting 2-byte samples.')
            self.sample_rate = float(snd.getframerate())
            self.n_wav_samps = snd.getnframes()
            stream = snd.readframes(self.n_wav_samps)
            self.sound_data = numpy.fromstring(string=stream, dtype=numpy.int16)
            self.delta_t = 1.0/self.sample_rate
            self.sample_times = numpy.arange(0,
                                             (self.n_wav_samps+1)*self.delta_t,
                                             self.delta_t)

            # determine number of cepstrum points to ignore (clear or skip)
            # e.g. sample rate is 44.1 kHz
##            cepstrum_[0] = 0 # no shift MUST CLEAR THIS, zero shift is always max
##            cepstrum_[1] = 0 # 44.1 kHz (won't be at sample rate, or even 1/2 it
##            cepstrum_[2] = 0 # 22 kHz - don't want this often-large value boosting goodness-of-pitch
##            cepstrum_[3] = 0 # 14.7 kHz
##            cepstrum_[4] = 0 # 11 kHz
##            cepstrum_[5] = 0 # 8.8 kHz
##            cepstrum_[6] = 0 # 7.4 kHz
##            cepstrum_[7] = 0 # 6.3 kHz
##            cepstrum_[8] = 0 # 5.5 kHz
##            cepstrum_[9] = 0 # 4.9 kHz
##            cepstrum_[10] = 0 # 4.4 kHz
            self.n_cepstrum_points_to_skip = 1 # always clear 1st point (zero shift)
            while True:
                next_f = self.sample_rate/(self.n_cepstrum_points_to_skip+1)
                if next_f < UPPER_CEPSTRUM_FREQ:
                    break
                self.n_cepstrum_points_to_skip += 1
            self.top_cepstrum_freq = self.sample_rate/self.n_cepstrum_points_to_skip
            print('n_cepstrum_points_to_skip = {}, top cepstrum freq = {:.1f}kHz'.format(
                self.n_cepstrum_points_to_skip, self.top_cepstrum_freq))
        finally:
            snd.close()

    def _plot_time(self, data, offset_i, num_points, title='', ylabel='Counts'):
        """Used internally to plot time history data.

        Args:
            data (numpy array): data to plot. Will use first sample passed, so
                    caller must send slice if he wants to plot from an offset.
            offset_i (int): 0-based index, used to index into sample_times
            num_points (int): number of samples to plot
            title (str): plot title
            ylabel (str): label to use for Y-axis

        May be overridden to plot using different library or method (e.g. to PNG file).
        """
        plt.figure()
        subplot = plt.subplot(1,1,1) # only needed if I want to call subplot methods
        plt.plot(self.sample_times[offset_i:offset_i+num_points],
                 data[:num_points],
                 'r')
        plt.title(title)
        plt.xlabel('Seconds')
        plt.ylabel(ylabel)
        subplot.set_autoscale_on(True)
        plt.grid(True)

    def _plot_freq(self, data, blocksize, title='', xlabel='Hz', ylabel=''):
        plt.figure()
        subplot = plt.subplot(1,1,1) # only needed if I want to call subplot methods
        delta_f = self.sample_rate/blocksize # 1/T
        x_scale = numpy.arange(0, (blocksize/2+1)*delta_f, delta_f)[:blocksize/2]
        plt.plot(x_scale, data, 'r')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        subplot.set_autoscale_on(True)
        plt.grid(True)

    def plot_time(self, offset_time=0.0, num_points=None, offset_dur=None, title=None):
        """Plot time history of sound file.
        """
        if title is None:
            title = self.path
        offset_i = int(0.5 + offset_time*self.sample_rate)
        if offset_dur:
            num_points = int(0.5 + offset_dur*self.sample_rate)
        elif num_points is None:
            num_points = self.n_wav_samps
        max_num_points = self.n_wav_samps - offset_i
        num_points = min(num_points, max_num_points)
        self._plot_time(self.sound_data[offset_i:], offset_i, num_points, title=title)

    def power_spectrum(self, offset_time, blocksize, plot_it=True, title=None):
        """Compute and plot power spectrum of sound file.
        """
        # TODO: window, verify alg
        i = int(0.5 + offset_time*self.sample_rate)
        fft = numpy.fft.fft(self.sound_data[i:i+blocksize])
        self.power = fft*fft
        self.power = numpy.abs(self.power) # combine with line above?
        if plot_it:
            if title is None:
                title = 'Power spectrum'
            self._plot_freq(self.power[:blocksize/2], blocksize,
                            title=title, xlabel='Hz',
                            ylabel='power (no units)')

    def autocorrelation(self, num_points, title=None):
        """Compute and plot autocorrelation of sound file.

        Uses result from power_spectrum()
        """
        # TODO: verify alg
        if title is None:
            title = 'Autocorrelation'
        autoc = numpy.abs(numpy.fft.ifft(self.power))
        self._plot_time(autoc, offset_i=0, num_points=num_points,
                        title=title, ylabel='autocorrelation')

    def cepstrum(self, num_points, plot_it=True, title=None):
        """Compute and plot cepstrum of sound file.

        Uses result from power_spectrum()
        """
        # TODO: verify alg
        cepstrum_ = numpy.abs(numpy.fft.ifft(numpy.log(self.power)))
        indx_max = self.n_cepstrum_points_to_skip + \
                   cepstrum_[self.n_cepstrum_points_to_skip:num_points].argmax()
        goodness_of_pitch = cepstrum_[indx_max]
        pitch = self.sample_rate/indx_max

        if plot_it:
            if title is None:
                title = 'Cepstrum'
            # n_cepstrum_points_to_skip ONLY AFFECTS pitch calculations, not plot. No need to alter plot.
            # cepstrum_[0:self.n_cepstrum_points_to_skip] = 0
            cepstrum_[0] = 0 # just clear the zero-shift point
            # ylabel = 'cepstrum (f>{:.1f}kHz'.format(UPPER_CEPSTRUM_FREQ)
            ylabel = 'cepstrum'
            self._plot_time(cepstrum_, offset_i=0, num_points=num_points,
                            title=title, ylabel=ylabel)

        return goodness_of_pitch, pitch


if __name__ == '__main__':
    # Example of how to use SignalLab.
    #
    # This can be run from IDLE (F5), but Python sometimes crashes. Would
    # running from command line or within wxPython stop that?
    #
    # path = 'C:\\Users\\Brandon\\Documents\\perkel\\motifs - clean 11-29-15\\zf3017_42337.39741472_11_29_11_2_21_motif_1.wav'
    path = 'zf3017_42337.39741472_11_29_11_2_21_motif_1.wav'
    data = SignalLab(path)
    data.plot_time(offset_time=0.0)
    N = 1024
    offset = 0.57 # nice harmonic stack at this location
    data.plot_time(offset_time=offset, num_points=N) #offset_dur=0.1)
    data.power_spectrum(offset_time=offset, blocksize=N)
    data.autocorrelation(N/2)   # good?
    data.cepstrum(N/2)          # bad? no looks good!
    plt.show() # shows plots and waits for user to close them all
