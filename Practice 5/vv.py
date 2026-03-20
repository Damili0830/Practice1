import re
s= input()
pattern = r"\d"
find = re.findall(pattern, s)
if find:
    print(find)
else:
    print("   ")
