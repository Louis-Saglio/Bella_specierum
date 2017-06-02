from random import randint, choice
from module import give_name


class ReproductionError(BaseException):
    pass


class MergingDifferentGenesError(ReproductionError):
    pass


class Gene:

    def __init__(self):
        self.nom = give_name(3)
        self._alleles = [give_name(2), give_name(2)]
        self._dominant = choice(self.alleles)
        self._apparence = self.dominant
        self.bonus = {
            self.alleles[0]: [give_name(2) for _ in range(randint(0, randint(3, 10)))],
            self.alleles[1]: [give_name(2) for _ in range(randint(0, randint(3, 10)))]
        }

    def __str__(self):
        return f"Non : {self.nom}\nAlleles : {self.alleles}\nDominant : {self.dominant}\nBonus : {self.bonus}\n\n"

    @property
    def apparence(self):
        return self.dominant if self.dominant in self.alleles else choice(self.alleles)

    @property
    def dominant(self):
        return self._dominant

    @dominant.setter
    def dominant(self, new):
        self._dominant = new

    @property
    def alleles(self):
        return self._alleles

    @alleles.setter
    def alleles(self, new):
        self._alleles = new

    def merge(self, other):
        """
        :type other Gene
        """
        if self.nom != other.nom:
            raise MergingDifferentGenesError
        bebe = Gene()
        bebe.nom = self.nom
        bebe.alleles = [self.alleles[randint(0, 1)], other.alleles[randint(0, 1)]]


class Sexe(Gene):

    def __init__(self):
        super().__init__()
        self.nom = "sexe"
        self.allele = ["male", "femelle"]
        self.bonus = [["femelle"], []]


class Caryotype(list):

    def __init__(self, pere=None, mere=None) -> None:
        """
        :type pere Caryotype
        :type mere Caryotype
        """
        super().__init__()
        self.apparence = [a.apparence for a in self]
