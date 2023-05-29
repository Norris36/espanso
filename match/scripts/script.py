import pyperclip

new_line = pyperclip.paste() + "; ;unknown\n"

path = r'C:\Users\jbay\AppData\Roaming\espanso\match\scripts\to_add.txt'

first_lines = open(path, "r").read()
textfile    = open(path, 'w')
textfile.write(first_lines)
textfile.write(new_line)
textfile.close()