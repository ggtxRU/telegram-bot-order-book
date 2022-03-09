"""Класс, принимающий на вход итоговый список котировок, форматирует его в два списка с покупками/продажами"""
class Result():
    def __init__(self, data):
        self.bids = []
        self.asks = []
        for d in data:
            if "Покупки" in d:
                self.bids.append("Покупают:")
                for dd in d[:-2]:
                    self.bids.append(dd)
                    
        else: 
            if "Продажи" in d:
                    self.asks.append("Продают:")
                    for dd in d[:-2]:
                        self.asks.append(dd)
                                
    def get_bids(self):
        return self.bids
    def get_asks(self):
        return self.asks
