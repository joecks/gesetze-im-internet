
import glob
import re
import xml.etree.ElementTree as ET

def extract_text(element):
    text = element.text.strip() if element.text else ''
    for child in element:
        text += extract_text(child)
    return text

if __name__ == "__main__":
    files = glob.glob('data/items/**/*.xml')
    paragraphs = []
    for f in files:
        # ignore the attachments for now 
        if not re.match(r'data\/items\/_.+', f):
            tree = ET.parse(f)
            root = tree.getroot()
            for doc in root.iter('norm'):
                # date = doc.get('ausfertigung-datum')
                # print(doc.attrib['doknr'])
                for text in doc.iter('Content'):
                    t = extract_text(text)
                    paragraphs.append(t)
        
    print(len(paragraphs))
