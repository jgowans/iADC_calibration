'''
   functions to deal with data
'''
'''
% Author: Hong Chen
% Date: August 5,2010
'''
import corr,pylab,numpy,struct



'''
input: stream x which represents a sine wave
output: the amplitude of the sine wave

calculate the amplitude of x
using the RMS = amp/sqrt(2)
'''
def amp(x):
    rms=0
    for i in range(0,size(x)):
       rms=rms+x[i]*x[i]
    rms=rms/size(x)
    rms=sqrt(rms)
    amp=rms*sqrt(2)
    return amp




'''
input: two stream x1 and x2, each of them represents a sine wave
output: the difference of the amplitudes of x1 and x2

take in two streams of data, caculate their amplitudes seperately, and get the difference between the two amplitudes
'''
def diff_amp(x1,x2):
    a1=amp(x1)
    a2=amp(x2)
    print 'amp1 '+str(a1)+'     '+'amp2 '+str(a2)
    return a1-a2




'''
input: a stream x
output: the difference of the amplitudes of x1 and x2, where x1 and x2 are from x (every other sample)
'''
def diff_amp_x(x):
    x1=x[0:size(x)+1:2]
    x2=x[1:size(x)+1:2]
    return diff_amp(x1,x2)





'''
input: a stream x, the smapling rate
output: the frequency of x
'''
def tone_freq(data, fs):
    data_len = data.size
    fft_data = numpy.fft.fft(data)
    fft_abs = numpy.abs(fft_data[0:data_len/2]);
    max_pos = numpy.where(fft_abs == fft_abs.max())[0][0]
    return float(max_pos)*float(fs)/float(data_len)




'''
input: a stream f which is the result of fft of a sine wave, the smapling rate
output: the frequency of x
'''
def get_freq(f, fs):
    data_len = size(f)*2
    max_pos = numpy.where(f == f.max())[0][0]
    return float(max_pos)*float(fs)/float(data_len)





'''
input: a stream f which is the result of fft of a sine wave, the sampling frequency Fs
output: the height of spike resulted in interleaving
'''
def h_interleaving(f,Fs):
    freq=get_freq(f,Fs)
    ind=int((Fs/2-freq)*size(f)/(Fs/2))
    print 'ind '+str(ind)+'    '+str(size(f))+'     freq: '+str(freq)+'    Fs:'+str(Fs)
    print ind*1.0/size(f), ((Fs/2)-freq)/(Fs/2)
    start=ind-50
    if start<0:
       start=0
    end=ind+50
    if end>size(f):
       end=size(f)
    spike=f.max()/100
    position=-1
    for i in range(start,end):
        if f[i]>spike:
           spike=f[i]
           position=i
    print 'spike: '+str(spike)+'    position: '+str(position)
    return position
    



'''
find the height of spike which is resulted in interleaving issue
'''
def h_s(f,position):
    spike=f[position]
    print 'spike: '+str(spike)+'    position: '+str(position)
    return spike