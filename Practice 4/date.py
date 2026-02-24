#Task 1 Subtract five days from current date
from datetime import datetime, timedelta  # Import required classes
# Get the current date and time
today = datetime.now()
# Subtract 5 days using timedelta
five_days_ago = today - timedelta(days=5)
# Print the result
print(five_days_ago)

#Task 2  Subtract five days from current date
from datetime import date, timedelta  # Import date and timedelta classes
# Get today's date
today = date.today()
# Calculate yesterday and tomorrow
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
# Print results
print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)

#Task 3 Drop microseconds from datetime
from datetime import datetime  # Import datetime class
# Get the current date and time
now = datetime.now()
# Remove microseconds by setting them to zero
no_microseconds = now.replace(microsecond=0)
# Print the datetime without microseconds
print(no_microseconds)

#Task 4  Calculate two date difference in seconds
from datetime import datetime  # Import datetime class
# Define two datetime objects
date1 = datetime(2024, 1, 1, 12, 0, 0)
date2 = datetime(2024, 1, 1, 12, 1, 30)
# Calculate the difference between the two dates
difference = date2 - date1  # This returns a timedelta objec
# Convert the difference to seconds
seconds = difference.total_seconds()
# Print the difference in seconds
print("Difference in seconds:", seconds)