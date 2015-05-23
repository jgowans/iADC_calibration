% Author: Hong Chen
% Date: August 5,2010

% read from a datafile and do the fft
% split the two streams, and plot each of them
clear all;

x= dlmread('default_0.txt','\n'); % read from datafile

Fs=1e9; % set the sampling rate

x1=x(1:2:end); % every other sample
x2=x(2:2:end); % every other sample

L1=length(x1);
nfft1=2^nextpow2(L1);
f1=Fs/2*linspace(0,1,nfft1/2+1);
Y1=fft(x1,nfft1)/L1;

L2=length(x2);
nfft2=2^nextpow2(L2);
f2=Fs/2*linspace(0,1,nfft2/2+1);
Y2=fft(x2,nfft2)/L2;

figure(1)
semilogy(f1,2*abs(Y1(1:nfft1/2+1))) % plot the result
graph_title='interleaved adcs with input signal: 93MHz (from ADC 1)';
title(graph_title);
xlabel('Frequency (Hz)');
ylabel('Power');

figure(2)
semilogy(f2,2*abs(Y2(1:nfft2/2+1))) % plot the result
graph_title='interleaved adcs with input signal: 93MHz (from ADC 2)';
title(graph_title);
xlabel('Frequency (Hz)');
ylabel('Power');
