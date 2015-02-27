% ADC simulation
% sampling point = 4*(2^16)
% delay
%
% Author: Hong Chen
% Date: August 5,2010

% Sampling frequency 
Fs = 2e9; 

% Sample time
T = 1/Fs;                     

% Length of signal
L = (2^11)*8;                    

% Time vector
t = (0:L-1)*T;   
t1 = t(1:2:end);
t2 = t(2:2:end);

% Frequency of Sine Wave
freq = 3.77632453e7;

% delay
delay=0.9;
t2=t2-delay*T;

% Create a sine wave of 200 Hz.
x = sin(2*pi*t*freq); 
y = x;
y1 = sin(2*pi*t1*freq);
y2 = sin (2*pi*t2*freq);
y(1:2:end)=y1;
y(2:2:end)=y2;

nfft = 2^nextpow2(L); % Next power of 2 from length of y
X = fft(x,nfft)/L;
Y = fft(y,nfft)/L;
f = Fs/2*linspace(0,1,nfft/2+1);


% Plot single-sided amplitude spectrum.
figure(1)
semilogy(f,2*abs(X(1:nfft/2+1)),'r') 
hold on;
semilogy(f,2*abs(Y(1:nfft/2+1)),'b')
graph_title=strcat('Power Spectrum of a ',num2str(freq));
graph_title=strcat(graph_title,'Hz Sine Wave, with delay:');
graph_title=strcat(graph_title,num2str(delay,8));
title(graph_title); 
xlabel('Frequency (Hz)'); 
ylabel('Power'); 

% Calculate the difference between two streams
z = sin(2*pi*t*freq);
diff = y - z;
figure(2)
plot(diff(1:200));
title('Difference between a perfect interleaved ADCs and a problematic interleaved ADCs(delay)');
hold on;
imit=-sin(pi*freq*delay*T)*(cos(2*pi*freq*t-pi*freq*delay*T)-0.5*(cos(2*pi*t*(Fs/2-freq)+pi*freq*delay*T)+cos(2*pi*t*(Fs/2+freq)-pi*freq*delay*T)));
plot(imit(1:200),'r');
figure(3)
plot(z(1:50),'r');
hold on;
plot(y(1:50));
title('Comparison between a perfect interleaved ADCs and a problematic interleaved ADCs(delay)');


