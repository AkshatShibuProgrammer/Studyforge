import re

with open(r'F:\Code by Akshat\testgemini\studyforge\resource\notes\new architect\StudyForge_Document_3_Canonical_Stored_Prompt_Library.md', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'## AI-07A[\s\S]*?```text\n([\s\S]*?)\n```', text)
if m:
    print(m.group(1).strip())
else:
    print("Not found")
