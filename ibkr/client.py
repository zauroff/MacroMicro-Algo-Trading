from ib_insync import *
import pandas as pd


ib = IB()
ib.connect('127.0.0.1', 7497, clientId=2)


class Client():
    
    
        def __init__(self):
            self.portfolio = ib.positions
    
        def forexHistorical(self, pair: str, duration: str, interval: str): #data presented in 30 sec increments within 1 day
            contract = Forex(pair)
            data = ib.reqHistoricalData(
                contract,
                endDateTime='',
                durationStr=duration,
                barSizeSetting=interval,
                whatToShow= 'MIDPOINT',
                useRTH=True
            )
            df = pd.DataFrame(data)
            return df

        def forexLive(self, pair: str): #get current bid and ask prices for pair
            contract = Forex(pair)
            reqData = ib.reqMktData(contract, '', False, False)
            data = ib.ticker(contract)
            ib.sleep(1)
            return [data.bid, data.ask]
    
        def positions(self):
            for pos in self.portfolio():
                return ([pos.contract.symbol, pos.position])
        
        def forexOrder(self, order_array: list):
            pair   = order_array[0]
            qnty   = order_array[1]
            action = order_array[2]
            price  = order_array[3]
            
            contract = Forex(pair)
            order = MarketOrder(action, qnty)
            ib.qualifyContracts(contract)
            
            trade = ib.placeOrder(contract, order)
            
        def cancelOrder(self, order):
             ib.sleep(5)
             ib.cancelOrder(order)
             print('Canceled')
        






