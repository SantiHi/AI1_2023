import sys; args = sys.argv[1:]
import time  
import random  

NumOfPuzToLoopThrough = 500 
puz = "KBDOACH_INMEFLGJ" 
if (len(args) != 0):  puz = args[0]
Ggoal = "KBD_ACHOINMEFLGJ"
if(len(args) >= 1): f1 = open(args[0])
else: f1 = open("astarLab/eckel.txt")
Gwidth = 4
size = Gwidth * Gwidth
start_time = time.process_time() 
order = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
randhelper = "0123456789_"
lookuptable = {} 
for index in range(size): 
    if(not (index % Gwidth == 0)): lookuptable[(index, index -1)]  = "L" 
    if(not (index % Gwidth == Gwidth - 1)): lookuptable[(index, index + 1)] = "R"; 
    if(index + Gwidth < size): lookuptable[(index, index + Gwidth)] = "D" 
    if(index - Gwidth >= 0): lookuptable[(index, index - Gwidth)] = "U"

def levelneighbors(level, puzzle): 
   if level == 0: 
      return 1
   depthSet = set()
   depthSet.add(puzzle)
   for k in range(level): 
      depthSet = {nbr for i in depthSet for nbr in neighbors(i)}
   return len(depthSet)

def condensepath(lstpuzzle): 
    if len(lstpuzzle) == 0: 
        print("X") 
    elif len(lstpuzzle) == 1 :
         print("G") 
    else: 
        for order, puzzle in enumerate(lstpuzzle):  
            if order < len(lstpuzzle)-1: 
                p = puzzle.index("_")
                c = lstpuzzle[order + 1].index("_")
                tup = (p , c)
                print(lookuptable[tup], end = "")
                
def solveable(puzzle, goal): 
    temp = puzzle.replace("_",'')
    tempgoal = goal.replace("_",'')
    invOfpuzzle = 0; 
    invOfGoal = 0; 
    for indx in range(len(temp)): 
        for i in temp[indx:]: 
            if(order.index(i) < order.index(temp[indx])): 
                invOfpuzzle += 1 
        for i in tempgoal[indx:]: 
            if(order.index(i) < order.index(tempgoal[indx])): 
                invOfGoal += 1 
          
    if(Gwidth % 2 == 1): 
        if invOfpuzzle % 2 == invOfGoal % 2: 
            return True 
        return False 
    else:   
        return True if (invOfpuzzle + int(puzzle.index("_")/Gwidth)) % 2 == (invOfGoal + int(goal.index("_")/Gwidth)) % 2 else False

def print_puzzle(puzzle):
    if(len(puzzle) < 12): 
        for i in range(Gwidth):
            for k in range(len(puzzle)): 
                print("".join(puzzle[k][:Gwidth]), end = " ") 
                puzzle[k] = puzzle[k][Gwidth:]
            print(" ")
    else : 
        z = puzzle[:len(puzzle) +1]
        z = z[::-1]
        temp = []
        while(len(z) != 0):
            for i in range(12) : 
                if(len(z) == 0): break
                temp.append(z[len(z)-1])
                del z[len(z)-1]
            for i in range(Gwidth):
                for k in range(len(temp)): 
                    print("".join(temp[k][:Gwidth]), end = " ") 
                    temp[k] = temp[k][Gwidth:] 
                print(" ")
            temp = []
def astar(puzzle, goal): 
    goaldict = {v:i for i, v in enumerate(goal)}
    smallestf = 0
    if not solveable(puzzle, goal): return []
    openset = [set() for i in range(40)]
    openset[0].add((0, puzzle, 0, puzzle.index("_")))
    closedset = {}; 
    while(True): 
        if(len(openset[smallestf]) > 0): puz = openset[smallestf].pop()
        else: 
            for i, sets in enumerate(openset[smallestf:]): 
                if(len(sets) > 0): 
                    puz = sets.pop()
                    smallestf = i + smallestf
                    break; 
        if(puz[1] in closedset): continue 
        closedset[puz[1]] = (puz[2]) 
        if(puz[1] == goal): 
            return findpath(puzzle, goal, closedset, puz) 
        for nbr in neighbors(puz[1], puz[3]): 
            if (f:=(hfast(nbr, puz, puz[0] - puz[2], goaldict) + puz[2] + 1)) < smallestf: smallestf = f
            openset[f].add((f, nbr[0], puz[2] + 1, nbr[1]))

