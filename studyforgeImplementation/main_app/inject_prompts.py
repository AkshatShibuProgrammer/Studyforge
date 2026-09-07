import json
import re

with open('extracted_prompts.json', 'r', encoding='utf-8') as f:
    prompts = json.load(f)

with open('studyforge_main.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Build the string to insert
insert_str = ""
for k, v in prompts.items():
    # Escape backticks
    escaped_v = v.replace('`', '\\`')
    insert_str += f"      {k}: `{escaped_v}`,\n"

# Find const DEFAULT_PROMPTS = {
pattern = r'const DEFAULT_PROMPTS = \{'
match = re.search(pattern, content)
if match:
    insert_pos = match.end()
    new_content = content[:insert_pos] + '\n' + insert_str + content[insert_pos:]
    with open('studyforge_main.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Prompts successfully injected!")
else:
    print("Could not find DEFAULT_PROMPTS.")
