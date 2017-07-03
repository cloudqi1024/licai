#encoding=gbk
from __future__ import print_function


from dateutil import relativedelta
import datetime
today = datetime.datetime.now()
todayStr = str(datetime.datetime.now().strftime('%Y%m%d'))
dataFormat = '%Y%m%d'


class Parser(object):
    def __init__(self, wrappee):
        self.w = wrappee()
    def parse(self, itemName, fileName):
        return self.w.parse(itemName, fileName)


class LufaxParser(object):
    def parse(self,itemName, fileName):
        
        invData = []
        cashFlow = {}
        with open(fileName) as f:
            for line in f:
                if line.startswith('#'): continue
                if line.startswith('名称'): continue
                item = line.strip().split('\t')
                #print line
                
                name = item[0]
                principle = float(item[1])
                #realized = float(item[2])
                unRealized = float(item[3])
                nextPayDate = datetime.datetime.strptime(item[4],'%Y-%m-%d') 
                
                nextAmount = unRealized/30 #TODO
                                
                if name.startswith('稳盈-安e'):
                    ret = 0.084
                elif name.startswith('点金'):
                    ret=0.085
                    unRealized = principle
                    
                else:
                    ret = 0
                                
                invData.append([
                                '陆金所',
                                item[0],
                                unRealized,
                                ret,
                                nextPayDate,
                                unRealized/30, #TODO: just an estimation!!
                                36
                                ])
       
                cashFlow[nextPayDate.strftime(dataFormat)] = cashFlow.get(nextPayDate, 0)+ nextAmount
                    
        return invData, cashFlow       
            
class WeiDaiParser(object):
    def parse(self, item, fileName):
        invData = []
        cashFlow = {}
        with open(fileName) as f:
            for line in f:
                if line.startswith('#'): continue
                if line.find('优选')==-1:continue
                name = line.strip()
                line = f.next().strip()
                [ret,left] = line.split('%')
                ret = float(ret)/100 #实际可能差不多， 考虑到0.6的费用
               
                if left.find('个月')!=-1:
                    [monthStr,left] = left.split('个月')
                else:
                    [monthStr,left] = left.split('天')
                    monthStr = 1
                
                [principle,_amountIntExp,startDateStr] = left.split('.')
                principle =float(principle.replace(',',''))
                startDate = datetime.datetime.strptime(startDateStr[2:],'%Y-%m-%d') 
                endDate = startDate+relativedelta.relativedelta(months=int(monthStr)) 
                
                
                
                r = relativedelta.relativedelta(today,startDate )
                usedMonth = r.months
                nextPayDate = startDate+relativedelta.relativedelta(months=int(usedMonth+1)) 
                
                unRealized = principle #unrealized just equal to priciple
               
                interest = principle*ret/int(monthStr)
                if (usedMonth+1)==int(monthStr):
                    nextPayAmt = interest+principle
                else:
                    nextPayAmt = interest
                    
                if today>endDate: 
                    print ('by pass ' , line)
                    continue
                     
                invData.append([
                                item,
                                name,
                                unRealized,
                                ret,
                                nextPayDate,
                                nextPayAmt,
                                int(monthStr)-usedMonth 
                                ])
                
                cashFlow[nextPayDate.strftime(dataFormat)] = cashFlow.get(nextPayDate, 0)+ nextPayAmt
        
            #End of parse.    
          
            return invData, cashFlow    


