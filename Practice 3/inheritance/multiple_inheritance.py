class Mammal:
    def give_birth(self):
        print("The animal gives live birth.")
class WingedAnimal:
    def can_fly(self):
        print("The animal can fly.")
# The Bat class inherits from both Mammal and WingedAnimal
class Bat(Mammal, WingedAnimal):
    pass
# Create an object of the Bat class
my_bat = Bat()
# Access methods from the Mammal class
my_bat.give_birth()
# Access methods from the WingedAnimal class
my_bat.can_fly()
