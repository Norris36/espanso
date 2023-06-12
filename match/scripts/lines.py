import re
import pyperclip

text = pyperclip.paste()    
# Add newlines after specific punctuation marks (.,?,!)
modified_text = re.sub(r'([.?!])', r'\1\n', text)

# Copy the modified text to the clipboard
pyperclip.copy(modified_text)

print("Modified text copied to clipboard")

