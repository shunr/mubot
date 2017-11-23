import numpy as np
from scipy.fftpack import rfft
from scipy.io import wavfile
import subprocess
import time

CHUNK_SIZE = 1024
SAMPLE_RATE = 16000
BIT_RATE = 10000

MAX_DURATION = 120
THRESHOLD = 1.28

def analyze(filename, peak_array):
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
    goodFluxValues = []
    thresholdWindow = 10
    j = 0

    for index, window in enumerate(audio):
        lastSpectrum = spectrum
        spectrum = np.abs(rfft(window)[:CHUNK_SIZE // 2])
        flux = 0.0
        for i in range(min(len(lastSpectrum), len(spectrum))):
            currFlux = spectrum[i] - lastSpectrum[i]
            if currFlux > 0:
                flux += currFlux
        spectralFlux.append(flux)
        if index >= thresholdWindow:
            i = index - thresholdWindow
            mean = 0.0
            lbound = max(0, i - thresholdWindow)
            ubound = min(len(spectralFlux) - 1, i + thresholdWindow)
            for j in range(lbound, ubound + 1):
                mean += spectralFlux[j]
            mean /= (ubound - lbound)
            thresholds.append(mean * THRESHOLD)
            if (thresholds[i] <= spectralFlux[i]):
                goodFluxValues.append(spectralFlux[i] - thresholds[i])
            else:
                goodFluxValues.append(0)
            if i > 0 and (goodFluxValues[i - 1] > goodFluxValues[i]):
                if i == 0 or peak_array[i-1] == 0:
                  peak_array.append(goodFluxValues[i - 1])
                else:
                  peak_array.append(0)
            else:
                peak_array.append(0)
    peak_array.append(-1)
    t2 = time.time()
    print("Time taken to FFT: {0:.6f}".format(t2 - t1))


def transcode(filename):
    newname = filename + ".wav"
    command = "ffmpeg -y -ss 1 -i " + filename
    arguments = [
        "-t " + str(MAX_DURATION),
        "-ar " + str(SAMPLE_RATE),
        "-ab " + str(BIT_RATE),
        newname
    ]
    subprocess.call(command + " " + " ".join(arguments), shell=True)
    return newname
