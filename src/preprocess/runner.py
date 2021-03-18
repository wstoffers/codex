#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
import os
import json

#define:
class corpus(object):
    def __init__(self, filePath):
        self.json = self.readJson(filePath)

    def readJson(self, filePath):
        with open(filePath) as jsonFile:
            decoded = json.load(jsonFile)
        return decoded

#run:
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', required=True,
                        help='path to raw data json')
    args = parser.parse_args()
    codex = corpus(args.file)
