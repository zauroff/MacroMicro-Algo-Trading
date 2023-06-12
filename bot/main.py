import os
import sys

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
        a.pricePlot(pair, tail = 30, tick = tick, graph= True)
        tick += 1
        
        if tick % 200 == 0:
            print(macro)
            macro = a.macroBandTest(pair)[0]
            
            if (macro[2] == 'BUY') or (macro[2] == 'SELL'):
                client.forexOrder(macro)
                
        if tick % a.microDelay(10) == 0:
            micro = a.microBandTest(pair)[0]
            print(micro)
            if (micro[2] == 'BUY') or (micro[2] == 'SELL'):
                client.forexOrder(micro)
            
        
        
        
if __name__ == "__main__":
    main()
