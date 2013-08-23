'''
Created on Aug 23, 2013

@author: sotiris
'''
import sys


def enum(**enums):
    return type('Enum', (), enums)

wordDict = dict()
maxWordLength = 0
cost = enum(SKIP=10, JOIN=0, CANT_JOIN=sys.maxint)
SKIP_CHAR = "-"

cache = dict()


#class Solution
def loadWords(fileName):
    global maxWordLength
    with open(fileName) as f:
        for word in f:
            word = word.rstrip("\n")
            wordDict[''.join(sorted(word))] = word
            if len(word) > maxWordLength:
                maxWordLength = len(word)


def canJoinPreviousWord(sequence, char):
    # go back till you find a Cap, SKIP_CHAR Or beginning
    i = len(sequence) - 1
    word = ""
    while i >= 0:
        if sequence[i] == SKIP_CHAR:
            break
        word += sequence[i]
        if sequence[i].isUpper():
            break

    candidate = ''.join(sorted(word[::-1] + char))
    if (candidate in wordDict) or (len(candidate) <= maxWordLength):
        return (True, candidate)
    return (False, None)


def canStartNewWord(char, sequence):
    pass


class Solution(object):

    def __init__(self, candidate="", suffix=None, cost=None):
        self.candidate = candidate
        self.suffix = suffix
        self.cost = cost
        self.str = ""

    def setCost(self, cost):
        self.cost = cost

    def getNextChar(self):
        if len(self.suffix) > 0:
            return self.suffix[0]
        return None
    
    def getNextSuffix(self):
        if len(self.suffix) > 1:
            return self.suffix[1:]
        return None
    
    def setString(self, str):
        self.str = str


def solve(solution):
    
    if solution.suffix is None:
        return Solution(cost=0, candidate=solution.candidate)
    
    if solution.candidate  + solution.suffix in cache:
        return cache[solution.suffix]
    
    print "entyr for " + solution.suffix + " cand " + solution.candidate
    # 3 possible solutions
    solutionList = list()
    # 1 : skip the current char
    skipSolution = solve(Solution(candidate="",
                                  suffix=solution.getNextSuffix()))
    skipSolution.cost += cost.SKIP
    skipSolution.str = SKIP_CHAR + skipSolution.str
    solutionList.append(skipSolution)
    print "Solved for skip " + solution.suffix + " str is " + skipSolution.str
    # 2 - join the previous candidate
    print "Will try to join "+ solution.candidate + solution.suffix[0] + " sufx: " + str(solution.getNextSuffix())
    joinCandidateSolution = solve(Solution(candidate=solution.candidate + solution.suffix[0],
                                           suffix=solution.getNextSuffix()))
    print "Solved for join " + solution.suffix + " cand:" + joinCandidateSolution.candidate
    if ("".join(sorted(joinCandidateSolution.candidate)) in wordDict) and len(joinCandidateSolution.candidate) >= 2:
        print "FOUND properWord " + joinCandidateSolution.candidate
        properWord = wordDict["".join(sorted(joinCandidateSolution.candidate))]
        properWord = properWord[0].upper() + properWord[1:].lower()
        joinCandidateSolution.str = properWord
    else:
        joinCandidateSolution.cost = cost.CANT_JOIN
        
    solutionList.append(joinCandidateSolution)
    solutionList.sort(key=lambda solution: solution.cost)
    print "** final sol for " + solution.suffix + " is " + str(solutionList[0].str)
    cache[solution.candidate + solution.suffix] = solutionList[0]
    return solutionList[0]
        
    
if __name__ == "__main__":
    loadWords(sys.argv[1])
    #print str(wordDict)
    solve(Solution(suffix="cesaleomrnu"))
