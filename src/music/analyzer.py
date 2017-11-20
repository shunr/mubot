import numpy as np
from scipy.fftpack import fft
from scipy.io import wavfile
import subprocess
import time

CHUNK_SIZE = 1024


def analyze(filename):
    t1 = time.time()
    global CHUNK_SIZE
    fs, data = wavfile.read(filename)
    print(fs)
    # calculates the number of 1024 sample windows
    numWindows = len(data) / CHUNK_SIZE
    audio = np.split(data.T[0], numWindows)  # this is a two channel soundtrack
    print(len(audio))
    samples = []
    spectrum = []
    lastSpectrum = []
    spectralFlux = []
    thresholds = []
    thresholdWindow = 10
    j = 0
    for window in audio:
        lastSpectrum = spectrum
        spectrum = np.abs(fft(window)[:CHUNK_SIZE // 2])
        flux = 0.0
        for i in range(min(len(lastSpectrum), len(spectrum))):
            currFlux = spectrum[i] - lastSpectrum[i]
            if currFlux > 0:
                flux += currFlux
        spectralFlux.append(flux)
    for i in range(len(spectralFlux)):
        mean = 0.0
        lbound = max(0, i - thresholdWindow)
        ubound = min(len(spectralFlux) - 1, i + thresholdWindow)
        for j in range(lbound, ubound + 1):
            mean += spectralFlux[j]
        mean /= (ubound - lbound)
        thresholds.append(mean * 1.9)
    goodFluxValues = []
    for i in range(len(thresholds)):
        if (thresholds[i] <= spectralFlux[i]):
            goodFluxValues.append(spectralFlux[i] - thresholds[i])
        else:
            goodFluxValues.append(0)
    peaks = []
    for i in range(len(goodFluxValues) - 1):
        if (goodFluxValues[i] > goodFluxValues[i + 1]):
            peaks.append(goodFluxValues[i])
        else:
            peaks.append(0)

    for i in range(len(peaks)):
        if (peaks[i] > 0):
            time = i * CHUNK_SIZE / fs
    t2 = time.time()
    print("Time taken to FFT: {0:.6f}".format(t2-t1))
    return peaks


def transcode(filename):
    newname = filename + ".wav"
    command = "ffmpeg -y -i " + filename + " " + newname
    subprocess.call(command, shell=True)
    return newname
