% Interleaved ADC's Simulation
% Backwards - composing signals to imitate effects caused by
% interleaving issues
%
% Author: Hong Chen
% Date: August 5,2010
% including gain, delay, and offset;

clear all;
format long;

% Sampling frequency 
Fs = 2e9; 

% Sample time
T = 1/Fs;                     

% Length of signal
L = (2^16)*8;                    

% Time vector
t = (0:L-1)*T;   
t1 = t(1:2:end);
t2 = t(2:2:end);

% Frequency of Sine Wave
freq = 1e8;

% Create a sine wave of input frequency.
% Default amplitude 1.0
amp = 1.0;
x = sin(2*pi*t*freq)*amp; 

% Noise signal I, at 0Hz, namely, a DC offset
% offset default value 0.0
offset = 0.1;
x1 = 1:L;
for i=1:1:L,
    x1(i)=offset*amp;
end;

% Noise signal II, at the position of the supplementary angle
% amplitude 2 default value is 0.0
freq_supple=Fs/2-freq;
ratio2=0.0;
amp2=ratio2*amp;
x2 = sin(2*pi*t*freq_supple)*amp2;

% Noise signal III, at the highest possible frequency on the plot
% amplitdue 3 default value is 0.0
freq_max=Fs/2;
ratio3=1;
amp3=ratio3*amp;
x3 = sin(2*pi*t*freq_max)*amp3;

% Combine the major signal and the noises
x = x + x1 + x2 + x3;
x_ex_1 = x - x1;
x_ex_2 = x - x2;
x_ex_3 = x - x3;

nfft = 2^nextpow2(L); % Next power of 2 from length of y
y = fft(x,nfft)/L;
f = Fs/2*linspace(0,1,nfft/2+1);
f = f/(1e6)*1.0;

% Plot single-sided amplitude spectrum.
figure(1)
semilogy(f,2*abs(y(1:nfft/2+1))) 
graph_title=strcat('Power Spectrum of a',char(32));
graph_title2=num2str(freq/(1e6)*1.0);
graph_title2=strcat(graph_title2,'MHz Sine Wave, with simulation noises');
title(graph_title); 
xlabel('Frequency (MHz)'); 
ylabel('Power');

% PLOT a small part of raw data
figure(2)
start_point=10000;
len=50;
ind=1:len;
plot(ind,x(start_point:1:start_point+len-1),'-o');
hold on;
zero_line=1:len;
for i=1:len,
    zero_line(i)=0;
end;
plot(ind,zero_line,'-r');
hold on;
plot(ind,x_ex_3(start_point:1:start_point+len-1),'k-o');

% plot each noise
figure(3)
%plot(ind,x1(start_point:1:start_point+len-1),'r');
hold on;
%plot(ind,x2(start_point:1:start_point+len-1),'k');
hold on;
%plot(ind,x3(start_point:1:start_point+len-1),'-o');
plot(x3);