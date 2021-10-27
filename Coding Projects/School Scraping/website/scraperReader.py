import datetime
from operator import index, sub
from typing import Text, Type
from requests_html import HTMLSession
import calendar
from flask_login import current_user
from .makeList import setList,getList
from .models import Major

tableSplit = '<table id="calender">'
subjects=['מתמטיקה','אזרחות','ספורט','ספרות','אנגלית']
tests=['מתכונת','בגרות','מבחן']
exeptions=['ראש השנה','יום כיפור','סוכות','טיול שנתי','חנוכה']
bools = []
for i in range(len(bools)):
    bools.append(False)
bools.append(False)


def ReadData(month_int,year,check):
    session = HTMLSession()
    #r = session.get('https://docs.google.com/document/d/e/2PACX-1vSRSgaKVSN_6Im5omfaSLmtJ0xUXN36hS-BUyYI4X3zvETy7Vfajc7tc8OwWE2ZqCh0T_FRItC12sjc/pub')    
    r=session.get('https://docs.google.com/document/d/e/2PACX-1vSsL2VtHsNVdBNPY7G-CL6ZflcCytnwlFmqW-6y4q190qVpfR9wFEr_iI2cBShlYgihm1-P13HrwJl5/pub')
    table_data = getTableData(month_int,year)
    hebrew_month = fromIntToStringMonth(month_int)
    last_date=0
    
    if not monthExists(r,hebrew_month,year):
        return getTable(table_data.getList())

    for i in range(6,36):            
        result_list =r.html.xpath("(//*[@id='contents']/div/p/span[contains(text(), '{0}')]/following::table[1]/tbody/tr/td)[{1}]/p/span/text()".format(hebrew_month,i+1))               

        if len(result_list)>0:
            
            text= checkSkip(result_list,check)
            if type(text) == str and text=="":
                continue
            result_list[0].replace('\xa0','')
            result_list[0].replace(' ','')
            date = result_list[0]

            split = date.split('.')
            if len(split)>1:
               #This date has a '.'
                date = int(split[0])

                split[1].replace('\xa0','')

                if split[1] == '':
                    #There is no month specefied, proceed as normal
                    if last_date<date:
                        last_date=date                    
                        table_data.updateFromDate(date,text)                       
                        continue
                    #There is no month specefied but the date doesnt make sence
                    else:                
                        update_broken_collumn(result_list,table_data,month_int,text)                    
                        continue

                elif split[1].isnumeric():
                    #Get the month specefied
                    date_month = int(split[1])

                    #Check if the month is correct, if not investigate whats wrong
                    if date_month == month_int:                
                        if last_date<date:                            
                            table_data.updateFromDate(date,text)
                        #Wrong date, investigate
                        else:
                            update_broken_collumn(result_list,table_data,month_int,text)                           
                            continue                    
                    else:                        
                        update_broken_collumn(result_list,table_data,month_int,text)
                        continue

                #The month isn't missing but is also not a number, investigate whats wrong                                    
                else:
                    update_broken_collumn(result_list,table_data,month_int,text)
                    continue
            #There is not '.' in the date
            else: 
                date = int(result_list[0])                
                if last_date<date:
                    last_date=date
                    table_data.updateFromDate(date,text)
                    continue
                #Wrong date, investigate
                else:                     
                    update_broken_collumn(result_list,table_data,month_int,text)                    
                    continue
    table = getTable(table_data.getList())
    return table 

