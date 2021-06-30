import requests
import time
from datetime import datetime
import json


class CryptoDayBot:
    def __init__(self):
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.params = {
            'start': '1',
            'limit': '100',
            'convert': 'USD'
        }
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '370ed3e1-ab73-4a01-9620-751fc6610856'
        }

    #funzione per creare una lista di criptovalute da coinmarketcap
    def fetchCryptoList(self):
        r = requests.get(url=self.url, headers=self.headers, params=self.params).json()
        return r['data']

    #La criptovaluta con il volume maggiore (in $) delle ultime 24 ore
    def maxVolumeCrypto24h(self, cryptoList):
        volume = 0
        for crypto in cryptoList:
            if crypto['quote']['USD']['volume_24h'] > volume:
                volume = crypto['quote']['USD']['volume_24h']
                maxVolume = crypto['name']
        return maxVolume

    #Le migliori criptovalute (per incremento in percentuale delle ultime 24 ore)
    def best10CryptoForPercentChange24(self, cryptoList):
        #utilizzo una funzione lambda per ordinare una lista di dizionari a seconda di un valore presnte in ciascuno di essi
        swapList = sorted(cryptoList, key=lambda i: i['quote']['USD']['percent_change_24h'], reverse=True)
        best10 = swapList[:10]
        return best10

    #Le peggiori 10 criptovalute (per incremento in percentuale delle ultime 24 ore)
    def worst10CryptoForPercentChange24(self, cryptoList):
        swapList = sorted(cryptoList, key=lambda i: i['quote']['USD']['percent_change_24h'])
        worst10 = swapList[:10]
        return worst10

    #La quantità di denaro necessaria per acquistare una unità di ciascuna delle prime 20 criptovalute
    def oneCoinOfTop20Crypto(self, cryptoList):
        sumTot = 0
        for crypto in cryptoList[:20]:
            sumTot += crypto['quote']['USD']['price']
        return sumTot

    #La quantità di denaro necessaria per acquistare una unità di tutte le criptovalute il cui volume delle ultime 24 ore sia superiore a 76.000.000$
    def buyCryptoVolumePlus76mln(self, cryptoList):
        MIN_VOLUME = 76000000
        sumTot = 0
        for crypto in cryptoList:
            if crypto['quote']['USD']['volume_24h'] > MIN_VOLUME:
                sumTot += crypto['quote']['USD']['price']
        return sumTot

    #La percentuale di guadagno o perdita che avreste realizzato se aveste comprato una unità di ciascuna delle prime 20 criptovalute* il giorno prima (ipotizzando che la classifca non sia cambiata)
    def gainsTop20Crypto(self, cryptoList):

        todayWallet = 0
        yesterdayWallet = 0

        for crypto in cryptoList[:20]:
            todayWallet += crypto['quote']['USD']['price']
            yesterdayWallet += (crypto['quote']['USD']['price'] * 100) / (100 + crypto['quote']['USD']['percent_change_24h'])

        percentGains = (todayWallet - yesterdayWallet) * 100 / yesterdayWallet
        return percentGains

#istanziamento dell'oggetto CryptoDayBot
cryptoDayBot = CryptoDayBot()

#inizio loop infinito
while(1):
    #per dare un nome man mano al file json datetime deve diventare una stringa
    today = datetime.now().strftime("%d-%m-%Y__%H-%M-%S")
    #creazione della lista
    cryptoList = cryptoDayBot.fetchCryptoList()

    #creazione variabile per ciscuna funzione richiesta
    maxVolumeCrypto = cryptoDayBot.maxVolumeCrypto24h(cryptoList)

    best10 = cryptoDayBot.best10CryptoForPercentChange24(cryptoList)

    worst10 = cryptoDayBot.worst10CryptoForPercentChange24(cryptoList)

    oneCoinOfTop20Crypto = cryptoDayBot.oneCoinOfTop20Crypto(cryptoList)

    buyCryptoVolumePlus76mln = cryptoDayBot.buyCryptoVolumePlus76mln(cryptoList)

    gainsTop20Crypto = cryptoDayBot.gainsTop20Crypto(cryptoList)

    #inserimento dei ciascuna variabile dentro un dizionario
    cryptoDict = {

        'maxVolumeCrypto24h': maxVolumeCrypto,

        'best10%Change24h': best10,

        'worst10%Change24h': worst10,

        'oneCoinOfTop20Crypto': oneCoinOfTop20Crypto,

        'buyCryptoVolumePlus76mln': buyCryptoVolumePlus76mln,

        'gainsTop20Crypto24h': gainsTop20Crypto

    }

    #la funzione open crea il file json dal dizionario
    with open(f"{today}.json", "w") as outfile:
        json.dump(cryptoDict, outfile, indent=4)


    #routine
    hour = 24
    minutes = 60
    seconds = 60 * minutes * hour
    time.sleep(seconds)