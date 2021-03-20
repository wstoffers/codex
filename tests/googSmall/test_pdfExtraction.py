#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
import re
import pytest
from pdfExtraction import unscrambler

#define:
@pytest.fixture
def modifiedUnscrambler(args):
    '''Returns an unscrambler object, modified for testing'''
    testObject = unscrambler('.')
    testObject.extract = lambda k: [args[0], args[1]]
    return testObject

def testDataSimpleTwoColumns():
    lines = ['this is a list from two columns']
    words = ['this', 'is', 'a', 'list', 'of', 'strings', 'in', 'order']    
    return [[words, lines]]

@pytest.mark.parametrize('args', testDataSimpleTwoColumns())
def test_overcomeColumnsObstacle(modifiedUnscrambler):
    modifiedUnscrambler.overcomeColumnsObstacle('1')
    
    assert modifiedUnscrambler.setInStone  == [['this',
                                                'is',
                                                'a',
                                                'list']]

def testDataOrphanedString():
    lines = ['this l ong list from two columns']
    words = ['this', 'long', 'list', 'of', 'strings']
    return [[words, lines]]

@pytest.mark.parametrize('args', testDataOrphanedString())
def test_overcomeColumnsObstacleWithOrphan(modifiedUnscrambler):
    modifiedUnscrambler.overcomeColumnsObstacle('1')
    assert modifiedUnscrambler.setInStone == [['this',
                                               'long',
                                               'list']]

#run:
if __name__ == '__main__':
    pass
