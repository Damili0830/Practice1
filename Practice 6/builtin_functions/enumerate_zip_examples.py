# Two lists
names = ["A", "B", "C"]
scores = [10, 20, 30]

# enumerate() → gives index + value
for i, name in enumerate(names):
    print(i, name)

# zip() → pairs elements from multiple lists
for name, score in zip(names, scores):
    print(name, score)

# Variable with string type
x = "123"

# Print type of variable
print(type(x))

# Convert string → integer
y = int(x)

# Print new type
print(type(y))