def checkSkip(lst,check):
    if check:
        if len(lst)>0:
            #Convert the list to a simple string sentence
            sentence = fromListToString(lst)
    
            #There is a test in the sentence
            foundTest = True
            output = ""
            while foundTest:
                foundTest=False
    
                for exeption in exeptions:            
                    if sentence.find(exeption)!=-1:
                        return exeption
    
                for test in tests:                
                    if sentence.find(test)!=-1:                    
                        
                        foundTest=True
                        min = len(sentence)
                        foundSubject=""
                            
                        if current_user.majors:
                            majors = getList(current_user.majors)   
                            for major in majors:
                                major = Major.query.get(major)
                                keywords=getList(major.keywords)
                                for keyword in keywords:                                
                                    find = sentence.find(keyword)
                                    if find!=-1 and find<min:
                                        min=find
                                        foundSubject=keyword                                    
    
                        for subject in subjects:
                            find = sentence.find(subject)
                            if find!=-1 and find<min and (sentence.find('כולם')!=-1 or sentence.find('עיוניות')!=-1):
                                min=find
                                foundSubject=subject                                 
    
    
                        sentence=sentence.replace(test,"",1)
    
                        if foundSubject!="":
                            if output=="":
                                output = test+" "+foundSubject
                            else:
                                output+=" "+test+" "+foundSubject
                                
                            sentence=sentence.replace(foundSubject,"",1)
                            break    
            return output
        else: return "" 
    else: return lst
                


def fromListToString(lst):
    sentence = lst[0]
    for i in range(1,len(lst)):
        sentence+=lst[i]

    return sentence
    

def checkIfSkip(lst):
    count=0
    text=""
    
    if current_user.majors:
        majors = getList(current_user.majors)   

        for i in range(len(majors)):
            majors[i]=Major.query.get(majors[i])
        
        for i in range(1,len(lst)):

            for f in range(len(tests)):
                if lst[i].find(tests[f])!=-1 and not bools[f]:
                    bools[f]=True
                    if text=="":
                        text+=tests[f]
                    else: text+=" "+tests[f]
                    count+=1

            for exeption in subjects:
                if lst[i].find(exeption)!=-1:
                    if text=="":
                        text+=exeption
                    else: text+=" "+exeption
                
            if lst[i].find('מתמטיקה')!=-1:
                if text=="":
                    text+='מתמטיקה'
                else: text+=" "+'מתמטיקה'
                count+=1

            if lst[i].find('עיוניות')!=-1 and not bools[len(bools)-1]:
                bools[len(bools)-1]=True
                if text=="":
                    text+='מתמטיקה'
                else: text+=" "+'מתמטיקה'
                count+=1


            for major in majors:
                keywords = getList(major.keywords)

                for keyword in keywords:
                    if lst[i].find(keyword)!=-1:
                        if text=="":
                            text+=exeption
                        else: text+=" "+exeption
                        count=2
        return count<2
    else: return False

    
def monthExists(result,hebrewMonth,year):
    now = datetime.datetime.now()
    lst = result.html.xpath("//*[@id='contents']/div/p/span[text()]/text()")
    months = ['ינואר','פברואר','מרץ','אפריל','מאי','יוני','יולי','אוגוסט','ספטמבר','אוקטובר','נובמבר','דצמבר']
    toRemove=[]

    for text in lst:
        
        exists = False

        for month in months:
            if text==month:
                exists=True
        
        if not exists:
            toRemove.append(text)

    for text in toRemove:
        lst.remove(text)

  

    for month in lst:
        if hebrewMonth==month:            
            return True
    
    return False



def is_broken_collumn(last_date,current_date):
    if last_date>current_date:
        return True
    return False
    
def is_unnecessary_dot(date:str): 
    month = date.split('.')[1]  
    if month == '' or not month.isnumeric():
        return True
    return False

