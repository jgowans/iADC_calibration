#!/usr/bin/env python

import json
import logging
import iadc_registers_control

class IAdcRegisters(object):
    def __init__(self):
        """
        Initialises the defined registers to 0
        """
        object.__setattr__(self, '_frozen', False)  # this is to define #__setattr__
        self.control = iadc_registers_control.IAdcRegistersControl()
        self.offset_vi = 0
        self.offset_vq = 0
        self.analogue_gain_vi = 0
        self.analogue_gain_vq = 0
        self.gain_compensation_vi = 0
        self.gain_compensation_vq = 0
        self._frozen = True

    def __setattr__(self, name, value):
        """
        This exists to ensure new registers can't be accidentally added.
        It should probably be swapped with a better interface to the registers.
        Dictionary, perhaps?
        """
        if self._frozen == True:
            if hasattr(self, name):
                object.__setattr__(self, name, value)
            else:
                raise TypeError("Cannot add new attribute")
        else:
            object.__setattr__(self, name, value)

    def get_from_file(self, filename):
        """
        Reads a JSON file which was written by #save_to_file
        and sets the registers to those values
        """
        with open(filename) as f:
            registers = json.loads(f.read())
            
        self.control = registers['control_reg']
        self.offset_vi = registers['offset_vi']
        self.offset_vq = registers['offset_vq']
        self.analogue_gain_vi = registers['analogue_gain_vi']
        self.analogue_gain_vq = registers['analogue_gain_vq']
        self.gain_compensation_vi = registers['gain_compensation_vi']
        self.gain_compensation_vq = registers['gain_compensation_vq']

    def save_to_file(self, filename):
        """
        Writes all register names and values to filename in
        the JSON file format
        """
        json_string = json.dumps({
            "control_reg": self.control_reg,
            "offset_vi": self.offset_vi,
            "offset_vq": self.offset_vq,
            "analogue_gain_vi": self.analogue_gain_vi,
            "analogue_gain_vq": self.analogue_gain_vq,
            "gain_compensation_vi": self.gain_compensation_vi,
            "gain_compensation_vq": self.gain_compensation_vq
        }, sort_keys=True, indent=4)

        with open(filename, 'w') as f:
            f.write(json_string)



