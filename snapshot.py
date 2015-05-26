"""
An interface to the snapshot blocks with some data analysis 
functions on the data received
"""

import numpy as np
import logging

class Snapshot:
    def __init__(self, fpga, name, logger=logging.getLogger(__name__)):
        logging.basicConfig()
        self.logger = logger
        self.fpga = fpga
        self.name = name

    def get_signal(self):
        raw = self.fpga.snapshot_get(self.name, man_valid=True, man_trig=True)['data']
        sig = np.frombuffer(raw, dtype=np.int8)
        return sig

    def get_mean(self):
        return (self.get_signal()).mean()

    def get_sum_squared(self):
        sum_squared = 0
        for _ in range(10):
            sum_squared += (self.get_signal()**2).sum()
        return sum_squared
