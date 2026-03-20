import os

# Create nested directories: folder/subfolder
# exist_ok=True → prevents error if already exists
os.makedirs("folder/subfolder", exist_ok=True)

# List all files/folders in current directory
print(os.listdir("."))

# Get current working directory path
print(os.getcwd())

# Remove subfolder first (must be empty)
os.rmdir("folder/subfolder")

# Then remove parent folder
os.rmdir("folder")

#os.listdir() returns a list of all files and folder names (as strings) in the specified directory path