'''
 Functions to write to registers of iADC and adjust it
 Author: Hong Chen
 Date: July 23, 2010
'''

val=roach.read('iadc_controller',128)

'''
  read the original value of iadc_controller
'''
def read_iadc():
    val=roach.read('iadc_controller',128)
    return val


'''
   #first thing to do
'''
def start_test():
    print '\n'
    print 'Starting the test...'
    roach.blindwrite('iadc_controller','%c%c%c%c'%(0x0,0x0,0x03,0x0))
    time.sleep(0.001)
    print 'You can write to the registers now.'
    return read_iadc()




'''
   # reset the DCM
'''
def reset_dcm():
    #print 'resetting the dcm...'
    roach.blindwrite('iadc_controller','%c%c%c%c'%(0x0,0x0,0x03,0x03))
    time.sleep(0.001)
    #print 'resetting dcm completed'
    return read_iadc()



'''
start a new calibration phase
Old DATA =0110 0100 0110 1100
DATA =X X X X 1 1 0 X X X X X X X X X = 0110 1100 0110 1100 = 0x6c, 0x6c   
ADDR =000
'''
def new_cal():
   print '\n'
   print 'starting a new calibration phase...'
   roach.blindwrite('iadc_controller','%c%c%c%c'%(0x6c,0x6c,0x0,0x1),offset=0x4)   
   time.sleep(0.001) # probably unnecessary wait for delay to take
   reset_dcm()
   print 'new calibration phase completed.'
   return read_iadc()


'''
set to no calibration mode
so that gain compensation and offset compensation can be done
'''
def no_calibration():
   print '\n'
   print 'setting to no calibration mode...'
   roach.blindwrite('iadc_controller','%c%c%c%c'%(0x60,0x6c,0x0,0x01),offset=0x4)
   time.sleep(0.001) # probably unnecessary wait for delay to take
   reset_dcm()
   print 'no calibration mode setting completed.'
   return read_iadc()



'''
   #intput_i
   analog input channel selection: analog I-i/q
   xxxx|xx0x|xx10|xxxx    =0x00,0x20 (adc0_data)
 #or = 0110 0100 0110 1100 =  0x64, 0x6c
     
'''
def input_i():   
   print '\n'
   print 'selecting input channel I...'
   roach.blindwrite('iadc_controller','%c%c%c%c'%(0x64,0x6c,0x0,0x1),offset=0x4)   
   time.sleep(0.001) # probably unnecessary wait for delay to take
   reset_dcm()
   print 'Input channel: I-> ADC I&Q'
   return read_iadc()


'''
   #intput_q
   analog input channel selection: analog Q-i/q
   xxxx|xx0x|xx0x|xxxx    =0x00,0x20 (adc0_data)
 #or = 0110 0100 0100 1100 =  0x64, 0x4c  
'''
def input_q():
   print '\n'
   print 'selecting input channel Q...'
   roach.blindwrite('iadc_controller','%c%c%c%c'%(0x64,0x4c,0x0,0x1),offset=0x4)   
   time.sleep(0.001) # probably unnecessary wait for delay to take
   reset_dcm()
   print 'Input channel:Q-> ADC I&Q'
   return read_iadc()



'''
   # input_iq
   analog input channel selection: analog I-i, Q-q
   xxxx|xx0x|xx11|xxxx 
   0110 0100 0111 1100 = 0x64,0x7c
'''
def input_iq():
   print '\n'
   print 'selecting input channel: I & Q ...'
   roach.blindwrite('iadc_controller','%c%c%c%c'%(0x64,0x7c,0x0,0x1),offset=0x4)  
   time.sleep(0.001) # probably unnecessary wait for delay to take
   reset_dcm()
   print 'Input channel: I-> ADC I;   Q-> ADC Q'
   return read_iadc()   


# default offset value = 00000000b = 0x00 = 0LSB
# i channel and q channel
offset_vi=0x00
offset_vq=0x00


'''
   # offset compensation 
   #step 1 * 0.25LSB
   address 010 = 0x02
   DATA7 to DATA0: channel I
   DATA15 to DATA8: channel Q
   code 11111111b=0xff = 31.75LSB
   code 10000000b=00000000b= 0x80=0x00= 0LSB
   code 01111111b=0x7f= -31.75LSB
   # code 10000001b=0x81 = 1LSB
'''
def offset_inc(channel):
    global offset_vi
    global offset_vq
    v=offset_vi
    v2=offset_vq
    if v>=128:
       v=v+1
    elif v==0:
       v=129
    else:
       v=v-1
    if v2>=128:
       v2=v2+1
    elif v2==0:
       v2=129
    else:
       v2=v2-1
    if channel=='i':
       offset_vi=v
    elif channel=='q':
       offset_vq=v2
    elif channel=='iq' or channel=='qi':
       offset_vi=v
       offset_vq=v2
    else:
       print 'invalid argument!'  
       return
    roach.blindwrite('iadc_controller','%c%c%c%c'%(offset_vq,offset_vi,0x02,0x01),offset=0x4)
    time.sleep(0.001) # probably unnecessary wait for delay to take
    return read_iadc()


