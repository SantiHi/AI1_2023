import sys 
sys.setrecursionlimit(100000)
CASHE = {} 
def change(n, coinList): 
    if (n < 0): return 0
    if(not n or len(coinList)== 1):return 1 
    key = (n, *coinList)
    if key in CASHE: 
        return CASHE[key]
    else: 
        CASHE[key] = change(n - coinList[0], coinList[:]) + change(n, coinList[1:])
        return CASHE[key]
print(change(10000, [100, 50, 25, 10, 5, 1]))

"""
   CACHE = {} - state recursion 
   def change(n, cL): 
   terminating conditions blah blah 
   key = (n, *cL)
   if ket in CACEH: return CACHE[key]
   return change() + change()


"""
