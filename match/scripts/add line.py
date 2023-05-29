import yaml
import pyperclip as py

def add_string_to_yaml_file(path, string_to_add):
    with open(path, 'a') as file:
        file.write(string_to_add)

x = py.paste()
x = x.split('\n')
trigger = x[0].strip()
replace = x[1].strip()
y = '    - trigger: "{trigger}" \n      replace: "{replace}"\n      propagate_case: true\n      word: true\n'
formatted_y = y.format(trigger=trigger, replace=replace)

path = r'C:\Users\jbay\AppData\Roaming\espanso\match\_email.yml'

add_string_to_yaml_file(path = path,
                        string_to_add=formatted_y)


z = f'added t:{trigger}, r:{replace}'

print(z)