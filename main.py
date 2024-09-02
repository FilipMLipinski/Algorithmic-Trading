# simple request to test the API
import json
import requests
from Model import Model, Action, Log
from Broker import Broker
import datetime

APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

def readKeys(filename):
    # return a list first element is the key the second is the secret key
    f = open(filename, 'r')
    l1 = f.readline()[:-1].split(":")
    l2 = f.readline().split(":")
    return [l1[1], l2[1]]

def main():
    model = Model()
    log = Log(str(datetime.datetime.now().month) + "_" + \
              str(datetime.datetime.now().day) + "_" + \
              str(datetime.datetime.now().hour) + "_" +  
              str(datetime.datetime.now().minute))
    btcurl = "https://data.alpaca.markets/v1beta3/crypto/us/latest/quotes?symbols=BTC%2FUSD"
    keys = readKeys(".alpacakeys")
    broker = Broker(keys[0], keys[1])
    infoHeaders = {
          "accept": "application/json",
          "APCA-API-KEY-ID": keys[0],
          "APCA-API-SECRET-KEY": keys[1]
    }
    try:
        while(1):
            response = requests.get(btcurl, headers=infoHeaders)
            ask = response.json()['quotes']['BTC/USD']['ap']
            bid = response.json()['quotes']['BTC/USD']['bp']
            model.recordEvent(ask, bid)
            action = model.getAction()
            if(action != Action.NO_ACTION):
                broker_response = broker.performAction(action)
                print(model.reference)
                print(action)
                print(broker_response.text)
            log.recordEvent(ask, bid, action)
    except KeyboardInterrupt:
        broker_response = broker.performAction(Action.SELL_ALL)
        print(broker_response.text)


if __name__ == "__main__":
    main()