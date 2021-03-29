#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
import os
import json
import re
import codecs

#define:
class corpus(object):
    def __init__(self, filePath):
        self.pages, self.pageOrder = self._extractPages(filePath)
        self.documents = self._initializeDocuments()
        self.documentOps = []

    def _readJson(self, filePath):
        with open(filePath) as jsonFile:
            decoded = json.load(jsonFile)
        return decoded

    def _extractPages(self, filePath):
        json = self._readJson(filePath)
        pages, pageOrder = {}, []
        for key in json:
            page = json[key]['page']
            pageOrder.append(page)
            #lists must be kept in original form for later:
            try:
                pages[page] = json[key]['text']
            except KeyError:
                #page is just a photo
                pages[page] = []
        return pages, pageOrder

    def _initializeDocuments(self):
        documents = []
        parent = None
        for page in self.pageOrder:
            newSection = self._checkSection(page)
            if newSection:
                parent = newSection
            combined = ' '.join(self.pages[page])
            #.*? makes .* not greedy:
            for match in re.finditer('<.*?>',combined):
                raw = match.group()[1:-1]
                #handle octal utf-8 unicode bytes:
                raw = codecs.escape_decode(raw)[0].decode('utf8')
                doc = document(page,
                               parent,
                               raw)
                doc.title = re.search("\^(.*?)\^",raw).group(1)
                try:
                    doc.spec = re.search("`(.*?)`",raw).group(1)
                except AttributeError:
                    pass
                documents.append(doc)
        return documents

    def _checkSection(self,page):
        try:
            return {'1': 'Old-Fashioned',
                    '42': 'NA',
                    '59': 'Martini',
                    '101': 'Daiquiri',
                    '149': 'Sidecar',
                    '197': 'Whisky Highball',
                    '239': 'Flip',
                    '255': 'NA',
                    '256': 'Flip',
                    '278': 'Appendix',
                    '285': 'NA',
                    '287': 'Infusion',
                    '295': 'NA'}[page]
        except KeyError:
            return None
    
class document(object):
    def __init__(self,page,parent,raw):
        self.page = page
        self.parent = parent
        self.raw = raw
        self.title = None
        self.spec = None
        self.build = None

#run:
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', required=True,
                        help='path to raw data json')
    args = parser.parse_args()
    codex = corpus(args.file)
    titles = {}
    leaveOut = ['NA', 'Appendix','Infusion']
    with open(os.path.join(os.path.dirname(args.file),'runner.log'),'w') as log:
        for doc in codex.documents:
            try:
                titles[doc.parent].append(doc.title)
            except KeyError:
                titles[doc.parent] = [doc.title]
            if doc.parent in leaveOut:
                continue
            elif not doc.spec:
                log.write(f'page {doc.page} ({doc.parent}): '
                          f'{doc.title}{os.linesep}')
    etoh, other = [], []
    for key in titles:
        quantity = len(titles[key])
        print(f'{key}: {quantity}')
        if key in leaveOut:
            other.append(quantity)
        else:
            etoh.append(quantity)
    print(f'{os.linesep}**WARNING** NA does not literally mean zero-proof!')
    print(f'EtOH: {sum(etoh)} (automatic label based on section)')
    print(f'{os.linesep}Total: {sum(etoh+other)} ({sum(other)} of these are '
          f'not auto-labeled cocktails)')
