from pathlib import Path
p=Path('modules/lithium_education.py')
s=p.read_text(encoding='utf-8')
# positions found earlier
open_pos=19750
close_pos=24982

def pos_to_linecol(s,pos):
    line=s.count('\n',0,pos)+1
    lastnl=s.rfind('\n',0,pos)
    col=pos-lastnl
    return line,col

print('open at',pos_to_linecol(s,open_pos))
print('close at',pos_to_linecol(s,close_pos))

# show 10 lines around open
lines=s.splitlines()
open_line,open_col=pos_to_linecol(s,open_pos)
start=max(0,open_line-6)
end=min(len(lines),open_line+5)
print('\n--- Context around opener ---')
for i in range(start,end):
    print(f'{i+1:4}: {lines[i]}')

close_line,close_col=pos_to_linecol(s,close_pos)
start=max(0,close_line-6)
end=min(len(lines),close_line+5)
print('\n--- Context around closer ---')
for i in range(start,end):
    print(f'{i+1:4}: {lines[i]}')
