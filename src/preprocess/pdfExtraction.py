#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
import os, re
import json
import codecs
import pdfplumber

#define:
class unscrambler(object):
    def __init__(self, filePath):
        self.filePath = filePath
        self.cursor = 0
        self.words = None
        self.setInStone = []

    def overcomeColumnsObstacle(self):
        self.words, lines = self.extract()
        with open(os.path.join(os.path.dirname(self.filePath),
                               'test.ing'),'w') as log:
            self.unscramble(lines, log)
        return self.setInStone

    def unscramble(self, lines, log):
        processAgain = []
        for line in lines:
            keep = []
            linePieces = line.split()
            batchSize = len(linePieces)
            batch = self.words[self.cursor:self.cursor+batchSize]
            log.write(f'    linePieces: {linePieces}{os.linesep}')
            log.write(f'    batch: {batch}{os.linesep}')
            orphan, batchOffset = '', 0
            for i, piece in enumerate(linePieces):
                if piece == batch[i-batchOffset]:
                    keep.append(piece)
                else:
                    if orphan:
                        reunited = orphan + piece
                        if reunited == batch[i-batchOffset]:
                            keep.append(reunited)
                            orphan = ''
                        else:
                            self.setInStone.append(keep)
                            batchOffset = 0
                            self.cursor += len(keep)
                            log.write(f'    orphan: {orphan}{os.linesep}')
                            log.write(f'    kept: {keep}{os.linesep}')
                            stillNeeded = ' '.join(linePieces[i-1:])
                            log.write(f'stillNeeded: {stillNeeded}{os.linesep}')
                            processAgain.append(stillNeeded)
                            break
                    else:
                        orphan = piece
                        batchOffset += 1
        log.write(f'{len(processAgain)} (orphan is {repr(orphan)}): {os.linesep}')
#        for thing in lines:
#            log.write(f'    line: {thing}{os.linesep}')
        self.unscramble(processAgain, log)
        for thing in self.setInStone:
            log.write(f'{thing}' + os.linesep)
        log.write(f'{lines}' + os.linesep)

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
