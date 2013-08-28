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
MIN_LEN = 4

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


def c(candidate):
    return str(candidate.index) + " " + "".join(candidate.part)


def replaceWithWord(candidate, word, rng):
    if ("".join(sorted(word)) in wordDict) and len(word) >= MIN_LEN:
            properWord = wordDict["".join(sorted(word))]
            properWord = properWord[0].upper() + properWord[1:].lower()
            candidate.part[rng[0]:rng[1]] = properWord
            return True
    return False


def solve(candidate):

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
        if replaceWithWord(joinSolution, candidate.part[:candidate.index + 1],
                           (0, candidate.index + 1)):
            joinSolution.index = 0
        else:
            joinSolution.cost = cost.MAX

    # Case 2 : skip str
    skipSolution = solve(Candidate(index=0,
                                   part=candidate.part[candidate.index + 1:]))
    skipSolution.part = candidate.part[0:candidate.index] + [SKIP_CHAR]\
        + skipSolution.part
    skipSolution.cost += cost.SKIP
    skipSolution.index = candidate.index

    newWordSolution = solve(Candidate(index=MIN_LEN,
                                      part=candidate.part[candidate.index:]))
    # Make sure whatever is left is a valid word
    if newWordSolution.index > 0:
        if not replaceWithWord(newWordSolution,
                           candidate.part[candidate.index:candidate.index +\
                                          newWordSolution.index],
                           (0, newWordSolution.index)):
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
    runString = "etaelehoyrnrsweeneiornvtsdelreiolrertsrhotruongpmghwsihlxtde"\
                "elaneeetldosheeralithtndareluttelderrocltaeiwrtodeoeyladfswp"\
                "sremeucraddfvrntaiansudynaeytnaidthioicheegblyoeielsvvneolii"\
                "wudveieuaoaodptetpurrdeieecnohasapiwdoehltflsbohlamthioeosis"\
                "tssbstwe"
    solution = solve(Candidate(part=runString))
    print "".join(solution.part)
    print str(reduce(lambda s, ch: s + 1 if ch == SKIP_CHAR else s,
                     solution.part, 0)) + " skips"
