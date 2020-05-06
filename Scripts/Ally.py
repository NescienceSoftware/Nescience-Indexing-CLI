from time import sleep
from sys import exit
import json
import time
import math
import datetime
import requests
import _strptime
from sys import exit
import ally

import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("Ally")


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

    with open('ally/config.json') as json_file:
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
            symbol["symbol_asset{0}".format(x)] = str(assets["asset{0}".format(x)] + stablecoin)

        configcheck = 'configured'

        algorithm = input('Threshold or Periodic: ').upper()

        if algorithm == 'THRESHOLD':
            threshold = input("Algorithm Threshold= ")
            threshold = float(threshold)
            threshold = (.01 * threshold)
            CONSUMER_KEY = input('CONSUMER KEY: ')
            CONSUMER_SECRET = input('CONSUMER SECRET: ')
            ACCESS_TOKEN = input('ACCESS TOKEN: ')
            ACCESS_SECRET = input('ACCESS SECRET: ')

            print("Initializing...")

            configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum,
                             'stablecoin': stablecoin, 'symbol': symbol, 'CONSUMER_KEY': CONSUMER_KEY,
                             'CONSUMER_SECRET': CONSUMER_SECRET, 'ACCESS_TOKEN': ACCESS_TOKEN,
                             'ACCESS_SECRET': ACCESS_SECRET, 'algorithm': algorithm}
            with open('ally/config.json', 'w') as outfile:
                json.dump(configuration, outfile)
        if algorithm == 'PERIODIC':
            period = input('Hourly, Daily, or Weekly: ').upper()
            CONSUMER_KEY = input('CONSUMER KEY: ')
            CONSUMER_SECRET = input('CONSUMER SECRET: ')
            ACCESS_TOKEN = input('ACCESS TOKEN: ')
            ACCESS_SECRET = input('ACCESS SECRET: ')

            print("Initializing...")

            configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                             'stablecoin': stablecoin, 'symbol': symbol, 'CONSUMER_KEY': CONSUMER_KEY,
                             'CONSUMER_SECRET': CONSUMER_SECRET, 'ACCESS_TOKEN': ACCESS_TOKEN,
                             'ACCESS_SECRET': ACCESS_SECRET, 'algorithm': algorithm}
            with open('ally/config.json', 'w') as outfile:
                json.dump(configuration, outfile)
        if algorithm != 'THRESHOLD' and algorithm != 'PERIODIC':
            print('Please check the spelling of' + " " + algorithm + ", and restart/retry.")
            time.sleep(60)

    else:
        reconfig = input('Would you like to reconfigure?  ')
        if reconfig == 'yes':
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
                symbol["symbol_asset{0}".format(x)] = str(assets["asset{0}".format(x)] + stablecoin)

            configcheck = 'configured'

            algorithm = input('Threshold or Periodic: ').upper()

            if algorithm == 'THRESHOLD':
                threshold = input("Algorithm Threshold= ")
                threshold = float(threshold)
                threshold = (.01 * threshold)
                CONSUMER_KEY = input('CONSUMER KEY: ')
                CONSUMER_SECRET = input('CONSUMER SECRET: ')
                ACCESS_TOKEN = input('ACCESS TOKEN: ')
                ACCESS_SECRET = input('ACCESS SECRET: ')

                print("Initializing...")

                configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck,
                                 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'CONSUMER_KEY': CONSUMER_KEY,
                                 'CONSUMER_SECRET': CONSUMER_SECRET, 'ACCESS_TOKEN': ACCESS_TOKEN,
                                 'ACCESS_SECRET': ACCESS_SECRET, 'algorithm': algorithm}
                with open('ally/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)
            if algorithm == 'PERIODIC':
                period = input('Hourly, Daily, or Weekly: ').upper()
                CONSUMER_KEY = input('CONSUMER KEY: ')
                CONSUMER_SECRET = input('CONSUMER SECRET: ')
                ACCESS_TOKEN = input('ACCESS TOKEN: ')
                ACCESS_SECRET = input('ACCESS SECRET: ')
                configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'CONSUMER_KEY': CONSUMER_KEY,
                                 'CONSUMER_SECRET': CONSUMER_SECRET, 'ACCESS_TOKEN': ACCESS_TOKEN,
                                 'ACCESS_SECRET': ACCESS_SECRET, 'algorithm': algorithm}

                print("Initializing...")

                with open('ally/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)

            if algorithm != 'THRESHOLD' and algorithm != 'PERIODIC':
                print('Please check the spelling of' + " " + algorithm + ", and restart/retry.")
                time.sleep(60)

        else:
            assetnum = config['assetnum']
            assetnum = int(assetnum)
            assets = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                assets["asset{0}".format(x)] = config['assets']["asset{0}".format(x)]
                assets["asset{0}".format(x)] = assets["asset{0}".format(x)].upper()

            CONSUMER_KEY = config['CONSUMER KEY']
            CONSUMER_SECRET = config['CONSUMER SECRET']
            ACCESS_TOKEN = config['ACCESS TOKEN']
            ACCESS_SECRET = config['ACCESS SECRET']
            stablecoin = config['stablecoin']
            stablecoin = stablecoin.upper()
            symbol = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                symbol["symbol_asset{0}".format(x)] = str(config['assets']["asset{0}".format(x)] + stablecoin)

            configcheck = 'configured'

            algorithm = config['algorithm']

            if algorithm == 'THRESHOLD':
                threshold = config['threshold']
                configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck,
                                 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'CONSUMER_KEY': CONSUMER_KEY,
                                 'CONSUMER_SECRET': CONSUMER_SECRET, 'ACCESS_TOKEN': ACCESS_TOKEN,
                                 'ACCESS_SECRET': ACCESS_SECRET, 'algorithm': algorithm}
                with open('ally/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)
            if algorithm == 'PERIODIC':
                period = config['period']
                configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'CONSUMER_KEY': CONSUMER_KEY,
                                 'CONSUMER_SECRET': CONSUMER_SECRET, 'ACCESS_TOKEN': ACCESS_TOKEN,
                                 'ACCESS_SECRET': ACCESS_SECRET, 'algorithm': algorithm}
                with open('ally/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)


def balances():
    # Pull  balance for each selected asset
    global cash_balance
    global balances
    # Balance USD
    attempt = False
    while attempt is False:
        try:
            cash_balance = a.get_accounts()[62986249]['accountbalance']['money']['cashavailable']
            attempt = True
        except OSError:
            time.sleep(2)
            pass
        except requests.exceptions.Timeout as e:
            print(e)
            time.sleep(2)
            pass
        except requests.exceptions.ReadTimeout as e:
            print(e)
            time.sleep(2)
            pass
    cash_balance = float(cash_balance)
    time.sleep(1)
    # Get Balances of each previously entered asset
    while attempt is False:
        try:
            balances = a.get_holdings(account=accountNumber)
            attempt = True
        except OSError:
            time.sleep(2)
            pass
        except requests.exceptions.Timeout as e:
            print(e)
            time.sleep(2)
            pass
        except requests.exceptions.ReadTimeout as e:
            print(e)
            time.sleep(2)
            pass
        except Exception as e:
            print(e)
            time.sleep(30)
            pass

    balance = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        for b in balances:
            if b['instrument']['sym'] == assets["asset{0}".format(x)].lower():
                balance["balance_asset{0}".format(x)] = [b['qty']]
            if "balance_asset{0}".format(x) not in balance:
                balance["balance_asset{0}".format(x)] = 0

    # save balances to json
    balance.update({'cash_balance': cash_balance})
    with open('ally/balance.json', 'w') as outfile:
        json.dump(balance, outfile)


def prices():
    # Grabs prices from ally
    global price
    price = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        attempt = False
        while attempt is False:
            try:
                price["price_asset{0}".format(x)] = a.get_quote(
                        symbols=assets[str('asset' + x)],
                        fields="last")['last']
                attempt = True
            except OSError:
                time.sleep(2)
                pass
            except requests.exceptions.Timeout as e:
                print(e)
                time.sleep(2)
                pass
            except requests.exceptions.ReadTimeout as e:
                print(e)
                time.sleep(2)
                pass
            except Exception as e:
                print(e)
                time.sleep(15)
                pass

            time.sleep(1)

    # saves to json
    with open('ally/prices.json', 'w') as outfile:
        json.dump(price, outfile)


def usd_value():
    # Calculates USD value of positions
    global usd
    global total_usd

    with open('ally/balance.json') as json_file:
        balance = json.load(json_file)

    with open('ally/prices.json') as json_file:
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

    marketStatus = a.market_clock()['status']['current']

    if marketStatus == 'open':

        if sell_asset >= 1:
            sell_asset = int(sell_asset)

            print("Selling" + " " + str(sell_asset) + " " + "of" + " " + str(asset))

            try:
                market_sell = ally.order.Order(

                    # Good for day order
                    timespan=ally.order.Timespan('day'),

                    # Buy order (to_open is True by defaul)
                    type=ally.order.Sell(),

                    # Market order
                    price=ally.order.Market(),

                    # Stock, symbol F
                    instrument=ally.instrument.Equity(asset),

                    # 1 share
                    quantity=ally.order.Quantity(sell_asset)
                )
                exec_status = a.submit_order(
                    order=market_sell,
                    preview=False
                )
            except Exception as e:
                print(e)
    else:
        pass


def buy_order(asset, buy_asset):

    marketStatus = a.market_clock()['status']['current']

    if marketStatus == 'open':

        if buy_asset >= 1:
            buy_asset = int(buy_asset)

            print("Buying" + " " + str(buy_asset) + " " + "of" + " " + str(asset))

            try:
                market_buy = ally.order.Order(

                    # Good for day order
                    timespan=ally.order.Timespan('day'),

                    # Buy order (to_open is True by defaul)
                    type=ally.order.Sell(),

                    # Market order
                    price=ally.order.Market(),

                    # Stock, symbol F
                    instrument=ally.instrument.Equity(asset),

                    # 1 share
                    quantity=ally.order.Quantity(buy_asset)
                )
                exec_status = a.submit_order(
                    order=market_buy,
                    preview=False
                )
            except Exception as e:
                print(e)
    else:
        pass

    # MAIN


# allocation = .99 / len(assets)

setup()

with open('ally/config.json') as json_file:
    config = json.load(json_file)

CONSUMER_KEY = config['CONSUMER_KEY']
CONSUMER_SECRET = config['CONSUMER_SECRET']
ACCESS_TOKEN = config['ACCESS_TOKEN']
ACCESS_SECRET = config['ACCESS_SECRET']
params = {
    'resource_owner_secret':ACCESS_SECRET,
    'resource_owner_key':ACCESS_TOKEN,
    'client_secret':CONSUMER_SECRET,
    'client_key':CONSUMER_KEY
}
a = ally.Ally(params)

allocation = (.99 / assetnum)

with open('ally/initial.json') as json_file:
    initial = json.load(json_file)
    initialcheck = initial['initialcheck']

if initialcheck != 'done':
    initial = {}
    balances()
    with open('ally/balance.json') as json_file:
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

    with open('ally/count.json', 'w') as outfile:
        json.dump(data2, outfile)

    with open('ally/initial.json', 'w') as outfile:
        json.dump(data, outfile)

else:
    with open('ally/count.json') as json_file:
        counts = json.load(json_file)
    count = int(counts['count'])

algorithm = config['algorithm']

if algorithm == 'THRESHOLD':
    threshold = config['threshold']
    while count < 99999:

        balances()

        prices()

        with open('ally/balance.json') as json_file:
            balance = json.load(json_file)
        with open('ally/prices.json') as json_file:
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
                        sell_order(symbol["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)])
                for x in range(0, assetnum):
                    x = str(x + 1)
                    if sell["sell_asset{0}".format(x)] < 0:
                        sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                        buy_order(symbol["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)])
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

                # Buy order API call

                    if buy["buy_asset{0}".format(x)] < 0:
                        sellasset = (-1 * buy["buy_asset{0}".format(x)])
                        sell_order(symbol["symbol_asset{0}".format(x)], sellasset)

                for x in range(0, assetnum):
                    x = str(x + 1)
                    if buy["buy_asset{0}".format(x)] > 0:
                        buy_order(symbol["symbol_asset{0}".format(x)], buy["buy_asset{0}".format(x)])

        balances()
        prices()
        usd_value()

        # Record data every 3.5 days
        count = count + 1
        if count == 95760:
            count = 0
        data3 = {'count': count}
        with open('ally/count.json', 'w') as outfile:
            json.dump(data3, outfile)
        time.sleep(60)

if algorithm == 'PERIODIC':

    period = config['period']

    global sleeptime
    if period == 'HOURLY':
        sleeptime = 3600
    if period == 'DAILY':
        sleeptime = 86400
    if period == 'WEEKLY':
        sleeptime = 604800
    if period == 'MONTHLY':
        sleeptime = 2.592e+6
    while count < 99999:

        balances()

        prices()

        with open('ally/balance.json') as json_file:
            balance = json.load(json_file)
        with open('ally/prices.json') as json_file:
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
                sell_order(symbol["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)])
        for x in range(0, assetnum):
            x = str(x + 1)
            if sell["sell_asset{0}".format(x)] < 0:
                sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                buy_order(symbol["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)])

        balances()
        prices()
        usd_value()

        count = count + 1
        if count == 9576000000:
            count = 0
        data3 = {'count': count}
        with open('ally/count.json', 'w') as outfile:
            json.dump(data3, outfile)
        time.sleep(sleeptime)