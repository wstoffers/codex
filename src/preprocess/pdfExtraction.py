#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
import os, re
import json
import warnings
import codecs
import pdfplumber

#define:
class unscrambler(object):
    def __init__(self, filePath):
        self.filePath = filePath
        self.cursor = 0
        self.words = None
        self.setInStone = []
        self.repetition = None

    def overcomeColumnsObstacle(self, page):
        self.words, lines = self.extract(page)
        lines = self.reuniteOrphans(lines)
        self.unscramble(lines)
        return self.setInStone

    def reuniteOrphans(self, lines):
        finalLines = [] 
        for line in lines:
            orphan, reunited = '', []
            linePieces = line.split()
            for piece in linePieces:
                if piece in self.words:
                    reunited.append(piece)
                else:
                    if orphan:
                        combined = orphan + piece
                        if combined in self.words:
                            reunited.append(combined)
                    else:
                        orphan = piece
            finalLines.append(' '.join(reunited))
        return finalLines
    
    def unscramble(self, lines):
        processAgain = []
        for line in lines:
            keep = []
            linePieces = line.split()
            batchSize = len(linePieces)
            batch = self.words[self.cursor:self.cursor+batchSize]
            for i, piece in enumerate(linePieces):
                if piece == batch[i]:
                    keep.append(piece)
                    continue
                else:
                    self.addToFinal(keep)
                    stillNeeded = ' '.join(linePieces[i:])
                    processAgain.append(stillNeeded)
                    break
            if self.setInStone:
                if keep != self.setInStone[-1]:
                    self.addToFinal(keep)
            else:
                self.addToFinal(keep)
            if batch == linePieces[::-1]:
                #assume this is just page number extraction bug (don't care):
                processAgain = []
        if processAgain:
            if processAgain == self.repetition:
                warnings.warn(f'This clause should only be reached by Pytest '
                              f'but {processAgain} was repeated')
            else:
                self.repetition = processAgain
                self.unscramble(processAgain)

    def addToFinal(self, keep):
        self.setInStone.append(keep)
        self.cursor += len(keep)
        
    def extract(self, pageNumber):
        with pdfplumber.open(self.filePath) as pdf:
            for page in pdf.pages:
                if page.page_number == int(pageNumber):
                    words = page.extract_words(use_text_flow=True)
                    everything = page.extract_text()
                    break
        lines = everything.split(os.linesep) if everything else []
        return [w['text'] for w in words], lines

def reformat(agglomerateString):
    lines = agglomerateString
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
    args = parser.parse_args()
    text = unscrambler(args.file).overcomeColumnsObstacle(args.page)
    with open(os.path.join(os.path.dirname(args.file),
                           'extractedText.txt'),'w') as extraction:
        extraction.write(os.linesep.join(reformat([' '.join(t) for t in text])))
