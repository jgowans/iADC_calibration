#!/usr/bin/env python

import corr
import numpy as np
import matplotlib.pyplot as plt
import time

FS = 800 # sample freq, MHz

fpga = corr.katcp_wrapper.FpgaClient('localhost')
time.sleep(1)
raw = fpga.snapshot_get('snap64', man_trig=True)['data']

signal = np.frombuffer(raw, dtype=np.int8)
fft = np.fft.rfft(signal)
fft_ax = np.linspace(0, FS/2, len(fft))
plt.plot(fft_ax, np.abs(fft))
plt.title('Spectrum of signal at interleaved iADCs')
plt.xlabel('Frequency (MHz)')
plt.ylabel('Linear power')
plt.show()

