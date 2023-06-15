import os
import sys
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from ibkr import client
from alg import Algo

client = client.Client()
a  = Algo()

def main():
    
    tick = 0
    pair = 'EURUSD'
    
    while True:
        time.sleep(.25) 
        a.pricePlot(pair, tail = 30, tick = tick, graph= False)
        tick += 1

        if tick % 20 == 0:
            macro = a.macroBandTest(pair)[0]
            print("macro", macro)
            if (macro[2] == 'BUY') or (macro[2] == 'SELL'):
                client.forexOrder(macro)
                
        if tick % a.microDelay(30) == 0:
            micro = a.microBandTest(pair)[0]
            print("micro", micro)
            if (micro[2] == 'BUY') or (micro[2] == 'SELL'):
                client.forexOrder(micro)
            
        
        
        
if __name__ == "__main__":
    main()
