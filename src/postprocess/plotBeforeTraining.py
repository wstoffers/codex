#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
import os
import joblib
import collections
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import colorsys

#define:
def plotCounts(data, sourceDirectory):
    imagesDirectory = os.path.join(os.path.dirname(sourceDirectory),
                                   'images')
    counts = collections.Counter([x.parent for x in data])
    
                
#run:
if __name__ == '__main__':
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', required=True,
                        help=f'path prefix to serialized data, like '
                             f'sandbox/codexSubset121')
    args = parser.parse_args()
    sourceDirectory = os.path.dirname(os.path.dirname(sys.argv[0]))
    sys.path.append(sourceDirectory)
    data = {'train': '',
            'test': '',
            'unseen': ''}
    for key in data:
        data[key] = joblib.load(f'{args.file}{key}.joblib')
    plotCounts(data['train']+data['test'], os.path.abspath(sourceDirectory))
