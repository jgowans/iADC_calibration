#!/usr/bin/env python

import corr
import snapshot
import iadc
import calibrator
import logging
import time

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fpga = corr.katcp_wrapper.FpgaClient('localhost')
time.sleep(1)
print(fpga.est_brd_clk())
snap = snapshot.Snapshot(fpga, 0, 'IQ', logger)
iadc = iadc.IAdc(fpga, zdok_n = 0, mode = 'indep', logger=logger)
#iadc.registers.get_from_file('registers')
iadc.write_all_registers()
cal = calibrator.Calibrator(iadc, snap, interleaved=False, logger=logger.getChild('calibrator'))
cal.run_offset_cal()
cal.run_analogue_gain_cal()
iadc.registers.save_to_file('registers')
