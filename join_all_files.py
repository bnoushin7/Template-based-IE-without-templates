'''
Created on 8/29/17
Sample code for  
@author: Noushin
'''

function = lambda path: '\n\n'.join([open(path.rstrip(__import__('os').sep) + __import__('os').sep + file, 'r').read()
                                     for file in __import__('os').listdir(path)])

content = function(path = '/home/noushin/summerTask/sub_files')
f = open("file_name", "w")
f.write(content)
f.close()
