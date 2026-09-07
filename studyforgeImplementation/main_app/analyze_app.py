import sys

def main():
    filename = 'studyforge_main.html'
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return

    with open('output_app.txt', 'w', encoding='utf-8') as out:
        app_start = -1
        for i, line in enumerate(lines):
            if 'const App =' in line:
                app_start = i
                break
                
        if app_start != -1:
            for i in range(app_start, min(app_start + 100, len(lines))):
                out.write(f"{i}: {lines[i]}")

if __name__ == '__main__':
    main()
