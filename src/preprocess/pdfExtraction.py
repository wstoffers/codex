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

    def overcomeColumnsObstacle(self):
        words, lines = self.extract()
        cursor = 0
        setInStone = []
        with open(os.path.join(os.path.dirname(self.filePath),
                               'test.ing'),'w') as log:
            processAgain = []
            for line in lines:
                keep = []
                linePieces = line.split()
                batchSize = len(linePieces)
                batch = words[cursor:cursor+batchSize]
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
                                setInStone.append(keep)
                                batchOffset = 0
                                cursor += len(keep)
                                processAgain.append(' '.join(linePieces[i-1:]))
                                break
                        else:
                            orphan = piece
                            batchOffset += 1
            for thing in setInStone:
                log.write(f'{thing}' + os.linesep)
            log.write(f'{lines}' + os.linesep)
        return setInStone
    
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
