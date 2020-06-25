

import talib

def indexCal(closed,opened,highed,lowed,amounted):

    ma5 = talib.SMA(closed, timeperiod=5)
    ma10 = talib.SMA(closed, timeperiod=10)
    ma20 = talib.SMA(closed, timeperiod=20)
    ma30 = talib.SMA(closed, timeperiod=30)
    ma60 = talib.SMA(closed, timeperiod=60)
    rsi =talib.RSI(closed, timeperiod=14)
    macd,signal,hist = talib.MACD(closed, fastperiod=12, slowperiod=26, signalperiod=9)

    #5,10,20,30,60 hashed
    maCal_list=[[ma5,ma10,50],[ma5,ma20,100],[ma5,ma30,150],[ma5,ma60,300]]

    maUp_list =[]
    maDown_list = [0]
    for [m1,m2,n] in maCal_list:
        if m1[-1] > m2[-1] and m1[-2] < m2[-2]:
            angle = ((m1[-1]-m1[-2])/m1[-2]+(m1[-2]-m1[-3])/m1[-3])*10000
            kCount = 1
            for i in range(3, 30):
                if (m1[-i] > m2[-i]):break
                else: kCount+=1
            maUp_list.append([n,angle,kCount])

        if (n==150 or n==300) and m1[-1] < m2[-1] and m1[-2] > m2[-2]:
            maDown_list.append(n)



    #0 is satisfied ,1 is not
    underK60 = 0
    if closed[-1]>ma60[-1]:underK60 = 1

    k60GoUp = 0
    a = [ma60[-3], ma60[-4], ma60[-5]]
    if a != sorted(a, reverse=True):
        k60GoUp = 1

    kUp = 0
    if closed[-1]<opened[-1]:kUp = 1

    amountUp = 0
    preKamountUp = 0
    amountDown=0

    if kUp==0: amountUp = amounted[-1]/amounted[-2]
    else:amountDown = amounted[-1]/amounted[-2]
    if closed[-2]>opened[-2]:preKamountUp= amounted[-2]/amounted[-3]


    lowPlace1 = 0
    lowIndex1 = 0
    lowPlace2 = 0
    lowIndex2 = 0
    lowPlace3 = 0
    for i in range(1, 10):
        if ma5[-i] > ma5[-i + 1] > ma5[-i + 2] and ma5[-i] > ma5[-i - 1] > ma5[-i - 2]:
            lowPlace1 = ma5[-i]
            lowIndex1 = i
            break
    if lowIndex1 > 0:
        for i in range(lowIndex1 + 2, 50):
            if ma5[-i] > ma5[-i + 1] > ma5[-i + 2] and ma5[-i] > ma5[-i - 1] > ma5[-i - 2]:
                lowPlace2 = ma5[-i]
                lowIndex2 = i
                break
    if lowIndex2 > 0:
        for i in range(lowIndex2 + 2, 60):
            if ma5[-i] > ma5[-i + 1] > ma5[-i + 2] and ma5[-i] > ma5[-i - 1] > ma5[-i - 2]:
                lowPlace3 = ma5[-i]
                break

    if lowPlace1 < lowPlace2:
        lowHold =1
    else:lowHold=0


    macdSell = 0
    if macd[-1] < signal[-1] and macd[-2] > signal[-2]:
        for i in range(1,6):
            highPointLong = highed[-i] - max(closed[-i], opened[-i])
            highPointLongRate = highPointLong / (highed[-i] - lowed[-i])
            if highPointLong>15 and highPointLongRate>0.6 and rsi[-i]>70:
                macdSell = 1
                break


    return [maUp_list,maDown_list,underK60,k60GoUp,kUp,amountUp,preKamountUp,
            amountDown,rsi[-2],rsi[-1],lowHold,macdSell]











#
#
# import json
# import pandas as pd
#
# testData = ["kline_1min_20200517_2000.json"]
# for data in testData:
#     with open(data, 'r') as load_f:
#         kline_1min = json.load(load_f)
#
#
#     for i in range(len(kline_1min)-120):
#         kline = (pd.DataFrame.from_dict(kline_1min[i:i+120]))[['id', 'close', 'high', 'low', 'open','amount']]
#         closed = kline['close'].values
#         indexCal(kline)

