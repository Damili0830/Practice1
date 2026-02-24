 #Task 1
 def squares_generator(N):
    """Generator that yields squares from 0 to N"""
    for i in range(N + 1):
        yield i * i  # yield returns one value at a time
# Test
N = 10
print(f"Squares 0 to {N}:")
for square in squares_generator(N):
    print(square, end=" ")
print()
#Task 2
def even_numbers(n):
    """Generator for even numbers 0 to n"""
    for i in range(0, n + 1, 2):  # step by 2
        yield i

# Get input
n = int(input("Enter n: "))
evens = list(even_numbers(n))  # convert generator to list
print(", ".join(map(str, evens)))  # comma-separated output

#Task 3
def divisible_by_3_and_4(n):
    """Generator for numbers divisible by both 3 and 4 (LCM=12)"""
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:  # divisible by both
            yield i
# Test
n = 50
result = list(divisible_by_3_and_4(n))
print(f"Numbers divisible by 3 and 4 (0-{n}):")
print(", ".join(map(str, result)))

#Task 4
def squares(a, b):
    """Generator for squares of numbers from a to b"""
    for i in range(a, b + 1):
        yield i * i
# Test with for loop
a, b = 5, 15
print(f"Squares {a} to {b}:")
for square in squares(a, b):
    print(square, end=" ")
print()

#Task 5
def countdown(n):
    """Generator that counts down from n to 0"""
    for i in range(n, -1, -1):  # start, stop, step
        yield i
# Test
n = 10
print(f"Countdown {n} to 0:")
print(" → ".join(map(str, list(countdown(n)))))
