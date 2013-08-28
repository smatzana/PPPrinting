'''
Created on Aug 23, 2013

@author: sotiris
'''
import sys


def enum(**enums):
    return type('Enum', (), enums)

wordDict = dict()
cost = enum(SKIP=10, JOIN=0, MAX=sys.maxint)
SKIP_CHAR = "-"

cache = dict()


def loadWords(fileName):
    global maxWordLength
    with open(fileName) as f:
        for word in f:
            word = word.rstrip("\n")
            wordDict[''.join(sorted(word))] = word


class Candidate(object):

    def __init__(self, index=0, part='', cost=cost.JOIN):
        self.index = index
        self.part = list(part)
        self.cost = cost

    def __str__(self):
        return "index:" + str(self.index) + " STR:" + "".join(self.part)\
            + " Cost: " + str(self.cost)


def c(candidate):
    return str(candidate.index) + " " + "".join(candidate.part)


def solve(candidate):

    global sTimes, cTimes

    if c(candidate) in cache:
        cached = cache[c(candidate)]
        return Candidate(index=cached.index, part=cached.part,
                         cost=cached.cost)

    if candidate.index >= len(candidate.part):
        return Candidate(index=len(candidate.part))

    # case 1 join previous string
    joinSolution = solve(Candidate(index=candidate.index + 1,
                                       part=candidate.part))
    if joinSolution.index > candidate.index:
        candidateWord = candidate.part[:candidate.index + 1]
        if ("".join(sorted(candidateWord)) in wordDict)\
                                and len(candidateWord) >= 4:
            joinSolution.index = candidate.index
            properWord = wordDict["".join(sorted(candidateWord))]
            properWord = properWord[0].upper() + properWord[1:].lower()
            joinSolution.part[:candidate.index + 1] = properWord
        else:
            joinSolution.cost = cost.MAX

    # Case 2 : skip str
    skipSolution = solve(Candidate(index=0,
                                   part=candidate.part[candidate.index + 1:]))
    skipSolution.part = candidate.part[0:candidate.index] + [SKIP_CHAR]\
        + skipSolution.part
    skipSolution.cost += cost.SKIP
    skipSolution.index = candidate.index

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
            newWordSolution.part[0:newWordSolution.index] = properWord
        else:
            newWordSolution.cost = cost.MAX
    newWordSolution.index = candidate.index
    newWordSolution.part = candidate.part[0:candidate.index] +\
        newWordSolution.part

    solutionList = [joinSolution, skipSolution, newWordSolution]

    solutionList.sort(key=lambda solution: solution.cost)
    s = solutionList[0]
    cache[c(candidate)] = Candidate(index=s.index, part=s.part, cost=s.cost)
    return s

if __name__ == "__main__":
    loadWords(sys.argv[1])
    final = solve(Candidate(part="etaelehoyrnrsweeneiornvtsdelreiolrertsrhotruongpmghwsihlxtde"
                            "elaneeetldosheeralithtndareluttelderrocltaeiwrtodeoeyladfswp"
                            "sremeucraddfvrntaiansudynaeytnaidthioicheegblyoeielsvvneolii"
                            "wudveieuaoaodptetpurrdeieecnohasapiwdoehltflsbohlamthioeosistssbstwe"
                             ))
    print "".join(final.part)
    print str(reduce(lambda s, ch: s + 1 if ch == SKIP_CHAR else s,
                     final.part, 0)) + " skips"
    #print "CTimes:" + str(cTimes) + " sTimes:" + str(sTimes)
    #for c in cache.keys():
    #    print str(c) + ' : ' + str(cache[c])