def h(puzzle, goal): 
    ManhattanDist = 0
    for i in range(size): 
        if(puzzle[i] == goal[i]): continue
        if(puzzle[i] != "_"): 
         yval = abs(i//Gwidth - abs((gindx:=goal.index(puzzle[i]))//Gwidth))  
         xval = abs(i % Gwidth - (gindx % Gwidth)) 
         ManhattanDist += xval + yval
    return ManhattanDist

def hfast(puzzle, lastpuz, oldh, goaldic):
      sub = oldh + 0 if (puzzle[1] == goaldic[lastpuz[1][(a:=puzzle[1])]]) else oldh -(abs(((a:= puzzle[1])//Gwidth) - ((gindx:=goaldic[lastpuz[1][a]])//Gwidth))  + abs(a % Gwidth - (gindx % Gwidth))) 
      new = 0 if puzzle[0][lastpuz[3]] == goal[lastpuz[3]] else abs((b:=lastpuz[3])//Gwidth - (gindx:=goaldic[puzzle[0][b]])//Gwidth) + abs(b % Gwidth - (gindx % Gwidth))
      val = sub + new 
      return sub + new 
      
def findpath(puzzle, goal, seen, beforegoal):
    plist = [goal] 
    if(goal == puzzle): return plist
    maxlevel = beforegoal[2]; val = (beforegoal[1], beforegoal[3]) 
    while(not maxlevel == 0): 
        for nbr in neighbors(val[0], val[1]): 
            if nbr[0] in seen and seen[nbr[0]] == maxlevel - 1: 
                plist.append(nbr[0]); val = nbr;  break
        maxlevel -= 1
    return plist[::-1]

        
def neighbors(puzzle, indx): 
    parseMe = [] 
    if((indx)) % Gwidth != (Gwidth - 1): parseMe.append((puzzle[:indx] + puzzle[indx + 1] + puzzle[indx] + puzzle[indx + 2:], indx + 1))
    if(indx % Gwidth != 0): parseMe.append((puzzle[:indx-1] + puzzle[indx] + puzzle[indx-1] + puzzle[indx + 1:], indx - 1))
    if(indx + Gwidth < len(puzzle)):  parseMe.append((puzzle[:indx] + puzzle[(gwidthplusindx:=indx + Gwidth)] + puzzle[indx + 1:gwidthplusindx] + puzzle[indx] + puzzle[gwidthplusindx + 1:], indx + Gwidth))
    if(indx - Gwidth >= 0 ):  parseMe.append((puzzle[:(indxminusGwidth:=indx - Gwidth)] + puzzle[indx] + puzzle[indxminusGwidth + 1: indx] + puzzle[indxminusGwidth] + puzzle[indx + 1:], indx - Gwidth))
    return parseMe
goal = ""
goalset = False
for line in f1: 
    l = line.strip()
    if(not goalset): goal = l; goalset = True
    puz = l
    path = astar(puz, goal)
    print("Steps:", len(path) -1, end = " ") 
    print(puz, "path", end = " ")
    condensepath(path) 
    end_time = time.process_time()  
    t = (round(end_time - start_time, 2))
    print(" Time:", t, "s")
steps = len(path) - 1 
end_time = time.process_time() 
print("Steps:", steps, ) 
t = (round(end_time - start_time, 2))
print("Time:", t, "s")

"""
    print(levelneighbors(33, "456327_18"))
    stats = [0, 0] #[0] = total len of the paths, [1] = number of possible puzzle pairts 
    for i in range(NumOfPuzToLoopThrough): 
        randpuztemp = []; 
        for i in range (8): 
            randpuztemp.append(randhelper[random.randint(0, 9)]) 
        randpuztemp.insert(random.randint(0, 9), "_")
        randgoaltemp = randpuztemp[:]
        random.shuffle(randgoaltemp)
        randpuz = "".join(randpuztemp)
        randgoal = "".join(randgoaltemp)
        if(solveable(randpuz, randgoal)):
            stats[0] += len(solve(randpuz, randgoal)) - 1 
            stats[1] +=1
    end_time = time.process_time() 
    time = (round(end_time - start_time, 2))
    print("Time:", time, "s") 
    print("Number of Random Pairs: ", NumOfPuzToLoopThrough)
    print("# of Solvable Puzzles: ", stats[1])
    print("Avg Length of Solvable Puzzles :", stats[0]/stats[1]) 
    """




# Santiago Criado, pd 6, 2024``