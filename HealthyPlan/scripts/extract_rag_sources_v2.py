import os
import glob
import json
from bs4 import BeautifulSoup
from pypdf import PdfReader

raw_base_dir = r"data/rag/v2/raw_sources"

def extract_html(html_path):
    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Remove navigation, headers, footers, scripts, styles, aside elements
    for el in soup(["nav", "header", "footer", "aside", "script", "style", "iframe", "noscript"]):
        el.decompose()
        
    # Also look for common class/id patterns for navigation/header/footer/banners
    for c in ["menu", "navbar", "cookie-banner", "footer-links", "advertisement", "ad-container", "sidebar"]:
        for el in soup.find_all(class_=lambda x: x and c in x.lower()):
            el.decompose()
        for el in soup.find_all(id=lambda x: x and c in x.lower()):
            el.decompose()

    # Extract text content by preserving layout (headings, paragraphs, lists)
    lines = []
    for elem in soup.descendants:
        if elem.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            text = elem.get_text().strip()
            if text:
                lines.append(f"\n\n### {text}\n")
        elif elem.name == "p":
            text = elem.get_text().strip()
            if text:
                lines.append(f"\n{text}\n")
        elif elem.name == "li":
            text = elem.get_text().strip()
            if text:
                lines.append(f"- {text}")
                
    # Fallback to plain text if structured text is too short
    text_content = "".join(lines).strip()
    if len(text_content) < 100:
        text_content = soup.get_text(separator="\n")
        
    # Clean up redundant spaces and empty lines
    cleaned_lines = []
    for line in text_content.splitlines():
        cleaned_line = line.strip()
        if cleaned_line:
            cleaned_lines.append(cleaned_line)
        else:
            if cleaned_lines and cleaned_lines[-1] != "":
                cleaned_lines.append("")
                
    return "\n".join(cleaned_lines).strip()

def extract_pdf(pdf_path):
    print(f"  Extracting PDF: {pdf_path}")
    reader = PdfReader(pdf_path)
    extracted_pages = []
    
    # Extract page by page
    for idx, page in enumerate(reader.pages):
        page_num = idx + 1
        page_text = page.extract_text()
        if page_text.strip():
            extracted_pages.append(f"\n--- [Page {page_num}] ---\n{page_text}")
            
    return "\n".join(extracted_pages).strip()

def process_extractions():
    # Find all html and pdf files recursively under raw_sources
    categories = ["diabetes", "prediabetes", "hypertension", "ckd", "gout", "obesity", "general_safety"]
    
    for category in categories:
        category_dir = os.path.join(raw_base_dir, category)
        if not os.path.exists(category_dir):
            continue
            
        print(f"Processing category: {category}")
        
        # HTML files
        html_files = glob.glob(os.path.join(category_dir, "*.html"))
        for html_path in html_files:
            source_id = os.path.splitext(os.path.basename(html_path))[0]
            txt_path = os.path.join(category_dir, f"{source_id}.txt")
            
            # Extract
            print(f"  Extracting HTML: {os.path.basename(html_path)}")
            text = extract_html(html_path)
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)
                
            # Update metadata JSON
            meta_path = os.path.join(category_dir, f"{source_id}.metadata.json")
            if os.path.exists(meta_path):
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                meta["extraction_status"] = "extracted"
                with open(meta_path, "w", encoding="utf-8") as f:
                    json.dump(meta, f, indent=2, ensure_ascii=False)
                    
        # PDF files
        pdf_files = glob.glob(os.path.join(category_dir, "*.pdf"))
        for pdf_path in pdf_files:
            source_id = os.path.splitext(os.path.basename(pdf_path))[0]
            txt_path = os.path.join(category_dir, f"{source_id}.txt")
            
            text = extract_pdf(pdf_path)
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)
                
            # Update metadata JSON
            meta_path = os.path.join(category_dir, f"{source_id}.metadata.json")
            if os.path.exists(meta_path):
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                meta["extraction_status"] = "extracted"
                with open(meta_path, "w", encoding="utf-8") as f:
                    json.dump(meta, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    process_extractions()
    print("Source extraction completed.")
