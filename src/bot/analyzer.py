import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from scipy.io import wavfile
import wave
import pyaudio

def analyze(filename):
    fs, data = wavfile.read(filename)
    print(fs)
    numWindows = len(data)/1024 #calculates the number of 1024 sample windows
    audio = np.split(data.T[0], numWindows) # this is a two channel soundtrack
    print(len(audio))
    samples = []
    spectrum = []
    lastSpectrum = []
    spectralFlux = []
    thresholds = []
    thresholdWindow = 30
    j = 0
    for window in audio:
        lastSpectrum = spectrum
        spectrum = np.abs(fft(window)[:1024//2])
        flux = 0.0
        for i in range(min(len(lastSpectrum), len(spectrum))):
            currFlux = spectrum[i] - lastSpectrum[i]
            if currFlux > 0:
                flux += currFlux
        spectralFlux.append(flux)
    for i in range(len(spectralFlux)):
        mean = 0.0
        lbound = max(0,i-thresholdWindow)
        ubound = min(len(spectralFlux)-1,i+thresholdWindow)
        for j in range(lbound,ubound+1):
            mean += spectralFlux[j]
        mean /= (ubound-lbound)
        thresholds.append(mean*1.9)
    goodFluxValues = []
    for i in range(len(thresholds)):
        if (thresholds[i] <= spectralFlux[i]):
            goodFluxValues.append(spectralFlux[i] - thresholds[i])
        else:
            goodFluxValues.append(0)
    peaks = []
    for i in range(len(goodFluxValues)-1):
        if (goodFluxValues[i] > goodFluxValues[i+1]):
            peaks.append(goodFluxValues[i])
        else:
            peaks.append(0)

    for i in range(len(peaks)):
        if (peaks[i] > 0):
            time = i*1024/fs
    #plt.plot(peaks,'r') 
    #plt.show()

    chunk = 1024  

    #open a wav format music  
    f = wave.open(filename,"rb")  
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)
    ind = 0
    data = f.readframes(chunk)  
    while data:
        if (peaks[ind] > 0):
            a=0
        # elif (ind < 3 or (peaks[ind-1] <= 0 and peaks[ind-2] <= 0 and peaks[ind-3] <= 0)):
            print("succ" + str(ind))
        stream.write(data)  
        ind += 1  
        data = f.readframes(chunk)

    #stop stream  
    stream.stop_stream()  
    stream.close()  

    #close PyAudio  
    p.terminate()

analyze('Martin-Garrix-Brooks-Byte.wav')