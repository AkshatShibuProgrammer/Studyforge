with open('studyforge_main.html', encoding='utf-8') as f:
    for i, l in enumerate(f):
        if 'id="screen-' in l:
            print(f'{i+1}: {l.strip()}')
