% Interleaved ADC mismatches simulation
% including gain, delay, and offset;
%
% Author: Hong Chen
% Date: August 5,2010

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

% delay
% default = 0.0
delay=0.05;
t2=t2+delay*(1/Fs);

% gain
% default= 1.0
gain=1.01;

% offset
% default = 0.0
offset=0.05;

% Create a sine wave of input frequency.
x = sin(2*pi*t*freq); 
x1 = (sin(2*pi*t1*freq)+offset)*gain;
x2 = sin (2*pi*t2*freq);
x(1:2:end)=x1;
x(2:2:end)=x2;

nfft = 2^nextpow2(L); % Next power of 2 from length of y
y = fft(x,nfft)/L;
f = Fs/2*linspace(0,1,nfft/2+1);
f = f/(1e6)*1.0;

% Plot single-sided amplitude spectrum.
figure(3)
%semilogy(f,2*abs(y(1:nfft/2+1))) 
semilogy(abs(y));
graph_title=strcat('Power Spectrum of a',char(32));
graph_title2=num2str(freq/(1e6)*1.0);
graph_title2=strcat(graph_title2,'MHz Sine Wave, with delay:');
graph_title2=strcat(graph_title2,num2str(delay,8));
graph_title2=strcat(graph_title2,' offset:');
graph_title2=strcat(graph_title2,num2str(offset,8));
graph_title2=strcat(graph_title2,' gain:');
graph_title2=strcat(graph_title2,num2str(gain,8));
graph_title={graph_title,graph_title2};
title(graph_title); 
xlabel('Frequency (MHz)'); 
ylabel('Power');

% Loop through different frequency value
% figure(2)
% for i=1:1:15,
%     freq=freq+i*(freq/15);
%     x1 = (sin(2*pi*t1*freq)+offset)*gain;
%     x2 = sin (2*pi*t2*freq);
%     x(1:2:end)=x1;
%     x(2:2:end)=x2;
%     y = fft(x,nfft)/L;
%     semilogy(f,2*abs(y(1:nfft/2+1))) 
%     graph_title=strcat('Power Spectrum of a ',num2str(freq));
%     graph_title=strcat(graph_title,'Hz Sine Wave, with delay:');
%     graph_title=strcat(graph_title,num2str(delay,8));
%     graph_title=strcat(graph_title,' offset:');
%     graph_title=strcat(graph_title,num2str(offset,8));
%     graph_title=strcat(graph_title,' gain:');
%     graph_title=strcat(graph_title,num2str(gain,8));
%     title(graph_title); 
%     xlabel('Frequency (Hz)'); 
%     ylabel('Power');
%     pause(1);
% end