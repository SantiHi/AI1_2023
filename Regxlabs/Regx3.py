import sys; args = sys.argv[1:]
idx = int(args[0])-50

myRegexLst = [
    r"/\w*(\w)\w*\1\w*/i",
    r"/\w*(\w)\w*\1\w*\1\w*\1\w*/i", 
    r"/^([01])[01]*\1$|^[01]$/",
    r"/\b(?=\w*cat)\w{6}\b/i",
    r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i",
    r"/\b(?!\w*cat)\w{6}\b/i", 
    r"/\b(?!\w*(\w)\w*\1)\w+\b/i", 
    r"/^(?!.*10011)[01]*$/", 
    r"/\w*([aeoiu])(?!\1)[aeoiu]\w*/i",
    r"/^(?!.*111)(?!.*101)[01]*$/"
] 
if idx < len(myRegexLst):
  print(myRegexLst[idx])
# Santiago Criado, pd 6, 2024