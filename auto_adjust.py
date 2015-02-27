'''
  Using e2v Dual 8-bit 1Gsps ADC, AT84AD001B, automatically adjust the register to minimize the offset, gain and delay mismatch
  Should be working on AT84AD001C as well
  Author: Hong Chen
  Date: July 23, 2010
'''

Fs=2e9

execfile('maker.py')
execfile('tester.py')  
execfile('fft_out.py')
execfile('iadc.py')
execfile('analysis_function.py')

execfile('start.py')   # reprogram the bof file
no_calibration()   # set to no calibration mode, so that I'll be able to access the registers and adjust the gain and offset compensation
offset_0('iq')    # set offset to 0 for both channel I and channel Q
gain_0()    # set analog gain to 0 dB (channel I & channel Q)
gc_0() # set gain compensation to 0 dB
test=tester()  # get the 8*(2**16) sample points, main purpose here is to make sure that the program has been compiled successfully
               # if an error message pops out, please re-run this *auto_adjust.py* again.




'''
automatically adjust offset for channel I or channel Q (seperately)

TOL is just an approximate expectation to the final result, when it says 'unseccessful!', the result may still be good
as long as it's not too far away from TOL
# function fft_out(chnl) defined in analysis_function.py
# function offset_inc(channel), offset_dec(channel) defined in iadc.py
related material in datasheet: AT84AD004B,p35   AT84AD001C,p33
'''
def offset_adjust(channel):
    print '\n Start adjusting the offset for channel: '+channel
    if channel=='i':
       chnl=1
    else:
       chnl=0
    Y=fft_out(chnl)  # get 8*(2**16) sample points, and do the fft, then get the absolute values and set them to Y
    

    off_v0=Y[0]   # measure the height(power) of the spike at 0Hz
    print off_v0  # print the current value in the register which controls the offset
    off_v1=off_v0
    TOL=Y.max()/600   # define the tolerance
    print 'TOL '+str(TOL)
    while off_v0>TOL:     # try increasing the offset, see if it can reduce the offset error
       offset_inc(channel)
       Y=fft_out(chnl)
       off_v1=Y[0]
       print 'offset value: '+str(off_v1)
       if off_v1<off_v0:
          off_v0=off_v1
       else:                     # if increase the offset will not improve the performance, restore to the last state
          offset_dec(channel) 
          break
    if off_v0>TOL:       # if the error is still larger than the tolerance
       Y=fft_out(chnl)
       off_v0=Y[0]
       while off_v0>TOL:    # try decreasing the offset, set if it can reduce the offset error
           offset_dec(channel)
           Y=fft_out(chnl)
           off_v1=Y[0]
           print 'offset value '+ str(off_v1)
           if off_v1<off_v0:
             off_v0=off_v1
           else:         # if decrease the offset will not improve the performance, restore it to the last state, which should be the optimal
             offset_inc(channel)
             break
    if off_v0>TOL:    # print the message, showing if we can reduce the offset error to the tolerance, and shows the value off the two registers
       print 'unseccessful! offset_vi: '+str(offset_vi)+'  offset_vq: '+str(offset_vq)+'\n'
    else:
       print 'secessful! offset_vi: '+str(offset_vi)+'  offset_vq: '+str(offset_vq)+'\n'


'''
automatically adjust the gain mismatch between two channels

TOL2 is just an approximate expectation to the final result, when it says 'unseccessful!', the result may still be good
as long as it's not too far away from TOL2
# function amp(x) defined in analysis_function.py
# function gc_inc_loop(n), gc_dec_loop(n) defined in iadc.py
related material in datasheet: AT84AD004B,p35     AT84AD001C,p33
'''
def gain_adjust():
    print '\n start adjusting the gain mismatch...'
    test=tester()
    x1=test[0:size(test)+1:2]    # channel Q
    x2=test[1:size(test)+1:2]    # channel I
    amp1=amp(x1)      # measure the amplitude of the sine wave x1, function amp() defined in "analysis_function.py"
    amp2=amp(x2)      # measure the amplitude of the sine wave x2
    print 'amp1 '+str(amp1)+'     '+'amp2 '+str(amp2)
    TOL2=abs(amp1-amp2)/2000    # define the tolerance
    print 'TOL: '+str(TOL2)
    diff0=amp1-amp2     # calculate the difference of the amplitudes for the two streams 
    while abs(diff0)>TOL2:   # try to reduce the difference till the tolerance
        if diff0<0:                  
           gc_dec_loop(1)
           test=tester()
           diff1=diff_amp_x(test)
           if abs(diff1)<abs(diff0):
              diff0=diff1
           else:
              gc_inc_loop(1)
              break;
        else:
           gc_inc_loop(1)
           test=tester()
           diff1=diff_amp_x(test)
           if abs(diff1)<abs(diff0):
              diff0=diff1
           else:
              gc_dec_loop(1)
              break;
    if abs(diff0)>TOL2:  # output message,  gain difference,  value of the register controls gain compensation
        print 'unseccessful! gain difference: '+str(diff0)+'    gc_v: '+str(gc_v)+'\n'
    else:
        print 'yeah! gain difference: '+str(diff0)+'    gc_v:' +str(gc_v)+'\n'



'''
delay adjustment

TOL is just an approximate expectation to the final result, when it says 'unseccessful!', the result may still be good
as long as it's not too far away from TOL
# function h_interleaving(f,Fs),  h_s(f,position) defined in analysis_function.py
# function fft_out(2) defined in fft_out.py
# function fisda_inc(),fisda_dec() defined in iadc.py
related material in datasheet:  AT84AD004B,p36      AT84AD001C,p34
'''    
def delay_adjust():
    print '\n start adjusting the delay...'
    f=fft_out(2)   # get the result of fft of the sample data
    position=h_interleaving(f,Fs)    # find the position of the spike mainly resulted in interleaving issue
    spike=h_s(f,position)    # measure the height(power) of the spike mainly resulted in interleaving issue
    TOL=f.max()/200     # define the tolerance
    while spike>TOL:
       fisda_inc()    # fisda: Fine Sampling Delay Adjustment(FISDA) on channel Q
       f=fft_out(2)
       spike2=h_s(f,position)
       if spike2>spike:
          fisda_dec()
          break
       else:
          spike=spike2
    while spike>TOL:
       fisda_dec()
       f=fft_out(2)
       spike2=h_s(f,position)
       if spike2>spike:
          fisda_inc()
          break
       else:
          spike=spike2
    if spike>TOL:
       print 'unseccessful! '+str(spike)+'   '+str(f.max())+'     '+'fisda_v(hex):  '+'%x'%fisda_v+'\n'
    else:
       print 'seccessful! '+str(spike)+'  '+str(f.max())+'     '+'fisda_v(hex):  '+'%x'%fisda_v+'\n'





'''
 Using the functions defined above, adjujst the offset for channel i and q, and then adjust the gain mismatch, finnally adjust the delay mismatch
'''
datafile_maker('default1.txt')
offset_adjust('i')
offset_adjust('q')
gain_adjust() 
delay_adjust()
print 'Automatic adjustment completed. Now start capturing data and make a datafile...'

datafile_maker('test1.txt')   # function datafile_maker(filename) defined in maker.py
                              # capture data and put the data into test1.txt
print 'Now datafile test1.txt is ready.'