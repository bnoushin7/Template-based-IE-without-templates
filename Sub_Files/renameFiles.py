import os
files_to_rename = os.listdir(os.getcwd())
files = [f for f in files_to_rename.iterdir()]
for file in files:
    file.rename(str(file).rstrip())
