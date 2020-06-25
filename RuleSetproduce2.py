


import pandas as pd
import itertools


def produceRules2():

    MaBuy_list= [0,50,100,150,300]
    angle_list = [2,4,7,10]
    kCount_list = [0,5,10,15,20]
    underK60_list=[0,1]
    k60GoUp_list=[0,1]
    kUp_list = [0,1]


    lowHold_list=[0,1]

    preKamountUp_list=[0,1]


    upHold_list = [0,1]
    amountUp_list =[0,2,3,4,5]


    MaSell_list = [0, 150, 300]
    amountDown_list = [0, 2, 3, 4, 5]
    RSISell_list=[0,70,80]
    macdSell_list=[0,1]



    rule_list = [MaBuy_list,angle_list,kCount_list,underK60_list,k60GoUp_list,
                 kUp_list,lowHold_list,preKamountUp_list,upHold_list,
                 amountUp_list,MaSell_list,amountDown_list,RSISell_list,macdSell_list]

    rule_data = []
    for x in itertools.product(*rule_list):
        rule_data.append(x)
    a = pd.DataFrame(rule_data)
    a.to_csv('ruleSet2.csv')

produceRules2()