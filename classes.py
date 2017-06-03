"""
Implémenter :
    Position de l'Individu (2d ou 3d) qui influe sur le partenaire de reproduction et l'ennemi à attaquer
    Un support optionnel du temps modifiant la probabilité de reproduction et les chances de survies
    Un gestionnaire de mutatuion aléatoire
    Une class pour les genes (actuellement un dictionnaire)
Améliorer l'API avec :
    Une méthode d'espèce créant un indivinu original de l'espece en question
    Un moteur sommaire prenant en compte le temps
    Améliorer le générateur de nom (implémenter une classe) pour éviter les doublons et permettre des famille de nom
    Des exceptions personnalisées
Clarifier le code :
    Rédigeant la documentation
    Divisant en plus de fonction (tant pis pour l'optimisation)
    Commentant
    Remplaçant les tab par des ljust()
"""
from random import randint, choice
from copy import deepcopy
from statistics import mean
from time import time
# from module import aleatoire


def pause(temps):
    debut = time()
    while time() - debut < temps:
        pass


def give_name():
    nbr = randint(3, 8)
    consonnes = "zrtypqsdfghjklmwxcvbn"
    voyelles = "aeyuio"
    rep = choice(consonnes) if randint(0, 1) == 0 else choice(voyelles)
    # noinspection PyShadowingNames
    for i in range(nbr):
        rep += choice(consonnes) if i % 2 == 0 else choice(voyelles)
    return rep.title()


def donne_nom(maxi=8, rand=False, mini=3):
    if rand:
        nbr = randint(mini, maxi)
    else:
        nbr = maxi - 1
    consonnes = "zrtypqsdfghjklmwxcvbn"
    voyelles = "aeyuio"
    rep = choice(consonnes) if randint(0, 1) == 0 else choice(voyelles)
    # noinspection PyShadowingNames
    for i in range(nbr):
        rep += choice(consonnes) if i % 2 == 0 else choice(voyelles)
    return rep.title()


def moyenne(data, approximation=3):
    return round(mean(data), approximation)


class UnitTestPassingWhereasItShouldNot(BaseException):
    pass


class Espece:
    """
    Espece.liste_espece : -> Liste des especes instanciées (lst)
    self.nom : -> Nom de l'instance de l'espèce (str). Sert d'identifiant
    self.genes : -> Genes de l'espèce (dict)
    """

    liste_especes = []

    def __init__(self, nom=None, genes: dict=None, sexe=True):

        Espece.liste_especes.append(self)

        self.nom = nom if nom is not None else give_name()

        if genes is None:
            self.generate_genes()
        elif isinstance(genes, dict) and isinstance(list(genes.values())[0], list):
            self._genes = genes
        else:
            raise TypeError("Le paramètre genes doit être un dictionnaire dont les valeurs sont des list.")

        # New feature : Rendre le sexe facultatif
        if not isinstance(sexe, bool):
            raise TypeError
        if sexe is False:
            raise NotImplemented("Pour l'instant les espèces sont forcément sexués.")
        else:
            self.genes["sexe"] = ['X', 'Y']
            self.dominants["sexe"] = "Y"

    @property
    def genes(self):
        self.__dict__['genes'] = self._genes
        # noinspection PyAttributeOutsideInit
        # self._genes_old sert à savoir si self.gene a été modifié. Ex: self.genes['bidule'] = 'toto'
        self._genes_old = deepcopy(self._genes)
        return self._genes

    @property
    def dominants(self):
        if self._genes != self._genes_old:
            self.find_dominants()
        self.__dict__['dominants'] = self._dominants
        return self._dominants

    def find_dominants(self):
        if '_dominants' not in self.__dict__:
            # noinspection PyAttributeOutsideInit
            self._dominants = {}
        for key, val in self._genes.items():
            # Si ce gêne vient d'être ajouté
            if key not in self._dominants:
                self._dominants[key] = choice(val)
            # Si ce gêne a été modifié
            elif val != self._genes_old[key]:
                self._dominants[key] = choice(val)

    def __str__(self):
        rep = ''
        for key, val in self.__dict__.items():
            rep += f"{key.ljust(15, ' ')}\t:\t{val}\n"
        return rep

    def generate_genes(self):
        self._genes = {}
        for i in range(randint(2, 7)):
            self._genes[donne_nom(4)] = [choice(range(1, 20)), choice(range(1, 20))]
        self.find_dominants()


