import numpy as np


def ModelVerhulstContinuous(K, N0, r, t):
    return K / (1 + (K / N0 - 1) * np.exp(-r * t))


def ModelVerhulstDiscrete(a, r, K, Nt):
    try:
        result = a * Nt - (r / K) * Nt ** 2
    except OverflowError as err:
        print('Za duża liczba ', err)
        result = 1
    return result


def CreateChromosoms(n, LBnCh, chromosomy, V_t, V_1, t):
    for i in range(n):
        j = LBnCh - 1
        chromosom = []
        while j >= 0:
            chromosom.append((i >> j) & 1)
            j -= 1
        chromosomy[i] = chromosom
        V_t[i] = V_1
        V_1 += (t[1] - t[0]) / (n - 1)
    return
