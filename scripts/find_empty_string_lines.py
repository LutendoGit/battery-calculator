import re
p='modules/lithium_education.py'
with open(p,'r',encoding='utf-8') as f:
    for i,line in enumerate(f,1):
        if re.match(r'^\s*""\s*(,)?\s*$', line):
            print(i,repr(line.rstrip()))
