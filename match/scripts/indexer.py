# lets write a script which takes the clipboard and indexes each of the lines and returns it
# lets import the necessary stuff
import pyperclip
# lets get the clipboard
clipboard = pyperclip.paste()
# lets split the clipboard by line
clipboard = clipboard.split('\n')
# lets create a new string
new_clipboard = ''
# lets loop through the clipboard
for index, line in enumerate(clipboard):
    # lets add the index to the line
    new_clipboard += f'{index + 1}. {line}\n'
# lets copy the new_clipboard to the clipboard
pyperclip.copy(new_clipboard)
print('Done')