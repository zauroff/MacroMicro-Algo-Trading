from backtesting import Backtest, Strategy
from backtesting.test import SMA
import numpy as np
import yfinance as yf
from decimal import Decimal

hist =yf.download('EURUSD=X', start='2023-06-6', end='2023-06-12', interval= "5m")



class MicroMacro(Strategy):
    
    def init(self):

        
        self.bought = 0
        self.sold = 0
        self.buysig = 0
        self.sellsig = 0
        self.tick = 0
        self.limit = 150
        
        
        
    def next(self):
        self.tick += 1
        self.ma5 = hist['Close'].rolling(5).mean()
        self.ma5 = self.ma5.tail(1).to_list()
        self.ma5 = self.ma5[0]

        
        self.ma10 = hist['Close'].rolling(10).mean()
        self.ma10 = self.ma10.tail(1).to_list()
        self.ma10 = self.ma10[0]

        
        self.ma30 = hist['Close'].rolling(30).mean()
        self.ma30 = self.ma30.tail(1).to_list()
        self.ma30 = self.ma30[0]

        
        self.ma35 = hist['Close'].rolling(35).mean()
        self.ma35 = self.ma35.tail(1).to_list()
        self.ma35 = self.ma35[0]
        
        ma5 =   self.ma5
        ma10 = self.ma10
        ma30 = self.ma30
        ma35 = self.ma35
        
        
        price = self.data.Close[-1]


    
        if self.buysig > 0:
            delayMultiplier = self.buysig
        elif self.sellsig > 0:
            delayMultiplier = self.sellsig
        else:
            delayMultiplier = 1
        
        
        macroDelay = 100 * delayMultiplier
        if macroDelay == 0:
            macroDelay = 1
        

        
        #MACRO
        
        if self.tick % 20 == 0:
            price = float(Decimal(price) + Decimal(.00005)
            if price < ma30 and price < ma35:
                if self.buysig < self.limit:
                    
                    qnty = round((np.mean([ma30, ma35]) - price) * 1000000)
                    self.buysig += 1
                    self.sellsig = 0
                    self.bought += qnty
                    Strategy.buy(self, size = qnty)
                    
            price = float(Decimal(price) - Decimal(.00005))        
            if price > ma30 and price > ma35:
                if self.sellsig < self.limit:
                    
                    if self.bought > 0:
                        self.position.close()
                        return
                    else:
                        qnty = round((price - np.mean([ma30, ma35])) * 1000000)
                    
                    self.sellsig += 1
                    self.buysig = 0
                    Strategy.sell(self, size = qnty)
                
        microDelay = 2 * delayMultiplier
        
        
        #MICRO
        if self.tick % 30 == 0:
            price = float(Decimal(price) + Decimal(.00005))
            if price < ma10 and price < ma5:
                if self.buysig < self.limit:
                    
                    qnty = round((np.mean([ma10, ma5]) - price) * 10000000)
                    self.buysig += 1
                    self.sellsig = 0
                    self.bought += qnty
                    Strategy.buy(self, size = qnty)
                    
                    
            price = float(Decimal(price) - Decimal(.00005))
            if price > ma10 and price > ma5:
                if self.sellsig < self.limit:
                    
                    if self.bought > 0:
                        self.position.close()
                        return
                    else:
                        qnty = round((price - np.mean([ma10, ma5])) * 10000000)
                        
                    self.sellsig += 1
                    self.buysig = 0 
                    Strategy.sell(self, size = qnty)
                    
                
        
bt = Backtest(hist, MicroMacro, cash=10000000, commission=.002)
stats = bt.run()
print(stats)
bt.plot()
        
        


        
     


    