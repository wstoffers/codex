#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
from productionModel import awaken

#define:


#run:
if __name__ == '__main__':
    probabilities = awaken(('2 ounces Rittenhouse rye 1 ounce Cocchi Vermouth di Torino 2 dashes Angostura bitters Garnish: 1 brandied cherry',))
    print(probabilities)
