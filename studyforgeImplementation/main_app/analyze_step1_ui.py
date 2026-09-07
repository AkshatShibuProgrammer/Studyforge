import sys

def main():
    filename = 'studyforge_main.html'
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return

    with open('output_step1_ui.txt', 'w', encoding='utf-8') as out:
        start_idx = -1
        end_idx = -1
        for i, line in enumerate(lines):
            if 'id="step-1"' in line:
                start_idx = i
            if start_idx != -1 and 'id="step-2"' in line:
                end_idx = i
                break
                
        if start_idx != -1:
            if end_idx == -1: end_idx = start_idx + 200
            for i in range(start_idx, end_idx):
                out.write(f"{i+1}: {lines[i]}")

if __name__ == '__main__':
    main()
