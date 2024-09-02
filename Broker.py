from Model import Action
import requests
import json

class Broker():
    def __init__(self, key_id, secret_key, url = "https://paper-api.alpaca.markets/v2/orders", \
                 asset="BTC/USD", notional=10):
        self.key_id = key_id
        self.secret_key = secret_key
        self.pos_url = "https://paper-api.alpaca.markets/v2/positions"
        self.url = url
        self.asset = asset
        self.notional = notional # dollar amount to trade
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "APCA-API-KEY-ID": str(key_id),
            "APCA-API-SECRET-KEY": str(secret_key)
        }
        self.buy_payload = {
            "side": "buy",
            "type": "market",
            "time_in_force": "gtc",
            "symbol": asset,
            "notional": notional
        }
        self.sell_payload = {
            "side": "sell",
            "type": "market",
            "time_in_force": "gtc",
            "symbol": asset,
            "notional": notional   
        }
    def performAction(self, action : Action):
        if(action == Action.BUY):
            response = requests.post(self.url, json=self.buy_payload, headers=self.headers)
            return response
        elif(action == Action.SELL):
            response = requests.post(self.url, json=self.sell_payload, headers=self.headers)
            return response
        elif(action == Action.SELL_ALL):
            requests.delete(self.url, headers=self.headers)
            response = requests.get(self.pos_url, headers=self.headers)
            qty = response.json()[0]["qty"]
            sell_payload = dict(self.sell_payload)
            del sell_payload["notional"]
            sell_payload["qty"] = qty
            response = requests.post(self.url, json=sell_payload,headers=self.headers)
            return response