class DaoKouDaiParser(object):
    
    def parse(self, itemName, fileName):
    
        invData = []
        cashFlow = {}
        with open(fileName) as f:
            for line in f:
                if line.startswith('#'): continue
                if line.startswith('序号'): continue
                item = line.strip().split('\t')
                print (fileName,line)
                
                name = item[1]+item[2]
               
                #realized = float(item[2])
               
                invDate = datetime.datetime.strptime(item[3],'%Y-%m-%d') 
                ret = float(item[4].replace('%',''))/100
                principle = float(item[5].replace(',',''))
                unRealized = principle
                nextPayDate = invDate+relativedelta.relativedelta(months=1) 
                r = relativedelta.relativedelta(today,invDate )
                usedMonth = r.months
                    
                if ret>0.09:
                    totMonth=6
                else:
                    totMonth=3
                
                if item[-1].strip().endswith('M'):
                    totMonth = int(item[-1][:-1]);#hint
                
                 
                interest = principle*ret/int(totMonth)
                if (usedMonth+1)==int(totMonth):
                    nextPayAmt = interest+principle
                else:
                    nextPayAmt = interest
                    
                                
                invData.append([
                                itemName,
                                name,
                                unRealized,
                                ret,
                                nextPayDate,
                                nextPayAmt,  
                                totMonth-usedMonth
                                ])
       
                cashFlow[nextPayDate.strftime(dataFormat)] = cashFlow.get(nextPayDate, 0)+ nextPayAmt
                    
        return invData, cashFlow       



class CommonParser(object):
    
    def parse(self, itemName, fileName):
    
        invData = []
        cashFlow = {}
        with open(fileName) as f:
            for line in f:
                if line.startswith('#'): continue
                if line.startswith('序号'): continue
                if len(line.strip())==0: continue
                
                item = line.strip().split('\t')
                
                for  i in range(len(item)):
                    item[i] = item[i].replace(' ','')
#                 print(line,item[3])
                
                name = item[1]+item[2]
               
                #realized = float(item[2])
                print (line,item[3])
                invDate = datetime.datetime.strptime(item[3],'%Y-%m-%d') 
                ret = float(item[4].replace('%',''))/100
                principle = float(item[5].replace(',',''))
                unRealized = principle
              
                r = relativedelta.relativedelta(today,invDate )
                usedMonth = r.months
                    
                
                dueDate =  datetime.datetime.strptime(item[6],'%Y-%m-%d') 
                r = relativedelta.relativedelta(dueDate,invDate )
                totMonth = r.months+r.years*12
                    
            
                nextPayAmt =  principle*(totMonth/12*ret+1);
                    
                                
                invData.append([
                                itemName,
                                name,
                                unRealized,
                                ret,
                                dueDate,
                                nextPayAmt,  
                                totMonth-usedMonth
                                ])
       
                cashFlow[dueDate.strftime(dataFormat)] = cashFlow.get(dueDate, 0)+ nextPayAmt
                    
        return invData, cashFlow   
    
class LanTouZiParser(object):
    def parse(self, itemName, fileName ):
        invData = []
        cashFlow = {}
        
        
        with open(fileName) as f:
            for line in f:
                if line.startswith('#'): continue
                if len(line.strip())==0:continue
                if line.find('正在还款')!=-1:
                    f.next()#已到账收益 
                    nextPayDateLine = f.next().strip()
                    
                    
                    nextPayDate = datetime.datetime.strptime(nextPayDateLine.split(' ')[1], '%Y-%m-%d') #下一个还款日 
                    name = f.next().strip() #下一个还款日 
                    
                    invDateLine =  f.next().strip()
                    invDate = datetime.datetime.strptime(invDateLine.split(' ')[0],'%Y-%m-%d') 
                
                    principle =float( f.next().strip().replace(',',''))
                    
                    f.next().strip()# 
                    f.next().strip()# 
                      
                    dueDateLine = f.next().strip() 
                    
                    dueDate =  datetime.datetime.strptime(dueDateLine.split(' ')[0],'%Y-%m-%d') 
#                     print (dueDate)
                    r = relativedelta.relativedelta(today,invDate )
                    usedMonth = r.months
             
                    r = relativedelta.relativedelta(dueDate,invDate )
                    totMonth = r.months+r.years*12
                    if totMonth==2 or totMonth==5 or totMonth==11 or totMonth==8 or totMonth==17:
                        totMonth=totMonth+1 
                    
                    if today>dueDate: 
