'''
Created on 8/29/17
Sample code for  
@author: Noushin
'''

function = lambda path: '\n\n'.join([open(path.rstrip(__import__('os').sep) + __import__('os').sep + file, 'r').read()
                                     for file in __import__('os').listdir(path)])

#content = function(path = '/home/noushin/summerTask/sub_files')
content = function(path = '/home/noushin/Downloads/stanford-corenlp-full-2017-06-09/muc_outputs')
f = open("file_name_outputs", "w")
f.write(content)
f.close()
print("done")