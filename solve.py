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


class Candidate(object):

    def __init__(self, index=0, part='', cost=cost.JOIN):
        self.index = index
        self.part = list(part)
        self.cost = cost

    def __str__(self):
        return "index:" + str(self.index) + " STR:" + "".join(self.part)\
            + " Cost: " + str(self.cost)

cTimes = 0
sTimes = 0


def c(candidate):
    return str(candidate.index) + " " + "".join(candidate.part)


def solve(candidate):

    global sTimes, cTimes

    if c(candidate) in cache:
        cTimes += 1
        cached = cache[c(candidate)]
        return Candidate(index=cached.index, part=cached.part, cost=cached.cost)

    if candidate.index >= len(candidate.part):
        return Candidate(index=len(candidate.part))

    sTimes += 1
    solutionList = list()
    
    # case 1 join previous string
    '''print "Solving for join " + str(Candidate(index=candidate.index + 1,
                                   part=candidate.part))'''
    joinSolution = solve(Candidate(index=candidate.index + 1,
                                       part=candidate.part))
    if joinSolution.index > candidate.index:
        candidateWord = candidate.part[:candidate.index + 1]
        if ("".join(sorted(candidateWord)) in wordDict)\
                                and len(candidateWord) >= 4:
            #print "Found new word:" + str(candidateWord)
            joinSolution.index = 0
            properWord = wordDict["".join(sorted(candidateWord))]
            properWord = properWord[0].upper() + properWord[1:].lower()
            #print "Proper:" + properWord
            joinSolution.part[:candidate.index + 1] = properWord
        else:
            joinSolution.cost = cost.MAX
    #print " -> Join solition " + str(joinSolution)

    # Case 2 : skip str
    #print "Solving for skip " + str(Candidate(index=0, part=candidate.part[candidate.index + 1:]))
    skipSolution = solve(Candidate(index=0,
                                   part=candidate.part[candidate.index + 1:]))
    skipSolution.part = candidate.part[0:candidate.index] + [SKIP_CHAR]\
        + skipSolution.part
    skipSolution.cost += cost.SKIP
    skipSolution.index = candidate.index
    #print " -> Skip solution is " + str(skipSolution)

    newWordSolution = solve(Candidate(index=4,
                                      part=candidate.part[candidate.index:]))
    # Make sure whatever is left is a valid word
    if newWordSolution.index > 0:
        candidateWord = candidate.part[candidate.index:candidate.index
                                       + newWordSolution.index]
        if ("".join(sorted(candidateWord)) in wordDict)\
                                and len(candidateWord) >= 4:
            properWord = wordDict["".join(sorted(candidateWord))]
            properWord = properWord[0].upper() + properWord[1:].lower()
            #print "Proper:" + properWord
            newWordSolution.part[0:newWordSolution.index] = properWord
        else:
            newWordSolution.cost = cost.MAX
    newWordSolution.index = candidate.index
    newWordSolution.part = candidate.part[0:candidate.index] + newWordSolution.part
    #print " -> Solved #3 for new Word: " + str(newWordSolution)

    solutionList.append(joinSolution)
    solutionList.append(skipSolution)
    solutionList.append(newWordSolution)

    solutionList.sort(key=lambda solution: solution.cost)
    #print "** final sol for candidate:" + str(candidate) + " is " + str(solutionList[0])
    s = solutionList[0]
    if s == newWordSolution:
        pass
    #print " -> Cacheing for " + str(s.part[s.index:])
    cache[c(candidate)] = Candidate(index=s.index, part=s.part, cost=s.cost)
    #print c(candidate) + "=" + str(s)
    return s

if __name__ == "__main__":
    loadWords(sys.argv[1])
    #print str(wordDict)
    final = solve(Candidate(part="etaelehoyrnrsweeneiornvtsdelreiolrertsrhotruongpmghwsihlxtde"
                            "elaneeetldosheeralithtndareluttelderrocltaeiwrtodeoeyladfswp"
                            "sremeucraddfvrntaiansudynaeytnaidthioicheegblyoeielsvvneolii"
                            "wudveieuaoaodptetpurrdeieecnohasapiwdoehltflsbohlamthioeosistssbstwe"
                             ))
    print "".join(final.part)
    print str(reduce(lambda s,ch: s+1 if ch == SKIP_CHAR else s, final.part, 0)) + " skips"
    #print "CTimes:" + str(cTimes) + " sTimes:" + str(sTimes)
    #for c in cache.keys():
    #    print str(c) + ' : ' + str(cache[c])
