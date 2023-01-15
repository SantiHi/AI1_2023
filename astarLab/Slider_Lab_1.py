import sys; args = sys.argv[1:]
import time  
import random 
NumOfPuzToLoopThrough = 500 
puz = '2543176_8'
if (len(args) != 0):  puz = args[0]
Ggoal = "83671542_"
if(len(args) > 1): Ggoal = args[1]
Gwidth = int(len(Ggoal)**(1/2)) 
start_time = time.process_time() 
order = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
randhelper = "0123456789_"



def levelneighbors(level, puzzle): 
   if level == 0: 
      return 1
   depthSet = set()
   depthSet.add(puzzle)
   for k in range(level):  
      depthSet = {nbr for i in depthSet for nbr in neighbors(i) if not nbr in depthSet} 
   return len(depthSet)
   
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
        return True if (invOfpuzzle + int(puz.index("_")/Gwidth)) % 2 == (invOfGoal + int(Ggoal.index("_")/Gwidth)) % 2 else False

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
def solve(puzzle, goal): 
    loops = 0 
    if puzzle == goal: 
        print_puzzle([puzzle]) 
        return [puzzle]
    else: 
        seen = {puzzle: " "} 
        parseT = [puzzle]
        if(solveable(puzzle, goal)):
            while(len(parseT) > 0): 
                temp = parseT[len(parseT)-1]
                del parseT[len(parseT)-1]
                for i in neighbors(temp): 
                    if i == goal:
                        plist = [i] 
                        val = temp
                        while(val != puzzle):
                            plist.append(val)
                            val = seen.get(val) 
                        plist.append(val)
                        plist = plist[::-1]
                        return plist
                    if(not i in seen): 
                        seen.update({i:temp})
                        parseT.insert(0, i)
        print_puzzle([puzzle])
        return []; 
        
def neighbors(puzzle): 
    parseMe = []
    indx = puzzle.index("_") 
    if(indx % Gwidth != (Gwidth - 1)): parseMe.append(puzzle[:indx] + puzzle[indx + 1] + puzzle[indx] + puzzle[indx + 2:])
    if(indx % Gwidth != 0): parseMe.append(puzzle[:indx-1] + puzzle[indx] + puzzle[indx-1] + puzzle[indx + 1:])
    if(indx + Gwidth < len(puzzle)):  parseMe.append(puzzle[:indx] + puzzle[indx + Gwidth] + puzzle[indx + 1:indx + Gwidth] + puzzle[indx] + puzzle[indx + Gwidth + 1:])
    if(indx - Gwidth >= 0 ):  parseMe.append(puzzle[:indx - Gwidth] + puzzle[indx] + puzzle[indx - Gwidth + 1: indx] + puzzle[indx - Gwidth] + puzzle[indx + 1:])
    return parseMe

if(not args): 
    path = solve(puz, Ggoal); 
    print_puzzle(path)
    steps = len(path) - 1 
    end_time = time.process_time() 
    print("Steps:", steps, ) 
    time = (round(end_time - start_time, 2))
    print("Time:", time, "s")
"""
else: 
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