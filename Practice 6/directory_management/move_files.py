import shutil

# Move file to another directory
# example.txt → folder/example.txt
shutil.move("example.txt", "folder/example.txt")

# Copy file back from folder to current directory
shutil.copy("folder/example.txt", "example.txt")