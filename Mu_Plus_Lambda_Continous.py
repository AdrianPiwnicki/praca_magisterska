import heapq
import random
from random import randint
import matplotlib.pyplot as plt
import numpy as np
from funkcje_pomocnicze import ModelVerhulstContinuous as MVC
from funkcje_pomocnicze import CreateChromosoms as createChromosom


def Mu_Plus_Lambda_Continous(plotting, najlepszy_osobnik=None):

    # podstawowe zmienne
    LBnCh = 8
    n = 2 ** LBnCh
    t = [0, 10]
    K = 100
    N0 = randint(1, K + 1)
    r = randint(-1, 2)
    while r == 0:
        r = randint(-1, 2)

    # tworzenie tablicy genotypu bitowego (chromosomów)
    chromosomy_t = [0] * n
    V_1 = t[0]
    V_t = [0] * n
    createChromosom(n, LBnCh, chromosomy_t, V_t, V_1, t)

    # specjalne zmienne
    mu = randint(2, 10)
    lmb = randint(2, 10)
    genotyp_rodzicow = list()
    pula_rodzicow = list()
    fenotyp_rodzicow = list()

    # Rysowanie wykresu
    if plotting == 1:
        plt.figure(2)
    os_x = np.arange(t[0], t[1] + 1)
    os_y = MVC(K, N0, r, os_x)
    if plotting == 1:
        plt.plot(os_x, os_y)

    # początkowa pula rodzicielska mu
    for i in range(mu):
        pula_rodzicow.append(random.choice(chromosomy_t))
        genotyp_rodzicow.append(V_t[chromosomy_t.index(pula_rodzicow[i])])
        fenotyp_rodzicow.append(MVC(K, N0, r, genotyp_rodzicow[i]))

    # zmienne dla puli potomnej
    genotyp_potomkow = list()
    pula_potomkow = list()
    fenotyp_potomkow = list()

    # zmienne do algorytmu
    pokolenie = 1
    end_modelling = 0

    while end_modelling < 11:
        if plotting == 1:
            plt.clf()
            plt.plot(os_x, os_y)
            plt.title("Pokolenie: " + str(pokolenie))
            plt.xlabel('Czas')
            plt.ylabel('Wielkość populacji')
            plt.plot(genotyp_rodzicow, fenotyp_rodzicow, 'rx')
        pokolenie += 1

        if r > 0:
            najlepszy_osobnik = max(fenotyp_rodzicow)
        else:
            najlepszy_osobnik = min(fenotyp_rodzicow)

        for i in range(lmb):
            genotyp_rodzic1 = random.choice(genotyp_rodzicow)
            rodzic1 = pula_rodzicow[genotyp_rodzicow.index(genotyp_rodzic1)]
            genotyp_rodzic2 = random.choice(genotyp_rodzicow)
            rodzic2 = pula_rodzicow[genotyp_rodzicow.index(genotyp_rodzic2)]

            # Krzyżowanie
            genotyp_potomek = list()
            for j in range(LBnCh):
                rownomierne_prawdopodobienstwo = random.uniform(0, 1)
                if rownomierne_prawdopodobienstwo < 0.5:
                    genotyp_potomek.append(rodzic1[j])
                else:
                    genotyp_potomek.append(rodzic2[j])

            # Mutacja
            for i in range(len(genotyp_potomek)):
                if abs(np.random.normal(0, 1)) < 1:
                    if genotyp_potomek[i] == 0:
                        genotyp_potomek[i] = 1
                    else:
                        genotyp_potomek[i] = 0

            # Dodanie nowego potomka
            pula_potomkow.append(genotyp_potomek)
            genotyp_potomkow.append(V_t[chromosomy_t.index(genotyp_potomek)])
            fenotyp_potomkow.append(MVC(K, N0, r, V_t[chromosomy_t.index(genotyp_potomek)]))

        # Nowa pula rodzicielska z rodziców i potomków
        fenotyp_pokolenia = fenotyp_rodzicow + fenotyp_potomkow
        genotyp_pokolenia = genotyp_rodzicow + genotyp_potomkow
        if r > 0:
            fenotyp_rodzicow = heapq.nlargest(mu, fenotyp_pokolenia)
            if max(fenotyp_rodzicow) == najlepszy_osobnik:
                end_modelling += 1
            else:
                end_modelling = 0
        else:
            fenotyp_rodzicow = heapq.nsmallest(mu, fenotyp_pokolenia)
            if min(fenotyp_rodzicow) == najlepszy_osobnik:
                end_modelling += 1
            else:
                end_modelling = 0
        pula_rodzicow.clear()
        genotyp_rodzicow.clear()

        # Nowa pula rodziców na kolejne pokolenie
        for i in fenotyp_rodzicow:
            nowy_rodzic = genotyp_pokolenia[fenotyp_pokolenia.index(i)]
            genotyp_rodzicow.append(nowy_rodzic)
            pula_rodzicow.append(chromosomy_t[V_t.index(nowy_rodzic)])

        if plotting == 1:
            plt.pause(0.1)

    if plotting == 1:
        plt.plot(genotyp_pokolenia[fenotyp_pokolenia.index(max(fenotyp_rodzicow))], najlepszy_osobnik, 'go')
        if r > 0:
            plt.suptitle("Największa liczba osobników: " + str(round(max(fenotyp_rodzicow),4)) + ", w czasie t = "
                         + str(round(genotyp_rodzicow[fenotyp_rodzicow.index(max(fenotyp_rodzicow))],4)))
        else:
            plt.suptitle("Najmniejsza liczba osobników: " + str(round(max(fenotyp_rodzicow),4)) + ", w czasie t = "
                         + str(round(genotyp_rodzicow[fenotyp_rodzicow.index(max(fenotyp_rodzicow))],4)))

    if plotting == 1:
        plt.savefig('models/modelVerhulst_continous5.png')
        plt.show()
    return pokolenie, najlepszy_osobnik
