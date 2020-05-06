from time import sleep
from sys import exit
import time
import datetime
import json
import alpaca_trade_api as tradeapi
import requests
import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("Alpaca")

def setup():
    # Prompt user for asset selection
    global assets
    global threshold
    global configcheck
    global config
    global assetnum

    with open('alpaca/config.json') as json_file:
        config = json.load(json_file)
        configcheck = config['configcheck']

    if configcheck != 'configured':
        assets = {}

        assetnum = input('Number of Assets in the Portfolio:')
        assetnum = int(assetnum)
        for x in range(0, assetnum):
            x = str(x + 1)
            assets["asset{0}".format(x)] = input('Asset' + " " + x + ':')
        threshold = input("Algorithm Threshold= ")
        threshold = float(threshold)
        threshold = (.01 * threshold)
        API_KEY = input('API KEY:')
        API_SECRET = input('API SECRET:')
        SITE = input('Live or Paper trading:')
        SITE = SITE.upper()
        ss = False
        while ss is False:
            if SITE == 'PAPER':
                SITE = 'https://paper-api.alpaca.markets'
                ss = True
            if SITE == 'LIVE':
                SITE = 'https://api.alpaca.markets'
                ss = True
            else:
                print('Please check your spelling and re-enter, Live or Paper:')
                pass
        configcheck = 'configured'
        configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum,
                         'API_KEY': API_KEY, 'API_SECRET': API_SECRET, 'SITE': SITE}
        with open('alpaca/config.json', 'w') as outfile:
            json.dump(configuration, outfile)

    else:
        reconfig = input('Would you like to reconfigure?  ')
        if reconfig == 'yes':
            assets = {}

            assetnum = input('Number of Assets in the Portfolio:')
            assetnum = int(assetnum)
            for x in range(0, assetnum):
                x = str(x + 1)
                assets["asset{0}".format(x)] = input('Asset' + " " + x + ':')
            threshold = input("Algorithm Threshold= ")
            threshold = float(threshold)
            threshold = (.01 * threshold)
            API_KEY = input('API KEY:')
            API_SECRET = input('API SECRET:')
            SITE = input('Live or Paper trading:')
            SITE = SITE.upper()
            ss = False
            while ss is False:
                if SITE == 'PAPER':
                    SITE = 'https://paper-api.alpaca.markets'
                    ss = True
                if SITE == 'LIVE':
                    SITE = 'https://api.alpaca.markets'
                    ss = True
                else:
                    print('Please check your spelling and re-enter, Live or Paper:')
                    pass
            configcheck = 'configured'
            configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum,
                             'API_KEY': API_KEY, 'API_SECRET': API_SECRET, 'SITE': SITE}
            with open('alpaca/config.json', 'w') as outfile:
                json.dump(configuration, outfile)

        else:
            assetnum = config['assetnum']
            assetnum = int(assetnum)
            assets = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                assets["asset{0}".format(x)] = config['assets']["asset{0}".format(x)]
            API_KEY = config['API_KEY']
            API_SECRET = config['API_SECRET']
            SITE = config['SITE']
            threshold = config['threshold']
            configcheck = 'configured'
            configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum,
                             'API_KEY': API_KEY, 'API_SECRET': API_SECRET, 'SITE': SITE}
            with open('alpaca/config.json', 'w') as outfile:
                json.dump(configuration, outfile)


def balances():
    # Pull  balance for each selected asset
    global cash_balance

    # Balance USD
    cash_balance = alpaca.get_account().cash
    cash_balance = float(cash_balance)
    # Get Balances of each previously entered asset
    balance = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        attempt = False
        while attempt is False:
            try:
                balance["balance_asset{0}".format(x)] = float(alpaca.get_position(assets[str('asset' + x)]).qty)
                balance["balance_asset{0}".format(x)] = round(balance["balance_asset{0}".format(x)])
                attempt = True
                time.sleep(.5)
            except ConnectionError:
                time.sleep(5)
                pass
            except requests.exceptions.HTTPError:
                time.sleep(5)
                pass
            except requests.exceptions.ConnectionError:
                time.sleep(5)
                pass
            except KeyError:
                balance["balance_asset{0}".format(x)] = 0
                attempt = True
                time.sleep(.1)
            except tradeapi.rest.APIError as e :
                balance["balance_asset{0}".format(x)] = 0
                print('asset ' + str(x) + ' ' + str(balance["balance_asset{0}".format(x)]))
                attempt = True
                time.sleep(.5)




    balance.update({'cash_balance': cash_balance})
    # save balances to json
    with open('alpaca/balance.json', 'w') as outfile:
        json.dump(balance, outfile)
        time.sleep(.5)


