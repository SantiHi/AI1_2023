import sys; args = sys.argv[1:]
idx = int(args[0])-30

myRegexLst = [
  r"/^10[01]$|^0$/", #1
  r"/^[01]*$/", #2
  r"/0$/", #3
  r"/\w*[aieou]\w*[aieou]\w*/i",  #4
  r"/^0$|^1[10]*0$/",  #5
  r"/^[01]*110[01]*$/",  #6
  r"/^.{2,4}$/s", #7 
  r"/^\d{3} *-? *\d\d *-? *\d{4}$/", #8
  r"/^.*?d\w*/im", #9
  r"/^[01]?$|^1[01]*1$|^0[01]*0$/" #10 
  r"/[xX.Oo]*{64}/"
]
if idx < len(myRegexLst):
  print(myRegexLst[idx])
# Santiago Criado, pd 6, 2024