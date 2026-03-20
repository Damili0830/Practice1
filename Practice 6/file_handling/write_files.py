# Open file in write mode ("w")
# If file exists → it will be overwritten
# If not → it will be created
f = open("example.txt", "w")
# Write multiple lines to file
f.write("Hello\nWorld\nPython")
# Close file to save changes
f.close()
# Open file in append mode ("a")
# It ADDS new content without deleting old
f = open("example.txt", "a")
# Add new line at the end
f.write("\nNew line added")
f.close()
# Open file again to read result
f = open("example.txt", "r")
# Print full content
print(f.read())

f.close()


#"x" - Create - will create a file, returns an error if the file exists
#"r" - Read - Default value. Opens a file for reading, error if the file does not exist
#"a" - Append - Opens a file for appending, creates the file if it does not exist
#"w" - Write - Opens a file for writing, creates the file if it does not exist
#"x" - Create - Creates the specified file, returns an error if the file exists
#"t" - Text - Default value. Text mode
#"b" - Binary - Binary mode (e.g. images)