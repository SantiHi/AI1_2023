import sys; args = sys.argv[1:] 
import time 
if (not args):  
    args = ["22x22", "10x15", "9x12", "8x13", "7x14", "4x6"] #10x13 3x6 4x10 7x9 1x1
    #args = ["10x13", "3x6", "4x10", "7x9", "1x1"]
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
    pzl = "." * height * width
    rectsize = sum([peice[0] * peice[1] for peice in blocks])  
    retpeices = sorted(blocks, key=lambda x: x[0]) 
    retpeices.reverse()
    lettertopuz = {peice: alphabet[i] for i, peice in enumerate(retpeices)}
    return (pzl, retpeices)



def isSolved(pzl): 
    return pzl.count(".") == size - rectsize 

def letterinpuz(letter, puz): 
    for row in puz: 
        if letter in row: return True 
    return False; 

def makepzl(puz, choice): 
    let = ""
    pzl = ""
    for letter in alphabet: 
        if letter in puz: continue 
        let = letter; break 
    pos = choice[0]
    blocks = choice[1]
    pzl = puz[:pos]
    finalrow= 0
    for row in range(pos, pos + blocks[0]*width,width): 
        pzl = pzl + let * blocks[1] + puz[row + blocks[1]: row + blocks[1] + (width - blocks[1])]
        finalrow = row + blocks[1] + (width - blocks[1])
    pzl = pzl + puz[finalrow:]
    return pzl 
        
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
    if topcornerlocation % width + (pw:=peice[1]) > width or topcornerlocation + (peice[0]-1)* width > size : return False 
    for rowpos in range(topcornerlocation, topcornerlocation + width * peice[0], width): 
        if (pzl[rowpos:rowpos + pw].count(".") != pw): return False
    return True 

def display(pzl): 
    i = 0
    for rows in range(0, len(pzl), width): 
        i+=1
        print(i, pzl[rows: rows + width])
 
def findchoices(pzl, avaliblepeices, index): 
    choices = []
    largestpeice = avaliblepeices[index]
    if(rotateable(largestpeice)): 
      rotatedlargepeice = (largestpeice[1], largestpeice[0]) 
    else: rotatedlargepeice = ""
    if (rotatedlargepeice): 
        for pos, v in enumerate(pzl): 
            if v == ".": 
                if placeable(pzl, largestpeice, pos): 
                      choices.append((pos, largestpeice))  
                if(placeable(pzl, rotatedlargepeice,pos)):
                     choices.append((pos, rotatedlargepeice))  
    else: 
        for pos, v in enumerate(pzl): 
            if v == ".": 
                 if placeable(pzl, largestpeice, pos): choices.append((pos, largestpeice))   
    return choices, index + 1

def rotateable(peice): 
    return not peice[0] == peice[1]

def interpretsol(solvedpuz, ogpeices): 
    seenset = set()
    interpretedsol = []
    #search for first pos of letter
    for i, block in enumerate(solvedpuz):
            if block not in seenset:
                if(block != "."): 
                    rowstart = i - i % width
                    seenset.add(block)
                    letter = block
                    peice = ogpeices[alphabet.index(letter)] 
                    #check if rotated 
                    if (solvedpuz[rowstart:rowstart + width].count(letter) != peice[1]): 
                        peice = (peice[1], peice[0])
                    else: 
                        totalnumofletters = 0
                        trow = 0
                        while(solvedpuz[i + trow] == letter): 
                            totalnumofletters +=1 
                            trow +=1 
                            if(trow >= height): break; 
                        if totalnumofletters != peice[1]: peice = (peice[1], peice[0]) 
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
            display(solved)
            thingtoprint = interpretsol(solved, pieces)
            print(f"Decomposition: {thingtoprint}")
    else: print("No solution")
    end = time.process_time()
    print("Time(s):", round(end - start, 4))

if (__name__ == "__main__"): 
    main()
    
# Santiago Criado, pd 6, 2024