p='modules/lithium_education.py'
with open(p,'r',encoding='utf-8') as f:
    for i,line in enumerate(f,1):
        if 1248 <= i <= 1260:
            print(f"{i}: {line.rstrip()!r}")
