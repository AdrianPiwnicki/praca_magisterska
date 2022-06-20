import random
import numpy as np
from matplotlib import pyplot as plt
from funkcje_pomocnicze import ModelVerhulstDiscrete as MVD
from funkcje_pomocnicze import CreateChromosoms as createChromosom


def One_Plus_One_Discrete(plotting):

    # podstawowe zmienne
    LBnCh = 6
    n = 2 ** LBnCh
    a = random.uniform(0, 4)
    r = a - 1
    K = 100
    Nt = random.uniform(1, K + 1)
    t = [0, n]

    # tworzenie zbioru genotypów
    chromosomy_t = [0] * n
    V_1 = t[0]
    V_t = [0] * n
    createChromosom(n, LBnCh, chromosomy_t, V_t, V_1, t)

    # specjalne zmienne
    os_genotyp = list()
    os_fenotyp = list()
    os_genotyp.append(t[0])
    os_fenotyp.append(Nt)
    for i in range(1, t[1] + 1):
        Nt_1 = MVD(a, r, K, Nt)
        os_genotyp.append(i)
        os_fenotyp.append(Nt_1)
        Nt = Nt_1

    # rodzic początkowy
    chr_rodzic = random.choice(chromosomy_t)
    rodzic = os_genotyp[chromosomy_t.index(chr_rodzic)]
    fenotyp_rodzic = os_fenotyp[os_genotyp.index(rodzic)]

    if plotting == 1:
        plt.scatter(os_genotyp, os_fenotyp, 10)
        plt.plot(rodzic, fenotyp_rodzic, 'ro')

    pokolenie = 1
    end_modelling = 0

    while end_modelling < 11:

        if plotting == 1:
            plt.pause(0.1)
            plt.title("Pokolenie: " + str(pokolenie) + "  Współczynnik a: "+ str(round(a,4)))
            plt.xlabel('Czas')
            plt.ylabel('Wielkość populacji')
        pokolenie += 1
        chr_potomek = []

        # Mutacja
        for i in chr_rodzic:
            rozklad_normalny = np.random.normal(0, 1)
            if 1 > rozklad_normalny > -1:
                if i == 0:
                    i = 1
                else:
                    i = 0
            chr_potomek.append(i)

        # Utworzenie osobnika potomnego
        potomek = os_genotyp[chromosomy_t.index(chr_potomek)]
        fenotyp_potomek = os_fenotyp[os_genotyp.index(potomek)]

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
        plt.plot(rodzic, fenotyp_rodzic, 'go')
        if r > 0:
            plt.suptitle("Największa liczba osobników: " + str(round(fenotyp_rodzic,4)) + ", w czasie t = " + str(round(rodzic,4)))
        else:
            plt.suptitle("Najmniejsza liczba osobników: " + str(round(fenotyp_rodzic,4)) + ", w czasie t = " + str(round(rodzic,4)))
        plt.savefig('models/modelVerhulst_discrete2.png')
        plt.show()

    return pokolenie, fenotyp_rodzic
