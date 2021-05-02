#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
import os
import joblib
import collections
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import ticker
import matplotlib.colors as colors
import colorsys

#define:
colorChoice = np.linspace(0,1,6)
#for 6 discrete colors out of ^ continuous color map
#https://stackoverflow.com/a/57227821/426649
colorCycle = plt.cycler('color',plt.cm.viridis(colorChoice))
plt.style.use("dark_background")

def adjustLightness(color, amount=1.4):
    #amount > 1 is lighter, < 1 is darker
    try:
        c = colors.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*colors.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])

familyColors = {'Old-Fashioned': adjustLightness(plt.cm.viridis([0.8])[0],1.15),
                'Daiquiri': adjustLightness(plt.cm.viridis([1.])[0],0.8),
                'Martini': plt.cm.viridis([0.35])[0],
                'Whisky Highball': adjustLightness(plt.cm.viridis([0.])[0],1.6),
                'Flip': plt.cm.viridis([0.65])[0],
                'Sidecar': plt.cm.viridis([0.2])[0]}
#specifically leaving this dead code until group resolves color debate^^^

def plotCounts(data, imagesDirectory):
    counts = collections.Counter([x.parent for x in data])
    orderedCounts = sorted(counts.items(),key=lambda k: k[1])
    fig, ax = plt.subplots()
    ax.set_title(f'Recipes in Cocktail Codex by Family', color='w')
    ax.set_xlabel('Number of Recipes')
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    #[ax.barh(x,y,color=familyColors[x]) for x,y in zip(*zip(*orderedCounts))]
    [ax.barh(x,y,color='lightgray') for x,y in zip(*zip(*orderedCounts))]
    plt.tight_layout()
    plotName = 'recipeCounts.png'
    fig.savefig(os.path.join(imagesDirectory,plotName),
                transparent=True,
                dpi=600)
    return counts

def plotTokenCounts(imagesDirectory, familyMembers):
    sandbox = os.path.join(os.path.dirname(imagesDirectory),
                           'sandbox')
    tokenCounts = joblib.load(os.path.join(sandbox,'tokenFrequency.joblib'))
    hashedTokens = {}
    with open(os.path.join(sandbox,'tokens.log'),'w') as log:
        for family in tokenCounts:
            toPlot, hashedTokens[family] = [], {}
            orderedTokens = sorted([x for x in tokenCounts[family]],
                                   key=lambda k: k[1],
                                   reverse=True)
            log.write(f'{os.linesep}{family}:{os.linesep}')
            threshold = orderedTokens[2][1]
            for token in orderedTokens:
                percentage = token[1]/familyMembers[family]
                hashedTokens[family][token[0]] = percentage
                log.write(f'{token[0]}: '
                          f'{token[1]}'
                          f'{os.linesep}')
                if token[1] >= threshold:
                    toPlot.append((token[0],percentage))
            fig, ax = plt.subplots()
            ax.set_title(f'Top {family} Token Counts', color='w')
            ax.set_xlabel('Appearances Per Recipe')
            ax.xaxis.set_major_formatter('{x:0.2f}')
            [ax.barh(x,y,color='lightgray') for x,y in zip(*zip(*toPlot[::-1]))]
            ax.axvline(1.0,color='w',linewidth=0.75)
            plt.tight_layout()
            plotName = f'{family.replace(" ","")}TokenCounts.png'
            fig.savefig(os.path.join(imagesDirectory,plotName),
                        transparent=True,
                        dpi=600)
    tokens = ['3/4 ounce', 'syrup', 'lemon', 'lime'][::-1]
    sours = {'Daiquiri': [],
             'Sidecar': []}
    for token in tokens:
        for family in sours.keys():
            sours[family].append(hashedTokens[family][token])
    fig, ax = plt.subplots()
    ax.set_title(f'Sour-Style Recipe Tokens: Daiquiri v. Sidecar', color='w')
    ax.set_xlabel('Appearances Per Recipe')
    _x = np.arange(len(tokens))
    width=0.35
    daiquiris = ax.barh(_x-width/2,
                        sours['Daiquiri'],
                        width,
                        color=adjustLightness(plt.cm.viridis([0.0])[0],1.6),
                        label='Daiquiri')
    sidecars = ax.barh(_x+width/2,
                       sours['Sidecar'],
                       width,
                       color=plt.cm.viridis([0.65])[0],
                       label='Sidecar')
    ax.axvline(1.0,color='w',linewidth=0.75)
    ax.set_yticks(_x)
    ax.set_yticklabels(tokens)
    ax.xaxis.set_major_formatter('{x:0.2f}')
    handles, labels = ax.get_legend_handles_labels()
    legend = ax.legend(handles[::-1], labels[::-1])
    legend.get_frame().set_alpha(None)
    legend.get_frame().set_facecolor((0, 0, 1, 0.1))
    plt.tight_layout()
    plotName = f'SourTokenCounts.png'
    fig.savefig(os.path.join(imagesDirectory,plotName),
                transparent=True,
                dpi=600)

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
    absoluteSourceDirectory = os.path.abspath(sourceDirectory)
    sys.path.append(sourceDirectory)
    data = {'train': '',
            'test': '',
            'unseen': ''}
    for key in data:
        data[key] = joblib.load(f'{args.file}{key}.joblib')
    imagesDirectory = os.path.join(os.path.dirname(absoluteSourceDirectory),
                                   'images')
    counts = plotCounts(data['train']+data['test'], imagesDirectory)
    plotTokenCounts(imagesDirectory, counts)
