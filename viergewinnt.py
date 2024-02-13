from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPainter
import GamePlayer


board = None
counter = 0

# optional function - if defined, is called when the game has started before the first move
# can be necessary, e.g. when having game options
def initGame():
    global board
    board = [ ['_', '_', '_', '_', '_', '_'],
              ['_', '_', '_', '_', '_', '_'],
              ['_', '_', '_', '_', '_', '_'],
              ['_', '_', '_', '_', '_', '_'],
              ['_', '_', '_', '_', '_', '_'],
              ['_', '_', '_', '_', '_', '_'],
              ['_', '_', '_', '_', '_', '_'] ]


# paint the Game - obligatory function that must exist!
def paintGame(painter : QPainter):
    painter.fillRect(0, 0, 700, 600, Qt.white)   #width, height

    pen = painter.pen()
    pen.setWidth(3)
    painter.setPen(pen)

    painter.drawLine(0, 100, 700, 100)          #x1, y1, x2, y2
    painter.drawLine(0, 200, 700, 200)
    painter.drawLine(0, 300, 700, 300)
    painter.drawLine(0, 400, 700, 400)
    painter.drawLine(0, 500, 700, 500)
    painter.drawLine(0, 600, 700, 600)

    painter.drawLine(0, 0, 0, 600)
    painter.drawLine(100, 0, 100, 600)
    painter.drawLine(200, 0, 200, 600)
    painter.drawLine(200, 0, 200, 600)
    painter.drawLine(300, 0, 300, 600)
    painter.drawLine(400, 0, 400, 600)
    painter.drawLine(500, 0, 500, 600)
    painter.drawLine(600, 0, 600, 600)
    painter.drawLine(700, 0, 700, 600)

    font = painter.font()
    font.setPixelSize(80)
    painter.setFont(font)

    for i in range(7):              #6 Zeilen
        for j in range(6):          #7 Spalten
            if board[i][j] != '_':
                painter.drawText(i*100, j*100, 100, 100, Qt.AlignCenter, board[i][j])


playerSymbols = ['X', 'O']


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
def makeMove(event : QEvent):
    global counter
    currentPlayerIndex = GamePlayer.getCurrentPlayerIndex()
    if event.type() == QEvent.MouseButtonRelease:
        pos = event.pos()
        i = pos.x() // 100      #Index i wird benötigt zur Berechnung neuer Matrix
        #j = pos.y() // 100
        if i < 0 or i > 6:
            return None
        playerSymbol = playerSymbols[currentPlayerIndex]

        # Berechne neue Matrix anhand von i
        pos_x, pos_y = None, None
        for k in range(5, -1, -1):
            if board[i][k] == '_':
                board[i][k] = playerSymbol
                counter += 1
                pos_x, pos_y = k, i
                break

        if pos_x == None or pos_y == None: return None    #Spieler erhält die Möglichkeit neuen Spielzug zu machen

        #vertical check
        if pos_x < 3:
            if board[pos_y][pos_x] == board[pos_y][pos_x+1] == board[pos_y][pos_x+2] == board[pos_y][pos_x+3] != '_':
                GamePlayer.showMessageLaterForAll('Game Over', GamePlayer.getPlayerNames()[
                    currentPlayerIndex] + ' has won the game. ' + 'vertical')
                return -1

        #horizontal check
        for pos_y in range(4):
            if board[pos_y][pos_x] == board[pos_y+1][pos_x] == board[pos_y+2][pos_x] == board[pos_y+3][pos_x] != '_':
                GamePlayer.showMessageLaterForAll('Game Over', GamePlayer.getPlayerNames()[
                    currentPlayerIndex] + ' has won the game. ' + 'horizontal')
                return -1

        #diagonal check (top left to bottom right)
        for pos_y in range(4):
            for pos_x in range(3):
                if board[pos_y][pos_x] == board[pos_y + 1][pos_x + 1] == board[pos_y + 2][pos_x + 2] == board[pos_y + 3][pos_x + 3] != '_':
                    GamePlayer.showMessageLaterForAll('Game Over', GamePlayer.getPlayerNames()[
                        currentPlayerIndex] + ' has won the game. ' + 'diagonal (top left to bottom right)')
                    return -1

        #diagonal lines (top right to bottom left)
        for pos_y in range(4):
            for pos_x in range(3, 6):
                if board[pos_y][pos_x] == board[pos_y + 1][pos_x - 1] == board[pos_y + 2][pos_x - 2] == board[pos_y + 3][pos_x - 3] != '_':
                    GamePlayer.showMessageLaterForAll('Game Over', GamePlayer.getPlayerNames()[
                        currentPlayerIndex] + ' has won the game. ' + 'diagonal (top right to bottom left)')
                    return -1

        #draw
        if counter >= 42:
            GamePlayer.showMessageForAll('Game Over', 'The game is a draw.')
            return -1

        return (currentPlayerIndex + 1) % GamePlayer.getPlayerCount()


# optional function - only relevant for network mode
# if not defined, the game will be over if a player leaves the game (e.g. by network interruption)
# must return the index of the next player to move or -1 if the game is over
# the next player to move will be probably the currently moving player in most cases but consider
# the case playerIndex == GamePlayer.getCurrentPlayerIndex(), i.e. the currently moving player left the game!!!
# is only called for the currently moving player or the next player if the moving player left the game
# playerLeftGame and makeMove must not return the index of players who already left the game!!!
# def playerLeftGame(playerIndex : int):
#     return -1


# obligatory call to start the game - must be the last command in your program because it will not return!
GamePlayer.run(
    playerTitles=playerSymbols,
)
