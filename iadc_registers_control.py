
"""
An interface to the main iADC control register. The one at address 0.

Contains some methods for modifying the parameters of this register
"""

class IAdcRegistersControl:
    def __init__(self, analogue_selection='indep', clock_selection='in', cal_mode='no_cal', clk_speed=800):
        """
        analogue_selection -- 'indep', 'inter_I' or 'inter_Q'. See #set_analogue_selection.
        clock_selection -- 'in', 'quad' or 'neg'. See #set_clock_selection
        cal_mode -- 'no_cal', 'new_cal', or 'keep_last_cal'.
        clk_speed -- clock speed in MHz
        """
        self.value = 0
        self.value |= (0b1 << 2)  # disable chip version output bit
        self.value |= (0b1 << 3)  # set demux to 1:2
        clk_bits = 0b00 if (clk_speed<125) else 0b01 if (clk_speed<250) else 0b10 if (clk_speed<500) else 0b11
        self.value |= (clk_bits << 12)  # control wait bit calibration value is dependent on clk speed
        self.value |= (1 << 14)  # set FDataReady to Fs/2. I don't know what this means
        self.set_analogue_selection(analogue_selection)
        self.set_clock_selection(clock_selection)
        self.set_cal_mode(cal_mode)

    def set_analogue_selection(self, mode):
        """
        Specifies how the RF channels will be connected to the ADC cores.
        Either independant or one channel interleaved

        mode --
            indep:      InI -> ADCI ; InQ -> ADCQ
            inter_I:    InI -> ADCI ; InI -> ADCQ
            inter_Q:    InQ -> ADCI ; InQ -> ADCQ
        """
        bits_map = {'inter_Q': 0b00, 'inter_I': 0b10, 'indep': 0b11}
        self.value &= ~(0b11 << 4)
        self.value |= (bits_map[mode] << 4)

    def set_clock_selection(self, mode):
        """
        Specifies the phase between each core's clock

        mode --
            in:     in phase.
            quad:   quadtrature
            neg:    180 degree phase shift (negative)
        """
        bit_map = {'neg': 0b00, 'in': 0b10, 'quad': 0b11}
        self.value &= ~(0b11 << 6)  # clear bits 7 downto 6
        self.value |= (bit_map[mode] << 6) 

    def set_cal_mode(self, mode):
        """
        Set to no_cal to be able to modify the XXXX registers manually

        cal -- 'no_cal', 'new_cal' or 'keep_last_cal'
        """
        bits_map = {'no_cal': 0b00, 'keep_last_cal': 0b01, 'new_cal': 0b11}
        # clear bits 10 and 11
        self.value &= ~(0b11 << 10)
        # set bits as per specification
        self.value |= (bits_map[mode] << 10)
