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
board = [[" "] * 7 for i in range(6)]  # [rows][columns]
try:
    file = open("weights.ai", "r")
    loaded = file.readlines()
    file.close()
except:
    print("File not found")
    loaded = ["400", "100", "35", "3", "400", "100", "35", "3"]

# print("{}".format(loaded))

# print("len1(rows): %d, len2(cols): %d" % (len(board),len(board[0])))
print("I wish you a good game")


# board[1][2] = "#"
# board[5][0] = " "
# board[5][1] = "#"
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
def maxInRow(player, row, col):
    inRow4 = 0
    inRow3 = 0
    inRow2 = 0
    inRowFree = 0
    numInRow = 0
    inRow = 0
    inRowPosib = 0
    inRowMax = 0
    sim = "O" if player == 0 else "#"
    rowTmp = board[row].copy()
    rowTmp[col] = sim
    start = col - 3
    if start < 0: start = 0
    end = col + 4
    if end > 7: end = 7

    for i in range(start, end):
        if rowTmp[i] == " ":
            inRowPosib += 1
            inRowFree += 1
            inRow = 0
            continue
        if rowTmp[i] == sim:
            inRow += 1
            inRowPosib += 1
            numInRow += 1
            if inRow > inRowMax: inRowMax = inRow
        else:
            inRowFree = 0
            inRow = 0
            inRowPosib = 0
            numInRow = 0

    # if len(rowTmp) < 4:
    #     inRowPosib = 0
    #     numInRow = 0
    else:
        if inRowMax >= 4: inRow4 = 1
        if inRowPosib >= 4:
            if inRowMax == 3 or numInRow >= 3 and inRowMax == 2 : inRow3 = 1
            if inRowMax == 2 or numInRow > 1: inRow2 = 1
        # if inRowPosib >= 5:
            # if numInRow >= 2: inRow2 += 1
    return inRow4, inRow3, inRow2, inRowFree

# both for the move and for checking
def maxInCol(player, row, col):
    inCol4 = 0
    inCol3 = 0
    inCol2 = 0
    numInCol = 0
    inCol = 0
    inColPosib = 0
    inColMax = 0
    colTmp = []
    sim = "O" if player == 0 else "#"
    for rows in board:
        colTmp.append(rows[col])
    colTmp[row] = sim

    start = row + 4
    if start > 5: start = 5
    # end = row - 3
    # if end < 0: end = 0
    end = -1

    for i in range(start, end, -1):
        if colTmp[i] == " ":
            inColPosib += 1
            inCol = 0
            continue
        if colTmp[i] == sim:
            inCol += 1
            inColPosib += 1
            numInCol += 1
            if inCol > inColMax: inColMax = inCol
        else:
            inCol = 0
            inColPosib = 0

    # if len(colTmp) < 4:
    #     inColPosib = 0
    #     numInCol = 0
    else:
        if inColMax >= 4: inCol4 = 1
        if inColPosib >= 4:
            if inColMax == 3: inCol3 = 1
            if inColMax == 2: inCol2 = 1
    return inCol4, inCol3, inCol2, inColPosib - numInCol

# \
def maxInDiagLeft(player, row, col):
    inDiag4 = 0
    inDiag3 = 0
    inDiag2 = 0
    numInDiag = 0
    inDiag = 0
    inDiagPosib = 0
    inDiagMax = 0
    diagTmp = []
    sim = "O" if player == 0 else "#"
    for i in range(6):
        cols = col - (row - i)
        if cols < 0: continue
        if cols > 6: break
        diagTmp.append(board[i][cols])
        if row == i: diagTmp[len(diagTmp) - 1] = sim

    diagTmp.reverse()
    for cell in diagTmp:
        if cell == " ":
            inDiagPosib += 1
            inDiag = 0
            continue
        if cell == sim:
            inDiag += 1
            inDiagPosib += 1
            numInDiag += 1
            if inDiag > inDiagMax: inDiagMax = inDiag
        else:
            inDiag = 0
            inDiagPosib = 0

    # if len(diagTmp) < 4:
    #     inDiagPosib = 0
    #     numInDiag = 0
    else:
        if inDiagMax >= 4: inDiag4 = 1
        if inDiagPosib >= 4:
            if inDiagMax == 3 or inDiag >= 1 and inDiagMax >= 2: inDiag3 = 1
            if inDiagMax == 2 or inDiag == 1 and numInDiag > 1: inDiag2 = 1
        if inDiagPosib >= 5:
            if inDiag == 1 and numInDiag >= 2: inDiag2 += 1
    return inDiag4, inDiag3, inDiag2, inDiagPosib - numInDiag

# /
def maxInDiagRight(player, row, col):
    inDiag4 = 0
    inDiag3 = 0
    inDiag2 = 0
    numInDiag = 0
    inDiag = 0
    inDiagPosib = 0
    inDiagMax = 0
    diagTmp = []
    sim = "O" if player == 0 else "#"
    for i in range(6):
        cols = col + (row - i)
        if cols < 0: break
        if cols > 6: continue
        diagTmp.append(board[i][cols])
        if row == i: diagTmp[len(diagTmp) - 1] = sim

    diagTmp.reverse()
    for cell in diagTmp:
        if cell == " ":
            inDiagPosib += 1
            inDiag = 0
            continue
        if cell == sim:
            inDiag += 1
            inDiagPosib += 1
            numInDiag += 1
            if inDiag > inDiagMax: inDiagMax = inDiag
        else:
            inDiag = 0
            inDiagPosib = 0

    # if len(diagTmp) < 4:
    #     inDiagPosib = 0
    #     numInDiag = 0
    else:
        if inDiagMax >= 4: inDiag4 = 1
        if inDiagPosib >= 4:
            if inDiagMax == 3 or inDiag >= 1 and inDiagMax >= 2: inDiag3 = 1
            if inDiagMax == 2 or inDiag == 1 and numInDiag > 1: inDiag2 = 1
        if inDiagPosib >= 5:
            if inDiag == 1 and numInDiag >= 2: inDiag2 += 1
    return inDiag4, inDiag3, inDiag2, inDiagPosib - numInDiag

