from abc import ABC, abstractmethod

class Balwan:
    @abstractmethod
    def tworznie_balwana(self):
        pass

    @abstractmethod
    def eliminacja_balwana(self):
        pass

class CyrkNaKulkach(Balwan):

    def tworznie_balwana(self):
        return "Bałwan powstał"

    def eliminacja_balwana(self):
        return "Bałwan umarł"

class Cyrk(CyrkNaKulkach):
    pass


person = Cyrk()

print(person.tworznie_balwana())
print(person.eliminacja_balwana())