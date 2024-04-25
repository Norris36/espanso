# Importing necessary modules
import os
import pyperclip as py
import regex as re

import pyperclip

# Get the content of the clipboard
clipboard = pyperclip.paste().encode('utf-8').decode('utf-8')

# Split the clipboard content into lines
lines = clipboard.split('\n')

# Get the first line from the clipboard content
important_line = lines[0]

# Define the path to the file to be read
path = r'C:\Users\jbay\OneDrive - GN Store Nord\Workspace\today.txt'

# Read the content of the file
with open(path, 'r') as file:
    data = file.read().split('\n')

# Remove the first line from the data
data = data[1:]

# This line sorts the 'data' list. The key for sorting is a lambda function that checks if '[x]' is in the string.
# The 'in' operator returns True if '[x]' is found in the string, and False otherwise.
# The 'lower()' function ensures the comparison is case-insensitive.
# The 'sorted()' function sorts the list in ascending order, so elements with '[x]' will be at the end of the list.
data = sorted(data, key=lambda x: '[x]' in x.lower())

# This line filters out empty lines from the 'data' list.
# The 'filter()' function applies a lambda function to each element in the 'data' list.
# The lambda function checks if the stripped string is not empty.
# The 'strip()' function removes leading and trailing whitespace from the string.
# The 'filter()' function returns an iterator, so 'list()' is used to convert it back to a list.
data = list(filter(lambda x: x.strip() != '', data))

# This 'if' statement checks if the string "braindump" is in 'important_line', ignoring case.
# If "braindump" is found, 'new_data' is set to the current 'data' list.
if "braindump" in important_line.lower():
    new_data = data
# If "braindump" is not found, a new line is added at the beginning of the 'data' list.
# The new line is formatted as '[ ] - {important_line.title()}', where 'important_line.title()' is the title-cased 'important_line'.
# The 'title()' function converts the first character of each word to uppercase and the rest to lowercase.
else:
    new_data = ['    [ ] - ' + important_line.title()] + data

# Add a separator line to the new_data list
new_data = ['--------------------------Brain Dump--------------------------------------'] + new_data

# Write the new_data to the file
with open(path, 'w') as file:
    file.write('\n'.join(new_data))

# Printing a message to indicate that the task has been completed
print('i added it to the list')