# 4 functions for analise in 1 massive
Review = [maxInRow, maxInCol, maxInDiagLeft, maxInDiagRight]
winType = ["row", "column", "left diagonal", "right diagonal"]

# Checking after move
def win(player, row, col):
    # print("Win check")
    winner = "Homo sapiens" if player == 0 else "Artificial Intelligence"
    for i in range(len(Review)):
        result = Review[i](player, row, col)
        if result[0] >= 1:
            print("Winner by {} - {}".format(winType[i], winner))
            return 1

# for AI
def makeValuation(player, row, col):
    four, three, two, possib = 0, 0, 0, 0
    for i in range(len(Review)):
        n4, n3, n2, p = Review[i](player, row, col)
        four += n4
        three += n3
        two += n2
        possib += p
    # print("{} four {}, thr {}, two {}, po {}-{}".format(col+1, four, three, two, possib,player))
    return four, three, two, possib

# to show table of game
def printBoard():
    for i in range(len(board)):
        sleep(0.02)
        print("%d " % i, end="")
        print("|", end="")
        for k in board[i]:
            print("_%s_|" % k, end='')
        print()
    print("  ",end="")
    for j in range(7):
        print("  %d " % (j + 1), end="")
    print("\n")

def newGame():
    global board
    board = [[" "] * 7 for i in range(6)]

# Put simon on table
def move(player, col):
    global board, currPlayer
    if player == 0:
        sim = "O"
        print('Player move, "O"')
    else:
        sim = "#"
        print('Ai move, "#"')
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

def AImove(myNum):
    global agr, agrTurns
    enemy = (myNum + 1) % 2

    moveList = [0]*7
    for i in range(7):
        moveList[i] = movePoints[myNum][i] + movePoints[enemy][i]*agr

    if agr > 0.8: agrTurns -= 1
    if agrTurns <= 0:
        print("Agr stoped")
        agr = 0.8
        agrTurns = strategy[1]
    # print("{}".format(moveList))
    return moveList.index(max(moveList))

# Cycle game
def playGame():
    global wins, movePoints, agr, agrTurns
    global choiceCl, currPlayer
    while (True):
        # weights for turn
        moveList = posMoves()
        for i in range(len(moveList)):
            floor = 1
            if moveList[i] == -1:
                movePoints[0][i] = -1
                movePoints[1][i] = -1
                continue
            n4H, n3H, n2H, pH = makeValuation(0, moveList[i], i)  # Human/opponent moves profit
            n4, n3, n2, p = makeValuation(1, moveList[i], i)  # AI moves profit
            floor -= (sum(moveList) / len(moveList) - moveList[i]) * 0.15
            if floor > 1: floor = 1
            movePoints[0][i] = (n4H * weights[4] + n3H * weights[5] + n2H * weights[6] + pH * weights[7])*floor
            movePoints[1][i] = (n4 * weights[0] + n3 * weights[1] + n2 * weights[2] + p * weights[3])*floor
            # print("floor",floor)
        # print("{}".format(movePoints))

        # Human
        if currPlayer == 0:
            try:
                choiceCl = int(input("Your turn(1-7): ")) - 1
                if 2 == move(currPlayer, choiceCl):
                    # if 2 == move(currPlayer, AImove(currPlayer)):
                    if currPlayer == 0:
                        wins[0] += 1
                    else:
                        wins[1] += 1
                    currPlayer = (currPlayer + 1) % 2
                    break  # WINNING()

                # Agressive mode
                if movePoints[0][choiceCl]+5 < movePoints[1][choiceCl]:
                    agr = 2
                    agrTurns = strategy[1]
                    print("Agr!", movePoints[0][choiceCl], movePoints[1][choiceCl])
            except:
                print("Not allowed")

        # AI
        elif currPlayer == 1:
            if 2 == move(currPlayer, AImove(currPlayer)):
                if currPlayer == 0:
                    wins[0] += 1
                else:
                    wins[1] += 1
                currPlayer = (currPlayer + 1) % 2
                break  # WINNING()
            else:
                continue


# Strategies with weights
# 1st - Multiplier aganst Human after agression, 2nd - how many turns
# Tit-for-tat – מכה מול מכה
Tit4Tat = [2, 1]
# Grim-Trigger – פוגע חזרה ולא סולח
GrimTrigger = [2, 200]
# Forgiving Trigger – פוגע חזרה וסולח
Forgiving = [2, 3]

# Some options
strategy = Forgiving
agr = 0.8
agrTurns = strategy[1]
# Variables
choiceCl = 0
weights = [int(x) for x in loaded]
movePoints = [[0]*7 for i in range(2)]
# print("{}".format(movePoints))
while (True):
    printBoard()
    playGame()
    print("Score of epic competition:\n Human: %d  AI: %d" % (wins[0], wins[1]))
    file = open("weights.ai", "w")

    file.writelines(str(weights[i]) + "\n" for i in range(len(weights)))

    file.close()
    ask = input("Play more?(y) or ("")")
    if len(ask) == 0: ask = "y"
    if not ask == "y": break
    newGame()
