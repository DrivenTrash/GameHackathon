import random as rnd

# Globals
numberOfPlayers = 0
deck = [('w', 1), ('w', 2), ('w', 3), ('w', 4),
        ('j', 1), ('j', 2), ('j', 3), ('j', 4),
        ('r', 1), ('r', 2), ('r', 3), ('r', 4), ('r', 5), ('r', 6), ('r', 7), ('r', 8), ('r', 9), ('r', 10), ('r', 11), ('r', 12), ('r', 13),
        ('y', 1), ('y', 2), ('y', 3), ('y', 4), ('y', 5), ('y', 6), ('y', 7), ('y', 8), ('y', 9), ('y', 10), ('y', 11), ('y', 12), ('y', 13),
        ('g', 1), ('g', 2), ('g', 3), ('g', 4), ('g', 5), ('g', 6), ('g', 7), ('g', 8), ('g', 9), ('g', 10), ('g', 11), ('g', 12), ('g', 13),
        ('b', 1), ('b', 2), ('b', 3), ('b', 4), ('b', 5), ('b', 6), ('b', 7), ('b', 8), ('b', 9), ('b', 10), ('b', 11), ('b', 12), ('b', 13)]
privateHands = []
publicStack = []
predictions = []
stitchCounter = []
score = []
firstOfSet = 0
firstOfRound = 0
setCounter = 1
trump = ''


# Functions
def initMatch():
    global numberOfPlayers, privateHands, publicStack, firstOfSet, firstOfRound, predictions, stitchCounter, score
    numberOfPlayers = int(input('Wie viele Spieler nehmen Teil?'))
    privateHands = [[] for i in range(numberOfPlayers)]
    publicStack = [0 for i in range(numberOfPlayers)]
    predictions = [0 for i in range(numberOfPlayers)]
    stitchCounter = [0 for i in range(numberOfPlayers)]
    score = [0 for i in range(numberOfPlayers)]
    firstOfSet = int(input('Wer ist der jüngste Spieler?'))
    firstOfRound = firstOfSet

def newSet():
    global privateHands, trump
    #Karten geben
    rnd.shuffle(deck)
    for i in range(numberOfPlayers):
        privateHands[i] = deck[i * setCounter : (i + 1)*setCounter]
    #Trumpf bestimmen
    if numberOfPlayers * setCounter == 60:
        trump = None
    elif deck[numberOfPlayers * setCounter][0] in ['g', 'y', 'b', 'r']:
        trump = deck[numberOfPlayers * setCounter][0]
    elif deck[numberOfPlayers * setCounter][0] == 'j':
        trump = None
    else:
        trump = input("Welche Farbe soll Trumpf sein?")

def makePredictions():
    global predictions
    for i in range(numberOfPlayers):
        predictions[(i + firstOfSet) % numberOfPlayers] = int(input("Wie viele Stiche wird Spieler " + str((i + firstOfRound) % numberOfPlayers) + " machen?"))

def playRound():
    #noch kein Check ob Karte legal ist
    global publicStack, privateHands
    for i in range(numberOfPlayers):
        temp = int(input('Welche Karte soll Spieler ' + str((i + firstOfRound) % numberOfPlayers) + ' spielen?'))
        #hand = privateHands[(i + firstOfRound) % numberOfPlayers]
        # publicStack[i] = hand.pop(temp)
        publicStack[i] = privateHands[(i + firstOfRound) % numberOfPlayers].pop(temp)

def evaluateRound():
    global stitchCounter, publicStack, trump, firstOfRound
    highest = 0
    pos = None
    roundColour = None
    #Wizard Check
    for i in range(numberOfPlayers):
        if publicStack[i][0] == 'w':
            stitchCounter[(firstOfRound + i) % numberOfPlayers] += 1
            firstOfRound = (firstOfRound + i) % numberOfPlayers
            return None
    #Narrenstich**
    if all(flag == 'j' for (flag, _) in publicStack):
        stitchCounter[firstOfRound] += 1
        return None
    #Trumpf-Check
    if any(flag == trump for (flag, _) in publicStack):
        for idx, i in enumerate(publicStack):
            if trump in i:
                if i[1] > highest:
                    highest = i[1]
                    pos = idx
        stitchCounter[(firstOfRound + pos) % numberOfPlayers] += 1
        firstOfRound = (firstOfRound + pos) % numberOfPlayers
        return None
    #Farbstich (roundcolour noch intern)
    for idx, i in enumerate(publicStack):
        if roundColour not in ['r', 'g', 'b', 'y']:
            roundColour = i[0]
        if i[0] == roundColour and roundColour != 'j':
            if i[1] > highest:
                highest = i[1]
                pos = idx
    stitchCounter[(firstOfRound + pos) % numberOfPlayers] += 1
    firstOfRound = (firstOfRound + pos) % numberOfPlayers
    return None

def calculateResult():
    global stitchCounter, predictions, score, setCounter, firstOfSet, firstOfRound
    for i in range(numberOfPlayers):
        if stitchCounter[i] == predictions[i]:
            score[i] += 20 + 10 * stitchCounter[i]
        else:
            score[i] -= 10 * abs(stitchCounter[i]-predictions[i])
    predictions = [0 for i in range(numberOfPlayers)]
    stitchCounter = [0 for i in range(numberOfPlayers)]
    setCounter += 1
    firstOfSet = (firstOfSet + 1) % numberOfPlayers
    firstOfRound = firstOfSet

def finalResult():
    for idx, i in enumerate(score):
        print(idx, i)

# Main
initMatch()
for i in range(60 // numberOfPlayers):
    newSet()
    print('setCounter:', setCounter)
    print('Trumpf: ', trump)
    print('Hands: ')
    for idx, i in enumerate(privateHands):
        print('Spieler ' + str(idx) + ': ', i)
    makePredictions()
    print('predictions: ', predictions)
    for i in range(setCounter):
        print('Hands: ')
        for idx, i in enumerate(privateHands):
            print('Spieler ' + str(idx) + ': ', i)
        print('firstOfRound: ', firstOfRound)
        playRound()
        print('publicStack: ', publicStack)
        evaluateRound()
        print('stitchCounter: ', stitchCounter)
    calculateResult()
    print('score: ', score)
finalResult()





