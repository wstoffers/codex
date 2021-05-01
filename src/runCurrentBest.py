#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
import os, collections
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split as Split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB as NaiveBayes
from sklearn.metrics import top_k_accuracy_score

from preprocess import corpus

#define:
class classifier(object):
    def __init__(self, dataPath, logObject):
        self.path = dataPath
        self.unseenObjects = None
        self.trainObjects = None
        self.testObjects = None
        self.extractor = None
        self.model = None
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
        self.unseenObjects = noLook
        finalSplit = Split(workWith,yWorkWith,
                           test_size=0.2,
                           random_state=5550134,
                           stratify=yWorkWith)
        self.trainObjects, self.testObjects, discard, discard = finalSplit

    def classify(self):
        self._logForTroubleshooting('initial train', self.trainObjects, log)
        zipped = self._extractSpecsAndTargets(self.trainObjects)
        self._trainBaseline(*zipped, self.log)
        self._logForTroubleshooting('initial test', self.testObjects, log)
        zipped = self._extractSpecsAndTargets(self.testObjects)
        return self._predictProbabilities(*zipped)

    def predictHoldOut(self, log):
        finalTraining = self.trainObjects + self.testObjects
        self._logForTroubleshooting('final training', finalTraining, log)
        zipped = self._extractSpecsAndTargets(finalTraining)
        self._trainBaseline(*zipped, log)
        joblib.dump((self.model,
                     self.extractor), os.path.join(os.path.dirname(self.path),
                                             'trained.joblib'))
        self._logForTroubleshooting('hold-out test', self.unseenObjects, log)
        zipped = self._extractSpecsAndTargets(self.unseenObjects)
        holdOutScore = self._predictProbabilities(*zipped, log)
        print(f'final hold out score: {holdOutScore}')

    def _logForTroubleshooting(self, label, children, log):
        counts = collections.Counter((r.parent for r in children))
        counts = sorted([f'{counts[r]} {r}' for r in counts],key=lambda k: k)
        log.write(f'breakdown for {label}:{os.linesep}'
                  f'{"/".join(counts)}{os.linesep}')
        log.write(f'{label}:{os.linesep}')
        for corpusChild in children:
            log.write(f'(algorithm cannot see this title) {corpusChild.title} '
                      f'({corpusChild.parent}){os.linesep}')
            log.write(f'{corpusChild.spec}')
            log.write(os.linesep*2)

    def _extractSpecsAndTargets(self, corpusChildren):
        specsAndTargets = [(r.spec,r.parent) for r in corpusChildren]
        return zip(*specsAndTargets)

    def _configureExtractor(self):
        #matches are unicode by default in python 3:
        expandedPattern = (r'\b[0-9]+ [0-9/]+ ounce[s]*|' +
                           r'\b[0-9/]*[0-9]+ ounce[s]*|' +
                           r'\b[0-9]+ dash[es]*|' +
                           r'(?!\b[0-9]+\))\b\w\w+\b')
        return CountVectorizer(strip_accents=None,
                               lowercase=True,
                               stop_words=None,
                               token_pattern=expandedPattern,
                               ngram_range=(1,1),
                               max_df=1.0,
                               min_df=1,
                               max_features=None)
    
    def _trainBaseline(self, documents, targets, log):
        bag = self._configureExtractor()
        xTrain = bag.fit_transform(documents)
        log.write(f'feature tokens:{os.linesep}')
        log.write(os.linesep.join(bag.get_feature_names()))
        args = bag.get_params()
        argsInOrder = sorted([(k,args[k]) for k in args],key=lambda k:k[0])
        log.write(f'{os.linesep*2} count vectorizer parameters: {os.linesep}'
                  f'{os.linesep.join([repr(x) for x in argsInOrder])}'
                  f'{os.linesep*10}')
        baseline = NaiveBayes()
        baseline.fit(xTrain,targets)
        self.extractor = bag
        self.model = baseline

    def _predictProbabilities(self, documents, targets, log=None):
        xTest = self.extractor.transform(documents)
        probabilities = self.model.predict_proba(xTest)
        if log:
            results = pd.DataFrame(data=probabilities,
                                   index=[r.title for r in self.unseenObjects],
                                   columns=self.model.classes_)
            results.loc[:,'Max'] = results.max(axis=1)
            results.loc[:,'Target'] = targets
            log.write(f'{results.to_markdown()}{os.linesep}')
        return top_k_accuracy_score(targets,
                                    probabilities,
                                    k=2,
                                    labels=self.model.classes_)

#run:
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', required=True,
                        help='path to raw data json')
    parser.add_argument('--data', '-d', required=True,
                        help='name of dataset for serialization')
    args = parser.parse_args()
    logFileName = os.path.join(os.path.dirname(args.file),'classification.log')
    with open(logFileName,'w') as log:
        sortingHat = classifier(args.file, log)
        sortingHat.performSplits()        
        print(f'top 2 scoring is {sortingHat.classify()}, what for top 1?')
    for objects in ['train', 'test', 'unseen']:
        joblib.dump(eval(f'sortingHat.{objects}Objects'),
                    os.path.join(os.path.dirname(args.file),
                                 f'{args.data}{objects}.joblib'))

    #do not run this during design cycles, only for hold-out validation at end:
    #with open(logFileName,'a') as log:
    #    sortingHat.predictHoldOut(log)
    print('done!')
