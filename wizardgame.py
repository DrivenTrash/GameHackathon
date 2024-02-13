import copy
import random
from PyQt5.QtCore import Qt, QEvent, QRect
from PyQt5.QtGui import QPainter, QPixmap, QFont, QColor
import numpy as np
from PyQt5.QtWidgets import QDialog

import GamePlayer
from Internal import Client

cards = [
    ('j', 0, '0_in_BLUE'), ('j', 1, '0_in_GREEN'), ('j', 2, '0_in_RED'), ('j', 3, '0_in_YELLOW'),
    ('b', 1, '1_in_BLUE'), ('g', 1, '1_in_GREEN'), ('r', 1, '1_in_RED'), ('y', 1, '1_in_YELLOW'),
    ('b', 2, '2_in_BLUE'), ('g', 2, '2_in_GREEN'), ('r', 2, '2_in_RED'), ('y', 2, '2_in_YELLOW'),
    ('b', 3, '3_in_BLUE'), ('g', 3, '3_in_GREEN'), ('r', 3, '3_in_RED'), ('y', 3, '3_in_YELLOW'),
    ('b', 4, '4_in_BLUE'), ('g', 4, '4_in_GREEN'), ('r', 4, '4_in_RED'), ('y', 4, '4_in_YELLOW'),
    ('b', 5, '5_in_BLUE'), ('g', 5, '5_in_GREEN'), ('r', 5, '5_in_RED'), ('y', 5, '5_in_YELLOW'),
    ('b', 6, '6_in_BLUE'), ('g', 6, '6_in_GREEN'), ('r', 6, '6_in_RED'), ('y', 6, '6_in_YELLOW'),
    ('b', 7, '7_in_BLUE'), ('g', 7, '7_in_GREEN'), ('r', 7, '7_in_RED'), ('y', 7, '7_in_YELLOW'),
    ('b', 8, '8_in_BLUE'), ('g', 8, '8_in_GREEN'), ('r', 8, '8_in_RED'), ('y', 8, '8_in_YELLOW'),
    ('b', 9, '9_in_BLUE'), ('g', 9, '9_in_GREEN'), ('r', 9, '9_in_RED'), ('y', 9, '9_in_YELLOW'),
    ('b', 10, '10_in_BLUE'), ('g', 10, '10_in_GREEN'), ('r', 10, '10_in_RED'), ('y', 10, '10_in_YELLOW'),
    ('b', 11, '11_in_BLUE'), ('g', 11, '11_in_GREEN'), ('r', 11, '11_in_RED'), ('y', 11, '11_in_YELLOW'),
    ('b', 12, '12_in_BLUE'), ('g', 12, '12_in_GREEN'), ('r', 12, '12_in_RED'), ('y', 12, '12_in_YELLOW'),
    ('b', 13, '13_in_BLUE'), ('g', 13, '13_in_GREEN'), ('r', 13, '13_in_RED'), ('y', 13, '13_in_YELLOW'),
    ('w', 0, '14_in_BLUE'), ('w', 1, '14_in_GREEN'), ('w', 2, '14_in_RED'), ('w', 3, '14_in_YELLOW'),
]

colors = {'b': 'blue', 'g': 'green', 'r': 'red', 'y': 'yellow'}
colorSort = {'w': 5, 'j': 4, 'b': 3, 'g': 2, 'r': 1, 'y': 0}

# GamePlayer Setup
wizardDict = dict()
for card in cards:
    wizardDict[card[2]] = QPixmap(GamePlayer.registerFile('wizardCards/' + card[2] + '.png'))
for name in ["back", "BG_game", "BG_lobby", "BG_main", "green", "header", "icon", "logo_downsized", "logo_new",
             "red", "symbols", "wizard", "wizard_small", "wizardgame", "yellow"]:
    wizardDict[name] = QPixmap(GamePlayer.registerFile('wizardCards/' + name + '.png'))

GamePlayer.addToNoSyncList('wizardDict')

options = [
    GamePlayer.addDropDownBoxOption(['Auto', 'Demo']),
    GamePlayer.addDropDownBoxOption(['Realmode', 'Devmode']),
    GamePlayer.addDropDownBoxOption(['Set 1', 'Set 2', 'Set 3', 'Set 4', 'Set 5', 'Set 6', 'Set 7', 'Set 8', 'Set 9', 'Set 10'])
]

# Globals
numberOfPlayers = 3
numberOfSets = 3    # just for demo mode
realMode = True
deck = []           # array of cards
publicStack = []
lastStack = []
hands = []          # 3x arrays of cards
predictions = []    #für jedes Set
predictionCount = 0
stitchCounter = []   #Anzahl der Stiche pro Set
score = []          #Punkte jedes Spielers

