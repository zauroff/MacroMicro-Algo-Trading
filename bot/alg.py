import pandas as pd
import numpy as np
import os, sys
import matplotlib.pyplot as plt
from decimal import Decimal

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from ibkr import client
client = client.Client()




class Algo():

        def __init__(self):
            self.buy_sigs = 0
            self.sell_sigs = 0
            self.limit = 20
            self.inv = 0
        
        def position(self):
            if client.positions():
                return client.positions()[1]
            else:
                return 0

        def live(self, pair):
            return client.forexLive(pair)
        
        def MA5(self, pair):
            hist = client.forexHistorical(pair, '2 D', '1 min')
            hist['MA5'] = hist['close'].rolling(5).mean()
            hist = hist.dropna()
            ma5 = hist['MA5']
            return ma5
        
        
        def MA10(self, pair):
            hist = client.forexHistorical(pair, '2 D', '1 min')
            hist['MA10'] = hist['close'].rolling(10).mean()
            hist = hist.dropna()
            ma10 = hist['MA10']
            return ma10
        
        def MA30(self, pair):
            hist = client.forexHistorical(pair, '2 D', '1 min')
            hist['MA30'] = hist['close'].rolling(30).mean()
            hist = hist.dropna()
            ma30 = hist['MA30']
            return ma30
        
        def MA35(self, pair):
            hist = client.forexHistorical(pair, '2 D', '1 min')
            hist['MA35'] = hist['close'].rolling(35).mean()
            hist = hist.dropna()
            ma35 = hist['MA35']
            return ma35
        
        
        def pricePlot(self, pair, tail,tick, graph:bool): #should be run in a loop         
            if graph == True:
                ma5  =  self.MA5(pair).tail(tail)
                ma10 = self.MA10(pair).tail(tail)
                ma30 = self.MA30(pair).tail(tail)
                ma35 = self.MA35(pair).tail(tail)
                hist = client.forexHistorical(pair, '2 D', '1 min').tail(tail)
                hist = hist['close']
                
                plt.style.use('dark_background')
                plt.ion()
                plt.clf()
                plt.title(f'Tick: {tick}')
                hist.plot(figsize=(5,5))
                ma5.plot()
                ma10.plot()
                ma30.plot()
                ma35.plot()

                plt.legend([f'{pair} Price','MA5','MA10','MA30','MA35'])
                plt.pause(.01)
            
        
        def qnty(self, maX, maY, price, action, size: int):
            
            if action == 'BUY':
                if self.limit == self.sell_sigs and self.position() < 0:
                    return round(-self.position() * .5)
                else:
                    return round((1 - (price/(np.mean([maX,maY])))) * (size * 10000))
            
            if action == 'SELL':
                if self.limit == self.buy_sigs and self.position() > 0:
                    return round(self.position() * .5)
                else:
                    return round((1 - ((np.mean([maX,maY]))/price)) * (size * 10000))
        
        
        def macroBandTest(self, pair):
            order = []
            prices = self.live(pair)
            ask   = prices[1] #buy
            bid   = prices[0] #sell
            
            bid = float(Decimal(bid) - Decimal(.00005))
            ask = float(Decimal(ask) + Decimal(.00005))            
    
            ma30 = self.MA30(pair).tail(1).to_list()
            ma35 = self.MA35(pair).tail(1).to_list()
            ma30 = ma30[0]
            ma35 = ma35[0]


            if ask < ma30 and ask < ma35:  #ask price is below MA's, buy
                if self.buy_sigs < self.limit: 
                    trigger = 'BUY'
                    qnty = self.qnty(ma30,ma35, ask, trigger, 100)
                    self.buy_sigs += 1
                    self.sell_sigs = 0
                    self.inv += qnty
                    order.append([pair, qnty, trigger, ask])
            
            
            if bid > ma30 and bid > ma35:  #bid price is above MA's, sell 
                if self.sell_sigs < self.limit:
                    trigger = 'SELL'
                    qnty = self.qnty(ma30,ma35, bid, trigger, 100)
                    self.sell_sigs += 1
                    self.buy_sigs = 0
                    self.inv -= qnty
                    order.append([pair, qnty, trigger, bid])

            order.append([pair, 0,'void'])
            return order      
        
        def microBandTest(self, pair):
            prices = self.live(pair)
            ask   = prices[1] #buy
            bid   = prices[0] #sell
            order = []
            
            bid = float(Decimal(bid) - Decimal(.00005))
            ask = float(Decimal(ask) + Decimal(.00005))
            
    
            ma10 = self.MA10(pair).tail(1).to_list()
            ma5  = self.MA5(pair).tail(1).to_list()
            ma10 = ma10[0]
            ma5  = ma5[0]
            

            if ask < ma5 and ask < ma10: #ask price is below MA's, Buy
                if self.buy_sigs < self.limit:                                               
                    trigger = 'BUY'
                    qnty = self.qnty(ma5,ma10, ask, trigger, 100)
                    self.buy_sigs += 1
                    self.sell_sigs = 0
                    self.inv += qnty
                    order.append([pair, qnty, trigger, ask])
            
            

            if bid > ma5 and bid > ma10: #bid price is higher than MA's, sell
                if self.sell_sigs < self.limit:
                    trigger = 'SELL'
                    qnty = self.qnty(ma5,ma10, bid, trigger, 100)
                    self.sell_sigs += 1
                    self.buy_sigs = 0
                    self.inv -= qnty
                    order.append([pair, qnty, trigger, bid])
            

            order.append([pair, 0,'void'])
            return order
            
        def microDelay(self, base_delay: int):
            if self.buy_sigs > 0:
                sigs = self.buy_sigs
            elif self.sell_sigs > 0:
                sigs = self.sell_sigs
            else:
                return base_delay
            
            return base_delay * sigs
                
        