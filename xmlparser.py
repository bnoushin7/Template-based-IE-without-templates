'''
Created on 7/31/17
Sample code for  
@author: Noushin
'''


def testfunc(fileName):
    data = open(fileName).read()
    data = data[data.index('<coreference>'):].split('<coreference>')[2:]

    dataList = []

    for x in data:
        data = __import__('re').findall('<text>(.*?)</text>', x)
        data = (data[0], data[-1])
        dataList.append(data)

    return dataList


if __name__ == "__main__":
    #fileName = __import__('sys').argv[1]
    print testfunc("atom_hasan.xml")
