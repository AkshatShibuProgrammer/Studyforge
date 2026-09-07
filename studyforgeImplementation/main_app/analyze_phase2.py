import sys

def main():
    filename = 'studyforge_main.html'
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return

    with open('output_phase2.txt', 'w', encoding='utf-8') as out:
        start_idx = -1
        for i, line in enumerate(lines):
            if 'id="upload-container"' in line:
                start_idx = i
                break
        if start_idx != -1:
            for i in range(start_idx, min(start_idx + 50, len(lines))):
                out.write(f"{i+1}: {lines[i]}")

        out.write("\n\n--- JS ---\n\n")
        
        start_idx = -1
        for i, line in enumerate(lines):
            if 'handleAIDraft()' in line:
                start_idx = i
                break
        if start_idx != -1:
            for i in range(start_idx, min(start_idx + 40, len(lines))):
                out.write(f"{i+1}: {lines[i]}")
                if 'handlePaste()' in lines[i]:
                    break

if __name__ == '__main__':
    main()
