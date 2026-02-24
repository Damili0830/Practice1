#The math module is Python's built-in library providing mathematical
# functions and constants for complex calculations.

import math
degree = float(input("Input degree: "))
radian = degree * math.pi / 180
print("Output radian:", format(radian, ".6f"))
#format(radian, ".6f") — output exactly 6 decimal places

#task 2
import math
def trapezoid_area_math(base1, base2, height):
    # Using math.fsum for accurate floating point addition
    bases_sum = math.fsum([base1, base2])
    area = bases_sum * height / 2
    return area
height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))
area = trapezoid_area_math(base1, base2, height)
print(f"\nHeight: {height}")
print(f"Base, first value: {base1}")
print(f"Base, second value: {base2}")
print(f"Expected Output: {area}")


#task 3
import math
n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))
# Using math functions: math.pi, math.tan
area = (n * math.pow(s, 2)) / (4 * math.tan(math.pi / n))
print(f"The area of the polygon is: {area}")

#task 4
import math
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))
# Calculate area using math functions
area = math.fsum([base, height])  # WRONG - this adds, not multiplies
# Correct way: multiplication
area = base * height
print(f"Expected Output: {area}")