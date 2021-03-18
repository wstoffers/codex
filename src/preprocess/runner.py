#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
import os
import json

#define:
class corpus(object):
    def __init__(self, filePath):
        self.json = self._readJson(filePath)
        self.pages = self._extractPages()

    def _readJson(self, filePath):
        with open(filePath) as jsonFile:
            decoded = json.load(jsonFile)
        return decoded

    def _extractPages(self):
        pages = []
        for key in self.json:
            pages.append(self.json[key]['page'])
        return pages

#run:
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', required=True,
                        help='path to raw data json')
    args = parser.parse_args()
    codex = corpus(args.file)
