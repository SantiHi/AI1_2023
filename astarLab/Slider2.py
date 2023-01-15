import sys; args = sys.argv[1:]
import time  
import random 

NumOfPuzToLoopThrough = 500 
puz = "KBDOACH_INMEFLGJ" 
if (len(args) != 0):  puz = args[0]
Ggoal = "KBD_ACHOINMEFLGJ"
if(len(args) >= 1): f1 = open(args[0])
else: f1 = open("astarLab/test.txt")
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
        print("")




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
    if puzzle == goal: 
        return [puzzle]
    else: 
        seen = {puzzle: " "} 
        parseMe = [(h(puzzle, goal), puzzle)]
        if(solveable(puzzle, goal)):
            while(parseMe): 
                parseMe.sort()
                temp = parseMe.pop(0)[1]
                for nbr in neighbors(temp): 
                    if nbr in seen: continue 
                    seen[nbr] = temp
                    parseMe.append((h(nbr, goal), nbr))
                    if nbr == goal:
                        return findpath(puzzle, goal, seen, temp)

        return []

def h(puzzle, goal): 
    ManhattanDist = 0
    for i in range(size): 
        ManhattanDist += abs((pindx:=puzzle.index("_"))//Gwidth - abs((gindx:=goal.index("_"))//Gwidth)) + abs(pindx % Gwidth - (gindx % Gwidth))
    return ManhattanDist

def findpath(puzzle, goal, seen, beforegoal): 
    plist = [goal] 
    val = beforegoal
    while(val != puzzle):
        plist.append(val)
        val = seen.get(val) 
    plist.append(val)
    plist = plist[::-1]
    return plist
        
def neighbors(puzzle): 
    parseMe = []
    indx = puzzle.index("_") 
    if(indx % Gwidth != (Gwidth - 1)): parseMe.append(puzzle[:indx] + puzzle[indx + 1] + puzzle[indx] + puzzle[indx + 2:])
    if(indx % Gwidth != 0): parseMe.append(puzzle[:indx-1] + puzzle[indx] + puzzle[indx-1] + puzzle[indx + 1:])
    if(indx + Gwidth < len(puzzle)):  parseMe.append(puzzle[:indx] + puzzle[indx + Gwidth] + puzzle[indx + 1:indx + Gwidth] + puzzle[indx] + puzzle[indx + Gwidth + 1:])
    if(indx - Gwidth >= 0 ):  parseMe.append(puzzle[:indx - Gwidth] + puzzle[indx] + puzzle[indx - Gwidth + 1: indx] + puzzle[indx - Gwidth] + puzzle[indx + 1:])
    return parseMe
goal = ""
goalset = False
for line in f1: 
    l = line.strip()
    if(not goalset): goal = l; goalset = True
    puz = l
    path = astar(puz, goal)
    print(puz, "path", end = " ")
    condensepath(path)
steps = len(path) - 1 
end_time = time.process_time() 
print("Steps:", steps, ) 
time = (round(end_time - start_time, 2))
print("Time:", time, "s")

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