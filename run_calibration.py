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
snap_I = snapshot.Snapshot(fpga, 'snapshot', logger)
snap_Q = snapshot.Snapshot(fpga, 'snapshot1', logger)
iadc = iadc.IAdc(fpga, zdok_n = 0, mode = 'indep', logger=logger)
iadc.write_all_registers()
cal = calibrator.Calibrator(iadc, snap_I, snap_Q, logger)
cal.run_offset_cal()
cal.run_analogue_gain_cal()
