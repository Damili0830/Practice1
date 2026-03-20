

# Open file in read mode ("r")
f = open("example.txt", "r")
# read() → reads entire file as ONE string
print(f.read())
# Always close file after using it
f.close()
# Open again to demonstrate other methods
f = open("example.txt", "r")
# readline() → reads ONLY ONE line
print(f.readline())
f.close()
# Open again
f = open("example.txt", "r")
# readlines() → reads ALL lines into a LIST
print(f.readlines())

f.close()