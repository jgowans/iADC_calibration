#!/usr/bin/env python

import corr
import iadc
import calibrator
from adc_data_wrapper import AdcDataWrapper
import logging
from colorlog import ColoredFormatter
import time
from directionFinder_backend.correlator import Correlator

ZDOK_N = 1


if __name__ == '__main__':
    logger = logging.getLogger('main')
    handler = logging.StreamHandler()
    colored_formatter = ColoredFormatter("%(log_color)s%(asctime)s%(levelname)s:%(name)s:%(message)s")
    handler.setFormatter(colored_formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    correlator = Correlator()
    fpga = correlator.fpga  # steal its fpga...
    logger.info("FPGA running at: {f} MHz".format(f = correlator.fpga.est_brd_clk()))
    adr = AdcDataWrapper(correlator, ZDOK_N, logger = logger.getChild('adr'))
    adr.resample()
    iadc = iadc.IAdc(fpga, zdok_n = ZDOK_N, mode = 'indep', logger=logger.getChild('iadc'))
    iadc.registers.get_from_file('registers_{zdok_n}.json'.format(zdok_n = ZDOK_N))
    iadc.write_all_registers()
    iadc.set_cal_mode('no_cal')
    time.sleep(0.5)
    cal = calibrator.Calibrator(iadc, adr, interleaved=False, logger=logger.getChild('calibrator'))
    cal.run_offset_cal()
    #cal.run_phase_difference_cal()
    #cal.run_analogue_gain_cal()
    iadc.registers.save_to_file('registers_{zdok_n}.json'.format(zdok_n = ZDOK_N))
