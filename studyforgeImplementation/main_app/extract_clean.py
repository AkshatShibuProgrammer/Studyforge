import os

def extract_html():
    master_path = r'F:\Code by Akshat\testgemini\studyforge\antigravity analysis\master_analysis.txt'
    out_path = r'F:\Code by Akshat\testgemini\studyforge\studyforgeImplementation\main_app\studyforge_main_clean.html'
    
    with open(master_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    html_lines = []
    in_block = False
    
    # We want to extract everything that is inside a markdown code block (```)
    # Actually, master_analysis.txt is an AI response.
    # The AI response is a single file split into multiple code blocks, e.g. ```html ... ```, ```javascript ... ```.
    # But wait, there is text BETWEEN the blocks! e.g. "Here is the rest of the code:"
    # We must EXCLUDE the text between the blocks!
    for line in lines:
        if line.strip().startswith('```'):
            in_block = not in_block
            continue
        if in_block:
            html_lines.append(line)
            
    with open(out_path, 'w', encoding='utf-8') as f:
        f.writelines(html_lines)
        
    print(f"Extracted {len(html_lines)} lines to {out_path}")

if __name__ == '__main__':
    extract_html()
