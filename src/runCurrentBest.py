#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
import os
from sklearn.model_selection import train_test_split as Split
from sklearn.naive_bayes import MultinomialNB as NaiveBayes
from sklearn.metrics import top_k_accuracy_score

from preprocess import corpus

#define:
class classifier(object):
    def __init__(self, dataPath):
        self.path = dataPath
        self.holdOut = None
        self.xTrain = None
        self.yTrain = None
        self.xTest = None
        self.yTest = None

    def performSplits(self):
        codex = corpus(self.path)
        #filter down to 6 root cocktail sections for now:
        skip = ['NA', 'Appendix', 'Infusion']
        the6 = [d for d in codex.documents if d.parent not in skip]
        Xy = [(d,d.parent) for d in the6 if d.spec]
        [X,y] = [x for x in zip(*Xy)]
        xWorkWith, xNoLook, yWorkWith, yNoLook = Split(X,y,
                                                       test_size=0.2,
                                                       random_state=528491,
                                                       stratify=y)
        self.holdOut = (xNoLook, yNoLook)
        finalSplit = Split(xWorkWith,yWorkWith,
                           test_size=0.2,
                           random_state=5550134,
                           stratify=yWorkWith)
        self.xTrain, self.xTest, self.yTrain, self.yTest = finalSplit
        
    def classify(self):
        self.performSplits()

#run:
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', required=True,
                        help='path to raw data json')
    args = parser.parse_args()
    sortingHat = classifier(args.file)
    sortingHat.classify()
    print('done!')
