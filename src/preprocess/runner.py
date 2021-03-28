#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
import os
import json
import re

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
                documents.append(document(page,parent,match.group()[1:-1]))
        return documents

    def _checkSection(self,page):
        if page == '1':
            return 'Old-Fashioned'
        elif page == '42':
            return 'NA'
        elif page == '59':
            return 'Martini'
        elif page == '101':
            return 'Daiquiri'
        elif page == '149':
            return 'Sidecar'
        elif page == '197':
            return 'Whisky Highball'
        elif page == '239':
            return 'Flip'
        elif page == '255':
            return 'NA'
        elif page == '256':
            return 'Flip'
        elif page == '278':
            return 'Appendix'
        elif page == '285':
            return 'NA'
        elif page == '287':
            return 'Infusion'
        elif page == '295':
            return 'NA'
    
class document(object):
    def __init__(self,page,parent,raw):
        self.page = page
        self.parent = parent
        self.raw = raw
    
#run:
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', required=True,
                        help='path to raw data json')
    args = parser.parse_args()
    codex = corpus(args.file)
    toMatch = "\^(.*?)~"
    titles = {}
    with open(os.path.join(os.path.dirname(args.file),'runner.log'),'w') as log:
        for doc in codex.documents:
            title = re.search(toMatch,doc.raw).group(1)
            try:
                titles[doc.parent].append(title)
            except KeyError:
                titles[doc.parent] = [title]
            log.write(f'page {doc.page} ({doc.parent}): '
                      f'{title}{os.linesep}')
    etoh, other = [], []
    for key in titles:
        quantity = len(titles[key])
        print(f'{key}: {quantity}')
        if key in ['NA', 'Appendix']:
            other.append(quantity)
        else:
            etoh.append(quantity)
    print(f'{os.linesep}**WARNING** NA does not literally mean zero-proof!')
    print(f'EtOH: {sum(etoh)} (automatic label based on section)')
    print(f'{os.linesep}Total: {sum(etoh+other)} ({sum(other)} other)')
