% Author: Hong Chen
% Date: August 5,2010
% ADC simulation
% sampling point = 8*(2^16)
% gain

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
freq = 1e7;

% gain
gain=0.85;

% Create a sine wave of 200 Hz.
x = sin(2*pi*t*freq); 
x1 = sin(2*pi*t1*freq);
x2 = sin (2*pi*t2*freq)*gain;
x(1:2:end)=x1;
x(2:2:end)=x2;

nfft = 2^nextpow2(L); % Next power of 2 from length of y
y = fft(x,nfft)/L;
f = Fs/2*linspace(0,1,nfft/2+1);


% Plot single-sided amplitude spectrum.
figure(1)
semilogy(f,2*abs(y(1:nfft/2+1))) 
graph_title=strcat('Power Spectrum of a ',num2str(freq,8));
graph_title=strcat(graph_title,'Hz Sine Wave, with gain:');
graph_title=strcat(graph_title,num2str(gain,8));
title(graph_title); 
xlabel('Frequency (Hz)'); 
ylabel('Power'); 

% Calculate the difference between two streams
z = sin(2*pi*t*freq);
diff = x - z;
figure(2)
plot(diff(1:200));
title('Difference between a perfect interleaved ADCs and a problematic interleaved ADCs(gain)');
hold on;
imit=(gain-1)*(0.5*sin( 2*pi*freq*t) - 0.25*( sin( 2*pi*t* (Fs/2 + freq)) - sin( 2*pi*t*( Fs/2 - freq))));
plot(imit(1:200),'r');

figure(3)
plot(z(1:200),'r');
hold on;
plot(x(1:200));
title('Comparison between a perfect interleaved ADCs and a problematic interleaved ADCs(gain)');