def prices():
    global price
    # Grabs prices from Polygon API

    price = {}

    for x in range(0, assetnum):
        x = str(x + 1)
        attempt = False
        while attempt is False:
            try:
                price["price_asset{0}".format(x)] = float(alpaca.polygon.last_trade(assets["asset{0}".format(x)]).price)
                print('asset ' + str(x) + ' ' + str(price["price_asset{0}".format(x)]))
                time.sleep(.5)
                attempt = True
            except ConnectionError:
                time.sleep(1)
                pass
            except requests.exceptions.ConnectionError:
                time.sleep(1)
                pass
            except requests.exceptions.HTTPError:
                time.sleep(1)
                pass
            except:
                time.sleep(1)
                pass

    # saves to json
    with open('alpaca/prices.json', 'w') as outfile:
        json.dump(price, outfile)


def usd_value():
    # Calculates USD value of positions
    global usd
    global total_usd

    with open('alpaca/balance.json') as json_file:
        balance = json.load(json_file)

    with open('alpaca/prices.json') as json_file:
        price = json.load(json_file)

    usd = {}

    for x in range(0, assetnum):
        x = str(x + 1)
        usd["usd_asset{0}".format(x)] = float(balance["balance_asset{0}".format(x)] * price["price_asset{0}".format(x)])

    usd_assets = 0
    for x in range(0, assetnum):
        x = str(x + 1)
        usd_assets = usd_assets + usd["usd_asset{0}".format(x)]

    total_usd = (usd_assets + cash_balance)


def deviation():
    # Calculates current % of portfolio and deviation from baseline
    global dev
    # % of portfolio, current%
    current = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        current["current_asset{0}".format(x)] = float(usd["usd_asset{0}".format(x)] / total_usd)
    # deviation from allocation, as a function of the allocation (allowing for infinite portfolio size scaling)
    dev = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        dev["dev_asset{0}".format(x)] = (current["current_asset"+x] - allocation)
        dev["dev_asset{0}".format(x)] = (dev["dev_asset{0}".format(x)] / allocation)
        dev["dev_asset{0}".format(x)] = float(dev["dev_asset{0}".format(x)])


def sell_order(asset, sell_asset):
    # Sell order logic
    sell_asset = round(sell_asset)
    market = str(alpaca.get_clock().is_open)
    try:
        if market == 'True':
            print("Selling" + " " + str(sell_asset) + " " + "of" + " " + str(asset))
            alpaca.submit_order(
                symbol=asset,
                qty=sell_asset,
                side='sell',
                type='market',
                time_in_force='gtc')
    except Exception as e:
        print(e)
        pass

def buy_order(asset, buy_asset):
    # Buy order logic
    buy_asset = round(buy_asset)
    market = str(alpaca.get_clock().is_open)
    try:
        if market == 'True':
            print("Buying" + " " + str(buy_asset) + " " + "of" + " " + str(asset))
            alpaca.submit_order(
                symbol=asset,
                qty=buy_asset,
                side='buy',
                type='market',
                time_in_force='gtc')
    except Exception as e:
        print(e)
        pass

    # MAIN

with open('alpaca/config.json') as json_file:
    config = json.load(json_file)
    configcheck = config['configcheck']

with open('alpaca/initial.json') as json_file:
    initial = json.load(json_file)
    initialcheck = initial['initialcheck']


setup()

API_KEY = config['API_KEY']
API_SECRET = config['API_SECRET']
SITE = config['SITE']

