import os
import pyperclip as py

path = r'C:\Users\jbay\OneDrive - GN Store Nord\Workspace\today.txt'

with open(path, 'r') as f:
    lines = f.readlines()
    
    
    
in_clip =py.paste().strip()
clip = '\t[ ] - ' + in_clip
var = False

end = ""

with open(path, 'w') as f:
    for i in range(len(lines)):
        line = lines[i]
        if 'Brain Dump' in line:
            var = True
            
        if '[x]' in line:
            end += line
            line = ''
            
            
        if var:
            if i == len(lines)-1:
                f.write(line + '\n')
                f.write(clip + '\n')
                var = False
            elif len(line.strip()) > 0:
                f.write(line)
            else:
                f.write(clip + '\n')
                var = False
        else:
            
            f.write(line)
            
    #done_stuff = len(end.split('\n'))
    #f.write(f'----------------------------------------------------------------')
    f.write(end)
print('i added it to the list')
# Oneline comments, Dont Chug an expensive Wine
# :i added it to the list
# :i added it to the list
# i added it to the list
