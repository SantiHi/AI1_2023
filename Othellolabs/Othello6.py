import sys; args = sys.argv[1:] 
import re

HOLELIMIT = 10

def makeGlobals(): 
    global HOLELIMIT
    board = '.' * 27 + 'OX......XO' + '.' * 27
    moves = []
    currenttoken = ""
    if(args): 
        for val in args: 
            if (val in "XxOo"): currenttoken = val 
            elif "." in val: board = val; 
            elif "HL" in val: HOLELIMIT  = int(val[2:])
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
    xnum = board.lower().count("x") 
    onum = board.lower().count("o")
    print(f"{board} {xnum}/{onum} \n")
    if not currenttoken: 
       currenttoken = "x" if (board.lower().count("x") - board.lower().count("o")) % 2 == 0 else "o"
    return board.lower(), moves, currenttoken

def checkpossible(pos, board, token): 
        moves = set()
        for cset in postoconstraints[pos]: 
            tempstring = ""; 
            for ps in cset: 
                tempstring += board[ps]
            if(checkstring(tempstring, token)): 
                moves.add(pos)
        return moves

def checkstring(csstring, tokens): 
    token = tokens[0].lower()
    othertoken = "o" if token == "x" else "x"
    string = csstring.lower(); 
    if not token in string: return False
    ind = string.index(token)
    if(string[1:ind].count(".") >= 1 or string[1:ind].count(othertoken) == 0): return False
    return True

def tinit(board, token, cs): 
    for i, v in enumerate(cs):
        if i == 0: continue 
        if board[v] == ".": return False
        if board[v] == token: return True 
    return False

def makeMove(board, token, move):
        t = token.lower()
        brd = board.lower()
        ch = [*brd]; 
        for cs in postoconstraints[move]: 
            if not tinit (brd, t, cs): continue 
            for i, ps in enumerate(cs): 
                if i == 0: continue
                if (ts:=brd[ps]) == ".": break
                if ts == t: break 
                ch[ps] = t
        ch[move] = t.upper()
        return "".join(ch)


def makeMove1(board, token, move): 
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
            board = board[:changedpos].lower() + t + board[changedpos + 1:].lower()
        return board[:move] + token.upper() + board[move + 1:]

fmcache = {}

def findMoves(board, currenttoken): 
    if (key:=(board, currenttoken)) in fmcache: return fmcache[key] 
    dotpositions = {i for i, v in enumerate(board) if v == "."}
    moves = set()
    for pos in dotpositions: 
        possiblepositions = checkpossible(pos, board, currenttoken)
        if possiblepositions: 
            for pp in possiblepositions: moves.add(pp)
    fmcache[key] = moves
    return fmcache[key] 

def display(board):  
    [print(board[pos]) if (pos + 1) % 8 == 0 else print(board[pos], end = "") for pos in range(64)]

corners = {0, 7, 63, 56}; hedges = {0, 1, 2, 3, 4, 5, 6, 7, 56, 57, 58, 59, 60, 61, 62, 63}; vedges = {0,8,16,24,32,40,48,56,7,15,23,31,39,47,55,63}
cornertoedges = {0:{1, 8, 9}, 7:{6, 15, 14}, 63:{62, 55, 54}, 56:{57, 48, 49}}; dangerzone = {9, 10, 11, 12, 13, 14, 17, 25, 33, 41, 49, 57, 50, 51, 52, 53, 54, 46, 38, 30, 22}

def alphabeta(brd, tkn, firstpass, lowerBnd, upperBnd): 
    eTkn = "x" if tkn.lower() == "o" else "o"
    if brd.count(".") == 0 or (not (fm:=findMoves(brd, tkn)) and not (efm:=findMoves(brd, eTkn))): 
        return [brd.lower().count(tkn)-brd.lower().count(eTkn)]
    if firstpass: fm = [(fqm:=quickMove1(brd, tkn))] + [*(fm - {fqm})]
    if not fm: 
        for mv in efm: 
            ab = alphabeta(brd, eTkn, False, -upperBnd, -lowerBnd)
            return [-ab[0]] + ab[1:] + [-1]
    best = [lowerBnd-1]
    for mv in fm: 
        ab = alphabeta(makeMove(brd, tkn, mv), eTkn, False, -upperBnd, -lowerBnd)
        score = -ab[0]  
        if score < lowerBnd: continue 
        if score > upperBnd: return [score] 
        best = [score] + ab[1:] + [mv]
        lowerBnd = score + 1
    return best

def quickMove(board, tkn): 
    global HOLELIMIT
    if board == "": HOLELIMIT = tkn
    if board.count(".") < HOLELIMIT:  
        ab = alphabeta(board, tkn, True, -64, 64)
        return ab[-1]
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

def quickMove1(board, tkn): 
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
    print("\n" + f"{board.lower()} {scorex}/{scoreO}" ) 
    #printing possible moves
    if possiblemoves: 
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
       mypref = quickMove1(board, currenttoken)
       print(f"The preffered move is: {mypref}")
       if board.count(".") < HOLELIMIT : 
        ab = alphabeta(board, currenttoken, True, -64, 64)
        print(f"Min score: {ab[0]}; move sequence: {ab[1:]}") 
        board = makeMove(board, currenttoken, ab[1])
        printturn(board, findMoves(board, currenttoken), currenttoken)
    
global alphpos, alphpostoindex, postoconstraints 
postoconstraints = [] 
alph = "ABCDEFGH"
alphl = "abcdefgh"
alphpos = [letter + str((index + 1) % 9) for index in range(8) for letter in alph]
alphpos = alphpos + [letter + str((index + 1) % 9) for index in range(8) for letter in alphl]
alphpostoindex = {alphpos[index]: index%64 for index in range(128) }
cstr = ".Oxxo"
for i in range(64):  
        row = i - i %8 ; col = i % 8
        whattoadd = [[newpos for newpos in range(i, 64, 8)],
                     [newpos for newpos in range(i, -1, -8)], 
                     [newpos for newpos in range(i, i + 8- i %8)], 
                     [newpos for newpos in range(i, i -( i %8) -1, -1)],]
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