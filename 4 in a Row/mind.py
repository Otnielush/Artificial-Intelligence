
# ход - анализ каждого варианта хода на предмет результата и анализ действия которое выбрал опонент
#
# анализаторы:
# 1 - даёт мне Х очков к победе
# 2 - мешает сопернику набрать очки (сколько очков убавиться)
# 3 - попедный ход
# 4 - перекрыть победный ход сопернику
#
# стратегии:
# 1 - Bounded Rationality - сделать веса чтобы выбирать решение
# Random
# Tit-for-tat – מכה מול מכה
# Grim-Trigger – פוגע חזרה ולא סולח
# Forgiving Trigger – פוגע חזרה וסולח

from random import randint
from time import sleep

wins = [0, 0]
currPlayer = 0
board = [[" "]*7 for i in range(6)]  # [rows][columns]
try:
    file = open("weights.ai", "r")
    loaded = file.readlines()
    file.close()
except:
    print("File not found")
    loaded = ["200", "12", "70", "200", "12", "100"]

# print("{}".format(loaded))

# print("len1(rows): %d, len2(cols): %d" % (len(board),len(board[0])))
print("I wish you a good game")

# board[1][2] = "+"
# board[5][0] = " "
# board[5][1] = "+"
# board[5][3] = "O"
# board[4][2] = "O"

# possible moves
def posMoves():
    posList = []
    for j in range(7):
        i = 5
        if not board[0][j] == " ":
            posList.append(-1)
            continue
        while not board[i][j] == " " and i > 0:
            i -= 1
        posList.append(i)
    return posList

# both for the move and for checking
def maxInRow(player,row,col):
    inRow4 = 0
    lastTurn = 0
    inRow = 0
    inRowPosib = 0
    inRowMax = 0
    sim = "O" if player == 0 else "+"
    rowTmp = board[row].copy()
    rowTmp[col] = sim
    start = col-3
    if start < 0: start = 0
    end = col + 4
    if end > 7: end = 7

    for i in range(start, end):
        if rowTmp[i] == " ":
            inRowPosib += 1
            inRow = 0
            continue
        if rowTmp[i] == sim:
            inRow += 1
            inRowPosib += 1
            if inRow > inRowMax: inRowMax = inRow
        else:
            inRow = 0
            inRowPosib = 0

    if inRowMax >= 4: inRow4 = 1
    if inRowPosib >= 4:
        if inRow >= 1 and inRowMax >= 2 or inRowMax == 3: lastTurn = 1
    if len(rowTmp) < 4: inRowPosib = 0
    return inRow4, inRowPosib, lastTurn*1.5

# both for the move and for checking
def maxInCol(player, row, col):
    inCol4 = 0
    lastTurn = 0
    inCol = 0
    inColPosib = 0
    inColMax = 0
    colTmp = []
    sim = "O" if player == 0 else "+"
    for rows in board:
        colTmp.append(rows[col])
    colTmp[row] = sim

    start = row + 4
    if start > 5: start = 5
    end = row - 3
    if end < 0: end = 0

    for i in range(start, end, -1):
        if colTmp[i] == " ":
            inColPosib += 1
            inCol = 0
            continue
        if colTmp[i] == sim:
            inCol += 1
            inColPosib += 1
            if inCol > inColMax: inColMax = inCol
        else:
            inCol = 0
            inColPosib = 0

    if inColMax >= 4: inCol4 = 1
    if inColPosib >= 4:
        if inColMax == 3 or inCol >= 1 and inColMax >= 2: lastTurn = 1
    if len(colTmp) < 4: inColPosib = 0
    return inCol4, inColPosib, lastTurn

# \
def maxInDiagLeft(player, row, col):
    inDiag4 = 0
    lastTurn = 0
    inDiag = 0
    inDiagPosib = 0
    inDiagMax = 0
    diagTmp = []
    sim = "O" if player == 0 else "+"
    for i in range(6):
        cols = col-(row-i)
        if cols < 0: continue
        if cols > 6: break
        diagTmp.append(board[i][cols])
        if row == i: diagTmp[len(diagTmp)-1] = sim

    diagTmp.reverse()
    for cell in diagTmp:
        if cell == " ":
            inDiagPosib += 1
            inDiag = 0
            continue
        if cell == sim:
            inDiag += 1
            inDiagPosib += 1
            if inDiag > inDiagMax: inDiagMax = inDiag
        else:
            inDiag = 0
            inDiagPosib = 0

    if inDiagMax >= 4: inDiag4 = 1
    if inDiagPosib >= 4:
        if inDiag >= 1 and inDiagMax >= 2 or inDiagMax == 3: lastTurn = 1
    if len(diagTmp) < 4: inDiagPosib = 0
    return inDiag4, inDiagPosib, lastTurn

# /
def maxInDiagRight(player, row, col):
    inDiag4 = 0
    lastTurn = 0
    inDiag = 0
    inDiagPosib = 0
    inDiagMax = 0
    diagTmp = []
    sim = "O" if player == 0 else "+"
    for i in range(6):
        cols = col+(row-i)
        if cols < 0: break
        if cols > 6: continue
        diagTmp.append(board[i][cols])
        if row == i: diagTmp[len(diagTmp)-1] = sim

    diagTmp.reverse()
    for cell in diagTmp:
        if cell == " ":
            inDiagPosib += 1
            inDiag = 0
            continue
        if cell == sim:
            inDiag += 1
            inDiagPosib += 1
            if inDiag > inDiagMax: inDiagMax = inDiag
        else:
            inDiag = 0
            inDiagPosib = 0

    if inDiagMax >= 4: inDiag4 = 1
    if inDiagPosib >= 4:
        if inDiag >= 1 and inDiagMax >= 2 or inDiagMax == 3: lastTurn = 1
    if len(diagTmp) < 4: inDiagPosib = 0
    return inDiag4, inDiagPosib, lastTurn