def update_broken_collumn(lst,table_data,month_int,txt):
    lst_connect=[]

    for i in range(len(lst)):
        lst_connect.extend(lst[i].replace('\xa0',''))
    
    dot=False
    for i in range(len(lst)):
        if lst_connect[i] =='.':
            dot=True

    date = ""
    text =""
    index=0

    if not dot:
        for i in range(len(lst_connect)):
            if lst_connect[i]!=' ':
                date+=lst_connect[i]
                index = i
            else: break
        for i in range(index+1,len(lst_connect)):
            text+=lst_connect[i]
    else:
        for i in range(len(lst_connect)):
            if lst_connect[i] == '.':
                date+=lst_connect[i]
                index=i
                break
            else:
                index=i
                date+=lst_connect[i]

        for i in range(index+1,len(lst_connect)):
            if lst_connect[i].isnumeric():
                index=i
                date+=lst_connect[i]
            else:
                index = i
                break

        for i in range(index,len(lst_connect)):
            text+=lst_connect[i]
    split = date.split('.')
    
    if type(txt) == str:
        text=txt
        
    if len(split)>1 and split[1]!='':
        date_month = int(split[1]) 
        if date_month == '':
            table_data.updateFromDate(split[0],text)                
        else:
            if date_month ==month_int:
                table_data.updateFromDate(split[0],text)
            elif date_month > month_int:
                text = date +'</br>' + text
                table_data.updateInBlank(text,True)
            else: 
                text = date +'</br>' + text
                table_data.updateInBlank(text,False)
    else:
        table_data.updateFromDate(split[0],text)
            
def updatePlace(row,collumn):
    if collumn<7:
        return [row,collumn+1]
    elif row<6:
        return [row+1,collumn]
    else:
        return [row,collumn]

def getStringMonth(month):
    hebrewMonths = ['ינואר','פברואר','מרץ','אפריל','מאי','יוני','יולי','אוגוסט','ספטמבר','אוקטובר','נובמבר','דצמבר']
    englishMonths = ['January','February','March','April','May','June','July','August','September','October','November','December']

    for i in range(hebrewMonths.__len__()):
        if hebrewMonths[i] == month:
            return englishMonths[i]       

    return 'No month was found'

def fromIntToStringMonth(month):
    hebrewMonths = ['ינואר','פברואר','מרץ','אפריל','מאי','יוני','יולי','אוגוסט','ספטמבר','אוקטובר','נובמבר','דצמבר']
    return hebrewMonths[month-1]

def fromStringToIntMonth(month):
    lst = ['ינואר','פברואר','מרץ','אפריל','מאי','יוני','יולי','אוגוסט','ספטמבר','אוקטובר','נובמבר','דצמבר']
    for i in range(len(lst)):
        if lst[i]==month:
            return i+1

def getFirstDay(month):
    now = datetime.datetime.now()
    year = now.year
    intDay = datetime.date(year,month,1).weekday()
    Days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    for i in range(7):
        if intDay == i:
            return Days[i]
    
    return 'Day not found'

def getFDinInt(month,year):
    int_day = datetime.date(year,month,1).weekday()
    if int_day == 6:
        return 1
    else: return int_day+2

def getDaysInMonth(month,year):
    now = datetime.datetime.now()
    return calendar.monthrange(year, month)[1]

def getIntMonth(month):
    now = datetime.datetime.now()
    return calendar.monthrange(now.year, now.month)[1]

def getTable(tableData):
    table="{0}\n".format(tableSplit)
    
    table+="  <tr>\n"
    first_list=tableData[0]
    for td in first_list:
        table+="    <td><div class='significant-text'>{0}</div></td>\n".format(td)
    table+="</tr>\n"
    
    for i in range(1,len(tableData)):
        
        list1=tableData[i]
        list1=tableData[i]

        table+="  <tr>\n"
        for td in list1:            

            split=td.split('</br>') 
            if(len(split)>1):
                table+="    <td><div class='significant-text'>{0}</div><div class='table-div' contenteditable>{1}</div></td>\n".format(split[0],split[1])
            else:
                table+="    <td>{0}</td>\n".format(td)

        table+="</tr>\n"
    table+="</table>"

    return table

