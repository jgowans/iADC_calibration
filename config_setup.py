'''
  Connect to the ROACH board and run the design
'''
'''
% Author: Hong Chen
% Date: August 5,2010
'''


import corr,time

roach=corr.katcp_wrapper.FpgaClient('localhost',7147)
time.sleep(0.001)   # wait for roach to connect
#roach.progdev('interleaved_adc_64_2010_Jul_06_1446.bof')
