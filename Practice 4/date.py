#The datetime module is Python's built-in library for handling dates and times.

#Task 1 Subtract five days from current date
from datetime import datetime, timedelta  # Import required classes
today = datetime.now()
five_days_ago = today - timedelta(days=5) # Subtract 5 days using timedelta
print(five_days_ago)

#Task 2  Subtract five days from current date
from datetime import date, timedelta  # Import date and timedelta classes
today = date.today()
yesterday = today - timedelta(days=1) # Calculate yesterday and tomorrow
tomorrow = today + timedelta(days=1)
print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)

#Task 3 Drop microseconds from datetime
from datetime import datetime  # Import datetime class
now = datetime.now()
no_microseconds = now.replace(microsecond=0) # Remove microseconds by setting them to zero
print(no_microseconds)

#Task 4  Calculate two date difference in seconds
from datetime import datetime  # Import datetime class
date1 = datetime(2024, 1, 1, 12, 0, 0) # Define two datetime objects
date2 = datetime(2024, 1, 1, 12, 1, 30)
difference = date2 - date1  # This returns a timedelta objec
seconds = difference.total_seconds() # Convert the difference to seconds
print("Difference in seconds:", seconds)