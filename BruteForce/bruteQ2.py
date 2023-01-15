import sys; args = sys.argv[1:]
import time 
puz = "........................"
if len(args) != 0: 
    puz = args[0]

#generate list of set of constraints for Q1: 
constraints = [{5, 6, 7, 12, 13, 14}, {7, 8, 9, 14, 15, 16}, {9, 10 ,11, 16, 17, 19}, {0, 1, 2, 6, 7, 8}, {2, 3, 4, 8, 9, 10}, {13, 14, 15, 19, 20, 21}, {15, 16, 17, 21, 22, 23}]

def bruteForce(pzl): 

    if isInvalid(pzl): return "" 
    if isSolved(pzl): return pzl 
    i = pzl.index(".")
    for val in range(1, 7): 
        subPzl = pzl[:i] + str(val) + pzl[i + 1:]
        bF = bruteForce(subPzl)
        if bF: return bF 
    
def findspaces(pzl): 
    lst = [] 
    for i, v in enumerate(pzl): 
        if v == ".": 
            lst.append(i) 
    return lst 

def printsol(pzl): 
    for indx, val in enumerate(pzl): 
        if(indx == 5 or indx == 12): 
            print()
            print(val, end =" ")
        elif(indx == 0): 
            print(" ", val, end = " ")
        elif(indx ==19): 
            print()
            print(" ", val, end = " ")
        else: 
            print(val, end =" ") 

def findind(pzl, val): 
    return [i for i, v in enumerate(pzl) if v == val]

def isInvalid(pzl): 
    for i, v in enumerate(pzl): 
        if (v != "."): 
            for indx in findind(pzl, v): 
                if(indx != i): 
                  for const in constraints: 
                     if i in const and indx in const: return True 
    return False 

def isSolved(pzl):
    if(not "." in pzl): return True 
    return False 

def main(): 
    solved = bruteForce(puz)
    if solved: 
     printsol(solved)
    else: print("no solution")

if __name__ == "__main__": 
    start = time.process_time() 
    main()
    end = time.process_time() 
    t = (round(end - start, 2))
    print()
    print("Time:", t, "s")