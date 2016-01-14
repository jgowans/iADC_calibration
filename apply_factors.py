#!/usr/bin/env python

import corr
import logging
from colorlog import ColoredFormatter
from iadc import IAdc
import time

if __name__ == '__main__':
    logger = logging.getLogger('main')
    handler = logging.StreamHandler()
    colored_formatter = ColoredFormatter("%(log_color)s%(asctime)s%(levelname)s:%(name)s:%(message)s")
    handler.setFormatter(colored_formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    fpga = corr.katcp_wrapper.FpgaClient('localhost', timeout=10)
    time.sleep(1)
    logger.info("FPGA running at: {f}".format(f = fpga.est_brd_clk()))
    for zdok_n in (0, 1):
        iadc = IAdc(fpga, zdok_n = zdok_n, mode = 'indep', logger=logger.getChild('iadc'))
        iadc.registers.get_from_file('registers_{zdok_n}.json'.format(zdok_n = zdok_n))
        iadc.set_cal_mode('no_cal')
        iadc.write_all_registers()
