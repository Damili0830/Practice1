class Cat:
    species = "Feline"

    def __init__(self, name):
        self.name = name
a = Cat("Fluffy")
b = Cat("Whiskers")

print(a.species)  # Feline
print(b.species)  # Feline
print(a.name)  # Fluffy
print(b.name)  # Whiskers