#                         print ('by pass ' , line)
                        continue
                    
                    
                    
                     
                    unRealized = principle #unrealized just equal to priciple
                    ret = 0
                    if invDate>=datetime.datetime.strptime('20170216','%Y%m%d'):
                        if totMonth==3: ret = 0.072
                        elif totMonth==6: ret = 0.078
                        elif totMonth==9: ret = 0.086
                        elif totMonth==12: ret = 0.092
                        elif totMonth==18: ret = 0.10
                    else:
                        if totMonth==3: ret = 0.08
                        elif totMonth==6: ret = 0.085
                        elif totMonth==9: ret = 0.10
                        elif totMonth==12: ret = 0.12
                        elif totMonth==18: ret = 0.12
                             
                    
                    
                    interest = principle*ret/int(totMonth)
                    if (usedMonth+1)==int(totMonth):
                        nextPayAmt = interest+principle
                    else:
                        nextPayAmt = interest
                     
                    if int(totMonth)-usedMonth==0:
                        pass
                 
                        
                         
                    invData.append([
                                    itemName,
                                    name,
                                    unRealized,
                                    ret,
                                    nextPayDate,
                                    nextPayAmt,
                                    int(totMonth)-usedMonth 
                                    ])
           
                    cashFlow[nextPayDate.strftime(dataFormat)] = cashFlow.get(nextPayDate, 0)+ nextPayAmt
                    
        return invData, cashFlow    

def num2cs(x):
    x = int(round(x))
    if x == 0:
        return '0'
    elif x > 0:
        flag = 1
    else:
        flag = -1
    s = ''
    x = abs(x)
    while x >= 1000:
        s = ',%03d%s' % (int(x % 1000), s)
        x = x / 1000
    s = str(x) + s
    if flag == -1:
        s = '-' + s
    return s

                        
 

class DianRongParser(object):
    def parse(self, itemName, fileName):
        invData = []
        cashFlow = {}
        
     
        with open(fileName) as f:
            for line in f:
                if line.startswith('#'): continue
                if 0==len(line.strip()): continue
                
                item = line.strip().split()
                
    #           print line
                name = item[0]
                ret = float(item[1].replace('%',''))/100
                invDate = datetime.datetime.strptime(item[2],'%Y-%m-%d') 
                principle = float(item[3].replace(',',''))
                unRealized = principle
                nextPayDate = today+relativedelta.relativedelta(months=3) 
                
                r = relativedelta.relativedelta(today,invDate )
                usedMonth = r.months
                
                nextPayAmt = 0
                  
                                
                invData.append([
                                itemName,
                                name,
                                unRealized,
                                ret,
                                nextPayDate,
                                nextPayAmt,  
                                max(0, int(12)-usedMonth )
                                ])
       
                cashFlow[nextPayDate.strftime(dataFormat)] = cashFlow.get(nextPayDate, 0)+ nextPayAmt
                    
        return invData, cashFlow       

class CreditParser(object):
 
  
    def parse(self, itemName, fileName):
        cashFlowCredit={}
          
        with open(fileName) as f:
            for line in f:
                if line.startswith('#'): continue
                if len(line.strip())==0: continue
                item = line.split('\t')
                if item[0].strip()=='信用卡 ':continue
                
                date = int(item[5])
                if date>=int(todayStr[-2:]):
                    nextPayDate = (todayStr[0:6])+"%02d"%(date)
                else:
                    #Next Month Payment
                    nextMonthToday = today+relativedelta.relativedelta(months=1)
                    nextPayDate = (nextMonthToday.strftime(dataFormat))[0:6]+"%02d"%(date)
                
                cashFlowCredit[nextPayDate] = -1*(cashFlowCredit.get(nextPayDate,0)+float(item[1].replace(',','')))
        
        #cashFlowCredit[1]=cashFlowCredit.get(1,0)-40000 #5000 wuxun
        return [],cashFlowCredit
            
    
    


def printSummary(invData, name):
    
    totPrinciple = sum(x[2] for x in invData)
    if totPrinciple==0:
        return [name,totPrinciple, 0,0]
    
    
    totInterst = sum(x[2]*x[3] for x in invData)/totPrinciple
    totDuration = sum(x[2]*x[6] for x in invData)/totPrinciple
    
    
    item = [name,totPrinciple, totInterst,totDuration]
    return item


