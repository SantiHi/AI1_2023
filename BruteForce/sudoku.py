import sys; args = sys.argv[1:]
import time 

if len(args) != 0: 
    f1 = open(args[0])
else: 
    f1 = open("BruteForce/puzzles.txt")
#generate list of set of constraints for Q1: 
size = 9 

def setGlobals(pzl): 
    global constraints; global constraintsthatmakesense 
    constraints = [{value + val for val in range(0, size)} for value in range(0, size*size, size)]
    constraints = constraints + [{value + val for val in range(0, size*size, size)} for value in range(0, size)]
    constraints = constraints + [{0, 1, 2, 9, 10, 11, 18, 19, 20}, {3, 4, 5, 12, 13, 14, 21, 22, 23}, {6, 7, 8, 15, 16, 17, 24, 25, 26},
    {27, 28, 29, 36, 37, 38, 45, 46, 47}, {30, 31, 32, 39, 40, 41, 48, 49, 50}, {33, 34, 35, 42, 43, 44, 51, 52, 53}, {54, 55, 56, 63, 64, 65, 72, 73, 74},
    {57, 58, 59, 66, 67, 68, 75, 76, 77}, {60, 61, 62, 69, 70, 71, 78, 79, 80}] 
    constraintsthatmakesense = {ind: [cset for cset in constraints if ind in cset] for ind in range (0, size * size)}


#ascii table 
ascii_table = {"1":49, "2":50, "3":51, "4":52, "5":53, "6":54, "7":55, "8":56, "9":57}
def bruteForce(pzl, indx): 
    if isInvalid(pzl, indx): return "" 
    if isSolved(pzl): return pzl 
    i = pzl.index(".")
    for val in range(1, 10):     
        subPzl = pzl[:i] + str(val) + pzl[i + 1:]
        bF = bruteForce(subPzl,i)
        if bF: return bF 
    
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
        for const in constraintsthatmakesense[indx]: 
            for i in const: 
                if i in const and indx in const and i != indx and pzl[i] == pzl[indx]: 
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
    for line in f1: 
        print(num, end = "")
        if num > 9:
            print(": ", end ="")
        else: 
            print(": ", end = " ")
        puz = line.strip()
        setGlobals(puz)
        print(puz)
        start = time.process_time() 
        if(not isInvalidonce(puz)): 
            solved = bruteForce(puz, puz.index("."))
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
if __name__ == "__main__": 
    main()
# Santiago Criado, pd 6, 2024