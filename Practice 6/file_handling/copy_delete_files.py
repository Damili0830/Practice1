# shutil → used for copying files
import shutil
# os → used for file operations (delete, check existence)
import os
# Copy file: source → destination
shutil.copy("example.txt", "copy_example.txt")
# Check if copied file exists
if os.path.exists("copy_example.txt"):
  # Remove (delete) the file
  os.remove("copy_example.txt")

  #The os module in Python is a built-in standard library module
 # that provides a portable way to interact with the underlying operating system

 #shutil is a Python module that provides high-level operations for copying, moving,
# and deleting files and directories by wrapping system-level file operations into simple, optimized functions.