if __name__ == '__main__':
   
 
    
    invHeader = ['Category', 'Item                            ', 
                 'Amount    ', 'Return%  ', 'NextPayDt', 'NextPayAmt','Duration(Mon)' ]
  
     
    licaiItem = {
            'WeiDaiParser':{'weidai-L':'weidai.txt',
                      'Weidai-w':'weidai-wu.txt'
                      
                      },            
            'DaoKouDaiParser':{'DKD':'daokoudai.txt',
                               'DKD-W':'daokoudai-wu.txt',
                      },
                 
            'LufaxParser':{'Lu-L':'lufax.txt',
                      },     
            
            
            'DianRongParser':{'DR-L':'dianrong.txt',
                      },    
          
#                   
#             'LanTouZiParser':{'LTZ':'lantouzi.txt',
#                       }, 
                 
            'CreditParser':{'Credit-Li':'credit.txt',
                      },     
            
            'CommonParser':{'YangMao':'other.txt',
                            'LTZ':'lantouzi.txt', 
                            
                      },    
                 
                     
            }
            
    
    cashFlowDict = {}
    allInvData = {}
   
    for item in licaiItem:
        itemParser=Parser(eval(item))
        print (item)
        for key in licaiItem[item]:
            itemKey = key
            invData, cashFlow =  itemParser.parse(itemKey,licaiItem[item][key])
            allInvData[itemKey]=(invData)
            cashFlowDict[itemKey]=cashFlow
        
     
    
    print ('-'*100)
    
    formatStr = '%-10s'
    for item in invHeader[1:]:
        formatStr+=("|%"+str(len(item))+"s")
    
    print (formatStr % tuple(invHeader))
    for key in allInvData:
        itemList = allInvData[key]
        for item in itemList:
            print (formatStr % tuple([
                              item[0],
                            item[1].replace(' ','-'),
                            num2cs(item[2]),
                            '%.2f'%(100*item[3]),
                            item[4].strftime(dataFormat),
                            num2cs(item[5]),
                            str(item[6])
                            ]))
    print ('-'*100 )   
    
      
    
    allKeyItem = sorted( cashFlowDict.keys() )
    cashFlowHeader = ['Date   ']+ allKeyItem
    itemFmt = "|%10s"
    dateItemFmt = "%-10s"
    formatStr = dateItemFmt+len(allKeyItem)*itemFmt
    print (formatStr%tuple(cashFlowHeader))
 
    
    total = {}
    for i in range(1,30):
        
        nextPayDate = today+relativedelta.relativedelta(days=i)
        nextPayDateStr = nextPayDate.strftime(dataFormat)
        
        dateIdx = nextPayDate.day 
        
       
        for i in range(len(allKeyItem)):
            key  = cashFlowDict.keys()[i]
            total[key]= cashFlowDict[key].get(nextPayDateStr,0.0)+total.get(key,0)
          
        print (dateItemFmt%nextPayDateStr,end='')
        for key in allKeyItem:
            print  (itemFmt%num2cs(cashFlowDict[key].get(nextPayDateStr,0.0)).strip(),end='')
        print ('\n',end='')
         
    print ( dateItemFmt % 'Total',end=''),
                        
    for key in allKeyItem:
        print (itemFmt % num2cs(total.get(key)),end='')
        
    
    ##################################
    #Inv Summary
    print ('\n'+'-'*100)
    summaryHeader = ['Source', 'Category', 'Principle', 'Return', 'AvgDur(Mon)' ]
    formatStr = "%-10s%10s%12s%10s%14s"
    print (formatStr%tuple(summaryHeader))
    
   
    allItemData = []
    for key in allKeyItem:
        if key=='Credit-Li':continue
        allItemData.append(printSummary(allInvData[key],key))
            

    for item in allItemData:
        print (formatStr%tuple(
                      [item[0].split('-')[0],
                       item[0],
                      num2cs(item[1]),
                      '%.2f%%'%(item[2]*100),
                      '%.1f'%(item[3])
                      ]))
#                        
#     print  formatStr%tuple(
#                       ['Total',
#                       num2cs(sum(x[1] for x in allItemData)),
#                       '--',
#                       '--'
#                       ])
#                        
    
    
    
    
    
    