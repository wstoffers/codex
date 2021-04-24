#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
import os, re
import docx

#define:
class extractor(object):
    def __init__(self, filePath):
        self.filePath = filePath

    def extract(self):
        recipeStart = False
        word = docx.Document(self.filePath)
        keep = []
        for paragraph in word.paragraphs:
            boldRuns = self.findBold(paragraph)
            if boldRuns:
                recipeStart = True
                keep.append(boldRuns)
            else:
                keep.append([paragraph.text])
                recipeStart = False
        return keep

    def findBold(self, paragraph):
        bold = []
        for run in paragraph.runs:
            if run.bold:
                bold.append(f'**bold**{run.text}')
        return bold

def reformat(agglomerateString):
    reformatted = agglomerateString
    return reformatted
                
#run:
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', required=True,
                        help='path to word doc')
    args = parser.parse_args()
    extracted = extractor(args.file).extract()
    with open(os.path.join(os.path.dirname(args.file),
                           'extractedFromWord.log'),'w') as extraction:
        extraction.write(os.linesep.join([''.join(x) for x in extracted]))
