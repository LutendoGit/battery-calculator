#!/usr/bin/env python3
"""Find exact bracket mismatch in section 5.4"""

with open('modules/lithium_education.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract just section 5.4
start = content.find('"title": "5.4')
end = content.find('"title": "5.5', start)
section = content[start:end]

# Count brackets
open_br = section.count('{')
close_br = section.count('}')
open_sq = section.count('[')
close_sq = section.count(']')

print(f'Section 5.4:')
print(f'  Braces: {open_br} open, {close_br} close (diff: {open_br - close_br})')
print(f'  Brackets: {open_sq} open, {close_sq} close (diff: {open_sq - close_sq})')
print(f'\nTotal lines in section: {len(section.splitlines())}')
print(f'\nLast 5 lines of section:')
for line in section.splitlines()[-5:]:
    print(repr(line))
