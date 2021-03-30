#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
import os, re
import json
import warnings
import codecs
import pdfplumber

#define:
class extractor(object):
    def __init__(self, filePath):
        self.filePath = filePath

    def extract(self, pageNumber, percents):
        with pdfplumber.open(self.filePath) as pdf:
            page = pdf.pages[int(pageNumber)]
            crop = [float(p) for p in percents]
            width = float(page.width)
            height = float(page.height)
            subset = page.crop((crop[0]*width,
                                crop[1]*height,
                                crop[2]*width if len(crop)>2 else page.width,
                                crop[3]*height if len(crop)>3 else page.height))
            everything = subset.extract_text()
        return everything

def reformat(agglomerateString):
    lines = agglomerateString.split(os.linesep)
    prefix = ' '*12 + '"'
    suffix = '",'
    reformatted = [f'{prefix}{l}{suffix}' for l in lines]
    return reformatted
                
#run:
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', required=True,
                        help='path to pdf')
    parser.add_argument('--page', '-p', required=True,
                        help='page in pdf')
    parser.add_argument('--cropping', '-c', nargs='+',
                        required=False, help='')
    args = parser.parse_args()
    if args.cropping:
        extracted = extractor(args.file).extract(args.page, args.cropping)
    else:
        extracted = ''
        for crops in ([0,0,0.36,1], [0.36,0,0.65,1], [0.65,0,1,1]):
            extracted += extractor(args.file).extract(args.page, crops)
            extracted += os.linesep
    with open(os.path.join(os.path.dirname(args.file),
                           'extractedText.txt'),'w') as extraction:
        extraction.write(os.linesep.join(reformat(extracted)))