def getTableData(month,year):
    big_list = [[]]
    table_data = tableData()
    table_data.setList(big_list)
    days = getDaysInMonth(month,year)
    startsAt = getFDinInt(month,year)
    
    table_data.addDays()
    
    for i in range(startsAt-1):
        table_data.addCollumn('')
    
    for i in range(days):
        table_data.addCollumn(str(i+1)+"</br>")
    
    for i in range(35-startsAt):
        table_data.addCollumn('')
    table_data.reverse()
    
    #Checks if the last list is empty and removes it if it is
    lst = table_data.getList()
    last_lst = lst[lst.__len__()-1]
    allEmpty=True
    for Str in last_lst:
        if Str!='':
            allEmpty=False
    if allEmpty:
        lst.pop(lst.__len__()-1)

    return table_data

def getBlankTable(month):     
    table_data = getTableData(month)

   
    return getTable(table_data.getList())

def reverse(lst):
    for i in range(len(lst)/2):
        temp = lst[i]
        lst[i]=lst[i*2-1]
        lst[i*2-1]=temp
    return lst

class tableData():    
    
    def getList(self):
        return self.list1
    def setList(self,list2):
        self.days=False
        self.list1=list2
    
    def reverse(self):
        for i in range(1,self.list1.__len__()):
            lst = self.list1[i]
            for j in range(lst.__len__()//2):
                
                temp = lst[j]
                lst[j]=lst[lst.__len__()-j-1]
                lst[lst.__len__()-j-1]=temp

    def addDays(self):
        days_list = ['שבת','שישי','חמישי','רביעי','שלישי','שני','ראשון']
        self.list1.insert(0,days_list)
        self.days=True

    def updateInBlank(self,list2,last):
        #print(type(list2))

        if last:
            blank_list=self.list1[self.list1.__len__()-1]
        else: blank_list=self.list1[1]
                         
        for i in range(blank_list.__len__()-1,-1,-1):
            fixedStr = blank_list[i]
            fixedStr = blank_list[i].replace('</br>','')
            if fixedStr == '':
                if type(list2)!=str:
                    if not str(list2[0]).isnumeric():list2[0]=list2[0].replace('\xa0','')
                    blank_list[i]+=str(list2[0])
                    blank_list[i]+="</br>"
                    for j in range(1,list2.__len__()):
                        list2[j]=list2[j].replace('\xa0','')
                        blank_list[i]+=str(list2[j])
                    return
                else: 
                    blank_list[i]+= list2
                    return
               

    def updateFromDate(self, date, list2):
        for i in range(1,self.list1.__len__()):
            sub_list = self.list1[i]
            for j in range(sub_list.__len__()):
                fixedStr = sub_list[j].replace('</br>','')
                if fixedStr== str(date):
                    if type(list2) != str:
                        for k in range(1,list2.__len__()): 
                                if list2[k] != '':
                                    list2[k]=list2[k].replace('\xa0','')
                                    sub_list[j]+=str(list2[k])
                    else: sub_list[j]+=list2
                    return

    def update(self,row,collumn,text):
        sub_list=self.list1[row]
        sub_list[collumn]+=text
        

    def addCollumn(self, Collumn):
        
        len = self.list1.__len__()
        if len == 0: #The big list is empty, create a new list and append it to the big list
            newList = [Collumn]
            self.list1.append(newList)
            return
        
       
        if not self.days:
            maxLen=6
        else:
            maxLen=7
        if len>0 and len <maxLen:
            #The big list isn't full but isn't empty, if it's full create a new one. Else put the text in the last spot
            last_list = self.list1[len-1]
            last_list_len = last_list.__len__()
            
            if last_list_len <7: #The list is not full
                last_list.append(Collumn)
                return
            else: #The list is full, create a new one and append it to the list of lists
                newList = [Collumn]
                self.list1.append(newList)
                return 
        else: #The big list is full, if the last list is full override the last place. Else add to the last list
            last_list = self.list1[len-1]
            last_list_len = last_list.__len__()

            
            if last_list_len <7: #The last list isn't full
                last_list.append(Collumn)
                return
            else: # The last list is full
                last_list[last_list_len-1]=Collumn
                return
