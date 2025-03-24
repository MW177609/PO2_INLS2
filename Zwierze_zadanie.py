from abc import ABC, abstractmethod

# klasa abstrakcyjna
class Base(ABC):
    def __init__(self, name: str, year: int):
        self.name = name
        self.year = year

    @abstractmethod
    def info(self):
        pass

# klasa człowiek - dziedziczy po (Base)
class Czlowiek(Base):
    def __init__(self, name: str, year: int, profession: str):
        super().__init__(name, year)
        self.profession = profession # nowe pole (zawód)

    def info(self):
        return f"Człowiek: {self.name}, Rok urodzenia: {self.year}, Zawód: {self.profession}"

# klasa zwierze - dziedziczy po (Base)
class Zwierze(Base):
    def __init__(self, name: str, year: int, species: str):
        super().__init__(name, year)
        self.species = species # nowe pole (gatunek)

    def info(self):
        return f"Zwierze: {self.name}, Rok urodzenia: {self.year}, Gatunek: {self.species}"

# tworzenie obiektu
czlowiek = Czlowiek(name="Jan Kowalski", year=1990, profession="Inżynier")
zwierze = Zwierze(name="Reksio", year=2015, species="Pies")

# wypisanie informacji
print(czlowiek.info())
print(zwierze.info())