from enum import Enum

class Action(Enum):
    BUY = 1
    SELL = 2
    NO_ACTION = 3
    SELL_ALL = 4

class Event(Enum):
    UP_OVERSHOOT = 1
    CHANGE_TO_DOWN = 2
    DOWN_OVERSHOOT = 3
    CHANGE_TO_UP = 4
    NO_EVENT = 5

class Model():
    def __init__(self, delta=0.00001, short=False):
        self.extreme = 0
        self.reference = 0
        self.isUp = False
        self.delta = delta
        self.short = short
        self.recentEvent = Event.NO_EVENT

    def recordEvent(self, ask : int, bid : int) -> None:
    # implements the algorithm from the Madrid paper, page 17
        if(self.isUp):
            if bid > self.extreme:
                self.extreme = bid
                if bid > self.reference+self.reference*self.delta:
                    self.reference = self.extreme
                    self.recentEvent = Event.UP_OVERSHOOT
                    return
            elif ask < self.reference-self.reference*self.delta:
                self.extreme = ask
                self.reference = ask
                self.isUp = False
                self.recentEvent = Event.CHANGE_TO_DOWN
                return
        elif(not self.isUp):
            if ask < self.extreme:
                self.extreme = ask
                if ask < self.reference - self.reference*self.delta:
                    self.reference = self.extreme
                    self.recentEvent = Event.DOWN_OVERSHOOT
                    return
            elif (bid > self.reference + self.reference * self.delta):
                self.extreme = bid
                self.refernce = bid
                self.isUp = True
                self.recentEvent = Event.CHANGE_TO_UP
                return
        else:
            self.recentEvent = Event.NO_EVENT
            return
        
    def getAction(self) -> Action:
        if self.recentEvent == Event.NO_EVENT:
            return Action.NO_ACTION
        if(not self.short):
            if self.recentEvent==Event.DOWN_OVERSHOOT or \
               self.recentEvent==Event.CHANGE_TO_UP:
                self.recentEvent = Event.NO_EVENT
                return Action.BUY
            else:
                self.recentEvent = Event.NO_EVENT
                return Action.SELL
        elif(self.short):
            if self.recentEvent==Event.DOWN_OVERSHOOT or \
               self.recentEvent==Event.CHANGE_TO_UP:
                self.recentEvent = Event.NO_EVENT
                return Action.SELL
            else:
                self.recentEvent = Event.NO_EVENT
                return Action.BUY
            
class Log():
    def __init__(self, timestamp : str):
        self.timestamp = timestamp
        self.file = open("logs/log_" + timestamp + ".csv", 'w')
    
    def recordEvent(self, ask : int, bid : int, action : Action) -> None:
        line = f"{ask},{bid},{action.value}\n"
        self.file.write(line)
    