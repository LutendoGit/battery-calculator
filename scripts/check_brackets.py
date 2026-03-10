from pathlib import Path
p=Path('modules/lithium_education.py')
s=p.read_text(encoding='utf-8')
stack=[]
pairs={'(':')','[':']','{':'}'}
openers='([{' 
closers=')]}'
for idx,ch in enumerate(s,1):
    if ch in openers:
        stack.append((ch,idx))
    elif ch in closers:
        if not stack:
            print('Unmatched closer',ch,'at',idx)
            break
        last,pos=stack.pop()
        if pairs[last]!=ch:
            print('Mismatch: opener',last,'at',pos,'but closer',ch,'at',idx)
            break
else:
    if stack:
        for op,pos in stack:
            print('Unclosed',op,'from',pos)
    else:
        print('All matched')
