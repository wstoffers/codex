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
        self.repitition = None

    def overcomeColumnsObstacle(self):
        self.words, lines = self.extract()
        with open(os.path.join(os.path.dirname(self.filePath),
                               'test.ing'),'w') as log:
            self.unscramble(lines, log)
        return self.setInStone

    def unscramble(self, lines, log):
        log.write(f'unscramble called{os.linesep}')
        processAgain = []
        for line in lines:
            keep = []
            linePieces = line.split()
            batchSize = len(linePieces)
            log.write(f'    cursor: {self.cursor}{os.linesep}')
            batch = self.words[self.cursor:self.cursor+batchSize]
            log.write(f'    linePieces: {linePieces}{os.linesep}')
            log.write(f'    batch: {batch}{os.linesep}')
            for i, piece in enumerate(linePieces):
                if piece == batch[i]:
                    keep.append(piece)
                    continue
                else:
                    self.addToFinal(keep,log)
                    stillNeeded = ' '.join(linePieces[i:])
                    log.write(f'stillNeeded: {stillNeeded}{os.linesep}')
                    processAgain.append(stillNeeded)
                    break
            if keep != self.setInStone[-1]:
                self.addToFinal(keep,log)
            if batch == linePieces[::-1]:
                #assume this is just page number extraction bug (don't care):
                processAgain = []
        log.write(f'{len(processAgain)}: {os.linesep}')
        if processAgain:
            if processAgain == self.repitition:
                warnings.warn('This clause should only be reached by Pytest')
            else:
                self.repitition = processAgain
                self.unscramble(processAgain, log)

    def addToFinal(self, keep, log):
        self.setInStone.append(keep)
        self.cursor += len(keep)
        log.write(f'    kept: {keep}{os.linesep}')
        
    def extract(self):
        with pdfplumber.open(self.filePath) as pdf:
            for page in pdf.pages:
                if page.page_number == 7:
                    words = page.extract_words(use_text_flow=True)
                    everything = page.extract_text()
                    break
        return [w['text'] for w in words], everything.split(os.linesep)
                
#run:
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', required=True,
                        help='path to pdf')
    args = parser.parse_args()
    final = unscrambler(args.file).overcomeColumnsObstacle()
    with open(os.path.join(os.path.dirname(args.file),
                           'extractedText.txt'),'w') as extraction:
        extraction.write(os.linesep.join([' '.join(s) for s in final]))