'''
   # offset compensation 
   #step -1 * 0.25LSB
   address 010 = 0x02
   DATA7 to DATA0: channel I
   DATA15 to DATA8: channel Q
   code 11111111b=0xff = 31.75LSB
   code 10000000b=00000000b= 0x80=0x00= 0LSB
   code 01111111b=0x7f= -31.75LSB
   # code 00000001b=0x01 = -1LSB
'''
def offset_dec(channel):
    global offset_vi
    global offset_vq
    v=offset_vi
    v2=offset_vq
    if v==128:
       v=1
    elif v==0:
       v=1
    elif v<128:
       v=v+1
    else:
       v=v-1
    if v2==128:
       v2=1
    elif v2==0:
       v2=1
    elif v2<128:
       v2=v2+1
    else:
       v2=v2-1
    if channel=='i':
       offset_vi=v
    elif channel=='q':
       offset_vq=v2
    elif channel=='iq' or channel=='qi':
       offset_vi=v
       offset_vq=v2
    else:
       print 'invalid argument!'  
       return
    roach.blindwrite('iadc_controller','%c%c%c%c'%(offset_vq,offset_vi,0x02,0x01),offset=0x4)
    time.sleep(0.001) # probably unnecessary wait for delay to take
    reset_dcm()
    return read_iadc()



'''
   # offset compensation 
   #step -1 * 0.25LSB
   address 010 = 0x02
   DATA7 to DATA0: channel I
   DATA15 to DATA8: channel Q
   code 11111111b=0xff = 31.75LSB
   code 10000000b=00000000b= 0x80=0x00= 0LSB
   code 01111111b=0x7f= -31.75LSB
   # code 00000000b=0x00 = 0LSB
'''
def offset_0(channel):
    print '\n'
    print 'setting the offset to 0 for channel: '+channel
    global offset_vi
    global offset_vq
    if channel=='i':
       offset_vi=0
    elif channel=='q':
       offset_vq=0
    elif channel=='iq' or channel=='qi':
       offset_vi=0
       offset_vq=0
    roach.blindwrite('iadc_controller','%c%c%c%c'%(offset_vi,offset_vq,0x02,0x01),offset=0x4)
    time.sleep(0.001) # probably unnecessary wait for delay to take
    reset_dcm()
    print 'setting completed. channel '+channel+': offset 0'
    return read_iadc()


'''
 # offset compensation inc loop
'''
def offset_inc_loop(channel,n):
    for i in range(0,n):
        offset_inc(channel)
    return read_iadc()


'''
 # offset compensation dec loop
'''
def offset_dec_loop(channel,n):
    for i in range(0,n):
        offset_dec(channel)
    return read_iadc()









'''
   # offset compensation 
   #step -1 * 0.25LSB
   address 010 = 0x02
   DATA7 to DATA0: channel I
   DATA15 to DATA8: channel Q
   code 11111111b=0xff = 31.75LSB
   code 10000000b=00000000b= 0x80=0x00= 0LSB
   code 01111111b=0x7f= -31.75LSB
   # code 11111111b=0xff = 31.75LSB
'''
def offset_max():
    global offset_vi,offset_vq
    print '\n'
    print 'setting offset to maximum value...'
    roach.blindwrite('iadc_controller','%c%c%c%c'%(0xff,0xff,0x02,0x01),offset=0x4)
    time.sleep(0.001) # probably unnecessary wait for delay to take
    reset_dcm()
    offset_vi=0xff
    offset_vq=0xff 
    print 'setting completed. Offset: 31.75LSB(maximum)'
    return read_iadc()

'''
   # offset compensation 
   #step -1 * 0.25LSB
   address 010 = 0x02
   DATA7 to DATA0: channel I
   DATA15 to DATA8: channel Q
   code 11111111b=0xff = 31.75LSB
   code 10000000b=00000000b= 0x80=0x00= 0LSB
   code 01111111b=0x7f= -31.75LSB
   # code 01111111b=0xff = -31.75LSB
'''
def offset_min():
    print '\n'
    print 'setting the offset to minimum value...'
    global offset_vi,offset_vq
    roach.blindwrite('iadc_controller','%c%c%c%c'%(0x7f,0x7f,0x02,0x01),offset=0x4)
    time.sleep(0.001) # probably unnecessary wait for delay to take
    reset_dcm()
    offset_vi=0x7f
    offset_vq=0x7f
    print 'setting completed.  Offset: -31.75LSB(minimum)'
    return read_iadc()




