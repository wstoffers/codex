#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
import os, re
import json
import codecs
import pdfplumber

#define:
def pdfExperiment(filePath):
    with pdfplumber.open(filePath) as pdf:
        for page in pdf.pages:
            if page.page_number == 7:
                words = page.extract_words(use_text_flow=True)
                everything = page.extract_text()
                break
    directory = os.path.dirname(filePath)
    with open(os.path.join(directory,'words.plumbing'),'w') as wordsLog:
        wordsLog.write(os.linesep.join([w['text'] for w in words]))
    with open(os.path.join(directory,'text.plumbing'),'w') as textLog:
        textLog.write(everything)
#run:
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', required=True,
                        help='path to pdf')
    args = parser.parse_args()
    pdfExperiment(args.file)
