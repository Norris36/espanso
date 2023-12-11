# the goal with this script is to take the clipboard check that it has less than 3 spaces, no lines, and under 30 chars, if so, it should add a set of lines to the file package.yml in the packages/name-fixer folder
# the lines shoulder by the clipboard, stripped of info, plus - trigger: in front then the next line should be the clibpard titel cased, and then the next line should be word = true if there is no spaces in it
# lets import the necessary stuff
import pyperclip

# lets get the clipboard
clipboard = pyperclip.paste()

# lets check if the clipboard is empty
if clipboard == "":
    print('Nothing in clip')
elif len(clipboard.split(' ')) > 3:
    print('Clip has to many spaces')
elif len(clipboard) > 30:
    print('Clip is too long')
else:
    clipboard = clipboard.strip()
    if len(clipboard.split(' ')) == 1:
        new_line = f"  - regex: {clipboard}\n    replace: {clipboard.title()}\n    word: true\n"
    else:
        new_line = f"  - trigger: '{clipboard}'\n    replace: '{clipboard.title()}'\n"
        
    # now lets open the path and check the last line in the file
    # if it is not an empty line, lets first add an empty line
    # when we've done so, then lets add the new_line var to the file, followed by a new empty line
    path = r'C:\Users\jbay\AppData\Roaming\espanso\match\packages\name fixer\package.yml'
    
    with open(path, 'r') as file:
        lines = file.readlines()
        
    if lines[-1] != '\n':
        lines.append('\n')
    
    lines.append(new_line)
    lines.append('\n')
    
    with open(path, 'w') as file:
        file.writelines(lines)
        
    print('Done')