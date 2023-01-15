import sys; args = sys.argv[1:] 
import re
def makeGlobals(): 
    board = '.' * 27 + 'OX......XO' + '.' * 27
    moves = []
    currenttoken = ""
    if(args): 
        for val in args: 
            if (val in "XxOo"): currenttoken = val 
            elif "." in val: board = val  
            elif(len(val) > 2): 
                for i in range(0, len(val), 2): 
                    m = val[i:i+2]
                    if("_" in m): 
                        moves.append(int(m[1]))
                    elif("-" in m): 
                        continue
                    else: 
                        moves.append(int(m))
            elif str(val[0]) not in alph and str(val[0]) not in alphl: moves.append(val)
            else: moves.append(alphpostoindex[val])
    if not currenttoken: 
       currenttoken = "x" if (board.lower().count("x") - board.lower().count("o")) % 2 == 0 else "o"
    return board, moves, currenttoken

def checkpossible(pos, board, othertoken, token, alreadychecked): 
    moves = set()
    positionstocheck = [pos - 9, pos - 8, pos - 7, pos -1, pos + 1, pos + 7, pos + 8, pos + 9]
    for position in positionstocheck: 
        if(position >= len(board) or position < 0): continue
        if board[position] != "." or position in alreadychecked: continue
        for cset in postoconstraints[position]: 
            tempstring = ""; i = 0; btrue = True 
            for ps in cset: 
                tempstring += board[ps]
                if(position != ps) and btrue: 
                    i +=1 
                else: btrue = False
            if(checkstring(tempstring, i, token, position)): 
                moves.add(position)
        alreadychecked.add(position)
    return moves

def checkstring(csstring, postoken, tokens, pos): 
    token = tokens[0].lower()
    othertoken = "o" if token == "x" else "x"
    string = csstring.lower(); 
    if not token in string: return False
    ind = string.index(token)
    if(string[1:ind].count(".") >= 1 or string[1:ind].count(othertoken) == 0): return False
    return True

def makeMove(board, token, move): 
        t = token.lower()
        changelist = set()
        for cs in postoconstraints[move]: 
            tempstring = ""; 
            for ps in cs: 
                tempstring += board[ps]
            finalind =""
            for i, v in enumerate(tempstring[1:]): 
                if v == ".": break 
                if v.lower() == t: 
                  finalind = i + 1; break 
            if finalind: 
                for pos in range(finalind): changelist.add(cs[pos])
        for changedpos in changelist: 
            board = board[:changedpos] + token + board[changedpos + 1:]
        return board

def findMoves(board, currenttoken): 
    alreadchecked = set()
    lookingfortoken = "Oo" if currenttoken in "Xx" else "Xx"
    enemytokens = [] 
    moves = set()
    for i, val in enumerate(board): 
        if val in lookingfortoken: enemytokens.append(i)
    for pos in enemytokens: 
        possiblepositions = checkpossible(pos, board, lookingfortoken, currenttoken, alreadchecked)
        if possiblepositions: 
            for pp in possiblepositions: moves.add(pp)
    return moves 

def display(board):  
    [print(board[pos]) if (pos + 1) % 8 == 0 else print(board[pos], end = "") for pos in range(64)]

corners = {0, 7, 63, 56}; hedges = {0, 1, 2, 3, 4, 5, 6, 7, 56, 57, 58, 59, 60, 61, 62, 63}; vedges = {0,8,16,24,32,40,48,56,7,15,23,31,39,47,55,63}
cornertoedges = {0:{1, 8, 9}, 7:{6, 15, 14}, 63:{62, 55, 54}, 56:{57, 48, 49}}; dangerzone = {9, 10, 11, 12, 13, 14, 17, 25, 33, 41, 49, 57, 50, 51, 52, 53, 54, 46, 38, 30, 22}

def negamax(brd, tkn): 
    eTkn = "x" if tkn.lower() == "o" else "o"
    if brd.count(".") == 0 or (not (fm:=findMoves(brd, tkn)) and not (efm:=findMoves(brd, eTkn))): 
        return [brd.count(tkn)-brd.count(eTkn)]
    bestSoFar = [-65]
    if not fm: 
        for mv in efm: 
            nm = negamax(brd, eTkn)
            return [-nm[0]] + nm[1:] + [-1]
    for mv in fm: 
        newBrd = makeMove(brd, tkn, mv)
        nm = negamax(newBrd, eTkn)
        if -nm[0] > bestSoFar[0]: 
            bestSoFar = [-nm[0]] + nm[1:] + [mv]
    return bestSoFar

