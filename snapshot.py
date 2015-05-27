"""
An interface to the snapshot blocks with some data analysis 
functions on the data received
"""

import numpy as np
import logging

class Snapshot:
    def __init__(self, fpga, zdok_num, mode, logger=logging.getLogger(__name__)):
        """
        fpga -- instance of corr.katcp_wrapper.FpgaClient
        zdok_num -- which ADC to snap from. 0 or 1
        mode -- 'I', 'Q', or 'inter'.
            I: only get the snap from I channel
            Q: only get the snap from Q channel
            IQ: get both I and Q channels
            inter: get an interleaved channel
        """
        logging.basicConfig()
        self.logger = logger
        self.fpga = fpga
        self.name = name
        self.zdok_n = zdok_n
        self.set_mode(mode)

    def set_mode(self, mode):
        assert(mode in 'I', 'Q', 'IQ', 'inter')
        self._mode = mode

    def get_signals(self):
        """
        Returns a dictory of signal_name -> np.array of samples.
        Signal_name is 'I', 'Q', or 'inter' depending on what has been
        selected in self.mode.
        """
        self.fpga.write_int('adc_select', self.zdok_num)
        self.fpga.snapshot_arm('snapshot_I')
        self.fpga.snapshot_arm('snapshot_Q')
        self.fpga.write_int('trigger', 1)
        self.fpga.write_int('trigger', 0)
        signals = {}
        if(self._mode == 'inter'):
            # do interleaving stuff here
            raw = self.fpga.snapshot_get('snapshot_I')['data']
            sig_I = np.frombuffer(raw, dtype=np.int8)
            raw = self.fpga.snapshot_get('snapshot_Q')['data']
            sig_Q = np.frombuffer(raw, dtype=np.int8)
            interleaved = np.empty((sig_I.size + sig_Q.size,), dtype=a.dtype)  # create empty array of correct size
            interleaved[0::2] = sig_I  # set even elements to signal I
            interleaved[1::2] = sig_Q  # set odd elements to signal Q
            signals{'inter'} = interleaved
        else:
            for channel in ('I', 'Q'):
                if(channel in  self._mode):
                    snap_name = "snapshot_{X}".format(X = channel)
                    raw = self.fpga.snapshot_get(snap_name)['data']
                    signals[channel] = np.frombuffer(raw, dtype=np.int8)
        return signals

    def get_means(self):
        means = {}
        for name, samples in self.get_signals():
            means[name] = samples.mean()
        return means

    def get_sum_squared(self):
        sum_squares = {}
        for name, samples in self.get_signals():
            sum_squares[name] = (samples**2).sum()

        return sum_squares
