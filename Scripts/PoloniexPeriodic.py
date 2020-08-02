import time
import datetime
import math
import json
import requests
from poloniex import Poloniex
import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("Poloniex")


def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


def setup():
    # Prompt user for asset selection
    global assets
    global threshold
    global configcheck
    global config
    global assetnum
    global stablecoin
    global symbol

    with open('poloniex/config.json') as json_file:
        config = json.load(json_file)
        configcheck = config['configcheck']

    if configcheck != 'configured':
        assets = {}

        assetnum = input('Number of Assets in the Portfolio:')
        assetnum = int(assetnum)
        stablecoin = input('What currency would you like to trade against: ')
        stablecoin = stablecoin.upper()
        for x in range(0, assetnum):
            x = str(x + 1)
            assets["asset{0}".format(x)] = input('Asset' + " " + x + ':')
            assets["asset{0}".format(x)] = assets["asset{0}".format(x)].upper()

        symbol = {}
        for x in range(0, assetnum):
            x = str(x + 1)
            symbol["symbol_asset{0}".format(x)] = str(stablecoin + '_' + assets["asset{0}".format(x)])

        configcheck = 'configured'

        algorithm = input('Threshold or Periodic: ').upper()

        if algorithm == 'THRESHOLD':
            threshold = input("Algorithm Threshold= ")
            threshold = float(threshold)
            threshold = (.01 * threshold)
            API_KEY = input('API KEY:')
            API_KEY = str(API_KEY)
            API_SECRET = input('API SECRET:')
            API_SECRET = str(API_SECRET)

            print("Initializing...")

            configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum,
                             'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY, 'API_SECRET': API_SECRET,
                             'algorithm': algorithm}
            with open('kucoin/config.json', 'w') as outfile:
                json.dump(configuration, outfile)
        if algorithm == 'PERIODIC':
            period = input('Hourly, Daily, or Weekly: ').upper()
            API_KEY = input('API KEY:')
            API_KEY = str(API_KEY)
            API_SECRET = input('API SECRET:')
            API_SECRET = str(API_SECRET)

            print("Initializing...")

            configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                             'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY, 'API_SECRET': API_SECRET,
                             'algorithm': algorithm}
            with open('kucoin/config.json', 'w') as outfile:
                json.dump(configuration, outfile)
        if str(algorithm) != 'THRESHOLD' and str(algorithm) != 'PERIODIC':
            print('Please check the spelling of' + " " + algorithm + ", and restart/retry.")
            time.sleep(60)


    else:
        reconfig = input('Would you like to reconfigure?  ')
        if reconfig == 'yes':
            assets = {}
            API_KEY = input('API KEY:')
            API_KEY = str(API_KEY)
            API_SECRET = input('API SECRET:')
            API_SECRET = str(API_SECRET)
            assetnum = input('Number of Assets in the Portfolio:')
            assetnum = int(assetnum)
            stablecoin = input('What currency would you like to trade against: ')
            stablecoin = stablecoin.upper()
            for x in range(0, assetnum):
                x = str(x + 1)
                assets["asset{0}".format(x)] = input('Asset' + " " + x + ':')
                assets["asset{0}".format(x)] = assets["asset{0}".format(x)].upper()

            symbol = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                symbol["symbol_asset{0}".format(x)] = str(stablecoin + '_' + assets["asset{0}".format(x)])

            print("Loading... This may take a few seconds.")

            client = Poloniex(API_KEY, API_SECRET)

            old_cash = client.returnBalances()[stablecoin]
            old_cash = float(old_cash)
            # Get Balances of each previously entered asset
            new_balance = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                try:
                    new_balance["balance_asset{0}".format(x)] = client.returnBalances()[assets[str('asset' + x)]]
                except KeyError:
                    new_balance["balance_asset{0}".format(x)] = 0
                except ConnectionError:
                    time.sleep(3)
                    new_balance["balance_asset{0}".format(x)] = client.returnBalances()[assets[str('asset' + x)]]
                time.sleep(.15)


            old = {}

            for x in range(0, assetnum):
                x = str(x + 1)
                try:
                    old['old_asset{0}'.format(x)] = new_balance['balance_asset{0}'.format(x)]
                except:
                    pass

            olddata = {'old': old, 'old_cash': old_cash}

            with open('poloniex/old.json', 'w') as outfile:
                json.dump(olddata, outfile)

            configcheck = 'configured'

            algorithm = input('Threshold or Periodic: ').upper()

            if algorithm == 'THRESHOLD':
                threshold = input("Algorithm Threshold= ")
                threshold = float(threshold)
                threshold = (.01 * threshold)

                print("Initializing...")

                configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck,
                                 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'algorithm': algorithm}
                with open('kucoin/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)
            if algorithm == 'PERIODIC':
                period = input('Hourly, Daily, or Weekly: ').upper()

                print("Initializing...")

                configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'algorithm': algorithm}
                with open('kucoin/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)
            if str(algorithm) != 'THRESHOLD' and str(algorithm) != 'PERIODIC':
                print('Please check the spelling of' + " " + algorithm + ", and restart/retry.")
                time.sleep(60)


        else:
            assetnum = config['assetnum']
            assetnum = int(assetnum)
            assets = {}
            API_KEY = config['API_KEY']
            API_SECRET = config['API_SECRET']

            for x in range(0, assetnum):
                x = str(x + 1)
                assets["asset{0}".format(x)] = config['assets']["asset{0}".format(x)]
                assets["asset{0}".format(x)] = assets["asset{0}".format(x)].upper()

            stablecoin = config['stablecoin']
            stablecoin = stablecoin.upper()
            symbol = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                symbol["symbol_asset{0}".format(x)] = str(stablecoin + '_' + config['assets']["asset{0}".format(x)])

            configcheck = 'configured'

            algorithm = config['algorithm']

            if algorithm == 'THRESHOLD':
                threshold = config['threshold']

                print("Initializing...")

                configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck,
                                 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'algorithm': algorithm}
                with open('kucoin/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)
            if algorithm == 'PERIODIC':
                period = config['period']

                print("Initializing...")

                configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'algorithm': algorithm}
                with open('kucoin/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)


def balances():
    # Pull  balance for each selected asset
    global cash_balance
    global balance
    # Balance USD
    attempt = False
    while attempt is False:
        try:
            cash_balance = client.returnBalances()[stablecoin]
            cash_balance = float(cash_balance)
            attempt = True
        except ConnectionError or OSError:
            time.sleep(3)
            pass
        except requests.exceptions.HTTPError as e:
            time.sleep(3)
            print(e)
            pass
    # Get Balances of each previously entered asset
    balance = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        try:
            balance["balance_asset{0}".format(x)] = client.returnBalances()[assets[str('asset' + x)]]
        except KeyError:
            balance["balance_asset{0}".format(x)] = 0
        except ConnectionError or OSError:
            time.sleep(3)
            balance["balance_asset{0}".format(x)] = client.returnBalances()[assets[str('asset' + x)]]
        except requests.exceptions.HTTPError as e:
            time.sleep(3)
            print(e)
            balance["balance_asset{0}".format(x)] = client.returnBalances()[assets[str('asset' + x)]]
        time.sleep(.15)
    # save balances to json
    balance.update({'cash_balance': cash_balance})
    with open('poloniex/balance.json', 'w') as outfile:
        json.dump(balance, outfile)


def prices():
    # Grabs prices from Poloniex
    global price
    price = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        attempt = False
        while attempt is False:
            try:
                price["price_asset{0}".format(x)] = float(client.returnTicker()[symbol["symbol_asset{0}".format(x)]]['last'])
                attempt = True
            except ConnectionError or OSError:
                time.sleep(3)
                pass
            except requests.exceptions.HTTPError:
                time.sleep(3)
                pass
        time.sleep(.1)
    # saves to json
    with open('poloniex/prices.json', 'w') as outfile:
        json.dump(price, outfile)


def usd_value():
    # Calculates USD value of positions
    global usd
    global total_usd

    with open('poloniex/balance.json') as json_file:
        balance = json.load(json_file)

    with open('poloniex/prices.json') as json_file:
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


def sell_order(asset, sell_asset, current_price):

    sell_asset = truncate(sell_asset, 4)
    value = float(client.returnTicker()[asset]['last']) * sell_asset
    if value >= 10:
        print("Selling" + " " + str(sell_asset) + " " + "of" + " " + str(asset))
        current_price = (current_price * .8)
        client.sell(currencyPair=asset, rate=current_price, amount=sell_asset, fillOrKill=None, immediateOrCancel=None, postOnly=None)


def buy_order(asset, buy_asset, current_price):

    buy_asset = truncate(buy_asset, 4)
    value = float(client.returnTicker()[asset]['last']) * buy_asset
    if value >= 10:
        print("Buying" + " " + str(buy_asset) + " " + "of" + " " + str(asset))
        current_price = current_price * 1.5
        client.buy(currencyPair=asset, rate=current_price, amount=buy_asset, fillOrKill=None, immediateOrCancel=None, postOnly=None)


# MAIN


setup()

with open('poloniex/config.json') as json_file:
    config = json.load(json_file)

api_key = config['API_KEY']
api_secret = config['API_SECRET']

client = Poloniex(api_key, api_secret)

allocation = (.99 / assetnum)

with open('poloniex/initial.json') as json_file:
    initial = json.load(json_file)
    initialcheck = initial['initialcheck']

if initialcheck != 'done':
    initial = {}
    balances()
    with open('poloniex/balance.json') as json_file:
        balance = json.load(json_file)
    for x in range(0, assetnum):
        x = str(x + 1)
        initial["initial_balance_asset{0}".format(x)] = float(balance["balance_asset{0}".format(x)])
    initialcheck = 'done'
    count = 0
    data = {'initial': initial,
            'initialcheck': initialcheck,
            'initialcheck2': ""}
    data2 = {'count': count}

    with open('poloniex/count.json', 'w') as outfile:
        json.dump(data2, outfile)

    with open('poloniex/initial.json', 'w') as outfile:
        json.dump(data, outfile)

else:
    try:
        with open('poloniex/count.json') as json_file:
            counts = json.load(json_file)
        count = int(counts['count'])
    except:
        count = 0
        counts = {"count": count}
        with open('poloniex/count.json', 'w') as outfile:
            json.dump(counts, outfile)

algorithm = config['algorithm']

if algorithm == 'THRESHOLD':

    threshold = config['threshold']

    while count < 99999:

        balances()

        prices()

        with open('poloniex/balance.json') as json_file:
            balance = json.load(json_file)
        with open('poloniex/prices.json') as json_file:
            price = json.load(json_file)

        usd_value()

        deviation()

        # print date and asset deviations

        print(datetime.datetime.now().time())
        print('Portfolio Value:' + " " + " " + str(total_usd) + " " + str(stablecoin))

        for x in range(0, assetnum):
            x = str(x + 1)
            print(
                "Asset: " + assets["asset{0}".format(x)] + " :::: " + "Current Variation: " + str(
                    dev["dev_asset{0}".format(x)] * 100) + "%")

        # Sell order trade trigger
        for x in range(0, assetnum):
            x = str(x + 1)
            balances()
            usd_value()
            deviation()

            if dev["dev_asset{0}".format(x)] > config['threshold']:
                # Calculate # of shares to sell
                dif = {}
                sell = {}
                goal_allocation = total_usd * allocation
                for x in range(0, assetnum):
                    x = str(x + 1)
                    usd_value()
                    dif["dif_asset{0}".format(x)] = usd["usd_asset{0}".format(x)] - goal_allocation
                    sell["sell_asset{0}".format(x)] = float(dif["dif_asset{0}".format(x)]) / float(price['price_asset{0}'.format(x)])
                    sell["sell_asset{0}".format(x)] = float(sell["sell_asset{0}".format(x)])

                # Sell order API call
                    if sell['sell_asset{0}'.format(x)] > 0:
                        sell_order(symbol["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)], price["price_asset{0}".format(x)])
                for x in range(0, assetnum):
                    x = str(x + 1)
                    if sell["sell_asset{0}".format(x)] < 0:
                        sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                        buy_order(symbol["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)], price["price_asset{0}".format(x)])

        time.sleep(4)
        balances()
        usd_value()
        deviation()

        # Buy order trade trigger
        negative_threshold = (-1 * config['threshold'])
        for x in range(0, assetnum):
            x = str(x + 1)
            balances()
            usd_value()
            deviation()
            if dev["dev_asset{0}".format(x)] < negative_threshold:

                # Calculate # of shares to buy
                dif = {}
                buy = {}
                goal_allocation = total_usd * allocation
                for x in range(0, assetnum):
                    x = str(x + 1)
                    usd_value()
                    dif["dif_asset{0}".format(x)] = usd["usd_asset{0}".format(x)] - goal_allocation
                    buy["buy_asset{0}".format(x)] = float(dif["dif_asset{0}".format(x)]) / float(price['price_asset{0}'.format(x)])
                    buy["buy_asset{0}".format(x)] = float(-1 * buy["buy_asset{0}".format(x)])

                # Order API call
                    if buy["buy_asset{0}".format(x)] < 0:
                        sellasset = (-1 * buy["buy_asset{0}".format(x)])
                        sell_order(symbol["symbol_asset{0}".format(x)], sellasset, price["price_asset{0}".format(x)])
                for x in range(0, assetnum):
                    x = str(x + 1)
                    if buy["buy_asset{0}".format(x)] > 0:
                        buy_order(symbol["symbol_asset{0}".format(x)], buy["buy_asset{0}".format(x)], price["price_asset{0}".format(x)])

        balances()
        prices()
        usd_value()

        count = count + 1
        if count == 95760:
            count = 0
        data3 = {'count': count}
        with open('poloniex/count.json', 'w') as outfile:
            json.dump(data3, outfile)
        time.sleep(60)

if algorithm == 'PERIODIC':

    period = config['period']

    if period == 'HOURLY':

        while count < 99999:

            balances()

            prices()

            with open('poloniex/balance.json') as json_file:
                balance = json.load(json_file)
            with open('poloniex/prices.json') as json_file:
                price = json.load(json_file)

            usd_value()

            deviation()

            # print date and asset deviations

            print(datetime.datetime.now().time())
            print('Portfolio Value:' + " " + " " + str(total_usd) + " " + str(stablecoin))

            for x in range(0, assetnum):
                x = str(x + 1)
                print(
                    "Asset: " + assets["asset{0}".format(x)] + " :::: " + "Current Variation: " + str(
                        dev["dev_asset{0}".format(x)] * 100) + "%")

            # Calculate # of shares to sell
            dif = {}
            sell = {}
            goal_allocation = total_usd * allocation
            for x in range(0, assetnum):
                x = str(x + 1)
                usd_value()
                dif["dif_asset{0}".format(x)] = usd["usd_asset{0}".format(x)] - goal_allocation
                sell["sell_asset{0}".format(x)] = float(dif["dif_asset{0}".format(x)]) / float(
                    price['price_asset{0}'.format(x)])
                sell["sell_asset{0}".format(x)] = float(sell["sell_asset{0}".format(x)])

                # Sell order API call
                if sell['sell_asset{0}'.format(x)] > 0:
                    sell_order(symbol["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                               price["price_asset{0}".format(x)])
            for x in range(0, assetnum):
                x = str(x + 1)
                if sell["sell_asset{0}".format(x)] < 0:
                    sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                    buy_order(symbol["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                              price["price_asset{0}".format(x)])

            time.sleep(4)
            balances()
            prices()
            usd_value()
            deviation()

            count = count + 1
            if count == 95760:
                count = 0
            data3 = {'count': count}
            with open('poloniex/count.json', 'w') as outfile:
                json.dump(data3, outfile)
            time.sleep(3600)

    if period == 'DAILY':

        while count < 99999:

            balances()

            prices()

            with open('poloniex/balance.json') as json_file:
                balance = json.load(json_file)
            with open('poloniex/prices.json') as json_file:
                price = json.load(json_file)

            usd_value()

            deviation()

            # print date and asset deviations

            print(datetime.datetime.now().time())
            print('Portfolio Value:' + " " + " " + str(total_usd) + " " + str(stablecoin))

            for x in range(0, assetnum):
                x = str(x + 1)
                print(
                    "Asset: " + assets["asset{0}".format(x)] + " :::: " + "Current Variation: " + str(
                        dev["dev_asset{0}".format(x)] * 100) + "%")

            # Calculate # of shares to sell

            dif = {}
            sell = {}
            goal_allocation = total_usd * allocation
            for x in range(0, assetnum):
                x = str(x + 1)
                usd_value()
                dif["dif_asset{0}".format(x)] = usd["usd_asset{0}".format(x)] - goal_allocation
                sell["sell_asset{0}".format(x)] = float(dif["dif_asset{0}".format(x)]) / float(
                    price['price_asset{0}'.format(x)])
                sell["sell_asset{0}".format(x)] = float(sell["sell_asset{0}".format(x)])

                # Sell order API call
                if sell['sell_asset{0}'.format(x)] > 0:
                    sell_order(symbol["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                               price["price_asset{0}".format(x)])
            for x in range(0, assetnum):
                x = str(x + 1)
                if sell["sell_asset{0}".format(x)] < 0:
                    sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                    buy_order(symbol["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                              price["price_asset{0}".format(x)])

            time.sleep(4)
            balances()
            prices()
            usd_value()
            deviation()

            count = count + 1
            if count == 95760:
                count = 0
            data3 = {'count': count}
            with open('poloniex/count.json', 'w') as outfile:
                json.dump(data3, outfile)
            time.sleep(86400)

    if period == 'WEEKLY':

        while count < 99999:

            balances()

            prices()

            with open('poloniex/balance.json') as json_file:
                balance = json.load(json_file)
            with open('poloniex/prices.json') as json_file:
                price = json.load(json_file)

            usd_value()

            deviation()

            # print date and asset deviations

            print(datetime.datetime.now().time())
            print('Portfolio Value:' + " " + " " + str(total_usd) + " " + str(stablecoin))

            for x in range(0, assetnum):
                x = str(x + 1)
                print(
                    "Asset: " + assets["asset{0}".format(x)] + " :::: " + "Current Variation: " + str(
                        dev["dev_asset{0}".format(x)] * 100) + "%")

            # Calculate # of shares to sell

            dif = {}
            sell = {}
            goal_allocation = total_usd * allocation
            for x in range(0, assetnum):
                x = str(x + 1)
                usd_value()
                dif["dif_asset{0}".format(x)] = usd["usd_asset{0}".format(x)] - goal_allocation
                sell["sell_asset{0}".format(x)] = float(dif["dif_asset{0}".format(x)]) / float(
                    price['price_asset{0}'.format(x)])
                sell["sell_asset{0}".format(x)] = float(sell["sell_asset{0}".format(x)])

                # Sell order API call
                if sell['sell_asset{0}'.format(x)] > 0:
                    sell_order(symbol["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                               price["price_asset{0}".format(x)])
            for x in range(0, assetnum):
                x = str(x + 1)
                if sell["sell_asset{0}".format(x)] < 0:
                    sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                    buy_order(symbol["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                              price["price_asset{0}".format(x)])

            time.sleep(4)
            balances()
            prices()
            usd_value()
            deviation()

            count = count + 1
            if count == 95760:
                count = 0
            data3 = {'count': count}
            with open('poloniex/count.json', 'w') as outfile:
                json.dump(data3, outfile)
            time.sleep(604800)