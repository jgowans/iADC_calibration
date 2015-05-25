'''
 Functions to write to registers of iADC and adjust it
 Author: Hong Chen
 Date: July 23, 2010
'''

import corr
import logging
import json
import iadc_registers

class IAdc:
    def __init__(self, fpga, zdok_n, mode='indep', logger=logging.getLogger()):
        """
        fpga -- corr.katcp_wrapper.FpgaClient instance used to talk to ROACH
        zdok_n -- either 0 or 1. Specifies which ADC card to control
        mode -- How should the I and Q channels be sampled. 
            either: 'indep', 'inter_Q' or'inter_I'. Default: 'indep'
        logger -- instance of a Logger. Default: root logger.
        """
        logging.basicConfig()
        self.logger = logger
        self.zdok_n = zdok_n
        self.fpga = fpga
        corr.iadc.set_mode(self.fpga, mode='SPI')  # enable software control
        self.registers = iadc_registers.IAdcRegisters()
        self.write_control_reg()
        logger.debug("Initialised iADC for software control")

    def read_controller(self):
        """
        Reads the first 128 bytes at the controller address. Why 128? I don't know...
        """
        return self.fpga.read('iadc_controller', 128)

    def write_control_reg(self):
        corr.iadc.spi_write_register(self.fpga, self.zdok_n, 0x00, self.registers.control.value)
        logging.debug("Control register set to: {cr:#06x}".format(cr = self.registers.control.value))

    def reset_dcm(self):
        corr.iadc.rst(self.fpga, self.zdok_n)
        self.logger.info("iADC DCM reset for ZDOKL {n}".format(n = self.zdok_n))

    def set_cal_mode(self, mode):
        """
        Defines the calibration mode of the iADC

        cal_type --
            new_cal: starts a new calibration and applies values
            keep_last_cal: applies the result of the last cal.
            no_cal: removes cal values and allows register modifications
        """
        # just pass it on. Validation is done there.
        self.registers.control.set_cal_mode(mode)
        self.write_control_reg()
        self.logger.info("For ADC {z}, calibration set to: '{c}'".format(z = self.zdok_n, c = mode))

    def set_analogue_selection(self, mode):
        """
        Specifies how the RF channels will be connected to the ADC cores.
        Either independant or one channel interleaved

        mode --
            indep:      InI -> ADCI ; InQ -> ADCQ
            inter_I:    InI -> ADCI ; InI -> ADCQ
            inter_Q:    InQ -> ADCI ; InQ -> ADCQ
        """
        self.registers.control.set_analogue_selection(mode)
        self.write_control_reg()
        self.logger.info("On ADC: {z}, set analogue mode to: {m}".format(z = self.zdok_n, m = mode))

    def set_clock_selection(self, mode):
        """
        Specifies the phase between each core's clock

        mode --
            in:     in phase.
            quad:   quadtrature
            neg:    180 degree phase shift (negative)
        """
        self.registers.control.set_clock_selection(mode)
        self.write_control_reg()
        self.logger.info("On ADC: {z} set clock selection to: {m}".format(z = self.zdok_n, m = mode))

    def offset_inc(self, channel):
        """
        Increases the offset for the channel by 0.25 lsb 

        channel -- 'I' or 'Q'
        Returns True if offset could be increased or False it it's already at maximum
        """
        assert(channel in ('I', 'Q'))
        if ( (channel == 'I' and self.registers.offset_vi >= 31.75) or 
                (channel == 'Q' and self.registers.offset_vq >= 31.75) ):
            self.logger.warn("Offset for channel {c} already at maximum.".format(c = channel))
            return False
        if channel == 'I':
            self.registers.offset_vi += 0.25
        elif channel == 'Q':
            self.registers.offset_vq += 0.25
        corr.iadc.offset_adj(self.fpga, self.zdok_n, self.registers.offset_vi, self.registers.offset_vq)
        # this reall should be moved into the corr.iadc file...
        self.logger.info("For ADC {z}, offset for I: {vi}, offset for Q: {vq}".format(
            z = self.zdok_n, vi = self.registers.offset_vi, vq = self.registers.offset_vq))
        return True

    def offset_dec(self, channel):
        """
        Decreases the offset for the channel by 0.25 lsb

        channel -- 'I' or 'Q'
        Returns True if offset could be decreased of False if it's already at minimum.
        """
        assert(channel in ('I', 'Q'))
        if ( (channel == 'I' and self.offset_vi <= -31.75) or
                (channel == 'Q' and self.offset_vq <= 31.75) ):
            self.logger.warn("Offset for channel {c} already at minimum".format(c = channel))
            return False
        if channel == 'I':
            self.offset_vi -= 0.25
        elif channel == 'Q':
            self.offset_qi -= 0.25
        corr.iadc.offset_adj(self.fpga, self.zdok_n, self.offset_vi, self.offset_vq)
        self.logger.info("For ADC {z}, offset for I: {vi}, offset for Q: {vq}".format(
            z = self.zdok_n, vi = self.offset_vi, vq = self.offset_vq))
        return True

    def offset_set(self, channel, value):
        """
        Sets the offset for the channel to a specific value.
        This is as opposed to the other methods which do a relative inc or dec.

        channel -- 'I' or 'Q'
        value -- Value in LSB from -31.75 to 31.75
        """
        assert(channel in ('I', 'Q'))
        assert( (value <= 31.75) and (value >= -31.75) )
        if channel == 'I':
            self.offset_vi = value
        if channel == 'Q':
            self.offset_vq = value
        corr.iadc.offset_adj(self.fpga, self.zdok_n, self.offset_vi, self.offset_vq)
        self.logger.info("For ADC {z}, offset for I: {vi}, offset for Q: {vq}".format(
            z = self.zdok_n, vi = self.offset_vi, vq = self.offset_vq))


# Note, the ADC must be set to No calibation beofre ghain and offsdrt adjustment can be made

# I don't see the point of these functions.... 
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
drda_q = 4  # this makes the Data Ready Delay Adjust = 0 ps
drda_i = 4
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

'''
Sets ISA to -100 ps which is recommended for DMUX 1:2 usage
ADDR = 100 = 0x04
D[0:2] : channel I (xxx 010 = 0x02)
D[3:5] : channel Q (010 xxx = 0x10)
D[6:15]: 1000 0100 00 = 0x8400
'''
def set_isa():
    print("\nSetting ISA to -100 ps for I and Q\n")
#    roach.blindwrite('iadc_controller','%c%c%c%c'%(0x84, 0x12, 0x04, 0x01),offset=0x4)
    roach.blindwrite('iadc_controller','%c%c%c%c'%(0x84, 0x02, 0x04, 0x01),offset=0x4)
    time.sleep(0.1)

