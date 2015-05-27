"""
Has the logic to perform the various calibration routines by reading data
via a Snapshot class and modifying ADC parameters via and IAdc class
"""

import logging
import time

class Calibrator:
    def __init__(self, iadc, snapshot, interleaved=True, logger=logging.getLogger()):
        """ Calibrator is contains logic for calibration routines
        
        iadc -- instance of IAdc which is used for modifying parameters
        snapshot -- instance of Snapshot which has been initialised to the
            same ADC ZDOK as iad has.
        interleaved -- if True, read data interleaved from RF input I.
            If False, read I and Q seperately.
        """
        logging.basicConfig()
        self.logger = logger
        self.iadc = iadc
        self.snapshot = snapshot
        self.interleaved = interleaved

    def run_offset_cal(self):
        """ Performs offset calibration
        """
        if self.interleaved == True:
            self.snapshot.set_mode('inter')
        for channel in ('I', 'Q'):
            if self.interleaved == False:
                self.snapshot.set_mode(channel)  # only bother reading out the core we're keen on if not interleaving
            new_mean = snap.get_means()[channel] # should have a magnitute somewhere between 0 and 4
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

    def run_analogue_gain_cal(self, interleaved=True):
        """Attempts to get the sum of the squared output values to be equal for each channel.
        """
        channel_I_sum = self.snapshot_I.get_sum_squared()
        channel_Q_sum = self.snapshot_Q.get_sum_squared()
        self.logger.info("Before calibration, channel I sum squared: {i}, channel Q sum squared: {q}, difference: {d}".format(
            i = channel_I_sum, q = channel_Q_sum, d = abs(channel_I_sum - channel_Q_sum)))
        # set Q to minimum gain and then increment until approximately equal
        while(channel_I_sum > channel_Q_sum):
            self.iadc.analogue_gain_dec('I')
            channel_I_sum = self.snapshot_I.get_sum_squared()
            if(channel_I_sum > channel_Q_sum):
                self.iadc.analogue_gain_inc('Q')
                channel_Q_sum = self.snapshot_Q.get_sum_squared()
        while(channel_I_sum < channel_Q_sum):
            self.iadc.analogue_gain_inc('I')
            channel_I_sum = self.snapshot_I.get_sum_squared()
            if(channel_I_sum < channel_Q_sum):
                self.iadc.analogue_gain_dec('Q')
                channel_Q_sum = self.snapshot_Q.get_sum_squared()
        # channel_I must now be greater than channel_Q
        before_difference = channel_I_sum - channel_Q_sum
        self.iadc.analogue_gain_inc('Q')
        channel_Q_sum = self.snapshot_Q.get_sum_squared()
        after_difference = abs(channel_Q_sum - channel_I_sum)  # abs just in case it's marginally greater (approx equal)
        if(before_difference < after_difference):  # if going lower was a bad idea...
            self.iadc.analogue_gain_dec('Q')  # ...go back up
        channel_I_sum = self.snapshot_I.get_sum_squared()
        channel_Q_sum = self.snapshot_Q.get_sum_squared()
        self.logger.info("After calibration, channel I sum squared: {i}, channel Q sum squared: {q}, difference: {d}".format(
            i = channel_I_sum, q = channel_Q_sum, d = abs(channel_I_sum - channel_Q_sum)))

