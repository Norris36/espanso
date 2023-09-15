import os 

input = os.getenv('ESPANSO_INPUT')

input = input.replace('_', ' ')
input = input.capitalize()

test = '----------------------------------------------------------------'

if len(input) % 2 == 0:
    part = len(test) / 2 - len(input) / 2
else:
    part = (len(test) / 2 - len(input) / 2) + 1 
    
y = ''

for i in range(int(part)):
    y += '-'
    
if len(input) % 2 == 0:
    z = f"----------------------------------------------------------------\n{y}{input}{y}\n----------------------------------------------------------------"
    print(z) 
else:
    z = f"-----------------------------------------------------------------\n{y}{input}{y}\n-----------------------------------------------------------------"
    print(z)
    