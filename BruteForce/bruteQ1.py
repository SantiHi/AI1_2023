import sys; args = sys.argv[1:]
import time 
n = 6
puz = "." * (n*n) 
if len(args) != 0: 
    pzl = args[0]

#generate list of set of constraints for Q1: 
constraints = [] 
for col in range(n): 
    constraints.append(set(col + n*i for i in range(n)))
for row in range(0, n * n, n): 
    constraints.append(set(row + i for i in range(n)))
constraints.append(set(0 + n*i + i for i in range(n)))
constraints.append(set((n*n - n) -n*i + i for i in range(n)))

def bruteForce(pzl): 

    if isInvalid(pzl): return "" 
    if isSolved(pzl): return pzl 
    i = pzl.index(".")
    for val in range(1, n + 1): 
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
    for i, val in enumerate(pzl): 
        if(i % n == 0): 
            print("")
        print(val, end = "")

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
    return pzl.count(".") == 0

def main(): 
    solved = bruteForce(puz)
    printsol(solved)

if __name__ == "__main__": 
    start = time.process_time() 
    main()
    end = time.process_time() 
    t = (round(end - start, 2))
    print()
    print("Time:", t, "s")