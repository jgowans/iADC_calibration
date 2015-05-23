SNAPBLOCK_NAME = 'snap64'
SNAPBLOCK_TYPE = 'bram' # bram or dram
#SNAPBLOCK_NAME = 'snapshot'
#SNAPBLOCK_TYPE = 'dram' # bram or dram
SNAPBLOCK_LENGTH = 8*2**19 # only relevant for DRAM. The BRAM length is ascertained from fabric.

import struct
import time

def get_snap():
  roach.snapshot_arm(SNAPBLOCK_NAME, man_trig=True, man_valid=True, offset=-1, circular_capture=False)
  if SNAPBLOCK_TYPE == 'bram':
    adc_data = roach.snapshot_get(SNAPBLOCK_NAME, wait_period=-1, arm=False)["data"]
  else:
    time.sleep(0.1)
    adc_data = roach.read_dram(SNAPBLOCK_LENGTH)
  return  struct.unpack(str(len(adc_data) ) + "b", (adc_data))