class Individu:

    def __init__(self, espece: Espece, genes: dict=None):
        self.nom = give_name()
        self.genes = genes
        if genes["sexe"] is None:
            genes["sexe"] = ['X', 'X'] if randint(0, 1) == 0 else ["X", "Y"]
        self.espece = espece
        self.apparents = self.synchronise_genes()
        self.population = Population()
        self.population.nom = "Aucune"
        self.moyenne = mean([g for g in self.apparents.values() if (isinstance(g, int) or isinstance(g, float))])

    def synchronise_genes(self):
        apparents = {}
        for key, val in self.genes.items():
            apparents[key] = self.espece.dominants[key] if self.espece.dominants[key] in val else choice(val)
        return apparents

    def seduire(self, other):
        """
         :type other Individu
        """
        if self.moyenne - randint(-2, +2) >= other.moyenne and self.apparents["sexe"] != other.apparents["sexe"]:
            return True

    def __add__(self, other):
        """
        :param other: Individu
        :type other: Individu
        :return: Un individu héritant des gênes de ses parents ou None
        """
        if self.seduire(other) and self.espece.nom == other.espece.nom:
            pere, mere = self.genes, other.genes
            bebe = {}
            for key in pere:
                p_index = randint(0, len(pere[key]) - 1)
                m_index = randint(0, len(mere[key]) - 1)
                if key in mere:
                    bebe[key] = [pere[key][p_index], mere[key][m_index]]
                else:
                    if randint(0, 1) == 0:
                        bebe[key] = pere[key][p_index]
            for key in mere:
                p_index = randint(0, len(pere[key]) - 1)
                m_index = randint(0, len(mere[key]) - 1)
                if key in pere:
                    bebe[key] = [pere[key][p_index], mere[key][m_index]]
                else:
                    if randint(0, 1) == 0:
                        bebe[key] = pere[key][p_index]
            return Individu(bebe, self.espece)
        else:
            return None

    def attaquer(self, other):
        s, o = self.moyenne, other.moyenne
        if s > o:
            other.mourir()
        elif o > s:
            self.mourir()
        if s == o:
            choice((self, other)).mourir()

    def set_sexe(self, new: list):
        self.genes["sexe"] = new
        self.synchronise_genes()

    def __str__(self):
        rep = f"Nom\t\t\t\t:\t{self.nom}\nEspece\t\t\t:\t{self.espece.nom}\nPopulation\t\t:\t{self.population.nom}\n"
        for attribut, valeur in self.genes.items():
            attr = f"{attribut}".ljust(15, ' ')
            if attribut == "espece" or attribut == "population":
                val = f"{valeur.nom}".ljust(15, ' ')
            elif attribut != "population":
                val = f"{valeur}".ljust(15, ' ')
            rep += f"{attr}\t:\t{val}\t\t{self.apparents[attribut]}\n"
        return rep + '\n\n'

    def mourir(self):
        if self.population is not None:
            self.population.remove(self)
        del self


