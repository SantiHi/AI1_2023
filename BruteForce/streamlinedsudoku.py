import sys; args = sys.argv[1:]
import time 

if len(args) != 0: 
    f1 = open(args[0])
else: 
    f1 = open("BruteForce/puzzles.txt")
#generate list of set of constraints for Q1: 
size = 9 
symbolset = {"1", "2", "3", "4", "5", "6", "7", "8", "9"};
global STATSs
STATSs = {"OptimalCC":0}
def setGlobals(pzl): 
    global constraints; global constraintsthatmakesense; global neighbors;
    constraints = [{value + val for val in range(0, size)} for value in range(0, size*size, size)]
    constraints = constraints + [{value + val for val in range(0, size*size, size)} for value in range(0, size)]
    constraints = constraints + [{0, 1, 2, 9, 10, 11, 18, 19, 20}, {3, 4, 5, 12, 13, 14, 21, 22, 23}, {6, 7, 8, 15, 16, 17, 24, 25, 26},
    {27, 28, 29, 36, 37, 38, 45, 46, 47}, {30, 31, 32, 39, 40, 41, 48, 49, 50}, {33, 34, 35, 42, 43, 44, 51, 52, 53}, {54, 55, 56, 63, 64, 65, 72, 73, 74},
    {57, 58, 59, 66, 67, 68, 75, 76, 77}, {60, 61, 62, 69, 70, 71, 78, 79, 80}] 
    constraintsthatmakesense = {ind: [cset for cset in constraints if ind in cset] for ind in range (0, size * size)}
    neighbors = [{nbr for cset in constraintsthatmakesense[indx] for nbr in cset if nbr != indx} for indx in range (0, size * size)]
#ascii table 
ascii_table = {"1":49, "2":50, "3":51, "4":52, "5":53, "6":54, "7":55, "8":56, "9":57}
def bruteForce(pzl, listofsets, indx): 
    if isInvalid(pzl, indx): return "" 
    if isSolved(pzl): return pzl 
    choice = findchoice(listofsets, pzl); STATSs["OptimalCC"] += 1
    length = len(listofsets[choice])
    i = 0 
    for symbol in listofsets[choice]: 
        i+= 1    
        copyset = makecopy(listofsets) if (i!= length) else listofsets
        subPzl = pzl[:choice] + symbol + pzl[choice + 1:]
        update(copyset, symbol, choice)
        bF = bruteForce(subPzl, copyset, choice)
        if bF: return bF 
    
def makecopy(listofsets): 
    return [{val for val in s} for s in listofsets]
def findchoice(listofsets, pzl): 
    indx = min([(len(s), i) for i, s in enumerate(listofsets) if pzl[i] == "." ])[1]
    return indx

def update(datastruc, symbol, indx): 
    for nbr in neighbors[indx]: 
        datastruc[nbr] = datastruc[nbr] - {symbol} 
    datastruc[indx] = set()
def findspaces(pzl): 
    lst = [] 
    for i, v in enumerate(pzl): 
        if v == ".": 
            lst.append(i) 
    return lst 

def printsol(pzl): 
    print("   ", pzl, end = " ")

def findind(pzl, val): 
    return [i for i, v in enumerate(pzl) if v == val]

def isInvalidonce(pzl): 
    for i, v in enumerate(pzl): 
        if (v != "."): 
            for indx in findind(pzl, v): 
                if(indx != i): 
                  for const in constraintsthatmakesense[indx]: 
                     if i in const and indx in const: return True 
    return False 
def isInvalid(pzl, indx): 
    if(pzl[indx] != "."):
        for nbr in neighbors[indx]: 
            if pzl[nbr] == pzl[indx]: 
                return True 
    return False 

def ord(pzl): 
    checksum = -81*49
    for val in pzl: 
        checksum = checksum + ascii_table[val]
    return checksum

def isSolved(pzl):
    return pzl.count(".") == 0

def display(pzl): 
    for i, val in enumerate(pzl): 
        if (i + 1) % (size * size / 3) == 0 and i != 80 :
            print(val); print("---------------------") 
        elif (i + 1) % size == 0: 
            print(val) 
        elif (i+ 1) % 3 == 0: 
            print(val, "|", end = " ") 
        else: 
            print(val, end = " ")
def main(): 
    num = 1
    totalstart = time.process_time()
    for line in f1: 
        if time.process_time() - totalstart > 60: break; 
        print(num, end = "")
        if num > 9:
            print(": ", end ="")
        elif num > 99: 
            print (":", end = "")
        else: 
            print(": ", end = " ")
        pzl = line.strip()
        setGlobals(pzl)
        print(pzl)
        start = time.process_time() 
        if(not isInvalidonce(pzl)): 
            fred = [(symbolset - {pzl[indx]} - {pzl[nbr]for nbr in neighbors[indx] if pzl[nbr] != "."}) if pzl[indx] == "." else set() for indx in range(size*size)]
            solved = bruteForce(pzl, fred, pzl.index("."))
        else: solved = "" 
        if solved: 
            #display(solved)
            printsol(solved)
            print("checksum:", ord(solved), end = " ")
        else: print("no solution") 
        end = time.process_time()  
        t = (round(end - start, 2))
        num = num + 1
        print("Time:", t, "s") 
    print("Finished!", round(time.process_time() - totalstart, 2), "(s)") 
    print("number of times findchoice is called:" , STATSs["OptimalCC"])
if __name__ == "__main__": 
    main()
# Santiago Criado, pd 6, 2024