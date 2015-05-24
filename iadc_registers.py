#!/usr/bin/env python

import json
import logging
import iadc_registers_control

class IAdcRegisters:
    def __init__(self):
        """
        Initialises the defined registers to 0
        """
        self.control = iadc_registers_control.IAdcRegistersControl()
        self.offset_vi = 0
        self.offset_vq = 0
        self.gain_vi = 0
        self.gain_vq = 0

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
        self.gain_vi = registers['gain_vi']
        self.gain_vq = registers['gain_vq']

    def save_to_file(self, filename):
        """
        Writes all register names and values to filename in
        the JSON file format
        """
        json_string = json.dumps({
            "control_reg": self.control_reg,
            "offset_vi": self.offset_vi,
            "offset_vq": self.offset_vq,
            "gain_vi": self.gain_vi,
            "gain_vq": self.gain_vq
        }, sort_keys=True, indent=4)

        with open(filename, 'w') as f:
            f.write(json_string)



