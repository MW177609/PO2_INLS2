# importujemy modół abc (abstract base classes)
from abc import ABC, abstractmethod

# definiujemy warstwę abstrakcyjną Shape dziedziczącą po ABC
class Base(ABC):
    # definiujemy metodę abstrakcyjną area, którą którą muszę implementować klasy dziedziczące
    @abstractmethod
    def area(self):
        pass

    # Definiujemy inną metodę abstrakcyjną
    @abstractmethod
    def perimeter(self):
        pass


class Rectangle(Base):
    # Konstruktor przyjmuje długość i szerokość prostokąta
    def __init__(self, length, width):
        # Przypisanie atrybutów instancji
        self.lenght = length
        self.width = width

    # Implementujemy wymaganą metodę area
    def area(self):
        # Zwracamy pole powierzchni prostokąta
        return self.lenght * self.width

    # Implementujemy wymaganą metodę perimeter
    def perimeter(self):
        # Zwracamy obwód prostokąta
        return 2 * (self.lenght + self.width)


rect = Rectangle(4, 5)
print("Pole prostokąta:", rect.area()) # Pole prostokąta: 20
print("Obwód prostokąta:", rect.perimeter()) #Obwód prostokąta: 18