def quickMove(board, tkn): 
    if board.count(".") < 8: 
        return negamax(board, tkn)[-1]
    moves = findMoves(board, tkn)
    etkn = "x" if tkn.lower() == "o" else "o"
    unhappy = []; dangerzoness = []
    for m in moves: 
        if m in corners: 
            return m
    unwantedcmoves = set() 
    for k in cornertoedges: 
        if board[k] == ".": 
            unwantedcmoves.update(cornertoedges[k])
    potato = [*moves]
    for i, m in enumerate(potato): 
        if m in unwantedcmoves: unhappy.append(potato.pop(i))
        elif m in dangerzone: dangerzoness.append(potato.pop(i))
    potato= potato + dangerzoness + unhappy
    for m in potato:
            if m in vedges: 
                tstrd = "".join([board[i] for i in postoconstraints[m][0]])
                tstru = "".join([board[i] for i in postoconstraints[m][1]])
                if tkn.lower() == "x":
                    if(re.search("^[Oo]*[Xx]+$", tstrd[1:])): return m 
                    if(re.search("^[Oo]*[Xx]+$", tstru[1:])): return m 
                else: 
                    if(re.search("^[Xx]*[Oo]+$", tstrd[1:])): return m 
                    if(re.search("^[Xx]*[Oo]+$", tstru[1:])): return m 
            if m in hedges: 
                tstrr = "".join([board[i] for i in postoconstraints[m][2]])
                tstrl = "".join([board[i] for i in postoconstraints[m][3]])
                if tkn.lower() == "x":
                    if(re.search("^[Oo]*[Xx]+$", tstrr[1:])): return m 
                    if(re.search("^[Oo]*[Xx]+$", tstrl[1:])): return m 
                else: 
                    if(re.search("^[Xx]*[Oo]+$", tstrr[1:])): return m 
                    if(re.search("^[Xx]*[Oo]+$", tstrl[1:])): return m 
    min = 100; move = 10231
    for m in moves: 
        tb = board
        if m not in unwantedcmoves: 
            tb = makeMove(tb, tkn, m)
            psmoves = findMoves(tb, etkn)
            if (v:=len(psmoves)) <= 1: return m
            if v < min: min = v; move = m 
    if not min == 100: return move
    return [*moves][0]

def showmoves(board, moves): 
    d = board
    for move in moves: 
        d = d[:move] + "*" + d[move + 1:]
    display(d)

def printturn(board, possiblemoves, token): 
    #showingmoves
    showmoves(board, possiblemoves)
    #printing 1D board
    scorex = board.lower().count("x"); scoreO = board.lower().count("o")
    print("\n" + f"{board} {scorex}/{scoreO}" ) 
    #printing possible moves
    print(f"Possible moves for {token}:", end = " ")
    [print(f"{v},", end = " ") if i+1 != len(possiblemoves) else print(v) for i, v in enumerate(possiblemoves)]
    print(" ")

def turn(currenttoken, othertoken, board, move):  
    print(f"{currenttoken} plays to {move}")
    board = makeMove(board, currenttoken, move)
    othertoken, currenttoken = currenttoken, othertoken
    newpos = findMoves(board, currenttoken)
    if newpos: 
        printturn(board, newpos, currenttoken)
    else: 
        othertoken, currenttoken = currenttoken, othertoken
        newpos = findMoves(board, currenttoken)
        printturn(board, newpos, currenttoken)
    return currenttoken, othertoken, board


def main(): 
    board, moves, currenttoken = makeGlobals()
    othertoken = "o" if currenttoken.lower() == "x" else "x"
    #Othello3 run 
    if(mvs:=findMoves(board, currenttoken)):
        printturn(board, mvs, currenttoken)
    else: 
        othertoken, currenttoken = currenttoken, othertoken
        printturn(board, findMoves(board, currenttoken), currenttoken)
    for m in moves:
        if (move:=int(m)) >= 0: 
            possiblemoves = findMoves(board, currenttoken) 
            if(move in possiblemoves): 
                currenttoken, othertoken, board = turn(currenttoken, othertoken, board, move)
            else: 
                othertoken, currenttoken = currenttoken, othertoken
                possiblemoves = findMoves(board, currenttoken) 
                if possiblemoves: 
                   currenttoken, othertoken, board = turn(currenttoken, othertoken, board, move)
    #Checking if there are any moves left
    if (cct:=findMoves(board, currenttoken)) or (cot:=findMoves(board, othertoken)): 
       currenttoken = currenttoken if cct else othertoken
       mypref = quickMove(board, currenttoken)
       print(f"The preffered move is: {mypref}")
       nm = negamax(board, currenttoken)
       print(f"Min score: {nm[0]}; move sequence: {nm[1:]}")

global alphpos, alphpostoindex, postoconstraints 
postoconstraints = [] 
alph = "ABCDEFGH"
alphl = "abcdefgh"
alphpos = [letter + str((index + 1) % 9) for index in range(8) for letter in alph]
alphpos = alphpos + [letter + str((index + 1) % 9) for index in range(8) for letter in alphl]
alphpostoindex = {alphpos[index]: index%64 for index in range(128) }
cstr = ".Oxxo"
print(True if re.search("^[Oo]*[Xx]+$", cstr[1:]) else False)
for i in range(64):  
        row = i - i %8 ; col = i % 8
        whattoadd = [[newpos for newpos in range(i, 64, 8)],
                     [newpos for newpos in range(i, -1, -8)], 
                     [newpos for newpos in range(i, i + 8- i %8)], 
                     [newpos for newpos in range(i, i -( i %8) -1, -1)],
                     ]
        #findstart for downright 
        startind = i 
        while startind % 8 != 0 and startind >= 9: 
            startind = startind - 9 
        longdiagr = [newdiagonalrd for newdiagonalrd in range(startind, 64 - 8 * (startind % 8), 9)]
        ind = longdiagr.index(i) 
        ul = longdiagr[:ind + 1]
        ul.reverse() 
        dr = longdiagr[ind:]
        #find initial for downleft 
        startind = i
        while (startind + 1) % 8 != 0 and startind > 7: 
            startind = startind - 7
        longdiagl = [newdiagonalld for newdiagonalld in range(startind, 8 * ((startind) % 8 + 1) -1 , 7)]
        if i == 63: 
            ur = [63]
            dl = [63]
        else: 
            ind = longdiagl.index(i)
            ur = longdiagl[:ind +1]
            ur.reverse()
            dl = longdiagl[ind:]
        whattoadd.append(ul); whattoadd.append(ur); whattoadd.append(dl); whattoadd.append(dr)
        postoconstraints.append(whattoadd)

if (__name__ == "__main__"): 
    main()
# Santiago Criado, pd 6, 2024