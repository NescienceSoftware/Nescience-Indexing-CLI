from time import sleep
from sys import exit
import time
import datetime
import math
import json
from kucoin.client import Client
from kucoin.exceptions import KucoinAPIException
import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("Kucoin")


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

    with open('Kucoin/config.json') as json_file:
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
            symbol["symbol_asset{0}".format(x)] = str(assets["asset{0}".format(x)] + '-' + stablecoin)

        configcheck = 'configured'

        algorithm = input('Threshold or Periodic: ').upper()

        if algorithm == 'THRESHOLD':
            threshold = input("Algorithm Threshold= ")
            threshold = float(threshold)
            threshold = (.01 * threshold)
            API_KEY = input('API KEY:')
            API_SECRET = input('API SECRET:')
            API_PASSPHRASE = input('API PASSPHRASE:')

            print("Initializing...")

            configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum,
                             'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY, 'API_SECRET': API_SECRET,
                             'algorithm': algorithm, 'API_PASSPHRASE': API_PASSPHRASE}
            with open('kucoin/config.json', 'w') as outfile:
                json.dump(configuration, outfile)
        if algorithm == 'PERIODIC':
            period = input('Hourly, Daily, or Weekly: ').upper()
            API_KEY = input('API KEY:')
            API_SECRET = input('API SECRET:')
            API_PASSPHRASE = input('API PASSPHRASE:')

            print("Initializing...")

            configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                             'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY, 'API_SECRET': API_SECRET,
                             'algorithm': algorithm, 'API_PASSPHRASE': API_PASSPHRASE}
            with open('kucoin/config.json', 'w') as outfile:
                json.dump(configuration, outfile)
        if algorithm != 'THRESHOLD' and algorithm != 'PERIODIC':
            print('Please check the spelling of' + " " + algorithm + ", and restart/retry.")
            time.sleep(60)

    else:
        reconfig = input('Would you like to reconfigure?  ')
        if reconfig == 'yes':
            assets = {}
            API_KEY = input('API KEY:')
            API_SECRET = input('API SECRET:')
            API_PASSPHRASE = input('API PASSPHRASE:')
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
                symbol["symbol_asset{0}".format(x)] = str(assets["asset{0}".format(x)] + '-' + stablecoin)

            print("Loading... This may take a few seconds.")

            client = Client(API_KEY, API_SECRET, API_PASSPHRASE)

            try:
                new_balances = client.get_accounts()
            except OSError:
                time.sleep(2)
                new_balances = client.get_accounts()

            # Balance USD

            def oldcash():
                cash = {}

                def cashcheck():
                    for b in new_balances:
                        if b['currency'] == 'USDT' and b['type'] == 'trade':
                            cash['old_cash'] = [b['balance']][0]
                            old_cash = float(cash['old_cash'])
                            return old_cash

                cashcheck = cashcheck()

                if cashcheck is None:
                    old_cash = 0
                    return old_cash
                else:
                    return cashcheck
            old_cash = oldcash()

            # Get Balances of each previously entered asset
            new_balance = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                for b in new_balances:
                    if b['type'] == 'trade':
                        if b['currency'] == config['assets']["asset{0}".format(x)]:
                            new_balance["balance_asset{0}".format(x)] = [b['balance']]
                            new_balance["balance_asset{0}".format(x)] = new_balance["balance_asset{0}".format(x)][0]
                            new_balance["balance_asset{0}".format(x)] = float(new_balance["balance_asset{0}".format(x)])
                    if "balance_asset{0}".format(x) not in new_balance:
                        new_balance["balance_asset{0}".format(x)] = 0

            old = {}

            for x in range(0, assetnum):
                x = str(x + 1)
                try:
                    old['old_asset{0}'.format(x)] = new_balance['balance_asset{0}'.format(x)]
                except:
                    pass

            olddata = {'old': old, 'old_cash': old_cash}

            with open('kucoin/old.json', 'w') as outfile:
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
                                 'algorithm': algorithm, 'API_PASSPHRASE': API_PASSPHRASE}
                with open('kucoin/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)
            if algorithm == 'PERIODIC':
                period = input('Hourly, Daily, or Weekly: ').upper()

                print("Initializing...")

                configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'algorithm': algorithm, 'API_PASSPHRASE': API_PASSPHRASE}
                with open('kucoin/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)
            if algorithm != 'THRESHOLD' and algorithm != 'PERIODIC':
                print('Please check the spelling of' + " " + algorithm + ", and restart/retry.")
                time.sleep(60)

        else:
            assetnum = config['assetnum']
            assetnum = int(assetnum)
            assets = {}
            API_KEY = config['API_KEY']
            API_SECRET = config['API_SECRET']
            API_PASSPHRASE = config['API_PASSPHRASE']
            for x in range(0, assetnum):
                x = str(x + 1)
                assets["asset{0}".format(x)] = config['assets']["asset{0}".format(x)]
                assets["asset{0}".format(x)] = assets["asset{0}".format(x)].upper()

            threshold = config['threshold']
            stablecoin = config['stablecoin']
            stablecoin = stablecoin.upper()
            symbol = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                symbol["symbol_asset{0}".format(x)] = str(assets["asset{0}".format(x)] + '-' + stablecoin)

            configcheck = 'configured'

            algorithm = config['algorithm']

            if algorithm == 'THRESHOLD':
                threshold = config['threshold']

                print("Initializing...")

                configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck,
                                 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'algorithm': algorithm, 'API_PASSPHRASE': API_PASSPHRASE}
                with open('kucoin/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)
            if algorithm == 'PERIODIC':
                period = config['period']

                print("Initializing...")

                configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'algorithm': algorithm, 'API_PASSPHRASE': API_PASSPHRASE}
                with open('kucoin/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)


def balances():
    # Pull  balance for each selected asset
    global cash_balance
    global balance
    # All account balances
    attempt = False
    while attempt is False:

        try:
            balances = client.get_accounts()
            attempt = True
        except OSError as e:
            print(e)
            time.sleep(2)
            pass
        except KucoinAPIException as e:
            print(e)
            time.sleep(2)
            pass
    # Balance USD
    def cash():
        cash = {}

        def cashcheck():
            for b in balances:
                if b['currency'] == 'USDT' and b['type'] == 'trade':
                    cash['old_cash'] = [b['balance']][0]
                    old_cash = float(cash['old_cash'])
                    return old_cash

        cashcheck = cashcheck()

        if cashcheck is None:
            old_cash = 0
            return old_cash
        else:
            return cashcheck
    cash_balance = cash()
    # Get Balances of each previously entered asset
    balance = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        for b in balances:
            if b['type'] == 'trade':
                if b['currency'] == config['assets']["asset{0}".format(x)]:
                    balance["balance_asset{0}".format(x)] = [b['balance']]
                    balance["balance_asset{0}".format(x)] = balance["balance_asset{0}".format(x)][0]
                    balance["balance_asset{0}".format(x)] = float(balance["balance_asset{0}".format(x)])
            if "balance_asset{0}".format(x) not in balance:
                balance["balance_asset{0}".format(x)] = 0
    # save balances to json
    balance.update({'cash_balance': cash_balance})
    with open('kucoin/balance.json', 'w') as outfile:
        json.dump(balance, outfile)


def prices():
    global price
    # Grabs prices from Kucoin
    price = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        attempt = False
        while attempt is False:
            try:
                price["price_asset{0}".format(x)] = float(client.get_ticker(symbol["symbol_asset{0}".format(x)])['price'])
                attempt = True
            except OSError:
                time.sleep(2)
                pass
            except KucoinAPIException as e:
                print(e)
                time.sleep(2)
                pass
            time.sleep(1)

    # saves to json
    with open('Kucoin/prices.json', 'w') as outfile:
        json.dump(price, outfile)


def usd_value():
    # Calculates USD value of positions
    global usd
    global total_usd

    with open('Kucoin/balance.json') as json_file:
        balance = json.load(json_file)

    with open('Kucoin/prices.json') as json_file:
        price = json.load(json_file)

    usd = {}

    for x in range(0, assetnum):
        x = str(x + 1)
        usd["usd_asset{0}".format(x)] = float(balance["balance_asset{0}".format(x)]) * float(price["price_asset{0}".format(x)])

    usd_assets = 0
    for x in range(0, assetnum):
        x = str(x + 1)
        usd_assets = usd_assets + float(usd["usd_asset{0}".format(x)])

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


def sell_order(asset, sell_asset, current_price, pair):

    value = current_price * sell_asset
    if value >= 10:
        pair = str(pair)
        try:
            currencies = client.get_symbols()
        except OSError:
            time.sleep(2)
            currencies = client.get_symbols()
        except KucoinAPIException as e:
            print(e)
            time.sleep(2)
            currencies = client.get_symbols()
        for c in currencies:
            if c['symbol'] == pair:
                minimum = float(c['baseMinSize'])
        if minimum <= .001:
            sell_asset = truncate(sell_asset, 4)
        else:
            if minimum <= .01:
                sell_asset = truncate(sell_asset, 3)
            else:
                if minimum <= .1:
                    sell_asset = truncate(sell_asset, 2)
                else:
                    if minimum <= 1:
                        sell_asset = truncate(sell_asset, 1)
                    else:
                        if minimum == 1:
                            sell_asset = round(sell_asset)
        print("Selling" + " " + str(sell_asset) + " " + "of" + " " + str(asset))
        try:
            client.create_market_order(
                symbol=asset,
                size=sell_asset,
                side='sell')
        except OSError:
            client.create_market_order(
                symbol=asset,
                size=sell_asset,
                side='sell')


def buy_order(asset, buy_asset, current_price, pair):

    value = current_price * buy_asset
    if value >= 10:
        pair = str(pair)

        try:
            currencies = client.get_symbols()
        except OSError:
            time.sleep(2)
            currencies = client.get_symbols()
        except KucoinAPIException as e:
            print(e)
            time.sleep(2)
            currencies = client.get_symbols()
        for c in currencies:
            if c['symbol'] == pair:
                minimum = float(c['baseMinSize'])
        if minimum <= .001:
            buy_asset = truncate(buy_asset, 4)
        else:
            if minimum <= .01:
                buy_asset = truncate(buy_asset, 3)
            else:
                if minimum <= .1:
                    buy_asset = truncate(buy_asset, 2)
                else:
                    if minimum <= 1:
                        buy_asset = truncate(buy_asset, 1)
                    else:
                        if minimum == 1:
                            buy_asset = round(buy_asset)
        print("Buying" + " " + str(buy_asset) + " " + "of" + " " + str(asset))
        try:
            client.create_market_order(
                symbol=asset,
                size=buy_asset,
                side='buy')
        except OSError:
            client.create_market_order(
                symbol=asset,
                size=buy_asset,
                side='buy')

    # MAIN


setup()

with open('Kucoin/config.json') as json_file:
    config = json.load(json_file)

api_key = config['API_KEY']
api_secret = config['API_SECRET']
api_passphrase = config['API_PASSPHRASE']

client = Client(api_key, api_secret, api_passphrase)

allocation = (.99 / assetnum)

with open('Kucoin/initial.json') as json_file:
    initial = json.load(json_file)
    initialcheck = initial['initialcheck']

if initialcheck != 'done':
    initial = {}
    balances()
    with open('Kucoin/balance.json') as json_file:
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

    with open('kucoin/count.json', 'w') as outfile:
        json.dump(data2, outfile)

    with open('kucoin/initial.json', 'w') as outfile:
        json.dump(data, outfile)

else:
    try:
        with open('kucoin/count.json') as json_file:
            counts = json.load(json_file)
        count = int(counts['count'])
    except:
        count = 0
        counts = {"count": count}
        with open('kucoin/count.json', 'w') as outfile:
            json.dump(counts, outfile)

algorithm = config['algorithm']

if algorithm == 'THRESHOLD':

    threshold = config['threshold']

    while count < 99999:

        balances()

        prices()

        with open('Kucoin/balance.json') as json_file:
            balance = json.load(json_file)
        with open('Kucoin/prices.json') as json_file:
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

                    if sell["sell_asset{0}".format(x)] > 0:
                        sell_order(symbol["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)], price["price_asset{0}".format(x)], symbol["symbol_asset{0}".format(x)])
                for x in range(0, assetnum):
                    x = str(x + 1)
                    if sell["sell_asset{0}".format(x)] < 0:
                        sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                        buy_order(symbol["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)], price["price_asset{0}".format(x)], symbol["symbol_asset{0}".format(x)])

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

                # Buy order API call

                    if buy["buy_asset{0}".format(x)] < 0:
                        sellasset = (-1 * buy["buy_asset{0}".format(x)])
                        sell_order(symbol["symbol_asset{0}".format(x)], sellasset, price["price_asset{0}".format(x)], symbol["symbol_asset{0}".format(x)])
                for x in range(0, assetnum):
                    x = str(x + 1)
                    if buy["buy_asset{0}".format(x)] > 0:
                        buy_order(symbol["symbol_asset{0}".format(x)], buy["buy_asset{0}".format(x)], price["price_asset{0}".format(x)], symbol["symbol_asset{0}".format(x)])
        time.sleep(3)
        balances()
        prices()
        usd_value()

        count = count + 1
        if count == 95760:
            count = 0
        data3 = {'count': count}
        with open('kucoin/count.json', 'w') as outfile:
            json.dump(data3, outfile)
        time.sleep(60)

if algorithm == 'PERIODIC':

    period = config['period']

    if period == 'HOURLY':

        while count < 99999:

            balances()

            prices()

            with open('Kucoin/balance.json') as json_file:
                balance = json.load(json_file)
            with open('Kucoin/prices.json') as json_file:
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

                if sell["sell_asset{0}".format(x)] > 0:
                    sell_order(symbol["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                               price["price_asset{0}".format(x)], symbol["symbol_asset{0}".format(x)])
            for x in range(0, assetnum):
                x = str(x + 1)
                if sell["sell_asset{0}".format(x)] < 0:
                    sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                    buy_order(symbol["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                              price["price_asset{0}".format(x)], symbol["symbol_asset{0}".format(x)])

            time.sleep(3)
            balances()
            prices()
            usd_value()
            deviation()

            count = count + 1
            if count == 95760:
                count = 0
            data3 = {'count': count}
            with open('kucoin/count.json', 'w') as outfile:
                json.dump(data3, outfile)
            time.sleep(3600)

    if period == 'DAILY':

        while count < 99999:

            balances()

            prices()

            with open('Kucoin/balance.json') as json_file:
                balance = json.load(json_file)
            with open('Kucoin/prices.json') as json_file:
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

                if sell["sell_asset{0}".format(x)] > 0:
                    sell_order(symbol["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                               price["price_asset{0}".format(x)], symbol["symbol_asset{0}".format(x)])
            for x in range(0, assetnum):
                x = str(x + 1)
                if sell["sell_asset{0}".format(x)] < 0:
                    sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                    buy_order(symbol["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                              price["price_asset{0}".format(x)], symbol["symbol_asset{0}".format(x)])

            time.sleep(3)
            balances()
            prices()
            usd_value()
            deviation()

            count = count + 1
            if count == 95760:
                count = 0
            data3 = {'count': count}
            with open('kucoin/count.json', 'w') as outfile:
                json.dump(data3, outfile)
            time.sleep(86400)

    if period == 'WEEKLY':

        while count < 99999:

            balances()

            prices()

            with open('Kucoin/balance.json') as json_file:
                balance = json.load(json_file)
            with open('Kucoin/prices.json') as json_file:
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

                if sell["sell_asset{0}".format(x)] > 0:
                    sell_order(symbol["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                               price["price_asset{0}".format(x)], symbol["symbol_asset{0}".format(x)])
            for x in range(0, assetnum):
                x = str(x + 1)
                if sell["sell_asset{0}".format(x)] < 0:
                    sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                    buy_order(symbol["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                              price["price_asset{0}".format(x)], symbol["symbol_asset{0}".format(x)])

            time.sleep(3)
            balances()
            prices()
            usd_value()
            deviation()

            count = count + 1
            if count == 95760:
                count = 0
            data3 = {'count': count}
            with open('kucoin/count.json', 'w') as outfile:
                json.dump(data3, outfile)
            time.sleep(604800)