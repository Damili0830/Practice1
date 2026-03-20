# reduce is not built-in → import from functools
from functools import reduce

# Sample list of numbers
numbers = [1, 2, 3, 4, 5]

# map() → applies function to each element
# lambda x: x * 2 → multiply each number by 2
mapped = list(map(lambda x: x * 2, numbers))
print(mapped)

# filter() → keeps elements that satisfy condition
# x % 2 == 0 → keep only EVEN numbers
filtered = list(filter(lambda x: x % 2 == 0, numbers))
print(filtered)

# reduce() → combines elements into ONE value
# lambda x, y: x + y → sum all numbers
reduced = reduce(lambda x, y: x + y, numbers)
print(reduced)