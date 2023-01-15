import sys; args = sys.argv[1:] 
import time 
if (not args):  
    args = ["22x22", "10x15", "9x12", "8x13", "7x14", "4x6"]
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
def createpuzzle(): 
    blocks = [] 
    global height, width, size, rectsize, lettertopuz
  #  posx = args[0].index("x")
   # height = int(args[0][:posx]); width = int(args[0][posx + 1:]); size = height * width; 
    skip = False
    for i, block in enumerate(b:=args): 
        if(skip): skip = False; continue; 
        if "x" in block: 
            posx = block.index("x")
            blocks.append((int(block[:posx]), int(block[posx + 1:])))
        elif "X" in block: 
            posx = block.index("X")
            blocks.append((int(block[:posx]), int(block[posx + 1:])))
        else: skip = True; blocks.append((int(b[i]), int(b[i + 1]))) 
    height = (definer:=blocks.pop(0))[0]; width = definer[1]; size = height * width; 
    pzl = [["." for i in range(width)] for v in range(height)] 
    rectsize = sum([peice[0] * peice[1] for peice in blocks])  
    retpeices = sorted(blocks, key=lambda x: (x[0] *  x[1])) 
    retpeices.reverse()
    lettertopuz = {peice: alphabet[i] for i, peice in enumerate(retpeices)}
    return (pzl, retpeices)



def isSolved(pzl): 
    t = "".join(["".join(row) for row in pzl])
    return t.count(".") == size - rectsize 

def letterinpuz(letter, puz): 
    for row in puz: 
        if letter in row: return True 
    return False; 

def makepzl(puz, choice): 
    pzl = [ [colval for colval in row] for row in puz]
    for letter in alphabet: 
        if(not letterinpuz(letter, puz)): 
           letforthisblock = letter; break; 
    pos, block = choice[0], choice[1] 
    for row in range(pos[0], pos[0]+ block[0]): 
        for col in range(pos[1], pos[1] + block[1]): 
            pzl[row][col] = letforthisblock 
    return pzl
def Brute_Force(pzl, peices, ind): 
    if isSolved(pzl): return pzl 
    choices, index = findchoices(pzl, peices, ind)
    for choice in choices:
        subpzl = makepzl(pzl, choice)
        bf = Brute_Force(subpzl, peices, index)
        if bf: 
            return bf 

def areascorrect(): 
    return size <= rectsize 

def placeable(pzl, peice, topcornerlocation): 
    if (tcpy:=topcornerlocation[0]) + (p1:=peice[0]) >= height + 1 or (tcpx:=topcornerlocation[1]) + (p2:=peice[1]) >= width + 1 : return False 
    for rowpos in range(tcpy, tcpy + p1): 
        for colpos in range(tcpx, tcpx + p2): 
            if pzl[rowpos][colpos] != ".": return False 
    return True 

def findchoices(pzl, avaliblepeices, index): 
    choices = []
    largestpeice = avaliblepeices[index]
    if(rotateable(largestpeice)): 
      rotatedlargepeice = (largestpeice[1], largestpeice[0]) 
    else: rotatedlargepeice = ""
    if (rotatedlargepeice): 
        for indxrow, row in enumerate(pzl): 
            for indxcol, cols in enumerate(row): 
                if cols == ".": 
                    if(placeable(pzl, largestpeice, (pos:=(indxrow, indxcol)))): choices.append((pos, largestpeice))  
                    if(placeable(pzl, rotatedlargepeice, pos)): choices.append((pos, rotatedlargepeice))  
    else: 
        for indxrow, row in enumerate(pzl): 
            for indxcol, cols in enumerate(row): 
                if cols == ".": 
                    if(placeable(pzl, largestpeice, (pos:=(indxrow, indxcol)))): choices.append((pos, largestpeice))   
    return choices, index + 1

def display(solvdpzl): 
    i = 0
    strs = "".join(["".join(row) for row in solvdpzl]) 
    for rows in range(0, len(strs), width): 
        i+=1
        print(i, strs[rows: rows + width])

def rotateable(peice): 
    return not peice[0] == peice[1]

def interpretsol(solvedpuz, ogpeices): 
    seenset = set()
    interpretedsol = []
    #search for first pos of letter
    for indxrow, row in enumerate(solvedpuz): 
        for indxcol, cols in enumerate(row):
            if cols not in seenset:
                if(cols != "."): 
                    seenset.add(cols)
                    letter = cols
                    peice = ogpeices[alphabet.index(letter)] 
                    #check if rotated 
                    if (solvedpuz[indxrow].count(letter) != peice[1]): 
                        peice = (peice[1], peice[0])
                    else: 
                        totalnumofletters = 0
                        trow = indxrow
                        while(solvedpuz[trow][indxcol] == letter): 
                            totalnumofletters +=1 
                            trow +=1 
                            if(trow >= height): break; 
                        if totalnumofletters != peice[0]: peice = (peice[1], peice[0]) 
                    interpretedsol.append(peice)
                else: interpretedsol.append((1, 1))
    return interpretedsol

def main(): 
    start = time.process_time()
    pzl, pieces = createpuzzle() 
    pzldims = (height, width)
    print(f"Area of rects: {rectsize}, container: {size}")
    print(f"Dims: {pzldims} \nRaw blocks: {pieces}")
    if(areascorrect): 
        solved = Brute_Force(pzl, pieces, 0)
        if(not solved): 
            print("No solution")
        else: 
            thingtoprint = interpretsol(solved, pieces)
            display(solved)
            print(f"Decomposition: {thingtoprint}")
    else: print("No solution")
    end = time.process_time()
    print("Time(s):", round(end - start, 4))

if (__name__ == "__main__"): 
    main()
    
# Santiago Criado, pd 6, 2024