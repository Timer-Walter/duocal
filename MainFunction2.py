
import json
import pandas as pd

import IndexCal2
import TradeRules2
import numpy as np
import talib


# buy index: Ma1XMa2Buy,angle,kCount,underK60,k60GoUp,kUp,amountUp,RSIBuy
# sell index: Ma1XMa2Sell,pressureDown,amountDown,LJBL,RSISell

rule_data=np.array(pd.read_csv('ruleSet2.csv'))

# ,"BTC_1min_20200620","BTC_1min_20200621","BTC_1min_20200623"
dataList = ["ETH_1min_20200523","ETH_1min_20200524","ETH_1min_20200525",
            "ETH_1min_20200526","ETH_1min_20200527","ETH_1min_20200528",
            "ETH_1min_20200531","ETH_1min_20200601","ETH_1min_20200602",
            "ETH_1min_20200607","ETH_1min_20200614","ETH_1min_20200615",
            "ETH_1min_20200616","ETH_1min_20200621","ETH_1min_20200623",
            "ETH_1min_20200624","ETH_1min_20200625","ETH_1min_20200626"]


for data in dataList:

    ruleObj ={}
    for rule in rule_data:
        ruleObj[rule[0]]=TradeRules2.rules(rule[1:])


    with open(data+".json", 'r') as load_f:
        kline_1min = json.load(load_f)

    safeAccount = [i for i in range(len(ruleObj))]


    for i in range(500,len(kline_1min) - 120):
        kline = (pd.DataFrame.from_dict(kline_1min[i:i + 120]))[['id', 'close', 'high', 'low', 'open', 'amount']]
        closed = kline['close'].values
        opened = kline['open'].values
        highed = kline['high'].values
        lowed = kline['low'].values
        amounted = kline['amount'].values
        ma5 = talib.SMA(closed, timeperiod=5)

        [maUp_list,maDown_list,amountUp,preKamountUp,amountDown,yangRate,yangKCount,
         rsi_forward,rsi,lowHold,macdSell]=IndexCal2.indexCal(closed,opened,highed,lowed,amounted)
        processAccount = safeAccount.copy()
        for j in processAccount:
            ruleObj[j].updateAccount(closed[-1],lowed[-1])
            if ruleObj[j].account_alive==False:
                safeAccount.remove(j)
                continue
            if max(amountUp,preKamountUp*ruleObj[j].preKamountUp)>=ruleObj[j].amountUp \
                    and lowHold*ruleObj[j].lowHold==0 and yangRate>=ruleObj[j].yangRate \
                    and yangKCount>=ruleObj[j].yangKCount:
                for maUp in maUp_list:
                    if maUp[0]== ruleObj[j].Ma1XMa2Buy and maUp[1]>=ruleObj[j].kCount:
                        ruleObj[j].firstBuy=1
                        ruleObj[j].buyOperation(closed[-1])
                        break

            if ruleObj[j].upHold==1 and ruleObj[j].firstBuy==1:
                if ma5[-1] > ma5[-2] and ma5[-4] > ma5[-3] > ma5[-2] and closed[-1] > opened[-1]:
                    holdPlace = min(lowed[-5:])
                    if holdPlace > ruleObj[j].costPrice * 1.005:
                        ruleObj[j].buyOperation(closed[-1])
                        ruleObj[j].costPrice = holdPlace / 0.995
                        ruleObj[j].firstBuy = 2



            # lowPointLong = min(closed[-1], opened[-1])-lowed[-1]
            # highPointLong = highed[-1]-max(closed[-1], opened[-1])
            # lowPointLongRate = lowPointLong / (highed[-1] - lowed[-1])
            # highPointLongRate = highPointLong/(highed[-1] - lowed[-1])
            # if lowPointLong>30 and lowPointLongRate>0.8 and amounted[-1]/amounted[-2]>3 and underK60==0 and highPointLongRate<0.1 and rsi<30:
            #     ruleObj[j].buyPosition = 1
            #     ruleObj[j].buyOperation(closed[-1])
            # if sdbuy==1:
            #     ruleObj[j].buyPosition = 1
            #     ruleObj[j].buyOperation(closed[-1])
            # if macdBuy==1:
            #     ruleObj[j].buyPosition = 0.5
            #     ruleObj[j].buyOperation(closed[-1])


            if macdSell==1 and ruleObj[j].macdSell==1:
                ruleObj[j].sellOperation(closed[-1])



            if rsi_forward>ruleObj[j].RSISell>0 and rsi_forward>rsi:
                ruleObj[j].sellOperation(closed[-1])

            if (ruleObj[j].Ma1XMa2Sell in maDown_list) and \
                    amountDown>=ruleObj[j].amountDown:
                ruleObj[j].sellOperation(closed[-1])


            if closed[-1]<ruleObj[j].costPrice*0.995:
                ruleObj[j].sellOperation(closed[-1])
            # # # #
            # if closed[-1]>ruleObj[j].costPrice*1.01:
            #     ruleObj[j].sellPosition = 0.8
            #     ruleObj[j].sellOperation(closed[-1])

            # pressureDown = 0
            # if (highed[-2] >= highed[-1]) and (highed[-2] >= highed[-3] >= highed[-4]):
            #     for i in range(5, 60):
            #         if highed[-i] >= highed[-i + 1] >= highed[-i + 2] and highed[-i] >= highed[-i - 1] >= highed[
            #             -i - 2]:
            #             if highed[-2] <= highed[-i]:
            #                 pressureDown = 1
            #             break
            # if pressureDown==1:
            #     ruleObj[j].sellPosition = 0.1
            #     ruleObj[j].sellOperation(closed[-1])
            #
            #
            # if pressureDown==1 and ruleObj[j].pressureDown==1:
            #     ruleObj[j].sellPosition = 0.5
            #     ruleObj[j].sellOperation(closed[-1])
            #
            # if highPointLong>10 and highPointLongRate>0.7:
            #     ruleObj[j].sellPosition = 0.5
            #     ruleObj[j].sellOperation(closed[-1])





        #print(i)

    result = []

    for i in safeAccount:
        [account_money, trade_count] = ruleObj[i].outPut()
        if account_money >= 950:
            result.append([account_money, i])

    result.sort(reverse=True)
    print(result[0])
    a = pd.DataFrame(result)
    a.to_csv(data+'_RulesResult2.csv')

