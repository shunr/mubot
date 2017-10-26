for i in range(len(spectralFlux)):
    mean = 0.0
    lbound = max(0,i-thresholdWindow)
    ubound = min(len(spectralFlux)-1,i+thresholdWindow)
    for j in range(lbound,ubound+1):
        mean += spectralFlux[j]
    if (ubound-lbound) == 0:
        print("AMIRETARED" + str(lbound) + str(ubound))
        break
    mean /= (ubound-lbound)
    thresholds.append(mean)