import os

from PyPDF2 import PdfReader

# using script from:
# https://gist.github.com/nadya-p/373e1dc335293e490d89d00c895ea7b3
def scan(dir):
    for root, dirs,  files in os.walk(dir):
        for file in files:
            path_pdf = os.path.join(root, file)
            [stem, ext] = os.path.splitext(path_pdf)

            if ext == '.pdf':
                print("다음 파일  처리 중: " + path_pdf)

                reader = PdfReader(path_pdf)
                pages = reader.pages
                text = ""
                path_txt = stem + '.txt'

                for page in pages:
                    sub = page.extract_text()
                    text += sub

                with open(path_txt, 'w', encoding="utf-8") as txt_file:
                    print("다음 파일에 저장: " +path_txt)
                    txt_file.write(text)