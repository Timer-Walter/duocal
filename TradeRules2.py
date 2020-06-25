

class rules:


    def __init__(self,rule):
        self.Ma1XMa2Buy = rule[0]
        self.angle = rule[1]
        self.kCount = rule[2]
        self.underK60 = rule[3]
        self.k60GoUp = rule[4]
        self.kUp = rule[5]
        self.lowHold = rule[6]
        self.preKamountUp = rule[7]
        self.upHold= rule[8]
        self.amountUp = rule[9]
        self.Ma1XMa2Sell = rule[10]
        self.amountDown = rule[11]
        self.RSISell = rule[12]
        self.macdSell = rule[13]
        self.rate = 10
        self.margin_available = 1000
        self.margin_frozen = 0
        self.volume = 0
        self.price = 0
        self.costPrice =0
        self.firstBuy = 0
        self.tradeCount = 0
        self.account_alive = True
        self.buyPosition = 0.6
        self.sellPosition = 1



    def updateAccount(self,closedPrice,lowedPrice):
        if (self.margin_available + self.margin_frozen +
            (lowedPrice -self.price) * self.volume) <= 800:
            self.account_alive = False
        self.margin_available += (closedPrice - self.price) * self.volume
        self.price = closedPrice


    def buyOperation(self,closedPrice):
        buyPrice = closedPrice * 1.001
        if self.margin_available > 0 and self.buyPosition > 0:
            margin_available_use = self.margin_available * self.buyPosition * self.rate * (1 - 0.0003)
            volume_add = margin_available_use / buyPrice
            self.volume += volume_add
            self.margin_frozen += self.margin_available * self.buyPosition
            self.margin_available -= self.margin_available * self.buyPosition
            self.tradeCount +=1
            self.costPrice = closedPrice

    def sellOperation(self,closedPrice):
        if self.volume > 0 and self.sellPosition > 0:
            self.margin_available += self.margin_frozen * self.sellPosition
            self.margin_frozen -= self.margin_frozen * self.sellPosition
            self.margin_available -= self.volume * self.sellPosition * closedPrice * 0.001
            self.volume -= self.volume * self.sellPosition
            self.tradeCount +=1
            if self.sellPosition==1:
                self.costPrice=0
                self.firstBuy=0


    def outPut(self):
        account_money = 0
        trade_count = 0
        if self.account_alive==True:
            account_money = self.margin_available + self.margin_frozen
            trade_count = self.tradeCount
        return [account_money,trade_count]