# 4 functions for analise in 1 massive
Review = [maxInRow,maxInCol,maxInDiagLeft,maxInDiagRight]

# Checking after move
def win(player,row,col):
    # print("Win check")
    winner = "Homo sapiens" if player == 0 else "Artificial Intelligence"
    four,posToWin,lastTurn = maxInRow(player,row,col)
    if four == 1:
       print("Winner by row! -",winner)
       return 1
    four, posToWin, lastTurn = maxInCol(player, row, col)
    if four == 1:
        print("Winner by column! -",winner)
        return 1
    four, posToWin, lastTurn = maxInDiagLeft(player, row, col)
    if four == 1:
        print("Winner by left diagonal! -", winner)
        return 1
    four, posToWin, lastTurn = maxInDiagRight(player, row, col)
    if four == 1:
        print("Winner by right diagonal! -", winner)
        return 1

# for AI
def makeValuation(player, row, col):
    winM, goodM, almWin = 0, 0, 0
    for i in range(len(Review)):
        w, g, a = Review[i](player, row, col)
        winM += w
        goodM += g
        almWin += a
    return winM, goodM, almWin

# to show table of game
def printBoard():
    for i in range(len(board)):
        sleep(0.02)
        # print("%d " % i, end="")
        print("|", end="")
        for k in board[i]:
            print(" %s |" % k, end='')
        print()
        print("-----------------------------")
    # print("  ",end="")
    for j in range(7):
        print("  %d " % (j+1), end="")
    print("\n")

def newGame():
    global board
    board = [[" "] * 7 for i in range(6)]

# Put simon on table
def move(player,col):
    global board, currPlayer
    if player == 0:
        sim = "O"
        print("Player move, 'O'")
    else:
        sim = "+"
        print("Ai move, '+'")
    r = 5

    if not board[0][col] == " ":
        print("Column full. Please choose another")
        return 0

    while not board[r][col] == " " and r > 0:
        r -= 1
    board[r][col] = sim
    printBoard()
    # Check for winning instanse
    if 1 == win(player, r, col): return 2
    currPlayer += 1
    currPlayer %= 2
    return 1

# Strategies with weights
# 1st - Multiplier aganst Human after agression, 2nd - how many turns
# Tit-for-tat – מכה מול מכה
Tit4Tat = [2,1]
# Grim-Trigger – פוגע חזרה ולא סולח
GrimTrigger = [2,200]
# Forgiving Trigger – פוגע חזרה וסולח
Forgiving = [2,3]


def AImove(myNum):
    global agr, agrTurns
    moveList = posMoves()
    movePoints = []
    for i in range(len(moveList)):
        floor = 1
        if moveList[i] == -1:
            movePoints.append(-1)
            continue
        winM, goodM, almWin = makeValuation(myNum, moveList[i], i) # AI moves profit
        winMH, goodMH, almWinH = makeValuation((myNum+1) % 2, moveList[i], i) # Human/opponent moves profit
        k = i-1 if i > 0 else 0
        j = i+1 if i < 6 else 6
        floor -= (moveList[k]+moveList[j]-moveList[i]*2)/10
        if floor > 1: floor = 1
        # print(floor)
        movePoints.append((winM+winMH*agr)*weights[0]+(goodM+goodMH*agr)*weights[1]*floor+(almWin+almWinH*agr)*weights[2])
    if agr > 1: agrTurns -= 1
    if agrTurns <= 0:
        agr = 1
        agrTurns = strategy[1]
    # print("{}".format(moveList))
    # print('{}'.format(movePoints))
    return movePoints.index(max(movePoints))

# Cycle game
def playGame():
    global wins
    while (True):
        global choiceCl, currPlayer
        if currPlayer == 0:
            try:
                choiceCl = int(input("Your turn(1-7): "))-1
                if 2 == move(currPlayer, choiceCl):
                # if 2 == move(currPlayer, AImove(currPlayer)):
                    if currPlayer == 0: wins[0] +=1
                    else: wins[1] += 1
                    currPlayer = (currPlayer+1) % 2
                    break #WINNING()
            except:
                print("Not allowed")
        elif currPlayer == 1:
            if 2 == move(currPlayer, AImove(currPlayer)):
                if currPlayer == 0: wins[0] += 1
                else: wins[1] += 1
                currPlayer = (currPlayer + 1) % 2
                break #WINNING()



# Some options
strategy = Tit4Tat
agr = strategy[0]
agrTurns = strategy[1]
weights = [int(x) for x in loaded]
# print("{}".format(weights))
while (True):
    printBoard()
    playGame()
    print("Score of epic competition:\n Human: %d  AI: %d" % (wins[0],wins[1]))
    file = open("weights.ai", "w")

    file.writelines(str(weights[i])+"\n" for i in range(3))

    file.close()
    ask = input("Play more?(y) or ("")")
    if len(ask) == 0: ask = "y"
    if not ask == "y": break
    newGame()

