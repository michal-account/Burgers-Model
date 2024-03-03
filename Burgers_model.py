# import biblioteki numpy oraz dwoch funkcji z biblioteki math
import numpy as np
from math import log, pow


#########
# WEJSCIE

# naprezenie [Pa]
sigma0 = 18.75 * pow(10, 6)

# czas [s]
t1 = np.array([0., 20., 40., 60., 90., 120., 150., 180., 240., 
               360., 480., 600.])

# wydluzenie probki, czujnik prawy [mm]
l1p = np.array([0.92, 1.15, 1.75, 1.81, 1.87, 1.91, 1.95, 1.98, 2.02,
                2.30, 2.44, 2.51])

# dlugosc poczatkowa probki [mm]
l0 = 50.

# odksztalcenie probki z eskperymentu [-]
eps_dosw = l1p / l0

#############
# ROZWIAZANIE

# >> funkcja kryterialna
def f(x):
    # x - wektor zmiennych decyzyjnych -> w tym przypadku: x = [E1, eta1, E2, eta2]

    # wyznaczenie odpowiedzi modelu Burgersa dla danego wektora x
    eps_mod = sigma0 * (1./x[0] + t1/x[1] + (1./x[2]) * (1. - np.exp(-x[2] * t1 / x[3])))
    
    # funkcja zwraca roznice pomiedzy odpowiedzia modelu Burgersa oraz
    # odksztalceniem z proby doswiadczalnej; rozpisana za pomoca najmniejszych
    # kwadratow; mozna tez poprzez wartosc bezwzgledna -> 
    # np.sum(np.abs((eps_mod - eps_dosw) * (eps_mod - eps_dosw)))
    return np.sum(np.sqrt((eps_mod - eps_dosw) * (eps_mod - eps_dosw)))

# >> liczba iteracji (losowan)
# ! mozna modyfikowac !
liczba_iteracji = 10000

# >> glowna petla programu
for i in range(liczba_iteracji):
    # losowanie wektora zmiennych decyzyjnych x
    # - pow(10, 11) to 10^11,
    # - np.array([0.15, 5., 0.15, 5.]) odpowiada za skalowanie poszczegolnych
    #    skladowych wektora x,
    # - skalowanie jest potrzebne bo np.random.rand zwraca liczby od 0. do 1.
    # ! mozna modyfikowac !
    x = np.random.rand(4) * pow(10, 11) * np.array([0.15, 5., 0.15, 5.])
    
    # wyznaczenie wartosci funkcji kryterialnej dla aktualnego x
    jakosc_modelu = f(x)

    # w pierwszej iteracji aktualny x jest najlepszy
    if i == 0:
        fmin = jakosc_modelu
        xmin = x
    else:
        # w kolejnych iteracjach sprawdzamy, czy aktualny x jest najlepszy
        if jakosc_modelu < fmin:
            # najlepszy wynik zapisujemy
            fmin = jakosc_modelu
            xmin = x

# wyswietlenie uzyskanych wynikow na ekranie konsoli
print("wartosc min. to:", fmin)
print("fmin uzyskane dla nast. x:", xmin)


##########################
### Rysowanie wykresow ###

# caly ponizszy fragment mozna zakomentowac/usunac (od tej linijki do konca)
# wtedy wykres koncowy nie zostanie wyswietlony

# import biblioteki matplotlib do rysowania wykresow
import matplotlib.pyplot as plt

# wyznaczenie eps dla najlepszego zestawu parametrow (xmin)
x = xmin
eps_mod = sigma0 * (1./x[0] + t1/x[1] + (1./x[2]) * (1. - np.exp(-x[2] * t1 / x[3])))

# wykresy - doswiadczenie i Burgers
plt.plot(t1, eps_dosw, 'g', label="doswiadczenie")
plt.plot(t1, eps_mod, 'r', label="Burgers") 

# legenda
plt.legend()

# podpisy osi
plt.xlabel("t [s]")
plt.ylabel("eps [%]")