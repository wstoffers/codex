#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
import os
from sklearn.model_selection import train_test_split as TrainTestSplit
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
        Xy = [(d,d.parent) for d in codex.documents]
        xWorkWith, xNoLook, yWorkWith, yNoLook = TrainTestSplit(*zip(*Xy),
        #                                                        stratify=y,
                                                                test_size=0.2)
        self.holdOut = (xNoLook, yNoLook)
        print(len(xWorkWith), len(xNoLook))
        
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
