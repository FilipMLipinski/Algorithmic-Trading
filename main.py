# simple request to test the API
import json
import requests
from Model import Model, Action

APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

def readKeys(filename):
    # return a list first element is the key the second is the secret key
    f = open(filename, 'r')
    l1 = f.readline()[:-1].split(":")
    l2 = f.readline().split(":")
    return [l1[1], l2[1]]

def main():
    model = Model()
    btcurl = "https://data.alpaca.markets/v1beta3/crypto/us/latest/quotes?symbols=BTC%2FUSD"
    keys = readKeys(".alpacakeys")
    headers = {
          "accept": "application/json",
          "APCA-API-KEY-ID": keys[0],
          "APCA-API-SECRET-KEY": keys[1]
    }
    while(1):
        response = requests.get(btcurl, headers=headers)
        ask = response.json()['quotes']['BTC/USD']['ap']
        bid = response.json()['quotes']['BTC/USD']['bp']
        model.recordEvent(ask, bid)
        action = model.getAction()
        if(action != Action.NO_ACTION):
            print(model.reference)
            print(action)

if __name__ == "__main__":
    main()