setCount = 0
cardsCount = 0  # zählt die gespielten Karten innerhalb eines Sets
trump = None    #color or None
trumpCard = None
firstOfSet = 0
firstOfRound = 0


def sortedCards(cards):
    s = sorted(cards, key=lambda x: (colorSort[x[0]], x[1]), reverse = True)
    return s


def newSet():
    global deck, publicStack, lastStack, hands, setCount, trump, trumpCard
    # Spielvariablen aktualisieren
    hands = []
    setCount += 1

    # Mischen, Karten geben, Hände sortieren
    random.seed()
    random.shuffle(deck)

    for player in range(numberOfPlayers):
         hand = []
         for n in range(setCount):
             hand.append(deck[setCount*player + n])
         hand = sortedCards(hand)
         hands.append(hand)

    #Trumpf bestimmen (Farbe oder None), Zusatz: Wizard --> Trumpf per Eingabe abfragen
    if numberOfPlayers*setCount >= 60:
        trump = None
    else:
        trumpCard = deck[numberOfPlayers*setCount]
        trump = trumpCard[0] if trumpCard[0] in ['b', 'g', 'r', 'y'] else None


# optional function - if defined, is called when the game has started before the first move
# can be necessary, e.g. when having game options
def initGame():
    global deck, numberOfPlayers, firstOfRound, firstOfSet, predictions, stitchCounter, score, setCount, cardsCount, \
        trump, trumpCard, firstOfSet, publicStack, hands, predictionCount, numberOfSets, realMode
    numberOfPlayers = GamePlayer.getPlayerCount()
    firstOfSet = GamePlayer.getCurrentPlayerIndex()
    firstOfRound = GamePlayer.getCurrentPlayerIndex()
    predictions = [-1 for _ in range(numberOfPlayers)]
    predictionCount = 0
    stitchCounter = [0 for _ in range(numberOfPlayers)]
    score = [0 for _ in range(numberOfPlayers)]
    cardsCount = 0
    trump = None
    trumpCard = None
    firstOfSet = 0
    firstOfRound = firstOfSet

    # Demo mode (nur 3 Sets bis zum Spielende)
    if options[0].value == "Demo":
        numberOfSets = 3
    else:
        numberOfSets = 60 // numberOfPlayers

    # Offenes oder verdecktes Spielfeld
    if options[1].value == "Realmode":
        realMode = True
    else:
        realMode = False

    # Starte Spiel mit ausgewählter Setnummer
    setCount = int(options[2].value[-1]) - 1

    #Spielkarten erstellen
    for card in cards:
        deck.append(card)

    #Set initialisieren
    newSet()


