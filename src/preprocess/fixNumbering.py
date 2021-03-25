#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
import os
import json
import re

#define:
def correctNumbering(oldPath):
    """Corrects page numbers in corrupted JSON representation of book
    Intended for one-off use, to fix issue discovered in Cocktail Codex JSON
        page numbering.

    Args:
        oldPath: path to the JSON file to fix
    Returns:
        None
    """
    
    with open(oldPath) as jsonFile:
        decoded = json.load(jsonFile)
    for key in decoded:
        sortNumber = sortOrder(decoded[key]['page'])
        if sortNumber > 168:
            decoded[key]['page'] = str(sortNumber-1)
    with open(os.path.join(os.path.dirname(oldPath),
                           'confirm.json'), 'w') as newFile:
        json.dump(decoded, newFile, indent=4)

def sortOrder(page):
    try:
        return int(page)
    except ValueError:
        return 0

#run:
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', required=True,
                        help='path to corrupted json')
    args = parser.parse_args()
    correctNumbering(args.file)
