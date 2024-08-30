# simple request to test the API
import requests

def readKeys(filename):
    # return a list first element is the key the second is the secret key
    f = open(filename, 'r')
    l1 = f.readline()[:-1].split(":")
    l2 = f.readline().split(":")
    return [l1[1], l2[1]]

def main():
    import requests

    url = "https://paper-api.alpaca.markets/v2/account"

    keys = readKeys(".alpacakeys")

    headers = {
          "accept": "application/json",
          "APCA-API-KEY-ID": keys[0],
          "APCA-API-SECRET-KEY": keys[1]
    }

    response = requests.get(url, headers=headers)

    print(response.text)



if __name__ == "__main__":
    main()