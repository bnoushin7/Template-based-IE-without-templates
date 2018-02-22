'''
Created on 9/8/17
Sample code for  
@author: Noushin
'''

'''

from pathlib import Path
files_to_rename = Path('F:/public_share/test')
files = [f for f in files_to_rename.iterdir()]
for file in files:
    file.rename(str(file).rstrip())
    print(file)

'''