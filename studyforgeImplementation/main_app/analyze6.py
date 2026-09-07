import sys

def main():
    filename = 'extracted_original.html'
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return

    print("--- Line 256 Context ---")
    for i in range(max(0, 250), min(260, len(lines))):
        print(f"{i+1}: {lines[i].rstrip()}")

if __name__ == '__main__':
    main()
