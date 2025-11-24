class Animal:
    def parler(self):
        raise NotImplementedError("Cette méthode doit être redéfinie")

class Chien(Animal):
    def parler(self):
        return "Ouaf !"

class Chat(Animal):
    def parler(self):
        return "Miaou !"

class Vache(Animal):
    def parler(self):
        return "Meuh !"

class Robot:
    def parler(self):
        return "Bip bop. Communication vocale activée."

def faire_parler(animal):
    print(animal.parler())

animaux_et_robots = [
    Chien(),
    Chat(),
    Vache(),
    Robot()
]

print("--- Résultat de la collection hétérogène ---")
for a in animaux_et_robots:
    faire_parler(a)