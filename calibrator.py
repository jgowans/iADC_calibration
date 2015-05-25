"""
Has the logic to perform the various calibration routines by reading data
via a Snapshot class and modifying ADC parameters via and IAdc class
"""

import logging
import time

class Calibrator:
    def __init__(self, iadc, snapshot_I, snapshot_Q, logger=logging.getLogger()):
        """
        snapshot_X -- instance of Snapshot which is used for getting data
            from ADC channel X
        iadc -- instance of IAdc which is used for modifying parameters
        """
        logging.basicConfig()
        self.logger = logger
        self.snapshot_I = snapshot_I
        self.snapshot_Q = snapshot_Q
        self.iadc = iadc

    def run_offset_cal(self):
        """
        Performs offset calibration
        """
        for channel in ('I', 'Q'):
            snap = getattr(self, "snapshot_{x}".format(x = channel))
            new_mean = snap.get_mean() # should have a magnitute somewhere between 0 and 4
            self.logger.info("Before clibration, offset = {o} for channel {c}".format(c = channel, o = new_mean))
            if(new_mean > 0):  # we want to decrease the offset
                while(new_mean > 0):
                    assert(self.iadc.offset_dec(channel) == True) # should never hit bottom
                    last_mean = new_mean
                    time.sleep(0.5)  # some time for the change to 'apply'
                    new_mean = snap.get_mean()
                    assert(new_mean < last_mean)
                # fix if we have gone too far
                if(abs(new_mean) > abs(last_mean)):
                   self.iadc.offset_inc(channel)
            elif(new_mean < 0):  # we want to increase the offset
                while(new_mean < 0):
                    assert(self.iadc.offset_inc(channel) == True)
                    last_mean = new_mean
                    time.sleep(0.5)
                    new_mean = snap.get_mean()
                if(abs(new_mean) > abs(last_mean)):
                   self.iadc.offset_dec(channel)
            time.sleep(0.5)
            new_mean = snap.get_mean()
            self.logger.info("After clibration, offset = {o} for channel {c}".format(c = channel, o = new_mean))
