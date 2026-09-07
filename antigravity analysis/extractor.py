import argparse
import os

def extract_pdf(file_path):
    import PyPDF2
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_html(file_path):
    from bs4 import BeautifulSoup
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text(separator='\n')
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

def extract_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

def main():
    parser = argparse.ArgumentParser(description="Extract text from PDF, HTML, or TXT and append to a file.")
    parser.add_argument("--source", required=True, help="Path to the source file.")
    parser.add_argument("--dest", required=True, help="Path to the destination text file.")
    parser.add_argument("--label", required=True, help="Label to prepend to the extracted text.")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.source):
        print(f"Error: Source file '{args.source}' does not exist.")
        return

    ext = os.path.splitext(args.source)[1].lower()
    
    try:
        if ext == '.pdf':
            content = extract_pdf(args.source)
        elif ext == '.html' or ext == '.htm':
            content = extract_html(args.source)
        else:
            content = extract_text_file(args.source)
            
        # Append to destination
        with open(args.dest, 'a', encoding='utf-8') as out_file:
            out_file.write(f"\n{'='*60}\n")
            out_file.write(f"--- START OF EXTRACTION: {args.label} ---\n")
            out_file.write(f"--- SOURCE FILE: {os.path.basename(args.source)} ---\n")
            out_file.write(f"{'='*60}\n\n")
            out_file.write(content)
            out_file.write(f"\n\n--- END OF EXTRACTION: {args.label} ---\n")
            
        print(f"Successfully appended {len(content)} characters from '{args.source}' to '{args.dest}'.")
        
    except Exception as e:
        print(f"Failed to process {args.source}: {e}")

if __name__ == "__main__":
    main()
