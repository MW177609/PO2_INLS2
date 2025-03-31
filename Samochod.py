# Deklaracja klasy
class Samochod:
    # Zmienne klasowe
    marka = None
    color = 0
    max_speed = None

    # Inicjalizator (Konstruktor) klasy, wywoływany podczas tworzenia instancji
    # self (odpowiednik this ) - zmienna pozwalajaca na dostanie sie do zmiennych 
    # klasowych, metod itd
    def __init__(self):
        pass

    # Definicja medody(funkcji w klasie) / akcja
    def speed(self, currentSpeed):
        if currentSpeed == 10:
            # odwolanie albo wywolanie samej siebie to rekurencja
            return self.speed
        self.max_speed = currentSpeed
        return currentSpeed
    

# Przypisanie zmiennej do klasy skutkuje referencja - czyli przejeciem "wlasciwosci" klasy
fiat = Samochod()
fiat.max_speed = 10
fiat.color = 'rozowy'
fiat.marka = "BMW"
fiat.speed(400)

print(fiat.color)

bmw = fiat
bmw.color = "czarny"

print(fiat.color)
print(bmw.color)