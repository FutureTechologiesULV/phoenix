clc
close all
clear

%------------------ Read BCI data as a table  --------------------

opts = detectImportOptions('OpenBCI-R-ARM-M-RAW-2023-12-13_14-49-07.txt');
opts = setvartype(opts, 'Timestamp_Formatted_', 'datetime');
T = readtable('OpenBCI-R-ARM-M-RAW-2023-12-13_14-49-07.txt', opts);


% number of data rows
N = length(T.SampleIndex);
t = T.Timestamp - T.Timestamp(1);

% ------GRAPH THE DATA FROM RAW DATA---------

% save channel data in a single matrix
CH = zeros(N,8);
CH(:,1) = T.EXGChannel0;
CH(:,2) = T.EXGChannel1;
CH(:,3) = T.EXGChannel2;
CH(:,4) = T.EXGChannel3;
CH(:,5) = T.EXGChannel4;
CH(:,6) = T.EXGChannel5;
CH(:,7) = T.EXGChannel6;
CH(:,8) = T.EXGChannel7;

figure
for n=0:7
    plot(t, CH(:,n+1),'DisplayName',sprintf('Channel %i',n))
    hold on
end
 xlabel('time (s)')
    ylabel('microvolts')
    legend
figure
for n=0:7
    subplot(8,1,n+1)
    plot(t, CH(:,n+1),'DisplayName',sprintf('Channel %i',n))
    xlabel('time (s)')
    ylabel('microvolts')
    legend
end

% -------DETREND AND GRAPH DETRENDED DATA-------

% Save detrended data in a single matrix

CH_D = zeros(N,8);
CH_D(:,1) = detrend(T.EXGChannel0);
CH_D(:,2) = detrend(T.EXGChannel1);
CH_D(:,3) = detrend(T.EXGChannel2);
CH_D(:,4) = detrend(T.EXGChannel3);
CH_D(:,5) = detrend(T.EXGChannel4);
CH_D(:,6) = detrend(T.EXGChannel5);
CH_D(:,7) = detrend(T.EXGChannel6);
CH_D(:,8) = detrend(T.EXGChannel7);


figure

for n=0:7
    subplot(8,1,n+1)
    plot(t, CH_D(:,n+1),'DisplayName',sprintf('Channel %i',n))
    xlabel('time (s)')
    ylabel('microvolts')
    legend
end
figure
for n=0:7
    plot(t,CH_D(:,n+1),"DisplayName",sprintf("Channel %i",n))
    hold on
end
xlabel('time (s)')
    ylabel('microvolts')
    legend

% -----FIND THE SIGNAL TO NOISE RATIO--------
%From Analyzing the graph THE DATA FOR SIGNAL IS FROM 60 TO 62 and for
%noise from 53 to 59
figure
for n=0:7
    signal = CH_D(250*60:250*62,n+1);
    noise = CH_D(250*53:250*59,n+1);
    signal_power = sum(abs(signal).^2)/length(signal);
    noise_power = sum(abs(noise).^2)/length(noise);
    
    s_to_n = 10*log10(signal_power/noise_power);
    %Uncoment the following line to print the SNR in the command window
    % fprintf('SNR %g : %.2f dB\n',n, s_to_n);
    subplot(8,1,n+1)
    plot(t, CH_D(:,n+1),'DisplayName',sprintf('SNR %g : %.2f dB\n',n, s_to_n))
    xlabel('time (s)')
    ylabel('microvolts')
    legend
    
end
%-------PLOT POWER SPECTRA---------
%I will use this function done by Dr Chappell for this part function plot_power_spec(y,dt)
figure
dt = mean(diff(t));
for n=0:7
    subplot(8,1,n+1)
    plot_power_spec(CH_D(:,n+1),dt,n)
end

%--------60HZ NOTCH FILTER---------
%Set the data and sampling frequency
pre_notch = CH_D;
sampling_fs = 250;
notch_fs = 60;
Q = 5; %Controls the width of the notch filter, can be adjusted

nn = notch_fs/(sampling_fs/2); %normalize notch
bw = nn/Q;
[b,a]= iirnotch(nn,bw);

post_notch = filter(b,a,pre_notch);

figure    
for n=0:7
    subplot(8,1,n+1)
    plot(t,post_notch(:,n+1),"DisplayName",sprintf('Channel %i',n))
    xlabel("time (s)")
    ylabel("microvolts")
    legend
end
figure
for n=0:7
    plot(t,post_notch(:,n+1),"DisplayName",sprintf('Channel %i',n))
    hold on
end
xlabel("time (s)")
ylabel("microvolts")
legend
%--------LOW PASS FILTER----------
pre_lpf = post_notch;
sampling_fs = 250;

ctoff_f = 20;
filter_type = "low";
filterO = 10;

d = fdesign.lowpass('N,F3dB', filterO, ctoff_f, sampling_fs);
lowpassFilter = design(d, 'butter');

post_lpf = filter(lowpassFilter, pre_lpf);

figure
for n=0:7
    plot(t,post_lpf(:,n+1),"DisplayName",sprintf("Channel %i",n))
    hold on
end
xlabel("time (s)")
ylabel("microvolts")
legend
figure
for n=0:7
    subplot(8,1,n+1)
    plot(t,post_lpf(:,n+1),"DisplayName",sprintf("Channel %i",n))
    xlabel("time (s)")
    ylabel("microvolts")
    legend
end

%--------DATA SMOOTHING------------
CH_MA = zeros(N,8);
CH_MA(:,1) = movmean(post_lpf(:,1),2);
CH_MA(:,2) = movmean(post_lpf(:,2),2);
CH_MA(:,3) = movmean(post_lpf(:,3),2);
CH_MA(:,4) = movmean(post_lpf(:,4),2);
CH_MA(:,5) = movmean(post_lpf(:,5),2);
CH_MA(:,6) = movmean(post_lpf(:,6),2);
CH_MA(:,7) = movmean(post_lpf(:,7),2);
CH_MA(:,8) = movmean(post_lpf(:,8),2);

figure
for n=0:7    
    plot(t,CH_MA(:,n+1),"DisplayName",sprintf("Channel %i",n))
    hold on
end
xlabel("time (s)")
ylabel("microvolts")
legend

figure
for n=0:7
    subplot(8,1,n+1)
    plot(t,CH_MA(:,n+1),"DisplayName",sprintf("Channel %i",n))
    xlabel("time (s)")
    ylabel("microvolts")
    legend
end
% % -------DATA DETERNDING QUADRATIC-------

poly_order = 2;  % Quadratic polynomial order
[p, ~, mu] = polyfit(t, CH_MA(:,3), poly_order);
quadratic_fit = polyval(p, t, [], mu);

% Subtract the quadratic fit from the signal to detrend it
detrended_signal = CH_MA(:,3) - quadratic_fit;
figure
plot(t,detrended_signal)
xlabel("time (s)")
ylabel("microvolts")
legend

% %--------DATA CONVERSION TO 1 AND 0-------


