#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
import os
from sklearn.model_selection import train_test_split as Split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB as NaiveBayes
from sklearn.metrics import top_k_accuracy_score

from preprocess import corpus

#define:
class classifier(object):
    def __init__(self, dataPath, logObject):
        self.path = dataPath
        self.holdOutObjects = None
        self.trainObjects = None
        self.testObjects = None
        self.log = logObject

    def performSplits(self):
        codex = corpus(self.path)
        #filter down to 6 root cocktail sections for now:
        skip = ['NA', 'Appendix', 'Infusion']
        the6 = [d for d in codex.documents if d.parent not in skip]
        Xy = [(d,d.parent) for d in the6 if d.spec]
        [X,y] = [x for x in zip(*Xy)]
        workWith, noLook, yWorkWith, yNoLook = Split(X,y,
                                                     test_size=0.2,
                                                     random_state=528491,
                                                     stratify=y)
        self.holdOutObjects = noLook
        finalSplit = Split(workWith,yWorkWith,
                           test_size=0.2,
                           random_state=5550134,
                           stratify=yWorkWith)
        self.trainObjects, self.testObjects, discard, discard = finalSplit
        
    def classify(self):
        self.performSplits()
        specsAndTargets = [(r.spec,r.parent) for r in self.trainObjects]
        self.runBaseline(*zip(*specsAndTargets))

    def runBaseline(self, documents, targets):
        bag = self.configureExtractor()
        xTrain = bag.fit_transform(documents)
        #xTest = bag.transform(notDocuments)
        self.log.write(os.linesep.join(bag.get_feature_names()))
        args = bag.get_params()
        argsInOrder = sorted([(k,args[k]) for k in args],key=lambda k:k[0])
        self.log.write(f'{os.linesep*2}'
                       f'{os.linesep.join([repr(x) for x in argsInOrder])}')
        baseline = NaiveBayes()
        baseline.fit(xTrain,targets)

    def configureExtractor(self):
        #matches are unicode by default in python 3:
        expandedPattern = r'[0-9 ]+/*[0-9 ]+ounce[s]*|(?!\b[0-9]+\))\b\w\w+\b'
        return CountVectorizer(strip_accents=None,
                               lowercase=True,
                               stop_words=None,
                               token_pattern=expandedPattern,
                               ngram_range=(1,1),
                               max_df=1.0,
                               min_df=1,
                               max_features=None)
    
#run:
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', required=True,
                        help='path to raw data json')
    args = parser.parse_args()
    with open(os.path.join(os.path.dirname(args.file),
                           'classification.log'),'w') as log:
        sortingHat = classifier(args.file, log)
        sortingHat.classify()
    print('done!')
