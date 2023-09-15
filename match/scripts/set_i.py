import pandas as pd 
import pyperclip as py
import regex as re
input = py.paste()  # Get the number variable from the environment variables.

matches = re.findall('^i-\w{17}$', input, re.MULTILINE)

if len(matches) > 0:
    input = matches[0]
    # print(matches[0])
else:
    print('No matches found.')
    
path = r'C:\Users\jbay\AppData\Roaming\espanso\match\scripts\i_codes.csv'

df = pd.read_csv(path)

df.loc[0, df.columns[0]] = input

df.to_csv(path, index=False)

print('Done.')