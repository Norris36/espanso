import pandas as pd 
import os 

input = os.getenv('ESPANSO_INPUT')  # Get the number variable from the environment variables.

path = r'C:\Users\jbay\OneDrive - GN Store Nord\Workspace\french\french_top_words.csv'

df = pd.read_csv(path, index_col=0)

y = ""

if input in df.english.values:
    out = df.loc[df.english == input, "french"].unique()
    put = ""
    for i in out:
        put += i + ", "
    y = put[:-2]
else:
    y = "Not found"
    
print(y)