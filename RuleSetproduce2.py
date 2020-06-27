


import pandas as pd
import itertools


def produceRules2():

    MaBuy_list = [50, 100, 150, 200, 300, 450, 600]
    kCount_list = [5,10,20,30]
    amountUp_list = [2,3,4,7,10,15]
    yangRate_list = [0,0.7,0.8,0.9]
    yangKCount_list = [0,3,4,5]

 
    lowHold_list=[0,1]
 
    preKamountUp_list = [0,1]

  
    upHold_list = [0,1]


  
    MaSell_list = [100,150,300]
    amountDown_list = [0,2, 3, 5, 8]
    RSISell_list=[0,70,80]
    macdSell_list=[0,1]



    rule_list = [MaBuy_list,kCount_list,amountUp_list,yangRate_list,yangKCount_list,
                 lowHold_list,preKamountUp_list,upHold_list,
                 MaSell_list,amountDown_list,RSISell_list,macdSell_list]

    rule_data = []
    for x in itertools.product(*rule_list):
        rule_data.append(x)
    a = pd.DataFrame(rule_data)
    a.to_csv('ruleSet2.csv')

produceRules2()