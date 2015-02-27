% read from a datafile and do the fft, then plot it
%
% Author: Hong Chen
% Date: August 5,2010

clear all;

x= dlmread('filename.txt','\n'); % read from datafile

Fs=2e9; % set the sampling rate

L=length(x);
nfft=2^nextpow2(L);
f=Fs/2*linspace(0,1,nfft/2+1);
Y3=fft(x,nfft)/L;

semilogy(f,2*abs(Y3(1:nfft/2+1))) % plot the result
graph_title='interleaved adcs with input signal: 93MHz (test1)';
title(graph_title);
xlabel('Frequency (Hz)');
ylabel('Power');


