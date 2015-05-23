% Author: Hong Chen
% Date: August 5,2010
% plot the a small part of the sample data
% zoom in and see the details

x= dlmread('default_0.txt','\n'); % read from a data file
start=1;   % set the begin of the segment
length=100; % set the length of the segment
p=1:2:length;  % the x-axis reference
plot(p,x(start:2:start+length-1),'or')
hold on;
plot(p+1,x(start+1:2:start+length),'o')
hold on;
plot(x(start:1:start+length-1),'-k')
