from abc import ABC, abstractmethod

class CarBuilder():
    @abstractmethod
    def choose_model(self):
        pass

    @abstractmethod
    def choose_engine(self):
        pass

    @abstractmethod
    def choose_wheels(self):
        pass

    @abstractmethod
    def choose_color(self):
        pass

    @abstractmethod
    def build(self):
        pass

class CustomCar(CarBuilder):
    def __init__(self):
        self.car = {}

    def choose_model(self):
        self.car['model'] = input("Wybierz model samochodu:")

    def choose_engine(self):
        self.car['engine'] = input("Wybierz silnik samchodu:")

    def choose_color(self):
        self.car['color'] = input("Wybierz kolor samochodu:")

    def build(self):
        print("\nTwój samochód zastał zbudowany:")



car_builder = CustomCar()
car_builder.choose_model()
car_builder.choose_engine()
car_builder.choose_wheels()
car_builder.choose_color()
car_builder.build()