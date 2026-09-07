lines = open('studyforge_main.html', encoding='utf-8').readlines()
with open('step3_dump.txt', 'w', encoding='utf-8') as f:
    for i, l in enumerate(lines):
        if 'Step3' in l or 'renderFeed' in l or 'appendCard' in l:
            f.write(f"{i}: {l.strip()}\n")
