# coding:utf-8
# 20130404-2105
'''
logoparser v2
'''
import os
import sys

configFile = 'config'

#
def eater(pathToFile):
    '''Read file. return list of strings of file without garbage'''
    inpFile = open(pathToFile,'r')
    rawList = inpFile.readlines()
    inpFile.close()
    clearList = []
    for i in rawList:
        clearList.append(' '.join(i.split()))
    return clearList

def divisor(inpList, separator, position='any'):
    '''return list of blocs
    position may be: first, any, last or [x](int)
    '''
    blocsDict={}
    begCut = None
    endCut = None
    if position == 'any':
        begCut = None
        endCut = None
    elif position == 'last':
        begCut = -len(separator)
        endCut = None
    elif position == 'first':
        begCut = None
        endCut = len(separator)
    elif type(position) == int:
            begCut = position-1
            endCut = position+len(str(position))
    else:
        print 'position in divisor may be: first, any, last or [x](int)'
        return blockDict
    
    itemName = ''
    for i in inpList:
        if separator in i[begCut:endCut]:
            print i
            itemName = i
            if i not in blocsDict:
                blocsDict.update({i:[]})
        elif itemName != '' and i not in ['\n',' ','']:
            blocsDict[itemName].append(i)
    return blocsDict

#def tager():

def pathfinder(fileName, logDir = os.getcwd()):
    '''return path to file'''
    if 'linux' in sys.platform:
        slash = '/'
    elif 'win' in sys.platform:
        slash = '\\'
    pathToFile = logDir+slash+fileName
    if os.path.isfile(pathToFile): 
        return(pathToFile)

def  deficator():
    '''write '''
    pass

rawConfig = eater(pathfinder(configFile))


print divisor(rawConfig,'* ','first')
