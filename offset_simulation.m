% Author: Hong Chen
% Date: August 5,2010
% ADC simulation
% sampling point = 8*(2^16)
% offset

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

% offset
offset=0.1;

% Create a sine wave of 200 Hz.
x = sin(2*pi*t*freq); 
x1 = sin(2*pi*t1*freq)+offset;
x2 = sin (2*pi*t2*freq);
x(1:2:end)=x1;
x(2:2:end)=x2;

nfft = 2^nextpow2(L); % Next power of 2 from length of y
y = fft(x,nfft)/L;
f = Fs/2*linspace(0,1,nfft/2+1);


% Plot single-sided amplitude spectrum.
figure(1)
semilogy(f,2*abs(y(1:nfft/2+1))) 
graph_title=strcat('Power Spectrum of a',num2str(freq));
graph_title=strcat(graph_title,'Hz Sine Wave, with offset:');
graph_title=strcat(graph_title,num2str(offset,8));
title(graph_title); 
xlabel('Frequency (Hz)'); 
ylabel('Power'); 

% Calculate the difference between two streams
z = sin(2*pi*t*freq);
diff = x - z;
figure(2)
ind=1:2:50;
plot(ind,diff(1:2:50),'ro');
hold on;
plot(ind+1,diff(2:2:50),'o');
hold on;
plot(diff(1:1:50),'-ko');


% Calculate the difference between two streams
figure(3)
plot(z(1:200),'r');
hold on;
plot(x(1:200));
hold on;
z=z+offset;
plot(z(1:200),'k');
title('Comparison between a perfect interleaved ADCs and a problematic interleaved ADCs(gain)');

% Compose basic sine waves to imitate the interleaved ADCs
z = sin(2*pi*t*freq);
%z1 = cos(2*pi*t1*(Fs/2))*offset;
z1 = offset*ones(1,L/2);
z(1:2:end) = z(1:2:end) + z1;

nfft = 2^nextpow2(L); % Next power of 2 from length of z
w = fft(z,nfft)/L;
f2 = Fs/2*linspace(0,1,nfft/2+1);


% Plot single-sided amplitude spectrum.
figure(4)
semilogy(f2,2*abs(w(1:nfft/2+1))) 
graph_title=strcat('Power Spectrum of a',num2str(freq));
graph_title=strcat(graph_title,'Hz Sine Wave, with offset:');
graph_title=strcat(graph_title,num2str(offset,8));
title(graph_title); 
xlabel('Frequency (Hz)'); 
ylabel('Power'); 

