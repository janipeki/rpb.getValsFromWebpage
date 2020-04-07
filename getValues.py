import re

def getValue(search, string, default):
   
#   print(string)
   returnVal = re.search(r'((?<=">)[A-Za-z0-9+, ]+?(?=</))', string)
   if returnVal == None:
       return default
   return returnVal[1]
   
