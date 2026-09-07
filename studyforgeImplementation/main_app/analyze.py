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

    print("--- Searching for appState ---")
    for i, line in enumerate(lines):
        if 'appState =' in line:
            print(f"{i}: {line.strip()}")

    print("\n--- Searching for Step/Screen/API declarations ---")
    pattern = re.compile(r'^\s*(const|let|var)\s+([A-Z][a-zA-Z0-9_]*)\s*=')
    namespaces = []
    for i, line in enumerate(lines):
        match = pattern.search(line)
        if match:
            namespaces.append(match.group(2))
            print(f"{i}: {line.strip()}")
            
    print(f"\nNamespaces found: {', '.join(namespaces)}")
    
    print("\n--- Searching for 50000 ---")
    for i, line in enumerate(lines):
        if '50000' in line:
            print(f"{i}: {line.strip()}")

if __name__ == '__main__':
    main()
