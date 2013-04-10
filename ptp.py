# -*- coding: utf-8 -*-
'''
Ептыть
'''
import os, sys

if "win" in sys.platform:
    slash = "\\"
if "linux" in sys.platform:
    slash = "/"

pwd = os.getcwd()
fconf = pwd+slash+'config'
rawconf = open(fconf,'r')
config=rawconf.readlines()

# Прическа 
for i in config:
    i = ' '.join(i.split())

def upars(inplist,target):
    outlist=[]
    for i in range(len(inplist)):
        if target in inplist[i]:
            outlist.append(i)
    outlist.append(len(inplist)-1) # Последним записывается длина списка


#get table of contents of the config
partsconf=[]
for i in upars(config,'* '):
    print i
    if config[i][0:2] == '* ':
        for j in config[i].split()[1:]:
            print j,i
            partsconf.append([j,i])
    elif config[i] == config[-1]:
        partsconf.append(['END',i])
#            print i, partsconf
#Loading txtsources
print partsconf

def getconfitem(item):
    confitem = []
    for i in xrange(len(partsconf)):
        if item in partsconf[i]:
            for j in config[partsconf[i][1]:partsconf[i+1][1]]:
                if j not in ['\n',' ','']: 
                    confitem.append(j)
    return confitem
txtdirs = []
txtsources = []
# если имя начинаеться с '.' - ищим логи в этой подпапке
# если Винда - ищим строки типа [диск]:
for i in getconfitem('TXTSOURCE'):
    if i[0] == '.':
        txtdirs.append(pwd+slash+i[1:-1])
    elif i[-4:] == '.txt' and 'log' in i:
        txtsources.append(i)
    elif "win" in sys.platform and i[1] == ':':
        txtdirs.append(i)
    elif i[0] == '/' and "linux" in sys.platform:
        if os.path.isfile(i):
            txtsource.append(i)
            print i
        else: txtdirs.append(i)

# Если ли папка?
for i in txtdirs:
     if not os.path.isdir(i):
         txtdirs.remove(i)    

# Никаких служебных файлов
blacklistsources = ['#','~','$','&','.']
for i in txtdirs:
    i=''.join(i.split())
    for j in os.listdir(i):
        if j[0] not in blacklistsources and j[-1] not in blacklistsources:
            if i[-1] not in ['/','\\']: 
                txtsources.append(i+slash+j)
            else: txtsources.append(i+j) 

# Есть ли файл
sourcefilelist=[]
for i in txtsources:
   if os.path.isfile(i):
       sourcefilelist.append(i)

#print txtdirs
#print txtsources
#print sourcefilelist

tagsconflist = getconfitem('TAGS')
print tagsconflist