class Population(list):

    def __init__(self) -> None:
        super().__init__()
        self.liste_especes = []
        nom = give_name()
        self.nom = "Les " + nom + ("n" if nom[-1] in "aei" else '') + "ais"

    def reproduire(self):
        rep = deepcopy(self)
        for n in rep:
            bebe = n + choice(self)
            if bebe is not None:
                self.append(bebe)

    def attaquer(self, ennemis, verbose=False):
        nbr_combattants = (len(self), len(ennemis))
        for n in range(max(nbr_combattants)):
            if len(self) > 0 and len(ennemis) > 0:
                choice(self).attaquer(choice(ennemis))
        if verbose:
            nbr_morts_self = nbr_combattants[0] - len(self)
            nbr_morts_ennemis = nbr_combattants[1] - len(ennemis)
            for pop in [self, ennemis]:
                print(f"Les {pop.nom} ont subi {nbr_morts_self if pop == self else nbr_morts_ennemis} mort(s)")

    def append(self, obj: Individu):
        super().append(obj)
        obj.population = self
        if obj.espece.nom not in self.liste_especes:
            self.liste_especes.append(obj.espece.nom)

    def auto_peupler(self, especes: tuple, nbr: int):
        # noinspection PyShadowingNames
        for i in range(nbr):
            espece = choice(especes)
            self.append(Individu(espece.genes, espece))

    def remove(self, obj) -> None:
        super().remove(obj)
        if obj.espece.nom in self.liste_especes and obj.espece.nom not in [i.espece.nom for i in self]:
            self.liste_especes.remove(obj.espece.nom)

    def bilan(self):
        noms = [i.nom for i in self]
        scp = [i.espece.nom for i in self]
        esp = {}
        for e in self.liste_especes:
            esp[e] = str(scp.count(e)) + " soit " + str(round((scp.count(e) * 100) / len(self), 1)) + '%'
        sexes = {"Y": len([i.apparents["sexe"] for i in self if i.apparents["sexe"] == "Y"])}
        sexes["X"] = len(self) - sexes["Y"]
        sexes["X"] = str(sexes["X"]) + " soit " + str(100 - int(sexes["Y"])) + '%'
        sexes["Y"] = str(sexes["Y"]) + " soit " + str(round((sexes["Y"] * 100 / len(self)), 2)) + '%'

        rep = f"Nom\t\t\t:\t{self.nom}\nTaille\t\t:\t{len(self)}\nIndividus\t:\t{noms}" \
              f"\nEspèces\t\t:\t{esp}\nSexes\t\t:\t{sexes}"
        return rep + '\n\n'

    def __str__(self, verbose=False):
        rep = self.bilan()
        if verbose:
            for indiv in self:
                rep += indiv.__str__()
        return rep + '\n'


def tester():
    e1 = Espece('abeille')
    p1 = Population()
    i1 = Individu(e1.genes, e1)
    i2 = Individu(e1.genes, e1)
    p1.append(i1)
    p1.append(i2)
    # i1.set_sexe(['X', 'Y'])
    # i2.set_sexe(['X', 'X'])
    i3 = i1 + i2
    if i3 is not None:
        p1.append(i3)
    print(p1.__str__(True))


def test_new():
    e = Espece("hommes")
    e1 = Espece("elfes")
    p = Population()
    p.auto_peupler((e, e1), 100)
    print(p)
    p1 = Population()
    p1.auto_peupler((e, e1), 100)
    print(p1)
    for _ in range(100):
        p.reproduire()
        p1.reproduire()
        if _ % 100 == 0:
            p.attaquer(p1, True)
            p1.attaquer(p, True)
        if len(p) * len(p1) == 0:
            break
    print("\n" + p.__str__(True))
    print(p1.__str__(True))


# noinspection PyUnusedLocal
def espece_unittest():
    try:
        a = Espece(genes={"e": 5, "r": 8})
        raise UnitTestPassingWhereasItShouldNot
    except TypeError:
        a = Espece()
        a = Espece("Homme", {"gene1": [1, 2], 'gene2': [1, 3, 5]}, sexe=True)
        assert a.nom == "Homme"
        assert "sexe" in a.genes
    print(a)


def individu_unittest():
    a = Espece()
    i = Individu(a, a.genes)
    j = Individu(a, a.genes)
    i.set_sexe(['X', 'Y'])
    j.set_sexe(['X', 'X'])
    assert i.apparents["sexe"] == 'Y'
    assert j.apparents["sexe"] == 'X'
    k = i + j
    print(i, j, k)


if __name__ == '__main__':
    # test_new()
    # tester()
    espece_unittest()
    # individu_unittest()
