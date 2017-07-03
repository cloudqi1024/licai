#coding=utf-8


print "**"
print "计算贷款月还款额度"
#年利率
myyearrate=0.049
#    计算出月利率，有时银行取整等会照成小数点差距，通常银行都是只入不舍
mymonthrate=myyearrate/12
#还款期数，一年12期
mymonthcount=360

#    总借款额度
myneedmoney=1000000

#等额本息还款
#    月还款额=本金*月利率*(1+月利率)^n/[(1+月利率)^n-1]
#月利率=年利率/12，n表示贷款月数，^n表示n次方，如^360，表示360次方（贷款30年、360月）。
#    注意：计算(1+月利率)^n-1时，要先将括号内的算出来，乘方后再减1。

mytemppow=pow((1+mymonthrate),mymonthcount)
mymonthmoney=myneedmoney*mymonthrate*mytemppow/(mytemppow-1)

print "贷款月还款额度 :%.2f" %(mymonthmoney)


#*******************************************part
print "****************************"

#    递增额度
multiple=100
intvalue=myneedmoney/multiple

#固定收益年化定为8%
yrate=0.08
ymonthrate=yrate/12


#    还款期数+本息利率
mylists=[[36,0.084],[36,0.118],[18,0.11],[12,0.11],[36,0.05],[18,0.05],[12,0.05],[6,0.05]]
for list in mylists:
        xc=list[0]
        xrate=list[1]
        xmonthrate=xrate/12
        for num in range(1,intvalue):
                    mx=num*multiple
                    my=myneedmoney-mx
                    temp1=pow((1+xmonthrate),xc)
                    temp2=mx*xmonthrate*temp1/(temp1-1)
                    temp3=my*ymonthrate*xc
                    temp4=mx/(ymonthrate*xc)
                    #                    print "temp2:%.2f     myneedmoney:%.2f     temp3:%.2f      mx:%.2f" %(temp2,mymonthmoney,temp3,mx)
                    if(temp2>=mymonthmoney and temp3>=mx):
                            print "选择项目"
                            print list
                            print "投资本息:%.2f          投资年化:%.2f 房贷支出:%.2f     每月回款:%.2f     本息期数:%.2f      年化回款:%.2f" %(mx,my,mymonthmoney,temp2,xc,temp3)
                            print "需要的最小年化投资:%.2f ,需要的总资金:%.2f" %(temp4,temp4+mx)
                            print "*******************************************************"
                            break
 