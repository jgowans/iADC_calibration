"""
An interface to the snapshot blocks with some data analysis 
functions on the data received
"""

import numpy as np
import logging

class AdcDataWrapper:
    def __init__(self, correlator, zdok_n, fs = 800e6, logger=logging.getLogger(__name__)):
        """
        correlator -- instance of directionFinder_backend.correlator.Correlator
        mode -- 'I', 'Q', or 'inter'.
            I: only get the snap from I channel
            Q: only get the snap from Q channel
            IQ: get both I and Q channels
            inter: get an interleaved channel
        """
        self.logger = logger
        self.correlator = correlator
        self.zdok_n = zdok_n
        self.fs = float(fs)

    def resample(self):
        """ Updates the samples from the ADC
        """
        self.correlator.fetch_time_domain_snapshot(force=True)

    def get_offset(self, channel):
        """ Returns the DC offset of a channel.
        Channel is ('I', 'Q')
        """
        chan_idx = ['I', 'Q'].index(channel) + (2*self.zdok_n)
        mean = np.mean(self.correlator.time_domain_signals[chan_idx])
        self.logger.debug("Offset for channel {c}: {v}".format(c = channel, v = mean))
        return mean

    def get_power(self, channel):
        chan_idx = ['I', 'Q'].index(channel) + (2*self.zdok_n)
        signal = self.correlator.time_domain_signals[chan_idx]
        energy = np.sum(np.square(signal))
        power = energy / len(signal)
        self.logger.debug("Power for channel {c}: {v}".format(c = channel, v = power))
        return power

    def get_phase_difference(self, channel_a, channel_b):
        """ Retuns phase difference between strongest signal
        in channel a vs the same tone in channel b.
        If the phase is positive, it means A comes before B
        If the phase is negative, it means B comes before A
        """
        chan_a_idx = ['I', 'Q'].index(channel_a) + (2 * self.zdok_n)
        chan_b_idx = ['I', 'Q'].index(channel_b) + (2 * self.zdok_n)
        chan_a_sub_arrays = np.split(
            self.correlator.time_domain_signals[chan_a_idx], 
            len(self.correlator.time_domain_signals[chan_a_idx])/2**11)
        chan_b_sub_arrays = np.split(
            self.correlator.time_domain_signals[chan_b_idx],
            len(self.correlator.time_domain_signals[chan_b_idx])/2**11)
        cross_acc = np.ndarray((2**11/2) + 1, dtype=np.complex128)
        for sub_idx in range(len(chan_a_sub_arrays)):
            fft_a = np.fft.rfft(chan_a_sub_arrays[sub_idx])
            fft_b = np.fft.rfft(chan_b_sub_arrays[sub_idx])
            cross = fft_a * np.conj(fft_b)
            cross_acc += cross
        max_idx = np.argmax(np.abs(cross_acc))
        max_freq = self.fs/2 * (max_idx / float(len(cross_acc)))
        max_phase = np.angle(cross_acc[max_idx])
        self.logger.debug("Between {a} and {b}, max freq: {f} with phase difference: {ph}".format(
            a = channel_a, b = channel_b,
            f = max_freq/1e6, ph = max_phase))