gain_vi=0x80
gain_vq=0x80
'''
   # analog gain adjustment
   # gain set to minimum = -1.5dB
   # address = 001 = 0x01
   DATA7 to DATA0: channel I
   DATA15 to DATA8: channel Q
   code 00000000=0x00= -1.5dB
   code 10000000 = 0x80 = 0dB
   code 11111111=0xff = 1.5dB
'''
def gain_min():
   print '\n'
   print 'setting the gain to minimum value...'
   global gain_vi,gain_vq
   roach.blindwrite('iadc_controller','%c%c%c%c'%(0x00,0x00,0x01,0x1),offset=0x4)
   time.sleep(0.001) # probably unnecessary wait for delay to take
   reset_dcm()
   gain_vi=0x00
   gain_vq=0x00
   print 'setting completed. Gain: -1.5dB(minimum)'
   return read_iadc()


'''
  # analog gain adjustment
   # gain set to 0dB
   # address = 001 = 0x01
   DATA7 to DATA0: channel I
   DATA15 to DATA8: channel Q
   code 00000000=0x00= -1.5dB
   code 10000000 = 0x80 = 0dB
   code 11111111=0xff = 1.5dB
'''
def gain_0():
   print '\n'
   print 'setting the gain to 0dB...'
   global gain_vi,gain_vq
   roach.blindwrite('iadc_controller','%c%c%c%c'%(0x80,0x80,0x01,0x1),offset=0x4)
   time.sleep(0.001) # probably unnecessary wait for delay to take
   reset_dcm()
   gain_vi=0x80
   gain_vq=0x80
   print 'setting completed. Gain: 0dB'
   return read_iadc()




'''
   # analog gain adjustment
   #gain set to max=1.5dB   
   # step -1*0.011 dB
   # address = 001 = 0x01
   DATA7 to DATA0: channel I
   DATA15 to DATA8: channel Q
   code 00000000=0x00= -1.5dB
   code 10000000 = 0x80 = 0dB
   code 11111111=0xff = 1.5dB
   # code 01111111 = 0x7f = -0.001dB
'''
def gain_max():
     print '\n'
     print 'setting the gain to maximum value...'
     global gain_vi,gain_vq
     roach.blindwrite('iadc_controller','%c%c%c%c'%(0xff,0xff,0x01,0x1),offset=0x4)
     time.sleep(0.001) # probably unnecessary wait for delay to take
     reset_dcm()
     gain_vi=0xff
     gain_vq=0xff
     print 'setting completed. Gain: 1.5dB(maximum)'
     return read_iadc()






'''
analog gain adjustment on channel i
'''
def gain_inc_loop_i(n):
   global gain_vi,gain_vq
   v=gain_vi
   if (n+v>255):
     return 'too big!'
   result=arange(0,n,1)
   for i in range(0,n):
       v=v+1
       roach.blindwrite('iadc_controller','%c%c%c%c'%(gain_vq,v,0x01,0x1),offset=0x4)
       time.sleep(0.001) # probably unnecessary wait for delay to take
       reset_dcm()
   gain_vi=v
   return read_iadc()




gc_v=0x00
'''
Gain Compensation adjustment
Gain compensation

NOTE:  ONLY 7 BITS,  THE EXAMPLE GIVEN IN THE DATASHEET IS NOT REALLY CORRECT

Data6 to Data0: channel I/Q (Q is matched to I for interleaving adjustment)
Code 11111111b: ?.315 dB
Code 10000000b: 0 dB
Code 0000000b: 0 dB
Code 0111111b: 0.315 dB
Steps: 0.005 dB
Data6: sign bit
Data15 to Data7 = XXX
'''


'''
increase gain compensation by 1
'''
def gc_inc():
    global gc_v
    v=gc_v
    if v==64:
       v=1
    elif v>64:
       v=v-1
    elif v==63:
       print 'maximum reached!'
       return
    else:
       v=v+1
    roach.blindwrite('iadc_controller','%c%c%c%c'%(v,v,0x03,0x01),offset=0x4)
    time.sleep(0.001) # probably unnecessary wait for delay to take
    reset_dcm()
    gc_v=v
    return read_iadc()



'''
decrease gain compensation by 1
'''
def gc_dec():
    global gc_v
    v=gc_v
    if v==0:
       v=65
    elif v>=64:
       v=v+1
    elif v==127:
       print 'minimum reached!'
       return
    else:
       v=v-1
    roach.blindwrite('iadc_controller','%c%c%c%c'%(v,v,0x03,0x01),offset=0x4)
    time.sleep(0.001) # probably unnecessary wait for delay to take
    reset_dcm()
    gc_v=v
    return read_iadc()

