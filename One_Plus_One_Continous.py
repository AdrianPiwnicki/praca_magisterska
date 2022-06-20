import math
import random
from random import randint
import matplotlib.pyplot as plt
import numpy as np
from funkcje_pomocnicze import ModelVerhulstContinuous as MVC
from funkcje_pomocnicze import CreateChromosoms as createChromosom


def One_Plus_One_Continous(plotting):
    LBnCh = 8
    n = 2 ** LBnCh
    t = [0, 30]
    K = 100
    N0 = randint(1, K + 1)
    r = randint(-1, 2)
    while r == 0:
        r = randint(-1, 2)

    chromosomy_t = [0] * n
    V_1 = t[0]
    V_t = [0] * n
    createChromosom(n, LBnCh, chromosomy_t, V_t, V_1, t)

    # Wylosowany pierwszy osobnik
    chr_rodzic = random.choice(chromosomy_t)
    rodzic = V_t[chromosomy_t.index(chr_rodzic)]
    fenotyp_rodzic = MVC(K, N0, r, rodzic)

    # rysowanie wykresu
    if plotting == 1:
        plt.figure(1)
        os_x = np.arange(t[0], t[1] + 1)
        os_y = MVC(K, N0, r, os_x)
        plt.plot(os_x, os_y)
        plt.plot(rodzic, fenotyp_rodzic, 'ro')
        plt.xlabel('Czas')
        plt.ylabel('Wielkość populacji')

    pokolenie = 1
    end_modelling = 0

    while end_modelling < 11:
        if plotting == 1:
            plt.pause(0.1)
            plt.title("Pokolenie: " + str(pokolenie))
        pokolenie += 1

        # Mutacja osobnika rodzicielskiego
        chr_potomek = []
        for i in chr_rodzic:
            rozklad_normalny = np.random.normal(0, 1)
            if 1 > rozklad_normalny > -1:
                if i == 0:
                    i = 1
                else:
                    i = 0
            chr_potomek.append(i)

        # Utworzenie osobnika potomnego
        potomek = V_t[chromosomy_t.index(chr_potomek)]
        fenotyp_potomek = MVC(K, N0, r, potomek)

        # Sprawdzenie fenotypów osobników
        if r > 0:
            if fenotyp_potomek > fenotyp_rodzic:
                rodzic = potomek
                fenotyp_rodzic = fenotyp_potomek
                end_modelling = 0
            else:
                end_modelling += 1
        else:
            if fenotyp_potomek < fenotyp_rodzic:
                rodzic = potomek
                fenotyp_rodzic = fenotyp_potomek
                end_modelling = 0
            else:
                end_modelling += 1

        if plotting == 1:
            plt.plot(rodzic, fenotyp_rodzic, 'ro')

    if plotting == 1:
        plt.savefig('models/modelVerhulst_continous3.png')
        plt.show()

    return pokolenie, fenotyp_rodzic
