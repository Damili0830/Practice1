import re
#task 1
text = input("1) Enter string for pattern 'a' followed by zero or more 'b': ")
pattern1 = r"ab*" # Define regex pattern: 'a' followed by zero or more 'b'
if re.fullmatch(pattern1, text): # Check if the whole string matches the pattern
    print("Match found")
else:
    print("No match")


#task 2
text = input("\n2) Enter string for pattern 'a' followed by two to three 'b': ")
pattern2 = r"ab{2,3}" # Define regex pattern: 'a' followed by 2 or 3 'b'
if re.fullmatch(pattern2, text):
    print("Match found")
else:
    print("No match")


# task 3
text = input("\n3) Enter string to find lowercase_with_underscore: ")
result3 = re.findall(r"[a-z]+_[a-z]+", text) # Find lowercase words connected with underscore
print("Matches:", result3)


# task 4
text = input("\n4) Enter string to find Capitalized words: ")
result4 = re.findall(r"[A-Z][a-z]+", text) # Find patterns like 'Hello', 'World'
print("Matches:", result4)


# task 5
text = input("\n5) Enter string that starts with 'a' and ends with 'b': ")
pattern5 = r"a.*b" # Define regex pattern: starts with 'a', ends with 'b'
if re.fullmatch(pattern5, text):
    print("Match found")
else:
    print("No match")


# task 6
text = input("\n6) Enter string to replace space, comma, dot with colon: ")
result6 = re.sub(r"[ ,\.]", ":", text) # Replace space, comma, or dot with colon
print("Result:", result6)


# task 7
text = input("\n7) Enter snake_case string: ")
parts = text.split("_") # Split string by underscore
camel_case = parts[0] + "".join(word.capitalize() for word in parts[1:]) # Convert to camelCase
print("camelCase:", camel_case)


# task 8
text = input("\n8) Enter string to split at uppercase letters: ")
result8 = re.findall(r"[A-Z][^A-Z]*", text) # Split string at uppercase letters
print("Result:", result8)


# task 9
text = input("\n9) Enter string to insert spaces before capitals: ")
result9 = re.sub(r"([A-Z])", r" \1", text).strip() # Insert space before each capital letter
print("Result:", result9)


# task 10
text = input("\n10) Enter camelCase string: ")
result10 = re.sub(r"([A-Z])", r"_\1", text).lower() # Insert underscore before capital letters and convert to lowercase
print("snake_case:", result10)