# paint the Game - obligatory function that must exist!
def paintGame(painter : QPainter):
    painter.fillRect(-200, -100, 2000, numberOfPlayers*200 + 400, Qt.white)
    # painter.drawPixmap(QRect(-500, -100, 2500, numberOfPlayers*200 + 400), wizardDict["BG_game"]) # zu langsam

    pen = painter.pen()
    pen.setWidth(3)
    # pen.setBrush(Qt.GlobalColor.white)
    painter.setPen(pen)
    # painter.drawLine(0, 0, setCount*100, 0)
    painter.drawLine(0, 200, setCount*100, 200)
    for p in range(numberOfPlayers):
        painter.drawLine(0, 200*p + 400, setCount*100, 200*p + 400)

    # wizard design -- png zu groß
    painter.drawPixmap(QRect(-195, -145, 180*2, 101*2), wizardDict["logo_downsized"])
    #painter.drawPixmap(QRect(-155, 15, 100, 170), wizardDict["back"])

    # visualize setCount / maximale Setanzahl
    font = QFont("Times", 20)
    painter.setFont(font)
    painter.drawText(1500, -30, "set:         " + str(setCount) + " / " + str(numberOfSets))

    # visualize publicStack
    for col, value in enumerate(publicStack):
        painter.drawPixmap(QRect(col * 100 + 2, 15, 96, 170), wizardDict[value[2]])

    # visualize lastStack
    for col, value in enumerate(lastStack):
        painter.drawPixmap(QRect(col * 50 + 902, 15, 96, 170), wizardDict[value[2]])

    # visualize hands
    if hands != []:
        if realMode:
            thisPlayerIndex = Client.gameObject.thisPlayerIndex
            for row in range(numberOfPlayers):
                if row == thisPlayerIndex:
                    for col, value in enumerate(hands[row]):
                        painter.drawPixmap(QRect(col * 100 + 2, (row + 1) * 200 + 15, 96, 170), wizardDict[value[2]])
                else:
                    for col, _ in enumerate(hands[row]):
                        painter.drawPixmap(QRect(col * 100 + 2, (row + 1) * 200 + 15, 96, 170), wizardDict["back"])
        else:
            for row in range(numberOfPlayers):
                for col, value in enumerate(hands[row]):
                    painter.drawPixmap(QRect(col * 100 + 2, (row+1) * 200 + 15, 96, 170), wizardDict[value[2]])

    # visualize trumpCard
    if trumpCard != None:
        # painter.setFont(QFont("Times", 20))
        painter.drawText(1500, 75, "trump: ")
        if trump == None:
            painter.drawText(1500, 125, "none")
        else:
            painter.drawText(1500, 125, colors[trump])
        row, col = 0, 16
        painter.drawPixmap(QRect(col * 100 + 2, row * 200 + 15, 96, 170), wizardDict[trumpCard[2]])

    # Beschriftung Player, Vorhersagen, Score
    playerNames = GamePlayer.getPlayerNames()
    for row in range(numberOfPlayers):
        #painter.setFont(QFont("Times", 15))
        font = QFont("Times", 15)
        font.setWeight(QFont.Bold)
        if row == GamePlayer.getCurrentPlayerIndex():
            painter.drawText(-185, (row + 1) * 200 + 40, "→")
        painter.setFont(font)
        painter.drawText(-150, (row + 1) * 200 + 40, str(playerNames[row]))
        font.setWeight(QFont.Normal)
        painter.setFont(font)
        pred = "--" if predictions[row] == -1 else str(predictions[row])
        painter.drawText(-150, (row + 1) * 200 + 80, "pred: " + pred)
        painter.drawText(-150, (row + 1) * 200 + 120, "stitches: " + str(stitchCounter[row]))
        painter.drawText(-150, (row + 1) * 200 + 160, "score: " + str(score[row]))


def getNextPlayerIndex():
    playersLeftSet = GamePlayer.getLeftPlayersSet()
    index = (GamePlayer.getCurrentPlayerIndex() + 1) % GamePlayer.getPlayerCount()
    while index in playersLeftSet:
        index = (index + 1) % GamePlayer.getPlayerCount()
    return index


# process an event for making a move - obligatory function that must exist!
# return a value in 0...playerCount-1 as the index of the next player to move
# return nothing or None if the move is not yet finished
# return -1 if the game is over
# The following event types are sent to the makeMove function:
#   QEvent.MouseButtonPress
#   QEvent.MouseButtonRelease
#   QEvent.MouseButtonDblClick
#   QEvent.KeyPress
#   QEvent.KeyRelease
#   QEvent.Wheel (mouse wheel)
#   QEvent.MouseMove (if enabled)
def evaluateRound():
    global stitchCounter, publicStack, trump, firstOfRound
    highest = 0
    pos = None
    roundColour = None
    # Wizard Check
    for i in range(numberOfPlayers):
        if publicStack[i][0] == 'w':
            stitchCounter[(firstOfRound + i) % numberOfPlayers] += 1
            firstOfRound = (firstOfRound + i) % numberOfPlayers
            return None
    # Narrenstich**
    if all(flag == 'j' for (flag, _, _) in publicStack):
        stitchCounter[firstOfRound] += 1
        return None
    # Trumpf-Check
    if any(flag == trump for (flag, _, _) in publicStack):
        for idx, i in enumerate(publicStack):
            if trump in i:
                if i[1] > highest:
                    highest = i[1]
                    pos = idx
        stitchCounter[(firstOfRound + pos) % numberOfPlayers] += 1
        firstOfRound = (firstOfRound + pos) % numberOfPlayers
        return None
    # Farbstich (roundcolour noch intern)
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
    global stitchCounter, predictions, score, setCount, firstOfSet, firstOfRound, cardsCount, predictionCount
    for i in range(numberOfPlayers):
        if stitchCounter[i] == predictions[i]:
            score[i] += 20 + 10 * stitchCounter[i]
        else:
            score[i] -= 10 * abs(stitchCounter[i] - predictions[i])
    predictions = [-1 for _ in range(numberOfPlayers)]
    predictionCount = 0
    stitchCounter = [0 for _ in range(numberOfPlayers)]
    cardsCount = 0
    firstOfSet = (firstOfSet + 1) % numberOfPlayers
    firstOfRound = firstOfSet


def finalResult():
    # global score
    res = "Final scores: \n"
    for i, value in enumerate(score):
        res +=  GamePlayer.getPlayerNames()[i] + ": " + str(value) + ". \n"
    winner = GamePlayer.getPlayerNames()[np.argmax(score)]
    res += winner + " has won the game."
    return res


