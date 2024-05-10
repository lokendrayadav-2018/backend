import requests
from bs4 import BeautifulSoup
from langdetect import detect, DetectorFactory
# import pdfplumber
import pytesseract
from PIL import Image
import pdf2image
DetectorFactory.seed = 0  # Ensure consistent langdetect behavior

def is_hindi(text):
    """Check if the text is predominantly in Hindi."""
    try:
        return detect(text) == 'hi'
    except:
        return False

def extract_hindi_content(url):
    """Extract meaningful Hindi content from the given URL, excluding modals."""
    response = requests.get(url)
    response.encoding = 'utf-8'  # Set correct encoding
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Remove script, style, and other non-content elements
    for tag in soup(["script", "style", "header", "footer", "nav", "iframe"]):
        tag.decompose()
    
    # Identify and decompose modal dialogs
    for modal in soup.find_all(['div', 'section', 'article'], class_=['modal', 'popup', 'overlay']):
        modal.decompose()

    # Extract text only from paragraphs that are likely to be content
    paragraphs = soup.find_all('p')
    hindi_content = []
    for p in paragraphs:
        text = p.get_text().strip()
        if text and is_hindi(text):
            hindi_content.append(text)

    return ' '.join(hindi_content)


def read_pdf(pdf_path):
    images = pdf2image.convert_from_path(pdf_path)
    text = ''
    for image in images:
        text += pytesseract.image_to_string(image, lang='hin')
    return text
