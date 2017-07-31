'''
Created on 7/31/17
Sample code for  reversing dictionaries
@author: Noushin
'''

a = {1:["a"], 2:["a","b"], 3:["a"], 4:["b", "cd"], 6:["a","cd"]}
b = dict()
for key, value in a.items():
    for item in value:
        if item in b.keys():
            b[item].append(key)
        else:
            b[item] = [key]

print type(b)
print(b)
