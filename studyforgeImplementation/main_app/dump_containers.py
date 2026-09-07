import re
with open('studyforge_main.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const CONTAINERS = \{[\s\S]*?\n    \};', text)
if m:
    print(m.group(0)[:1500])
else:
    print("Not found")
