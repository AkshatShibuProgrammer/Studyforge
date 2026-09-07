import sys
import re

def main():
    filename = 'studyforge_main.html'
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return

    print("--- Finding steps ---")
    for i, line in enumerate(lines):
        if 'id="step-' in line:
            print(f"{i}: {line.strip()}")

if __name__ == '__main__':
    main()