alpaca = tradeapi.REST(API_KEY, API_SECRET, SITE, 'v2')

allocation = (.999 / assetnum)

if initialcheck != 'done':
    initial = {}
    balances()
    with open('alpaca/balance.json') as json_file:
        balance = json.load(json_file)
    for x in range(0, assetnum):
        x = str(x + 1)
        initial["initial_balance_asset{0}".format(x)] = float(balance["balance_asset{0}".format(x)])
    initialcheck = 'done'
    count = 0
    data = {'initial': initial,
            'initialcheck': initialcheck}
    data2 = {'count': count}

    with open('alpaca/count.json', 'w') as outfile:
        json.dump(data2, outfile)

    with open('alpaca/initial.json', 'w') as outfile:
        json.dump(data, outfile)

else:
    with open('alpaca/count.json') as json_file:
        counts = json.load(json_file)
    count = int(counts['count'])

while count < 99999:

    balances()

    prices()
    with open('alpaca/prices.json') as json_file:
        price = json.load(json_file)
    with open('alpaca/balance.json') as json_file:
        balance = json.load(json_file)
    usd_value()

    deviation()

    # print date and asset deviations

    print(datetime.datetime.now().time())
    print('Portfolio Value:' + " " + " " + str(total_usd) + " " + 'USD')

    for x in range(0, assetnum):
        x = str(x + 1)
        print(
            "Asset: " + assets["asset{0}".format(x)] + " :::: " + "Current Variation: " + str(dev["dev_asset{0}".format(x)] * 100) + "%")

    # Sell order trade trigger
    for x in range(0, assetnum):
        x = str(x + 1)
        if dev["dev_asset{0}".format(x)] >= config['threshold']:
            # Calculate # of shares to sell
            dif = {}
            sell = {}
            goal_allocation = total_usd * allocation
            for x in range(0, assetnum):
                x = str(x + 1)
                dif["dif_asset{0}".format(x)] = usd["usd_asset{0}".format(x)] - goal_allocation
                sell["sell_asset{0}".format(x)] = dif["dif_asset{0}".format(x)] / price['price_asset{0}'.format(x)]
                sell["sell_asset{0}".format(x)] = round(sell["sell_asset{0}".format(x)])

                # Sell order API call
                if sell["sell_asset{0}".format(x)] > 0:
                    sell_order(assets["asset{0}".format(x)], sell["sell_asset{0}".format(x)])
            for x in range(0, assetnum):
                x = str(x + 1)
                if sell["sell_asset{0}".format(x)] < 0:
                    sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                    buy_order(assets["asset{0}".format(x)], sell["sell_asset{0}".format(x)])
            balances()
            prices()
            usd_value()
            deviation()
    # Buy order trade trigger
    negative_threshold = (-1 * config['threshold'])
    for x in range(0, assetnum):
        x = str(x + 1)
        if dev["dev_asset{0}".format(x)] <= negative_threshold:
            dif = {}
            buy = {}
            goal_allocation = total_usd * allocation

            for x in range(0, assetnum):
                x = str(x + 1)
                dif["dif_asset{0}".format(x)] = usd["usd_asset{0}".format(x)] - goal_allocation
                buy["buy_asset{0}".format(x)] = dif["dif_asset{0}".format(x)] / price['price_asset{0}'.format(x)]
                buy["buy_asset{0}".format(x)] = round(-1 * buy["buy_asset{0}".format(x)])

                # Buy order API call
                if buy["buy_asset{0}".format(x)] < 0:
                    sellasset = (-1 * buy["buy_asset{0}".format(x)])
                    sell_order(assets["asset{0}".format(x)], sellasset)
            for x in range(0, assetnum):
                x = str(x + 1)
                if buy["buy_asset{0}".format(x)] > 0:
                    buy_order(assets["asset{0}".format(x)], buy["buy_asset{0}".format(x)])
            balances()
            prices()
            usd_value()
            deviation()

    count = count + 1
    data3 = {'count': count}
    with open('alpaca/count.json', 'w') as outfile:
        json.dump(data3, outfile)
    time.sleep(60)
