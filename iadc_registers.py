#!/usr/bin/env python

import json
import logging
import iadc_registers_control
import os

class IAdcRegisters(object):
    def __init__(self):
        """
        Initialises the defined registers to 0
        """
        object.__setattr__(self, '_frozen', False)  # this is to define #__setattr__
        self.control = iadc_registers_control.IAdcRegistersControl('indep', 'in', 'no_cal')
        self.offset_vi = 0
        self.offset_vq = 0
        self.analogue_gain_vi = 0
        self.analogue_gain_vq = 0
        self.gain_compensation_vi = 0
        self.gain_compensation_vq = 0
        self.drda_vi = 0
        self.drda_vq = 0
        self.fisda_q = 0
        self.isa_i = -50  # for AT84AD001B this is recommended. It's different for AT84AD001C
        self.isa_q = -50
        self._frozen = True  # prevents accidentally adding new attributes.

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
        if os.path.isfile(filename) == True:
            with open(filename) as f:
                registers = json.loads(f.read())
                
            self.control.value = registers.get('control', iadc_registers_control.IAdcRegistersControl().value)
            self.offset_vi = registers.get('offset_vi', 0)
            self.offset_vq = registers.get('offset_vq', 0)
            self.analogue_gain_vi = registers.get('analogue_gain_vi', 0)
            self.analogue_gain_vq = registers.get('analogue_gain_vq', 0)
            self.gain_compensation_vi = registers.get('gain_compensation_vi', 0)
            self.gain_compensation_vq = registers.get('gain_compensation_vq', 0)

    def save_to_file(self, filename):
        """
        Writes all register names and values to filename in
        the JSON file format
        """
        json_string = json.dumps({
            "control": self.control.value,
            "offset_vi": self.offset_vi,
            "offset_vq": self.offset_vq,
            "analogue_gain_vi": self.analogue_gain_vi,
            "analogue_gain_vq": self.analogue_gain_vq,
            "gain_compensation_vi": self.gain_compensation_vi,
            "gain_compensation_vq": self.gain_compensation_vq
        }, sort_keys=True, indent=4)

        with open(filename, 'w') as f:
            f.write(json_string)



