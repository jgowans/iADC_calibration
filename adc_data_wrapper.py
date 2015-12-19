"""
An interface to the snapshot blocks with some data analysis 
functions on the data received
"""

import numpy as np
import logging

class AdcDataWrapper:
    def __init__(self, correlator, fs = 800e6, logger=logging.getLogger(__name__)):
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
        self.fs = float(fs)

    def resample(self):
        """ Updates the samples from the ADC
        """
        self.correlator.fetch_time_domain_snapshot(force=True)

    def get_offset(self, channel):
        """ Returns the DC offset of a channel.
        Channel is ('0I, 0Q, 1I, 1Q')
        """
        chan_idx = ['0I', '0Q', '1I', '1Q'].index(channel)
        return np.mean(self.correlator.time_domain_signals[chan_idx])

    def get_phase_difference(self, channel_a, channel_b):
        """ Retuns phase difference between strongest signal
        in channel a vs the same tone in channel b"
        """
        chan_a_idx = ['0I', '0Q', '1I', '1Q'].index(channel_a)
        chan_b_idx = ['0I', '0Q', '1I', '1Q'].index(channel_b)
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
        self.logger.info("Between {a} and {b}, max freq: {f} with phase difference: {ph}".format(
            a = channel_a, b = channel_b,
            f = max_freq/1e6, ph = max_phase))

    def set_mode(self, mode):
        assert(mode in ('I', 'Q', 'IQ', 'inter'))
        self._mode = mode

    def get_signals(self):
        """
        Returns a dictory of signal_name -> np.array of samples.
        Signal_name is 'I', 'Q', or 'inter' depending on what has been
        selected in self.mode.
        """
        self.fpga.write_int('adc_select', self.zdok_n)
        self.fpga.write_int('trigger', 0)
        self.fpga.snapshot_arm('snapshot_I')
        self.fpga.snapshot_arm('snapshot_Q')
        self.fpga.write_int('trigger', 1)
        self.fpga.write_int('trigger', 0)
        signals = {}
        if(self._mode == 'inter'):
            raw = self.fpga.snapshot_get('snapshot_I', arm=False)['data']
            sig_I = np.frombuffer(raw, dtype=np.int8)
            raw = self.fpga.snapshot_get('snapshot_Q', arm=False)['data']
            sig_Q = np.frombuffer(raw, dtype=np.int8)
            interleaved = np.empty((sig_I.size + sig_Q.size,), dtype=np.int8)  # create empty array of correct size
            interleaved[0::2] = sig_Q  # set even elements to signal I
            interleaved[1::2] = sig_I  # set odd elements to signal Q
            signals['inter'] = interleaved
        else:
            for channel in ('I', 'Q'):
                if(channel in  self._mode):
                    snap_name = "snapshot_{X}".format(X = channel)
                    raw = self.fpga.snapshot_get(snap_name, arm=False)['data']
                    signals[channel] = np.frombuffer(raw, dtype=np.int8)
        return signals

    def get_means(self):
        means = {}
        for name, samples in self.get_signals().items():
            means[name] = samples.mean()
        return means

    def get_sum_squared(self):
        sum_squares = {}
        for name, samples in self.get_signals().items():
            sum_squares[name] = (samples**2).sum()
        return sum_squares
