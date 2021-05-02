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
                keep.append(['**'] + boldRuns + ['**'])
            else:
                keep.append([paragraph.text])
                recipeStart = False
        return keep

    def findBold(self, paragraph):
        bold = []
        for run in paragraph.runs:
            if run.bold:
                bold.append(f'{run.text}')
        return bold

class recipe(object):
    def __init__(self, title):
        self.title = title
        self.credit = None
        self.spec = []
        self.build = []

def separate(lines):
    recipes = []
    bold = re.compile('^\*\*(.+)\*\*$')
    for line in lines:
        match = bold.match(line)
        if match:
            try:
                recipes.append(currentRecipe)
            except NameError:
                assert len(recipes) == 0
                #must be first recipe
            currentRecipe = recipe(match.group(1))
            build = False
        else:
            if currentRecipe.credit:
                if line.strip():
                    if build:
                        currentRecipe.build.append(line)
                    else:
                        currentRecipe.spec.append(line)
                else:
                    if currentRecipe.spec:
                        build = True
            else:
                currentRecipe.credit = line
    recipes.append(currentRecipe)
    return recipes
                
#run:
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', required=True,
                        help='path to word doc')
    args = parser.parse_args()
    lineParts = extractor(args.file).extract()
    lines = [''.join(x) for x in lineParts]
    recipes = separate([x.replace(' ','') for x in lines])
    with open(os.path.join(os.path.dirname(args.file),
                           'extractedFromWord.log'),'w') as csv:
        csv.write(('\n'*2).join([f'{r.title}{os.linesep}'
                                 f'{r.credit}{os.linesep}'
                                 f'{os.linesep.join(r.spec)}{os.linesep}'
                                 f'    '
                                 f'{"    ".join(r.build)}' for r in recipes]))
