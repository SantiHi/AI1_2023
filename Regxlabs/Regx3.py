import sys; args = sys.argv[1:]
idx = int(args[0])-50

myRegexLst = [
    r"/\w*(\w)\w*\1\w*/i",
    r"/\w*(\w)\w*\1\w*\1\w*\1\w*/i", 
    r"/^(([01])[01]*\2)$|^[01]$/",
    r"/\b(?=\w*cat)\w{6}\b/i",
    r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i",
    r"/\b(?!\w*cat)\w{6}\b/i", 
    r"", 
    r"/\b(?!10011)[01]+\b/" 
] 
if idx < len(myRegexLst):
  print(myRegexLst[idx])
# Santiago Criado, pd 6, 2024