#!/usr/bin/env python

import iadc
import calibrator
from adc_data_wrapper import AdcDataWrapper
import logging
from colorlog import ColoredFormatter
import time
from directionFinder_backend.correlator import Correlator

ZDOK_N = 0


if __name__ == '__main__':
    logger = logging.getLogger('maiin')
    handler = logging.StreamHandler()
    colored_formatter = ColoredFormatter("%(log_color)s%(asctime)s%(levelname)s:%(name)s:%(message)s")
    handler.setFormatter(colored_formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    correlator = Correlator()
    logger.info("FPGA running at: {f} MHz".format(f = correlator.fpga.est_brd_clk()))
    adr = AdcDataWrapper(correlator, logger = logger.getChild('adr'))
    adr.resample()
    print(adr.get_offset('0I'))
    print(adr.get_offset('0Q'))
    print(adr.get_phase_difference('0I', '0Q'))
    exit()
    iadc = iadc.IAdc(fpga, zdok_n = ZDOK_N, mode = 'indep', logger=logger.getChild('iadc'))
    #iadc.registers.get_from_file('registers')
    iadc.write_all_registers()
    cal = calibrator.Calibrator(iadc, correlator, interleaved=False, logger=logger.getChild('calibrator'))
    cal.run_offset_cal()
    cal.run_analogue_gain_cal()
    iadc.registers.save_to_file('registers')