def roundColor(publicStack):
    for card in publicStack:
        if card[0] in ['b', 'g', 'r', 'y']:
            return card[0]
    return None


def cardIsLegal(clickedPlayerIndex, clickedCardIndex):
    card = hands[clickedPlayerIndex][clickedCardIndex]
    # publicStack   # Array der bereits gespielte Karten, kann leer sein
    rC = roundColor(publicStack)
    if rC in [None]:
        return True
    if any(flag == rC for (flag, _, _) in hands[clickedPlayerIndex]):
        if hands[clickedPlayerIndex][clickedCardIndex][0] in ['w', 'j', rC]:
            return True
        return False
    return True


def makeMove(event : QEvent):
    global predictionCount, cardsCount, stitchCounter, publicStack, lastStack, trump, firstOfRound
    currentPlayerIndex = GamePlayer.getCurrentPlayerIndex()

    #dlg = QDialog()
    #dlg.setWindowTitle("Hello")
    #dlg.exec()

    #Vorhersagerunde
    if predictionCount < numberOfPlayers*2:
        if event.type() == QEvent.KeyRelease:
            eingabe = event.text()
            if eingabe not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                print("Nur Zahlen erlaubt! (Bsp. 03)")
                return None
            if predictionCount % 2 == 0:   #erste Stelle eingegeben
                predictions[currentPlayerIndex] = int(eingabe) * 10
                predictionCount += 1
                return None
            if predictionCount % 2 == 1:   #zweite Stelle eingegeben
                predictions[currentPlayerIndex] += int(eingabe)
                predictionCount += 1
                return getNextPlayerIndex()
    else:
        if event.type() == QEvent.MouseButtonRelease:
            pos = event.pos()
            #print('pos.x(): ' + str(pos.x()) + ' pos.y(): ' + str(pos.y()))
            if pos.x() < 0: return None
            clickedCardIndex = pos.x() // 100           #col
            clickedPlayerIndex = pos.y() // 200 - 1     #row

            try:
                # Karte spielen
                if clickedPlayerIndex == currentPlayerIndex:
                    if cardIsLegal(clickedPlayerIndex, clickedCardIndex):
                        publicStack.append(hands[clickedPlayerIndex][clickedCardIndex])
                        del hands[clickedPlayerIndex][clickedCardIndex]
                        cardsCount += 1
                    else:
                        GamePlayer.showMessageLater("Invalid card", "Please choose another card.")
                        return None

                    if cardsCount % numberOfPlayers == 0:
                        # Evaluieren und Stiche notieren, PublicStack kopieren und leeren
                        evaluateRound()
                        lastStack = publicStack.copy()
                        publicStack = []

                        # Set vollständig gespielt:
                        if cardsCount == setCount * numberOfPlayers:
                            calculateResult()

                            # alle Sets gespielt (Match zu Ende?)
                            if setCount == numberOfSets:
                                # show final result
                                GamePlayer.showMessageLaterForAll("Game over!", finalResult())
                                return -1

                            # sonst neues Set
                            newSet()
                        
                        # Gewinner des Stiches eröffnet immer Runde
                        return firstOfRound

                    return getNextPlayerIndex()
            except:
                print("Nicht erlaubt")
                return None


# optional function - only relevant for network mode
# if not defined, the game will be over if a player leaves the game (e.g. by network interruption)
# must return the index of the next player to move or -1 if the game is over
# the next player to move will be probably the currently moving player in most cases but consider
# the case playerIndex == GamePlayer.getCurrentPlayerIndex(), i.e. the currently moving player left the game!!!
# is only called for the currently moving player or the next player if the moving player left the game
# playerLeftGame and makeMove must not return the index of players who already left the game!!!
def playerLeftGame(playerIndex : int):
    if len(GamePlayer.getLeftPlayersSet()) == GamePlayer.getPlayerCount() - 1:
        GamePlayer.showMessageLater('You Won', 'You have won because all other players have left the game.')
        return -1
    GamePlayer.showMessageLaterForAll('Player Left', 'The player "{}" has left the game.'.
                                      format(GamePlayer.getPlayerNames()[playerIndex]))
    if playerIndex == GamePlayer.getCurrentPlayerIndex():
        return getNextPlayerIndex()
    else:
        return GamePlayer.getCurrentPlayerIndex()


# obligatory call to start the game - must be the last command in your program because it will not return!
GamePlayer.run(
    gameName="Wizard",
    minPlayerCount=3,
    maxPlayerCount=6,
    hostGame=3,
)