%
% Function to calculate and plot the power spectrum (in decibels) for a time series y


function plot_power_spec(y,dt,n)

N = length(y);      % number of data points

% if the length of the time series is odd, remove last point to make it
% even
if mod(N,2) == 1
    y = y(1:end-1);
    N = length(y);
end

%--------------------  Calculate the power spectrum   --------------------

my_fft = fft(y);           % Fast Fourier transform (FFT)
my_fft = my_fft(1:N/2+1);  % select only positive frequencies

Fs   = 1/dt;           % sampling frequency
dF   = Fs / N;         % frequency step
Fmax = Fs / 2;         % Nyquist (maximum) frequency
freq = 0:dF:Fmax;      % array of non-negative frequencies returnd by the fft

psd = (1/(Fs*N)) * abs(my_fft).^2;   % power spectral density (PSD)
psd(2:end-1) = 2*psd(2:end-1);       % double power except for freq = 0


%--------------------  Plot the Log Power (in decibels)  --------------------

logPSD = 10*log10(psd);     % calculate the decibals of the signal
plot(freq,logPSD)



grid on
title_text=(sprintf('Power Spectrum %g',n));
title(title_text)
xlabel('Frequency (Hz)')
ylabel('Power/Frequency (dB/Hz)')


end