import pyperclip

def make_citation():
    # now lets get the clipboard
    variable = pyperclip.paste()
    variables = variable.split('\n')
    # lets write a list comprehension which removes any empty strings
    variables = [v for v in variables if v != '']
    if len(variables) > 1:
        # now lets make sure that we remove the line breaks
        variable = ''
        for v in variables:
            v = v.strip()
            v = v + "', '"
            variable += v
        # now lets make sure that we add the citation
        variable = "'" + variable + "'"
        # now lets return the variable
    return variable

print(make_citation())