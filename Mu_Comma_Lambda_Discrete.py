import heapq
import random
import numpy as np
from matplotlib import pyplot as plt
from funkcje_pomocnicze import ModelVerhulstDiscrete as MVD
from funkcje_pomocnicze import CreateChromosoms as createChromosom


def Mu_Comma_Lambda_Discrete(plotting, najlepszy_osobnik=None):

    # zmienne podstawowe
    LBnCh = 6
    n = 2 ** LBnCh
    a = random.uniform(0, 4)
    r = a - 1
    K = 100
    Nt = random.uniform(1, K + 1)
    t = [0, n]

    # zmienne specjalne
    mu = random.randint(2, 10)
    lmb = random.randint(2, 10)
    pula_rodzicow = list()
    genotyp_rodzicow = list()
    fenotyp_rodzicow = list()

    # tworzenie zbioru chromosomów
    chromosomy_t = [0] * n
    V_1 = t[0]
    V_t = [0] * n
    createChromosom(n, LBnCh, chromosomy_t, V_t, V_1, t)

    # rysowanie funkcji
    if plotting == 1:
        plt.figure(2)
    os_x = list()
    os_y = list()

    # generowanie wszystkich genotypów oraz fenotypów
    os_x.append(t[0])
    os_y.append(Nt)
    for i in range(1, t[1] + 1):
        Nt_1 = MVD(a, r, K, Nt)
        os_x.append(i)
        os_y.append(Nt_1)
        Nt = Nt_1

    # początkowa pula rodzicielska mu
    for i in range(mu):
        genotyp_rodzicow.append(random.choice(chromosomy_t))
        rodzic = os_x[chromosomy_t.index(genotyp_rodzicow[i])]
        pula_rodzicow.append(rodzic)
        fenotyp_rodzicow.append(os_y[os_x.index(rodzic)])

    # zmienne dla puli potomnej
    pula_potomkow = list()
    genotyp_potomkow = list()
    fenotyp_potomkow = list()

    pokolenie = 1
    end_modelling = 0

    while end_modelling < 11:
        if plotting == 1:
            plt.clf()
            plt.scatter(os_x, os_y, 10)
            plt.title("Pokolenie: " + str(pokolenie) + "  Współczynnik a: " + str(round(a, 4)))
            plt.xlabel('Czas')
            plt.ylabel('Wielkość populacji')
            plt.plot(pula_rodzicow, fenotyp_rodzicow, 'rx')
        pokolenie += 1
        if r > 0:
            najlepszy_osobnik = max(fenotyp_rodzicow)
        else:
            najlepszy_osobnik = min(fenotyp_rodzicow)

        for i in range(lmb):
            rodzic1 = random.choice(pula_rodzicow)
            genotyp_rodzic1 = genotyp_rodzicow[pula_rodzicow.index(rodzic1)]
            rodzic2 = random.choice(pula_rodzicow)
            genotyp_rodzic2 = genotyp_rodzicow[pula_rodzicow.index(rodzic2)]

            # Krzyżowanie
            genotyp_potomek = list()
            for j in range(LBnCh):
                rownomierne_prawdopodobienstwo = random.uniform(0, 1)
                if rownomierne_prawdopodobienstwo < 0.5:
                    genotyp_potomek.append(genotyp_rodzic1[j])
                else:
                    genotyp_potomek.append(genotyp_rodzic2[j])

            # Mutacja
            for i in range(len(genotyp_potomek)):
                if abs(np.random.normal(0, 1)) < 1:
                    if genotyp_potomek[i] == 0:
                        genotyp_potomek[i] = 1
                    else:
                        genotyp_potomek[i] = 0

            genotyp_potomkow.append(genotyp_potomek)
            potomek = os_x[chromosomy_t.index(genotyp_potomek)]
            pula_potomkow.append(potomek)
            fenotyp_potomkow.append(os_y[os_x.index(potomek)])

            # Nowa pula rodzicielska tylko z osobników potomnych
            fenotyp_pokolenia = fenotyp_potomkow
            pula_pokolenia = pula_potomkow
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
            genotyp_rodzicow.clear()
            pula_rodzicow.clear()

            for i in fenotyp_rodzicow:
                nowy_rodzic = pula_pokolenia[fenotyp_pokolenia.index(i)]
                pula_rodzicow.append(nowy_rodzic)
                genotyp_rodzicow.append(chromosomy_t[os_x.index(nowy_rodzic)])

            if plotting == 1:
                plt.pause(0.1)

    if plotting == 1:
        plt.plot(pula_pokolenia[fenotyp_pokolenia.index(max(fenotyp_rodzicow))], najlepszy_osobnik, 'go')
        if r > 0:
            plt.suptitle("Największa liczba osobników: " + str(round(max(fenotyp_rodzicow),4)) + ", w czasie t = "
                         + str(round(pula_rodzicow[fenotyp_rodzicow.index(max(fenotyp_rodzicow))],4)))
        else:
            plt.suptitle("Najmniejsza liczba osobników: " + str(round(max(fenotyp_rodzicow),4)) + ", w czasie t = "
                         + str(round(pula_rodzicow[fenotyp_rodzicow.index(max(fenotyp_rodzicow))],4)))
        plt.savefig('models/modelVerhulst_discrete4.png')
        plt.show()
    return pokolenie, najlepszy_osobnik
