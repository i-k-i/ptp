# coding:utf-8
# 20130404-2105
'''
logoparser v2
'''
import os
import sys
import datetime
configFile = 'config'

#change work dir to scripts dir
os.chdir(os.path.dirname(os.path.realpath(__file__)))

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
        return blocsDict
    
    itemName = ''
    for i in inpList:
        if separator in i[begCut:endCut]:
            itemName = i
            if i not in blocsDict:
                blocsDict.update({i:[]})
        elif itemName != '' and i not in ['\n',' ','','*','#']:
            blocsDict[itemName].append(i)
    return blocsDict

def tagFinder(blocDict, tagList):
    tagDict = {}
    for i in blocDict:
        for j in blocDict[i]:
            for z in tagList:
                if z.lower() in j.lower():
                    if i not in tagDict:
                        tagDict.update({i:[z]});
                    else:     
                        if z not in tagDict[i]:
                            tagDict[i].append(z)
    for d in tagDict:
        print d
        for s in tagDict[d]:
            print s
    return tagDict

def pathFinder(fileName, logDir = os.getcwd()):
    '''return path to file'''
    pathToFile = os.path.join(logDir,fileName)
    if os.path.isfile(pathToFile): 
        return(pathToFile)

def  deficator(sourceList, tagList, separator, outFile=os.path.join(os.getcwd(),'finised.org')):
    '''write data in finised.org and in "archive"'''
    if not os.path.exists(os.path.join(os.getcwd(),'archive')):
        os.mkdir(os.path.join(os.getcwd(),'archive'))
    oFile = open(outFile,'w')
    date = ''.join(str(datetime.datetime.now())[:10].split('-'))
    time = ''.join((str(datetime.datetime.now())[11:19]).split(':'))
    arcName = date+'-'+time+'.org'
    arcFile = open(os.path.join(os.getcwd(),'archive',arcName),'w')

    for source in sourceList:
        rawFile = eater(source)
        blocDict = divisor(rawFile,separator,'first')
        tagsDict = tagFinder(blocDict,tagList)
        if len(tagsDict) > 0 :
            oFile.writelines('File-'+source+'\n')
            arcFile.writelines('File-'+source+'\n')
            for item in tagsDict:
                oFile.write(item)
                oFile.write('             Tags: ')
                arcFile.write(item)
                arcFile.write('             Tags: ')

                for tag in tagsDict[item]:
                    oFile.write(tag)
                    arcFile.write(tag)
                    if  tag != tagsDict[item][-1]:
                        oFile.write(', ')
                        arcFile.write(', ')
                    else:
                        oFile.write('\n')
                        arcFile.write('\n')
                for strings in blocDict[item]:
                    oFile.write(strings+'\n')
                    arcFile.write(strings+'\n')
                oFile.write('\n')
                arcFile.write('\n')
                
    oFile.close()
    arcFile.close()

def sourceList(rawSList, sTypes):
    sDirList = []
    sList = []

    for i in rawSList:
        #if elem beginig with '.' find sources in this subdir
        if i[0] == '.':
            subDir = os.getcwd()+'/'+i[1:]
            if os.path.isdir(subDir):
                sDirList.append(subDir)
            elif os.path.isdir(i):
                sDirList.append(i)
            elif os.path.isfile(i):
                sList.append(i)
    for i in sDirList:
        for root, dirs, files in os.walk(i):
            for name in files:
                source = os.path.join(root, name)
                if source[-1] not in ['~','#']:
                    for j in sTypeList: 
                        if j in source and source not in sList :
                            sList.append(source)
    return sList
#     
rawConfig = eater(pathFinder(configFile))
confDict = divisor(rawConfig,'* ','first')
# processing of '* TXTSOURCE'
sTypeList = confDict['* SOURCETYPES']
rawSList = confDict['* TXTSOURCE']
tagList = confDict['* TAGS']
# and make ".org" files
deficator(sourceList(rawSList, sTypeList), tagList, "* ")
