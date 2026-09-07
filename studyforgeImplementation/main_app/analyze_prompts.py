import re

with open('studyforge_main.html', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'const DEFAULT_PROMPTS = \{([\s\S]*?)\};', content)
if m:
    block = m.group(1)
    keys = re.findall(r'^\s*([a-zA-Z0-9_]+):', block, re.MULTILINE)
    print("PROMPTS:")
    for k in keys:
        print(k)
else:
    print("DEFAULT_PROMPTS not found")
