'''
% Author: Hong Chen
% Date: August 5,2010
'''

import corr
import struct
import time

from numpy import *
from pylab import *





'''
    Trigger the snap64 block and capture 
    data, then read it and get (2**16) 
    64-bit unsigned numbers. Each of the 
    unsigned numbers is concatnated by 8 
    8-bit unsigned numbers. We need to 
    split each long number and get the 
    original data.
    After the 8*(2**16) 8-bit signed number 
    is recovered, write it to a file using 
    argument 'name' as file name.
'''
def datafile_maker(name):

  y = get_snap()

  # write to file
  datafile=open(name,'w')
  for i in range(0,size(y)):
     datafile.write(str(y[i])+'\n')
  datafile.close()
  
  

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
  '''
  # FFT and plot
  # adc freq=0.8 GHz = 800 MHz
  Fs = 1600000000 # sampling frequency: 1.6 GHz
  T = 1.0/Fs  # sample time
  L = 8*(2**16)  # length of sample points
  nfft = L
  k = fft(y,nfft)/L
  f = Fs/2*linspace(0.0,1.0,nfft/2+1)

  #print size(f)
  #print size(k)
  semilogy(f,2*abs(k[0:nfft/2+1])) 
  title('interleaved ADCs on roach')
  xlabel('frequency')
  ylabel('magnitude')
  show()

  '''



  # val=roach.read('iadc_controller',128)
