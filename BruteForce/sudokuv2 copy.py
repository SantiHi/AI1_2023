import sys; args = sys.argv[1:]
import time 

if len(args) != 0: 
    f1 = open(args[0])
else: 
    f1 = open("BruteForce/puzzles.txt")
#generate list of set of constraints for Q1: 
size = 9 
symbolset = "123456789";
def setGlobals(pzl): 
    global constraints; global constraintsthatmakesense; global neighbors; global STATSs
    STATSs = {"OptimalCC":0}
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
    choice = findchoice(listofsets); STATSs["OptimalCC"] += 1
    for symbol in symbolset:     
        subPzl = pzl[:choice] + symbol + pzl[choice + 1:]
        if not symbol == "9": 
            copyset = makecopy(listofsets)
        else: copyset = listofsets
        update(copyset, symbol, choice)
        bF = bruteForce(subPzl, copyset, choice)
        if bF: return bF 
    
def makecopy(listofsets): 
    return [[tl[0], {v for v in tl[1]}, tl[2]] for tl in listofsets]
def findchoice(listofsets): 
    del listofsets[listofsets.index((v:=max(listofsets)))]
    return v[2]
def update(datastruc, symbol, indx): 
    for v in datastruc: 
        if symbol not in v[1] and indx in neighbors[v[2]]: 
            v[1].add(symbol); v[0] +=1

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
        if time.process_time() - totalstart > 120: print("times up!", STATSs["OptimalCC"]); print(round(time.process_time() - totalstart, 2)); break; 
        print(num, end = "")
        if num > 9:
            print(": ", end ="")
        else: 
            print(": ", end = " ")
        pzl = line.strip()
        setGlobals(pzl)
        print(pzl)
        start = time.process_time() 
        if(not isInvalidonce(pzl)): 
            i = 0
            solved = bruteForce(pzl, [[ len((z:={pzl[nbr]for nbr in neighbors[indx] if pzl[nbr] != "."})), z , indx] for indx, val in enumerate(pzl) if val == "."], pzl.index("."))
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
    import cProfile 
    cProfile.run("main()", "output1.dat")
    import pstats 
    from pstats import SortKey 

    with open("output_time1.txt", "w") as f: 
            p = pstats.Stats("output1.dat", stream = f) 
            p.sort_stats("time").print_stats() 

    with open("output_calls1.txt", "w") as f: 
            p = pstats.Stats("output1.dat", stream = f) 
            p.sort_stats("calls").print_stats()
# Santiago Criado, pd 6, 2024