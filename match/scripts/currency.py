import pyperclip as py
import regex as re

try: 
    
    x = py.paste()
    y = re.findall('\d+', x)[0]
    y = int(y) * 6.8
    z = f'100 USD [{y} DKK]'

    print(z)
except:
    print('bad format')