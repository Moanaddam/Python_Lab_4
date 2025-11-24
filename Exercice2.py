from abc import ABC, abstractmethod
import math

class ColorMixin:
    def __init__(self, couleur, *args, **kwargs):
        self._couleur = couleur
        super().__init__(*args, **kwargs)

    def __str__(self):
        parent_str = super().__str__()
        return f"{parent_str} | Couleur: {self._couleur}"

class Forme(ABC):
    @abstractmethod
    def aire(self):
        pass

    def __str__(self):
        return f"{self.__class__.__name__} – aire : {self.aire():.2f}"

class Cercle(ColorMixin, Forme):
    def __init__(self, rayon, couleur):
        self._rayon = rayon
        super().__init__(couleur=couleur)

    @property
    def rayon(self):
        return self._rayon

    def aire(self):
        return math.pi * self.rayon ** 2

class Rectangle(Forme):
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur

    def aire(self):
        return self.largeur * self.hauteur

class Carre(Rectangle):
    def __init__(self, cote):
        if cote <= 0:
            raise ValueError("Le côté doit être strictement positif.")
        super().__init__(cote, cote)

    @property
    def cote(self):
        return self.largeur

    @cote.setter
    def cote(self, valeur):
        if valeur <= 0:
            raise ValueError("Le côté doit être strictement positif.")
        self.largeur = valeur
        self.hauteur = valeur

class Triangle(Forme):
    def __init__(self, base, hauteur):
        self.base = base
        self.hauteur = hauteur

    def aire(self):
        return 0.5 * self.base * self.hauteur

if __name__ == "__main__":
    formes_etendues = [
        Cercle(3, "Rouge"),
        Rectangle(4, 5),
        Carre(5),
        Triangle(6, 2),
    ]

    print("--- Affichage de la collection hétérogène étendue ---")
    for f in formes_etendues:
        print(f)