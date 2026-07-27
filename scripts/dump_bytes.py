p='modules/lithium_education.py'
with open(p,'rb') as f:
    for i,line in enumerate(f,1):
        if 1246 <= i <= 1260:
            print(i, line)
