'''
Created on Aug 23, 2013

@author: sotiris
'''
import sys


def enum(**enums):
    return type('Enum', (), enums)

wordDict = dict()
maxWordLength = 0
cost = enum(SKIP=10, JOIN=0, MAX=sys.maxint)
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


'''
class Solution(object):

    def __init__(self, candidate="", suffix="", cost=cost.JOIN):
        self.candidate = candidate
        self.suffix = suffix
        self.cost = cost
        self.finalStr = ""

    def createJoinCandidate(self):
        if len(self.suffix) > 0:
            return (self.candidate + self.suffix[0], self.suffix[1:])
        return (self.candidate, list())

    def createSkip(self):
        if len(self.suffix) > 0:
            return ("", self.suffix[1:])
        return ("", list())

    def createNewWord(self):
        return (self.suffix[0:3], self.suffix[3:])

    def setCost(self, cost):
        self.cost = cost

    def setFinalStr(self, str):
        self.finalStr = str
        
    def __str__(self):
        return "FS:" + self.finalStr + " C:" + str(self.cost) + " CAND:" + str(self.candidate) + " SUF:" + str(self.suffix)


#class Tmp(object,):
def solve2(solution):

    if len(solution.suffix) <= 0:
        return Solution(cost=0, candidate=solution.candidate)

    if solution.candidate + solution.suffix in cache:
        return cache[solution.suffix]
    print "-> SOLVE FOR " + str(solution)
    # 3 possible solutions
    solutionList = list()
    # 1 : skip the current char
    newCandidate, newSuffix = solution.createSkip()
    skipSolution = solve2(Solution(candidate=newCandidate, suffix=newSuffix))
    skipSolution.cost += cost.SKIP
    skipSolution.setFinalStr(SKIP_CHAR + skipSolution.finalStr)
    solutionList.append(skipSolution)
    print "#1 skip " + str(skipSolution) + " ORG:" + str(solution)

    # 2 - join the previous candidate
    newCandidate, newSuffix = solution.createJoinCandidate()
    print "Will try to solve join " + str(newCandidate) + " + " + str(newSuffix)
    joinSolution = solve2(Solution(candidate=newCandidate, suffix=newSuffix))
    if ("".join(sorted(joinSolution.candidate)) in wordDict) and len(joinSolution.candidate) >= 4:
        print "FOUND properWord " +\
            wordDict["".join(sorted(joinSolution.candidate))]
        properWord = wordDict["".join(sorted(joinSolution.candidate))]
        properWord = properWord[0].upper() + properWord[1:].lower()
        joinSolution.setFinalStr(properWord + joinSolution.finalStr)
    else:
        joinSolution.cost = cost.MAX
    print "#2 join " + str(joinSolution) + " ORG:" + str(solution)
    solutionList.append(joinSolution)
    # 3 Try to start a new word
    newCandidate, newSuffix = solution.createNewWord()
    print "Will try NEW word for " + str(newCandidate) + " + " + str(newSuffix)
    newWordSolution = solve2(Solution(candidate=newCandidate, suffix=newSuffix))
    if ("".join(sorted(newWordSolution.candidate)) in wordDict) and len(newWordSolution.candidate) >= 4:
        print "FOUND properWord " + wordDict["".join(sorted(newWordSolution.candidate))]
        properWord = wordDict["".join(sorted(newWordSolution.candidate))]
        properWord = properWord[0].upper() + properWord[1:].lower()
        newWordSolution.setFinalStr(properWord + newWordSolution.finalStr)
    else:
        newWordSolution.cost = cost.MAX
    print "#3 new word " + str(newWordSolution) + " ORG:" + str(solution)
    solutionList.append(newWordSolution)
        
    
    solutionList.sort(key=lambda solution: solution.cost)
    print "** final sol for " + str(solution) + " is "
    for s in solutionList:
        print str(s)
    print "BEST SOL:" + str(solutionList[0])
    solution.cost += solutionList[0].cost
    solution.finalStr += solutionList[0].finalStr
    cache[solution.candidate + solution.suffix] = solutionList[0]
    print " ** Ret solition:" + str(solution)
    print "<- solved FOR " + str(solution)
    return solution
    
'''


class Candidate(object):

    def __init__(self, index=0, part=''):
        self.index = index
        self.part = list(part)
        self.cost = cost.JOIN

    def __str__(self):
        return "index:" + str(self.index) + " STR:" + "".join(self.part) + " Cost: " + str(self.cost)


def solve(candidate):

    if str(candidate.part[candidate.index:]) in cache:
        print "Cached for " + str(candidate.part[candidate.index:]) + " " + str(cache[str(candidate.part[candidate.index:])])
        return cache[str(candidate.part[candidate.index:])]
    
    if candidate.index >= len(candidate.part):
        return Candidate(index=len(candidate.part))
    
    solutionList = list()
    
    # case 1 join previous string
    print "Solving for join " + str(Candidate(index=candidate.index + 1,
                                   part=candidate.part))
    joinSolution = solve(Candidate(index=candidate.index + 1,
                                   part=candidate.part))
    if joinSolution.index > candidate.index:
        candidateWord = candidate.part[:candidate.index + 1]
        if ("".join(sorted(candidateWord)) in wordDict) and len(candidateWord) >= 4:
            print "Found new word:" + str(candidateWord)
            joinSolution.index = 0
            properWord = wordDict["".join(sorted(candidateWord))]
            properWord = properWord[0].upper() + properWord[1:].lower()
            joinSolution.part[:candidate.index + 1] = properWord
        else:
            joinSolution.cost = cost.MAX

    # Case 2 : skip str
    print "Solving for skip " + str(Candidate(index=0,
                                   part=candidate.part[candidate.index + 1:]))
    skipSolution = solve(Candidate(index=0,
                                   part=candidate.part[candidate.index + 1:]))
    skipSolution.part = candidate.part[0:candidate.index] + [SKIP_CHAR]\
        + skipSolution.part
    skipSolution.cost += cost.SKIP
    skipSolution.index = candidate.index
    print " -> Skip solution is " + str(skipSolution)

    # Case 3 : start a new word
    newWordSolution = solve(Candidate(index=4, part=candidate.part[candidate.index:]))
    # Make sure whatever is left is a valid word
    if newWordSolution.index > 0:
        candidateWord = candidate.part[candidate.index:candidate.index
                                       + newWordSolution.index]
        if ("".join(sorted(candidateWord)) in wordDict) and len(candidateWord) >= 4:
            properWord = wordDict["".join(sorted(candidateWord))]
            properWord = properWord[0].upper() + properWord[1:].lower()
            newWordSolution.part[candidate.index:candidate.index
                                       + newWordSolution.index] = properWord
        else:
            newWordSolution.cost = cost.MAX
    newWordSolution.index = candidate.index

    solutionList.append(joinSolution)
    solutionList.append(skipSolution)
    #solutionList.append(newWordSolution)

    solutionList.sort(key=lambda solution: solution.cost)
    print "** final sol is " + str(solutionList[0])
    s = solutionList[0]
    #print " -> Cacheing for " + str(s.part[s.index:])
    cache[str(s.part[s.index:])] = s
    return s

if __name__ == "__main__":
    loadWords(sys.argv[1])
    #print str(wordDict)
    print str(solve(Candidate(part="xecasmounr")))