'''
gain compensation adjustment, using gc_inc(), loop
'''
def gc_inc_loop(n):
    for i in range(0,n):
       gc_inc()


'''
gain compensation adjustment, using gc_dec(), loop
'''
def gc_dec_loop(n):
    for i in range(0,n):
       gc_dec()




'''
gain compensation to minimum  11111111 =0xff,  -0.315db
'''
def gc_min():
     print '\n'
     print 'setting the gain compensation to minimum value...'
     global gc_v
     roach.blindwrite('iadc_controller','%c%c%c%c'%(0xff,0xff,0x03,0x01),offset=0x4)
     time.sleep(0.001) # probably unnecessary wait for delay to take
     reset_dcm()
     gc_v=0xff
     print 'setting completed. Gain compensation: -0.315dB(minimum)'
     return read_iadc()


'''
gain compensation to maximum  01111111 =0x7f,  0.315db
REAL VALUE SHOULD BE          00111111 =0x3f,  0.315db
'''
def gc_max():
     print '\n'
     print 'setting the gain compensation to maximum value...'
     global gc_v
     roach.blindwrite('iadc_controller','%c%c%c%c'%(0x3f,0x3f,0x03,0x01),offset=0x4)
     time.sleep(0.001) # probably unnecessary wait for delay to take
     reset_dcm()
     gc_v=0x7f
     print 'setting completed. Gain compensation: 0.315dB'
     return read_iadc()

'''
gain compensation to 0  00000000 = 0x00, 0db
'''
def gc_0():
     print '\n'
     print 'setting the gain compensation to 0...'
     global gc_v
     roach.blindwrite('iadc_controller','%c%c%c%c'%(0x00,0x00,0x03,0x01),offset=0x4)
     time.sleep(0.001) # probably unnecessary wait for delay to take
     reset_dcm()
     gc_v=0x0
     print 'setting completed. Gain compensation: 0dB'
     return read_iadc()


   


fisda_v=0   # default value
'''
adjust the fine sampling data adjustment (FISDA) on channel Q
ADDR = 111 = 0x07
DATA10 to DATA6
'''
def fisda_inc():
    global fisda_v,drda_i,drda_q
    if fisda_v==0xf:
       print 'maximum reached!'
       return
    elif fisda_v==16:
       fisda_v=1
    elif fisda_v>16:
       fisda_v=fisda_v-1
    else:
       fisda_v=fisda_v+1
    b=((fisda_v&0x3)<<6)+(drda_q<<3)+drda_i     # marks out the lowest 2 bits in fisda_v, together with drda_q & drda_i, DATA7 to DATA0
    a=fisda_v>>2
    roach.blindwrite('iadc_controller','%c%c%c%c'%(a,b,0x07,0x01),offset=0x4)
    time.sleep(0.001) # probably unnecessary wait for delay to take
    reset_dcm()
    return read_iadc()


'''
adjust the fine sampling data adjustment (FISDA) on channel Q
ADDR = 111 = 0x07
DATA10 to DATA6
'''
def fisda_dec():
    global fisda_v,drda_i,drda_q
    if fisda_v==0x18:
       print 'minimum reached!'
       return
    elif fisda_v==0:
       fisda_v=0x11  # assume 11111 is the minimum, -60 ps,  so 10001 should be -4 ps
    elif fisda_v>16:
       fisda_v=fisda_v+1
    else:
       fisda_v=fisda_v-1
    b=((fisda_v&0x3)<<6)+(drda_q<<3)+drda_i     # marks out the lowest 2 bits in fisda_v, together with drda_q & drda_i, DATA7 to DATA0
    a=fisda_v>>2
    ##print '%x %x'%(a,b)
    roach.blindwrite('iadc_controller','%c%c%c%c'%(a,b,0x07,0x01),offset=0x4)
    time.sleep(0.001) # probably unnecessary wait for delay to take
    reset_dcm()
    return read_iadc()


'''
adjust the fine sampling data adjustment (FISDA) on channel Q
ADDR = 111 = 0x07
DATA10 to DATA6
loop using fisda_inc()
'''
def fisda_inc_loop(n):
    for i in range(0,n):
        fisda_inc()
    return read_iadc()


'''
adjust the fine sampling data adjustment (FISDA) on channel Q
ADDR = 111 = 0x07
DATA10 to DATA6
loop using fisda_dec()
'''
def fisda_dec_loop(n):
    for i in range(0,n):
        fisda_dec()
    return read_iadc()