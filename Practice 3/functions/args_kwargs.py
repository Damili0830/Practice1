#The *args parameter allows a function to accept any number of positional arguments.
def my_function(*args):
  print("Type:", type(args))
  print("First argument:", args[0])
  print("Second argument:", args[1])
  print("All arguments:", args)

my_function("Emil", "Tobias", "Linus")

#Type: <class 'tuple'>
#First argument: Emil
#Second argument: Tobias
#All arguments: ('Emil', 'Tobias', 'Linus')


#The **kwargs parameter allows a function to accept any number of keyword arguments.
def my_function(**kid):
  print("His last name is " + kid["lname"])

my_function(fname = "Tobias", lname = "Refsnes")

#His last name is Refsnes