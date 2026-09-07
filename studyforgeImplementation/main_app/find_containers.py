import os, re

out = open('containers_dump.txt', 'w', encoding='utf-8')
d = r'F:\Code by Akshat\testgemini\studyforge\resource\notes\new architect'
for f in os.listdir(d):
    path = os.path.join(d, f)
    if os.path.isfile(path):
        text = open(path, 'r', encoding='utf-8').read()
        for m in re.finditer(r'.{0,60}container.{0,60}', text, re.IGNORECASE):
            out.write(f"{f}: {m.group(0).strip()}\n")
out.close()
