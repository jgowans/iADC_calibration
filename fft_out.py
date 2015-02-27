'''
% Author: Hong Chen
% Date: August 5,2010
'''
import corr
import struct
import time

from numpy import *
from pylab import *


def fft_out(channel):

  x = roach.snapshot_arm("snap64", man_trig=True, man_valid=True, offset=-1, circular_capture=False)
  adc0_data = roach.snapshot_get("snap64", wait_period=-1, arm=False)["data"]
  y = struct.unpack(str(len(adc0_data) ) + "b", (adc0_data))



  

  '''
  i = range(0,size(y))
  print size(y)
  plot(i[0:1024/10],y[0:1024/10])
  show()

  '''
  '''
  plot(y[1:100])
  show()
  '''
  
  # FFT and plot
  # adc freq=1 GHz = 1000 MHz
  Fs = 1000000000 # sampling frequency: 2 GHz
  T = 1.0/Fs  # sample time
  L = 4*(2**16)  # length of sample points
  nfft = L
  if channel==0:
     p = y[0:L:2]
  elif channel==1:
     p = y[1:L:2]
  elif channel==2:
     p = y
     Fs=Fs*2
     T=1.0/Fs
     L=L*2
     nfft=L
  else:
     print 'invalid argument(s)!'
     return
  k = fft(p,nfft)/L
  f = Fs/2*linspace(0.0,1.0,nfft/2+1)



  return 2*abs(k[0:nfft/2+1])
  
  '''
  #print size(f)
  #print size(k)
  semilogy(f,2*abs(k[0:nfft/2+1])) 
  title('interleaved ADCs on roach')
  xlabel('frequency')
  ylabel('magnitude')
  show()
  '''





  # val=roach.read('iadc_controller',128)
