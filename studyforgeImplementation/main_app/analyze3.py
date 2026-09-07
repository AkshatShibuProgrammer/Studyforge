import sys

def main():
    filename = 'studyforge_main.html'
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return

    print("--- HTML Body Snippet ---")
    body_start = -1
    for i, line in enumerate(lines):
        if '<body' in line:
            body_start = i
            break
            
    if body_start != -1:
        for i in range(body_start, min(body_start + 50, len(lines))):
            print(f"{i}: {lines[i].rstrip()}")
            
if __name__ == '__main__':
    main()
