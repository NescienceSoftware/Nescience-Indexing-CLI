from time import sleep
from sys import exit
import json
import time
import math
import datetime
import requests
import _strptime
import robin_stocks as client
from sys import exit
import alpaca_trade_api as tradeapi


import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("Robinhood")


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

    with open('robinhood/config.json') as json_file:
        config = json.load(json_file)
        configcheck = config['configcheck']

    if configcheck != 'configured':
        assets = {}
        assetnum = input('Number of Assets in the Portfolio:')
        assetnum = int(assetnum)
        for x in range(0, assetnum):
            x = str(x + 1)
            assets["asset{0}".format(x)] = input('Asset' + " " + x + ':')
            assets["asset{0}".format(x)] = assets["asset{0}".format(x)].upper()

        configcheck = 'configured'

        algorithm = input('Threshold or Periodic: ').upper()

        if algorithm == 'THRESHOLD':
            threshold = input("Algorithm Threshold= ")
            threshold = float(threshold)
            threshold = (.01 * threshold)
            API_KEY = input('Username/Email:')
            API_SECRET = input('Password:')
            fractional = input('Are fractional shares enabled(Y/N): ').upper()

            print("Initializing...")

            configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum,
                             'symbol': symbol, 'API_KEY': API_KEY, 'API_SECRET': API_SECRET,
                             'algorithm': algorithm, 'fractional': fractional}
            with open('robinhood/config.json', 'w') as outfile:
                json.dump(configuration, outfile)
        if algorithm == 'PERIODIC':
            period = input('Hourly, Daily, or Weekly: ').upper()
            API_KEY = input('Username/Email:')
            API_SECRET = input('Password:')
            fractional = input('Are fractional shares enabled(Y/N): ').upper()

            print("Initializing...")

            configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                             'symbol': symbol, 'API_KEY': API_KEY, 'API_SECRET': API_SECRET,
                             'algorithm': algorithm, 'fractional': fractional}
            with open('robinhood/config.json', 'w') as outfile:
                json.dump(configuration, outfile)
        if algorithm != 'THRESHOLD' and algorithm != 'PERIODIC':
            print('Please check the spelling of' + " " + algorithm + ", and restart/retry.")
            time.sleep(60)

    else:
        reconfig = input('Would you like to reconfigure?  ')
        if reconfig == 'yes':
            assets = {}
            API_KEY = input('Username/Email:')
            API_SECRET = input('Password:')
            assetnum = input('Number of Assets in the Portfolio:')
            assetnum = int(assetnum)
            for x in range(0, assetnum):
                x = str(x + 1)
                assets["asset{0}".format(x)] = input('Asset' + " " + x + ':')
                assets["asset{0}".format(x)] = assets["asset{0}".format(x)].upper()

            configcheck = 'configured'

            algorithm = input('Threshold or Periodic: ').upper()

            if algorithm == 'THRESHOLD':
                threshold = input("Algorithm Threshold= ")
                threshold = float(threshold)
                threshold = (.01 * threshold)
                fractional = input('Are fractional shares enabled(Y/N): ').upper()

                print("Initializing...")

                configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck,
                                 'assetnum': assetnum,
                                 'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'algorithm': algorithm, 'fractional': fractional}
                with open('robinhood/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)
            if algorithm == 'PERIODIC':
                period = input('Hourly, Daily, or Weekly: ').upper()
                fractional = input('Are fractional shares enabled(Y/N): ').upper()
                configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                                 'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'algorithm': algorithm, 'fractional': fractional}

                print("Initializing...")

                with open('robinhood/config.json', 'w') as outfile:
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
            API_KEY = config['API_KEY']
            API_SECRET = config['API_SECRET']
            fractional = config['fractional']
            symbol = {}

            configcheck = 'configured'

            algorithm = config['algorithm']

            if algorithm == 'THRESHOLD':
                threshold = config['threshold']
                configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck,
                                 'assetnum': assetnum,
                                 'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'algorithm': algorithm, 'fractional': fractional}
                with open('robinhood/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)
            if algorithm == 'PERIODIC':
                period = config['period']
                configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                                'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'algorithm': algorithm, 'fractional': fractional}
                with open('robinhood/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)


def balances():
    # Pull  balance for each selected asset
    global cash_balance
    global balance
    global balances

    # Balance USD
    attempt = False
    while attempt is False:
        try:
            cash_balance = client.build_user_profile()['cash']
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
    attempt = False
    while attempt is False:
        try:
            balances = client.get_current_positions()
            attempt = True
        except ConnectionError:
            time.sleep(3)
            balances = client.get_current_positions()
        except ValueError:
            time.sleep(3)
            balances = client.get_current_positions()
    for b in balances:
        b['symbol'] = client.get_symbol_by_url(b['instrument'])

    # Get Balances of each previously entered asset
    balance = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        for b in balances:
            if b['symbol'] == assets["asset{0}".format(x)]:
                balance["balance_asset{0}".format(x)] = b['quantity']
                balance["balance_asset{0}".format(x)] = float(balance["balance_asset{0}".format(x)])
            if "balance_asset{0}".format(x) not in balance:
                balance["balance_asset{0}".format(x)] = 0
    # save balances to json
    balance.update({'cash_balance': cash_balance})
    with open('robinhood/balance.json', 'w') as outfile:
        json.dump(balance, outfile)


def prices():
    # Grabs prices from robinhood
    global price
    price = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        attempt = False
        while attempt is False:
            try:
                price["price_asset{0}".format(x)] = float(client.get_latest_price(symbol["symbol_asset{0}".format(x)])[0])
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

            time.sleep(1)

    # saves to json
    with open('robinhood/prices.json', 'w') as outfile:
        json.dump(price, outfile)


def usd_value():
    # Calculates USD value of positions
    global usd
    global total_usd

    with open('robinhood/balance.json') as json_file:
        balance = json.load(json_file)

    with open('robinhood/prices.json') as json_file:
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

    sell_asset = truncate(sell_asset, 6)
    market = str(alpaca.get_clock().is_open)
    try:
        if market == 'True':
            print("Selling" + " " + str(sell_asset) + " " + "of" + " " + str(asset))
            client.order_sell_fractional_by_quantity(symbol=asset, quantity=buy_asset, timeInForce='gfd', extendedHours=False)
    except Exception as e:
        print(e)
        pass

def buy_order(asset, buy_asset):

    buy_asset = truncate(buy_asset, 6)
    market = str(alpaca.get_clock().is_open)
    try:
        if market == 'True':
            print("Buying" + " " + str(buy_asset) + " " + "of" + " " + str(asset))
            client.order_buy_fractional_by_quantity(symbol=asset, quantity=buy_asset, timeInForce='gfd', extendedHours=False)
    except Exception as e:
        print(e)
        pass
    # MAIN


# allocation = .99 / len(assets)

setup()

with open('robinhood/config.json') as json_file:
    config = json.load(json_file)

api_key = config['API_KEY']
api_secret = config['API_SECRET']

login = client.login(username=api_key, password= api_secret, expiresIn=76400, scope= 'internal')

allocation = (.99 / assetnum)

with open('robinhood/initial.json') as json_file:
    initial = json.load(json_file)
    initialcheck = initial['initialcheck']

if initialcheck != 'done':
    initial = {}
    balances()
    with open('robinhood/balance.json') as json_file:
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

    with open('robinhood/count.json', 'w') as outfile:
        json.dump(data2, outfile)

    with open('robinhood/initial.json', 'w') as outfile:
        json.dump(data, outfile)

else:
    with open('robinhood/count.json') as json_file:
        counts = json.load(json_file)
    count = int(counts['count'])

algorithm = config['algorithm']
if fractional == 'Y':
    if algorithm == 'THRESHOLD':
        threshold = config['threshold']
        while count < 99999:

            balances()

            prices()

            with open('robinhood/balance.json') as json_file:
                balance = json.load(json_file)
            with open('robinhood/prices.json') as json_file:
                price = json.load(json_file)

            usd_value()

            deviation()

            # print date and asset deviations

            print(datetime.datetime.now().time())
            print('Portfolio Value:' + " " + " " + str(total_usd) + " USD")

            for x in range(0, assetnum):
                x = str(x + 1)
                print(
                    "Asset: " + assets["asset{0}".format(x)] + " :::: " + "Current Variation: " + str(
                        dev["dev_asset{0}".format(x)] * 100) + "%")

            # Sell order trade trigger
            for x in range(0, assetnum):
                x = str(x + 1)
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
            if count == 95760:
                count = 0
            data3 = {'count': count}
            with open('robinhood/count.json', 'w') as outfile:
                json.dump(data3, outfile)
            time.sleep(60)

    if algorithm == 'PERIODIC':

        period = config['period']

        if period == 'HOURLY':

            while count < 99999:

                balances()

                prices()

                with open('robinhood/balance.json') as json_file:
                    balance = json.load(json_file)
                with open('robinhood/prices.json') as json_file:
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
                        sell_order(assets["asset{0}".format(x)], sell["sell_asset{0}".format(x)])
                for x in range(0, assetnum):
                    x = str(x + 1)
                    if sell["sell_asset{0}".format(x)] < 0:
                        sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                        buy_order(assets["asset{0}".format(x)], sell["sell_asset{0}".format(x)])

                balances()
                prices()
                usd_value()

                count = count + 1
                if count == 95760:
                    count = 0
                data3 = {'count': count}
                with open('robinhood/count.json', 'w') as outfile:
                    json.dump(data3, outfile)
                time.sleep(3600)
        if period == 'DAILY':
            while count < 99999:

                balances()

                prices()

                with open('robinhood/balance.json') as json_file:
                    balance = json.load(json_file)
                with open('robinhood/prices.json') as json_file:
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
                        sell_order(assets["asset{0}".format(x)], sell["sell_asset{0}".format(x)])
                for x in range(0, assetnum):
                    x = str(x + 1)
                    if sell["sell_asset{0}".format(x)] < 0:
                        sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                        buy_order(assets["asset{0}".format(x)], sell["sell_asset{0}".format(x)])

                balances()
                prices()
                usd_value()

                count = count + 1
                if count == 95760:
                    count = 0
                data3 = {'count': count}
                with open('robinhood/count.json', 'w') as outfile:
                    json.dump(data3, outfile)
                time.sleep(86400)

        if period == 'WEEKLY':
            while count < 99999:

                balances()

                prices()

                with open('robinhood/balance.json') as json_file:
                    balance = json.load(json_file)
                with open('robinhood/prices.json') as json_file:
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
                        sell_order(assets["asset{0}".format(x)], sell["sell_asset{0}".format(x)])
                for x in range(0, assetnum):
                    x = str(x + 1)
                    if sell["sell_asset{0}".format(x)] < 0:
                        sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                        buy_order(assets["asset{0}".format(x)], sell["sell_asset{0}".format(x)])

                balances()
                prices()
                usd_value()


                count = count + 1
                if count == 95760:
                    count = 0
                data3 = {'count': count}
                with open('robinhood/count.json', 'w') as outfile:
                    json.dump(data3, outfile)
                time.sleep(604800)

if fractional == 'N':
    if algorithm == 'THRESHOLD':
        threshold = config['threshold']
        while count < 99999:

            balances()

            prices()

            with open('robinhood/balance.json') as json_file:
                balance = json.load(json_file)
            with open('robinhood/prices.json') as json_file:
                price = json.load(json_file)

            usd_value()

            deviation()

            # print date and asset deviations

            print(datetime.datetime.now().time())
            print('Portfolio Value:' + " " + " " + str(total_usd) + " USD")

            for x in range(0, assetnum):
                x = str(x + 1)
                print(
                    "Asset: " + assets["asset{0}".format(x)] + " :::: " + "Current Variation: " + str(
                        dev["dev_asset{0}".format(x)] * 100) + "%")

            # Sell order trade trigger
            for x in range(0, assetnum):
                x = str(x + 1)
                if dev["dev_asset{0}".format(x)] > config['threshold']:
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
                        sell["sell_asset{0}".format(x)] = int(sell["sell_asset{0}".format(x)])

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
                if dev["dev_asset{0}".format(x)] < negative_threshold:
                    # Calculate # of shares to buy
                    dif = {}
                    buy = {}
                    goal_allocation = total_usd * allocation
                    for x in range(0, assetnum):
                        x = str(x + 1)
                        usd_value()
                        dif["dif_asset{0}".format(x)] = usd["usd_asset{0}".format(x)] - goal_allocation
                        buy["buy_asset{0}".format(x)] = float(dif["dif_asset{0}".format(x)]) / float(
                            price['price_asset{0}'.format(x)])
                        buy["buy_asset{0}".format(x)] = int(-1 * buy["buy_asset{0}".format(x)])

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
            if count == 95760:
                count = 0
            data3 = {'count': count}
            with open('robinhood/count.json', 'w') as outfile:
                json.dump(data3, outfile)
            time.sleep(60)

    if algorithm == 'PERIODIC':

        period = config['period']

        if period == 'HOURLY':

            while count < 99999:

                balances()

                prices()

                with open('robinhood/balance.json') as json_file:
                    balance = json.load(json_file)
                with open('robinhood/prices.json') as json_file:
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
                    sell["sell_asset{0}".format(x)] = int(sell["sell_asset{0}".format(x)])

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

                count = count + 1
                if count == 95760:
                    count = 0
                data3 = {'count': count}
                with open('robinhood/count.json', 'w') as outfile:
                    json.dump(data3, outfile)
                time.sleep(3600)
        if period == 'DAILY':
            while count < 99999:

                balances()

                prices()

                with open('robinhood/balance.json') as json_file:
                    balance = json.load(json_file)
                with open('robinhood/prices.json') as json_file:
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
                    sell["sell_asset{0}".format(x)] = int(sell["sell_asset{0}".format(x)])

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

                count = count + 1
                if count == 95760:
                    count = 0
                data3 = {'count': count}
                with open('robinhood/count.json', 'w') as outfile:
                    json.dump(data3, outfile)
                time.sleep(86400)

        if period == 'WEEKLY':
            while count < 99999:

                balances()

                prices()

                with open('robinhood/balance.json') as json_file:
                    balance = json.load(json_file)
                with open('robinhood/prices.json') as json_file:
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
                    sell["sell_asset{0}".format(x)] = int(sell["sell_asset{0}".format(x)])

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

                count = count + 1
                if count == 95760:
                    count = 0
                data3 = {'count': count}
                with open('robinhood/count.json', 'w') as outfile:
                    json.dump(data3, outfile)
                time.sleep(604800)