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
            if page.page_number == 6:
                text = page.extract_text()
    if text:
        return text
    else:
        return 'blank page results in NoneType object'

#run:
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', required=True,
                        help='path to pdf')
    args = parser.parse_args()
    test = pdfExperiment(args.file)
    #for thing in test:
    #    print(thing)
    print(repr(test[:1000]))
