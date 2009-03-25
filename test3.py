import re

stg = {1:['a','aa'], 2:'b', 3:'c', 4:'d', 5:'e'}

beg = 0
portion = 3
if beg < len(stg.keys()):
    for i in range(1,len(stg), 2):
        print stg.items()[i]
        beg += portion
    
    


    