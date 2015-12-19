#!/usr/bin/env python

import json
import logging
from iadc_registers_control import IAdcRegistersControl
import os, copy

class IAdcRegisters(object):
    """ Instances of this will look similar to a list where the items are the 
    names of the registers
    """
    def __init__(self):
        self._registers = {}
        self.set_all_to_default()

    def __setitem__(self, name, value):
        if name in self._registers:
            self._registers[name] = value
        else:
            raise TypeError("Cannot add new attribute")

    def __getitem__(self, name):
        return self._registers[name]

    def default_values(self):
        """ Returns a dict mapping register names to their default values.
        The exception is the 'control' which actually maps to an instance of
        an IAdcRegistersControl.
        """
        return {
            'control': IAdcRegistersControl(),
            'offset_vi':                 0,
            'offset_vq':                 0,
            'analogue_gain_vi':          0,
            'analogue_gain_vq':          0,
            'gain_compensation_vi':      0,
            'gain_compensation_vq':      0,
            'drda_vi':                   0,
            'drda_vq':                   0,
            'fisda_q':                   0,
            'isa_i':                   -50, # for AT84AD001B this is recommended. It's different for AT84AD001C
            'isa_q':                   -50,
        }

    def set_all_to_default(self):
        for name, value in self.default_values().items():
            self._registers[name] = value

    def get_from_file(self, filename):
        """
        Reads a JSON file which was written by #save_to_fil and sets the registers to those values
        """
        with open(filename) as f:
            registers = json.loads(f.read())
        for name, value in registers:
            self._registers[name] = value
        # special case: the control register should be an instance of IadcRegistersControl
        control_reg = iadc_registers_control.IAdcRegistersControl()
        control_reg.value = self._registers['control']
        self._registers['control'] = control_reg

    def save_to_file(self, filename):
        """
        Writes all register names and values to filename in the JSON file format
        In order to be thread safe we duplicate the registers attribute.
        """
        # swap the control register object with just a value
        registers_to_write = copy.deepcopy(self._registers)
        registers_to_write['control'] = registers_to_write['control'].value
        json_string = json.dumps(registers_to_write, sort_keys=True, indent=4)
        with open(filename, 'w') as f:
            f.write(json_string)
