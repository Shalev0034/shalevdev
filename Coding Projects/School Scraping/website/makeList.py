def getList(strList):
    split = strList.split(';')

    if len(split)==1:
        return [split[0]]

    list = []

    for i in range(len(split)-1):
        list.append(split[i])
    
    return list

def add(strList,id):    

    if not strList:
        return str(id)+';'
    strList+=str(id)+';'
    
    return strList

def setList(lst):
    strList=""
    for id in lst:
        strList+=id+';'
    return strList