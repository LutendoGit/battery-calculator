p='modules/lithium_education.py'
bad=b'                    ""\r\n'
with open(p,'rb') as f:
    lines=f.readlines()
new=[]
removed=0
for L in lines:
    if L==bad:
        removed+=1
        continue
    new.append(L)
if removed:
    with open(p,'wb') as f:
        f.writelines(new)
    print('Removed',removed,'lines')
else:
    print('No matching lines found')
