from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPainter
import GamePlayer


board = None
rundencounter = 0

# optional function - if defined, is called when the game has started before the first move
# can be necessary, e.g. when having game options
def initGame():
    global board
    board = [['1', '_', '_', '_', '_', '_', '_'],
             ['2', '_', '_', '_', '_', '_', '_'],
             ['3', '_', '_', '_', '_', '_', '_'],
             ['4', '_', '_', '_', '_', '_', '_'],
             ['5', '_', '_', '_', '_', '_', '_'],
             ['6', '_', '_', '_', '_', '_', '_'],
             ['7', '_', '_', '_', '_', '_', '_']]


# paint the Game - obligatory function that must exist!
def paintGame(painter : QPainter):
    painter.fillRect(0, 0, 700, 700, Qt.white)

    pen = painter.pen()
    pen.setWidth(3)
    painter.setPen(pen)
    #horizontal
    painter.drawLine(0, 100, 700, 100) #x1, y1, x2, y2
    painter.drawLine(0, 200, 700, 200)
    painter.drawLine(0, 300, 700, 300)
    painter.drawLine(0, 400, 700, 400)
    painter.drawLine(0, 500, 700, 500)
    painter.drawLine(0, 600, 700, 600)

    #vertical
    painter.drawLine(100, 100, 100, 700)
    painter.drawLine(200, 100, 200, 700)
    painter.drawLine(300, 100, 300, 700)
    painter.drawLine(400, 100, 400, 700)
    painter.drawLine(500, 100, 500, 700)
    painter.drawLine(600, 100, 600, 700)

    font = painter.font()
    font.setPixelSize(80)
    painter.setFont(font)

    for i in range(7):
        for j in range(7):
            if board[i][j] != '_':
                painter.drawText(i*100, j*100, 100, 100, Qt.AlignCenter, board[i][j])


playerSymbols = ['r', 'g']


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
    global rundencounter
    currentPlayerIndex = GamePlayer.getCurrentPlayerIndex()
    if event.type() == QEvent.MouseButtonRelease:
        pos = event.pos()
        i = pos.x() // 100
        j = pos.y() // 100
        if i < 0 or i > 7 or j < 0 or j > 7:
            return None
        playerSymbol = playerSymbols[currentPlayerIndex]
        full = True
        for temp in range (6, 0, -1):
            if board[i][temp] == '_':
                board[i][temp] = playerSymbol
                rundencounter += 1
                full = False
                break
        if full:
            return None
        # Gewinncheck
        if iswon(board, playerSymbol):
            print('GAME OVER)')
            GamePlayer.showMessageLaterForAll('Game Over', GamePlayer.getPlayerNames()[currentPlayerIndex] + ' has won the game.')
            return -1
        # drawcheck
        if rundencounter == 42:
            print('GAME OVER')
            GamePlayer.showMessageForAll('Game Over', 'The game is a draw.')
            return -1

        return (currentPlayerIndex + 1) % GamePlayer.getPlayerCount()




# helper function
def iswon(board, symbol):
    # kernels festlegen
    kern_hor = [[1, 1, 1, 1]]
    kern_vert = [[1], [1], [1], [1]]
    kern_diag_1 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    kern_diag_2 = [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
    kernels = [kern_hor, kern_vert, kern_diag_1, kern_diag_2]
    # board konvertieren
    A = [[0 for i in range(7)] for j in range(6)]
    for i in range(7):
        for j in range(1, 7):
            if board[i][j] == symbol:
                A[i][j] = 1
    #konvolutions-check
    for kernel in kernels:
        if 4 in convolve2d(A, kernel, mode="valid"):
            return True
    return False


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
