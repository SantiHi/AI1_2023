import sys; args = sys.argv[1:] 
import re
def makeGlobals(): 
    global alphpos, alphpostoindex, postoconstraints 
    postoconstraints = [] 
    alph = "ABCDEFGH"
    alphl = "abcdefgh"
    alphpos = [letter + str((index + 1) % 9) for index in range(8) for letter in alph]
    alphpos = alphpos + [letter + str((index + 1) % 9) for index in range(8) for letter in alphl]
    alphpostoindex = {alphpos[index]: index%64 for index in range(128) }
    board = '.' * 27 + 'OX......XO' + '.' * 27
    moves = [] 
    currenttoken = ""
    if(args): 
        for val in args: 
            if (val in "XxOo"): currenttoken = val 
            elif "." in val or len(val) > 50: board = val  
            elif str(val[0]) not in alph and str(val[0]) not in alphl: moves.append(val)
            else: moves.append(alphpostoindex[val])
    if not currenttoken: 
       currenttoken = "x" if board.lower().count("x") <=board.lower().count("o") else "o"
    for i, v in enumerate(board):  
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
    return True;

def makemove(board, move, possiblemoves, token): 
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
def determinemoves(board, currenttoken): 
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
    
def main(): 
    board, moves, currenttoken = makeGlobals()
    possiblemoves = determinemoves(board, currenttoken) 
    if(possiblemoves): 
        printturn(board, possiblemoves, currenttoken)
        if moves: 
            move = int(moves.pop());  othertoken = "o" if currenttoken.lower() == "x" else "x"
            print(f"{currenttoken} plays to {move}")
            board = makemove(board, move, possiblemoves, currenttoken)
            newpos = determinemoves(board, othertoken)
            printturn(board, newpos, othertoken )
    else: 
        currenttoken = "o" if currenttoken.lower() == "x" else "x"
        othertoken = "o" if currenttoken.lower() == "x" else "x"
        possiblemoves = determinemoves(board, currenttoken) 
        printturn(board, possiblemoves, othertoken)
        if moves: 
            move = int(moves.pop());  othertoken = "o" if currenttoken.lower() == "x" else "x"
            print(f"{currenttoken} plays to {move}")
            board = makemove(board, move, possiblemoves, currenttoken)
            newpos = determinemoves(board, othertoken)
            printturn(board, newpos, othertoken )
if (__name__ == "__main__"): 
    main()
# Santiago Criado, pd 6, 2024