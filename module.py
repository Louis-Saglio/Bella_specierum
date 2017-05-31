import time
import timeit
from random import randint
from pprint import pprint


def pause():
    debut = time.time()

    while time.time() == debut:
        pass


def rand1(chars: str):
    chars = chars.replace('.', "0")
    rep = 0
    for l in chars:
        rep += int(l)
    return rep


def rand(chaine):
    chaine = str(rand1(str(chaine)))
    while len(chaine) > 1:
        chaine = str(rand1(chaine))
    return chaine


def aleatoire():
    pause()
    return rand(str(time.time()))


def stat(nbr=1000, verbose=False):

    rep = []
    for i in range(nbr):
        val = aleatoire()
        rep.append(val)

    resume = {}
    for n in range(0, 10):
        qtt = rep.count(str(n))
        pct = round((100 * qtt) / len(rep), 3)
        if verbose:
            print(f"{n} :\t{qtt}\tsoit\t{pct} %")
        resume[n] = {"pct": pct, "nbr": qtt}

    val = [n["pct"] for n in resume.values()]
    maxi = max(val)
    mini = min(val)

    resume["ecart"] = round(maxi - mini)
    resume["nbr"] = nbr

    if verbose:
        print(f"\nEcart max : {resume['ecart']}")
        print(f"Nombre de tests : {nbr}")

    return resume


def run_stat(mode="stat", nbr=1000):
    if mode != "timeit":
        deb = time.time()
        if "stat" in mode:
            verbose = True if '-v' in mode else False
            stat(nbr, verbose)
        if mode == "classique":
            for i in range(nbr):
                a = aleatoire()
        temps = round(time.time() - deb, 2)
        print(f"\nTemps d'exécution : {temps} secondes. Soit une moyenne de {round((temps * 1000) / nbr, 2)} millième "
              f"de seconde par test")
    else:
        name_space = locals()
        name_space.update({"aleatoire": aleatoire})
        temps = timeit.timeit("aleatoire()", globals=name_space, number=nbr) / nbr
        print(f"{temps * 1000} millième de seconde par test")


if __name__ == '__main__':
    run_stat("stat -v", 10)
