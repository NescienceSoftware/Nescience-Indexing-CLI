from time import sleep
from sys import exit
import time
import datetime
import math
import json
import ccxt
import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("Huobi")


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

    with open('huobi/config.json') as json_file:
        config = json.load(json_file)
        configcheck = config['configcheck']

    if configcheck != 'configured':
        assets = {}
        API_KEY = input('API KEY:')
        API_SECRET = input('API SECRET:')
        assetnum = input('Number of Assets in the Portfolio:')
        assetnum = int(assetnum)
        stablecoin = input('What currency would you like to trade against: ')
        if stablecoin == 'USDT':
            stablecoin = 'USD'
        stablecoin = stablecoin.upper()
        for x in range(0, assetnum):
            x = str(x + 1)
            assets["asset{0}".format(x)] = input('Asset' + " " + x + ':')
            assets["asset{0}".format(x)] = assets["asset{0}".format(x)].upper()

        symbol = {}
        for x in range(0, assetnum):
            x = str(x + 1)
            symbol["symbol_asset{0}".format(x)] = str(assets["asset{0}".format(x)] + '/' + stablecoin)

        configcheck = 'configured'

        algorithm = input('Threshold or Periodic: ').upper()

        if algorithm == 'THRESHOLD':
            threshold = input("Algorithm Threshold= ")
            threshold = float(threshold)
            threshold = (.01 * threshold)
            configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum,
                             'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY, 'API_SECRET': API_SECRET,
                             'algorithm': algorithm}
            with open('huobi/config.json', 'w') as outfile:
                json.dump(configuration, outfile)
        if algorithm == 'PERIODIC':
            period = input('Hourly, Daily, or Weekly: ').upper()
            configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                             'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY, 'API_SECRET': API_SECRET,
                             'algorithm': algorithm}
            with open('huobi/config.json', 'w') as outfile:
                json.dump(configuration, outfile)
        else:
            print('Please check the spelling of' + " " + algorithm)
            exit(0)

    else:
        reconfig = input('Would you like to reconfigure?  ')
        if reconfig == 'yes':
            assets = {}
            API_KEY = input('API KEY:')
            API_SECRET = input('API SECRET:')
            assetnum = input('Number of Assets in the Portfolio:')
            assetnum = int(assetnum)
            stablecoin = input('What currency would you like to trade against: ')
            if stablecoin == 'USDT':
                stablecoin = 'USD'
            stablecoin = stablecoin.upper()
            for x in range(0, assetnum):
                x = str(x + 1)
                assets["asset{0}".format(x)] = input('Asset' + " " + x + ':')
                assets["asset{0}".format(x)] = assets["asset{0}".format(x)].upper()

            symbol = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                symbol["symbol_asset{0}".format(x)] = str(assets["asset{0}".format(x)] + '/' + stablecoin)

            client = ccxt.huobipro({'apiKey': API_KEY, 'secret': API_SECRET})

            try:
                old_cash = client.fetch_balance()[stablecoin]['total']
                time.sleep(3)
            except ccxt.DDoSProtection as e:
                print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
                time.sleep(2)
                old_cash = float(client.fetch_balance()[stablecoin]['total'])
            except ccxt.RequestTimeout as e:
                time.sleep(.1)
                print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
                old_cash = float(client.fetch_balance()[stablecoin]['total'])
            except ccxt.ExchangeNotAvailable as e:
                time.sleep(.1)
                print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
                old_cash = float(client.fetch_balance()[stablecoin]['total'])
            except ccxt.AuthenticationError as e:
                time.sleep(.1)
                print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
                old_cash = float(client.fetch_balance()[stablecoin]['total'])
            except KeyError:
                old_cash = 0.0
                time.sleep(4)
            time.sleep(1.25)
            # Get Balances of each previously entered asset
            new_balance = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                try:
                    new_balance['balance_asset{0}'.format(x)] = float(
                        client.fetch_balance()[assets['asset{0}'.format(x)]]['total'])
                    time.sleep(3)
                except ccxt.DDoSProtection as e:
                    print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
                    time.sleep(2)
                    new_balance['balance_asset{0}'.format(x)] = float(
                        client.fetch_balance()[assets['asset{0}'.format(x)]]['total'])
                except ccxt.RequestTimeout as e:
                    time.sleep(.1)
                    print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
                    new_balance['balance_asset{0}'.format(x)] = float(
                        client.fetch_balance()[assets['asset{0}'.format(x)]]['total'])
                except ccxt.ExchangeNotAvailable as e:
                    time.sleep(.1)
                    print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
                    new_balance['balance_asset{0}'.format(x)] = float(
                        client.fetch_balance()[assets['asset{0}'.format(x)]]['total'])
                except ccxt.AuthenticationError as e:
                    time.sleep(.1)
                    print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
                    new_balance['balance_asset{0}'.format(x)] = float(
                        client.fetch_balance()[assets['asset{0}'.format(x)]]['total'])
                except KeyError:
                    new_balance['balance_asset{0}'.format(x)] = 0.0
                    time.sleep(4)
                time.sleep(1.25)

            old = {}

            for x in range(0, assetnum):
                x = str(x + 1)
                old['old_asset{0}'.format(x)] = new_balance['balance_asset{0}'.format(x)]

            olddata = {'old': old, 'old_cash': old_cash}

            with open('huobi/old.json', 'w') as outfile:
                json.dump(olddata, outfile)

            configcheck = 'configured'

            algorithm = input('Threshold or Periodic: ').upper()

            if algorithm == 'THRESHOLD':
                threshold = input("Algorithm Threshold= ")
                threshold = float(threshold)
                threshold = (.01 * threshold)
                configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck,
                                 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'algorithm': algorithm}
                with open('huobi/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)
            if algorithm == 'PERIODIC':
                period = input('Hourly, Daily, or Weekly: ').upper()
                configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'algorithm': algorithm}
                with open('huobi/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)
            else:
                print('Please check the spelling of' + " " + algorithm)
                exit(0)

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
            if stablecoin == 'USDT':
                stablecoin = 'USD'
            stablecoin = stablecoin.upper()
            symbol = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                symbol["symbol_asset{0}".format(x)] = str(assets["asset{0}".format(x)] + '/' + stablecoin)

            configcheck = 'configured'

            algorithm = config['algorithm']

            if algorithm == 'THRESHOLD':
                threshold = config['threshold']
                configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck,
                                 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'algorithm': algorithm}
                with open('huobi/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)
            if algorithm == 'PERIODIC':
                period = config['period']
                configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'algorithm': algorithm}
                with open('huobi/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)
            else:
                print('Please check the spelling of' + " " + algorithm)
                exit(0)


def balances():
    # Pull  balance for each selected asset
    global cash_balance
    global e
    # Cash Balance
    attempt = False
    while attempt is False:
        try:
            cash_balance = client.fetch_balance()[stablecoin]['total']
            attempt = True
        except ccxt.BaseError as e:
            pass
            time.sleep(2)
        except AttributeError:
            time.sleep(2)
            pass
        except ConnectionError:
            time.sleep(2)
            pass
        except KeyError as e:
            cash_balance = 0.0
            time.sleep(2)
            attempt = True
        time.sleep(1)
    # Get Balances of each previously entered asset
    balance = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        attempt = False
        while attempt is False:
            try:
                balance['balance_asset{0}'.format(x)] = float(client.fetch_balance()[assets['asset{0}'.format(x)]]['total'])
                attempt = True
            except ConnectionError:
                time.sleep(2)
                pass
            except KeyError as e:
                balance['balance_asset{0}'.format(x)] = 0.0
                time.sleep(2)
                attempt = True
            except AttributeError:
                time.sleep(2)
                pass
            except ccxt.BaseError as e:
                time.sleep(2)
                pass
        time.sleep(1)
    # save balances to json
    balance.update({'cash_balance': cash_balance})
    with open('huobi/balance.json', 'w') as outfile:
        json.dump(balance, outfile)


def prices():
    global price
    global e
    # Grabs prices from Coinbase Pro
    price = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        attempt = False
        while attempt is False:
            try:
                price["price_asset{0}".format(x)] = client.fetch_ticker(symbol["symbol_asset{0}".format(x)])['last']
                attempt = True
            except ConnectionError:
                time.sleep(2)
                pass
            except AttributeError:
                time.sleep(1)
                pass
            except ccxt.BaseError:
                time.sleep(1)
                pass
            time.sleep(1)
    # saves to json
    with open('huobi/prices.json', 'w') as outfile:
        json.dump(price, outfile)


def usd_value():
    # Calculates USD value of positions
    global usd
    global total_usd

    with open('huobi/balance.json') as json_file:
        balance = json.load(json_file)

    with open('huobi/prices.json') as json_file:
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


def sell_order(pair, sell_asset, current_price, asset):

    sell_asset = float(sell_asset)
    markets = client.fetch_markets()
    time.sleep(3)

    pairing = str(str(asset) + "/" + str(stablecoin))

    def minimums():
        for m in markets:
            if m['symbol'] == str(pairing):
                return float(m['limits']['amount']['min'])

    minimum = minimums()

    if sell_asset >= minimum:
        print("Selling" + " " + str(sell_asset) + " " + "of" + " " + pair)
        client.create_order(symbol=pair, type='market', side='sell', amount=sell_asset, price=current_price)
        time.sleep(1.25)


def buy_order(pair, buy_asset, current_price, asset):

    buy_asset = float(buy_asset)
    markets = client.fetch_markets()
    time.sleep(3)

    pairing = str(str(asset) + "/" + str(stablecoin))

    def minimums():
        for m in markets:
            if m['symbol'] == str(pairing):
                return float(m['limits']['amount']['min'])

    minimum = minimums()

    if buy_asset >= minimum:
        print("Buying" + " " + str(buy_asset) + " " + "of" + " " + pair)
        client.create_order(symbol=pair, type='market', side='buy', amount=buy_asset, price=current_price)
        time.sleep(1.25)

# MAIN


setup()

with open('huobi/config.json') as json_file:
    config = json.load(json_file)

api_key = config['API_KEY']
api_secret = config['API_SECRET']

client = ccxt.huobipro({'apiKey': api_key, 'secret': api_secret, 'enableRateLimit': True})

allocation = (.99 / assetnum)

with open('huobi/initial.json') as json_file:
    initial = json.load(json_file)
    initialcheck = initial['initialcheck']
with open('huobi/balance.json') as json_file:
    balance = json.load(json_file)
with open('huobi/prices.json') as json_file:
    price = json.load(json_file)

if initialcheck != 'done':
    initial = {}
    balances()
    for x in range(0, assetnum):
        x = str(x + 1)
        initial["initial_balance_asset{0}".format(x)] = float(balance["balance_asset{0}".format(x)])
    initialcheck = 'done'
    count = 0
    data = {'initial': initial,
            'initialcheck': initialcheck}
    data2 = {'count': count}

    with open('huobi/count.json', 'w') as outfile:
        json.dump(data2, outfile)

    with open('huobi/initial.json', 'w') as outfile:
        json.dump(data, outfile)

else:
    with open('huobi/count.json') as json_file:
        counts = json.load(json_file)
    count = int(counts['count'])
algorithm = config['algorithm']

if algorithm == 'THRESHOLD':

    threshold = config['threshold']

    while count < 99999:

        balances()

        prices()

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
            time.sleep(2)
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
                            sell_order(config['symbol']["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                                       price['price_asset{0}'.format(x)], config['assets']['asset{0}'.format(x)])

                for x in range(0, assetnum):
                    x = str(x + 1)
                    if sell["sell_asset{0}".format(x)] < 0:
                            sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                            buy_order(config['symbol']["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                                       price['price_asset{0}'.format(x)], config['assets']['asset{0}'.format(x)])

        time.sleep(3)
        balances()
        prices()
        usd_value()
        deviation()

        # Buy order trade trigger
        negative_threshold = (-1 * config['threshold'])
        for x in range(0, assetnum):
            x = str(x + 1)
            balances()
            usd_value()
            deviation()
            time.sleep(2)
            if dev["dev_asset{0}".format(x)] <= negative_threshold:

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
                            sellasset = ( -1 * buy["buy_asset{0}".format(x)])
                            sell_order(config['symbol']["symbol_asset{0}".format(x)], sellasset,
                                      price['price_asset{0}'.format(x)], config['assets']['asset{0}'.format(x)])

                for x in range(0, assetnum):
                    x = str(x + 1)
                    if buy["buy_asset{0}".format(x)] > 0:
                            buy_order(config['symbol']["symbol_asset{0}".format(x)], buy["buy_asset{0}".format(x)],
                              price['price_asset{0}'.format(x)], config['assets']['asset{0}'.format(x)])

        balances()
        prices()
        usd_value()
        deviation()

        # Record data every half day
        multiples = [n for n in range(1, 99999) if n % 1111 == 0]
        if count in multiples:
            # Checks for previous runs and calculates gain over initial allocation
            with open('huobi/performance.json') as json_file:
                performance = json.load(json_file)
                initialcheck2 = performance['initialcheck2']

            if initialcheck2 != 'done':

                compare = {}
                old = {}
                profit = {}

                for x in range(0, assetnum):
                    x = str(x + 1)
                    # calculate today's value of initial balances
                    compare["compare_asset{0}".format(x)] = (
                                initial['initial']["initial_balance_asset{0}".format(x)] *
                                price["price_asset{0}".format(x)])

                    # save current balances for future reference
                    old["old_asset{0}".format(x)] = balance["balance_asset{0}".format(x)]

                    # calculate profit of current usd value vs initial balance usd value
                    compare["compare_asset{0}".format(x)] = float(compare["compare_asset{0}".format(x)])
                    profit["profit_asset{0}".format(x)] = usd["usd_asset{0}".format(x)] - compare["compare_asset{0}".format(x)]
                old_cash = cash_balance

                # calculate profits of the small cash pool
                profit_cash = old_cash - cash_balance
                profit["current"] = 0

                # calculate current profits of the overall portfolio
                for x in range(0, assetnum):
                    x = str(x + 1)
                    profit["current"] = profit["current"] + profit["profit_asset{0}".format(x)]
                profit["current"] = profit["current"] + profit_cash

                # If portfolio > previous iteration, add to overall profit
                profit["overall"] = 0

                if profit["current"] >= 0:
                    profit["overall"] = profit["current"] + profit["overall"]

                initialcheck2 = 'done'

                data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                olddata = {'old': old, 'old_cash': old_cash}

                with open('huobi/old.json', 'w') as outfile:
                    json.dump(olddata, outfile)

                with open('huobi/performance.json', 'w') as outfile:
                    json.dump(data, outfile)
                # if not the initial setup, load previous iterations and calculate differences and profit
            else:
                with open('huobi/performance.json') as json_file:
                    performance = json.load(json_file)
                with open('huobi/old.json') as json_file:
                    oldload = json.load(json_file)
                compare = {}
                old = {}
                profit = {}

                for x in range(0, assetnum):
                    x = str(x + 1)
                    # call old asset balance from Performance and set as new old asset dict
                    old["old_asset{0}".format(x)] = oldload['old']["old_asset{0}".format(x)]

                    # calculate today's value of previous balances
                    compare["compare_asset{0}".format(x)] = (
                                old["old_asset{0}".format(x)] * price["price_asset{0}".format(x)])

                    # calculate profit of current usd value vs previous iteration balance usd value
                    compare["compare_asset{0}".format(x)] = float(compare["compare_asset{0}".format(x)])
                    profit["profit_asset{0}".format(x)] = (usd["usd_asset{0}".format(x)] - compare["compare_asset{0}".format(x)])
                old_cash = float(oldload['old_cash'])
                # calculate profit over previous cash pool
                profit_cash = cash_balance - old_cash

                # overwrite previous iteration balances save current balances for future reference
                for x in range(0, assetnum):
                    x = str(x + 1)
                    old["old_asset{0}".format(x)] = balance["balance_asset{0}".format(x)]

                # calculate current profits of the overall portfolio
                profit['current'] = 0
                for x in range(0, assetnum):
                    x = str(x + 1)
                    profit['current'] = profit['current'] + profit["profit_asset{0}".format(x)]
                profit['current'] = profit['current'] + profit_cash
                old_cash = cash_balance

                # If portfolio > previous iteration, add to overall profit
                profit['overall'] = performance['profit']['overall']
                initialcheck2 = 'done'
                if profit['current'] >= 0:
                    profit['overall'] = profit['current'] + profit['overall']

                    data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                    olddata = {'old': old, 'old_cash': old_cash}

                    with open('huobi/old.json', 'w') as outfile:
                        json.dump(olddata, outfile)

                    with open('huobi/performance.json', 'w') as outfile:
                        json.dump(data, outfile)

                else:
                    data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                    olddata = {'old': old, 'old_cash': old_cash}

                    with open('huobi/old.json', 'w') as outfile:
                        json.dump(olddata, outfile)

                    with open('huobi/performance.json', 'w') as outfile:
                        json.dump(data, outfile)

                # If profit due to the algorithm exceeds $100, donate X% to Nescience
                if performance['profit']['overall'] > 200:
                    # Sort Deviation for highest asset deviation and sell donation amount before buying equivalent ETH

                    hmm = list(sum(sorted(dev.items(), key=lambda x: x[1], reverse=True), ()))[0]

                    for a in assets:
                        if str('dev_' + a) == str(hmm):
                            print('Initiating Donation.')
                            donation_amount = (performance['profit']['overall'] * .10)

                            # Sell Highest Deviation
                            theasset = config['assets'][str(a)]

                            highest_asset = str(theasset + "/" + stablecoin)

                            try:
                                price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                                time.sleep(2)
                            except ccxt.base.errors.DDoSProtection as e:
                                print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
                                time.sleep(2)
                                price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                            except ccxt.base.errors.RequestTimeout as e:
                                time.sleep(1)
                                print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
                                price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                            except ccxt.base.errors.ExchangeNotAvailable as e:
                                time.sleep(1)
                                print(type(e).__name__, e.args,
                                      'Exchange Not Available due to downtime or maintenance (ignoring)')
                                price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                            except ccxt.base.errors.AuthenticationError as e:
                                time.sleep(1)
                                print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
                                price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                            time.sleep(1)

                            asset_amount = float(donation_amount / price_asset)
                            print('Donating' + ' ' + str(donation_amount) + " " + 'of' + ' ' + str(
                                performance['profit']['overall']) + " " + "dollars" + " " + "profit generated by this algorithm.")
                            sell_order(highest_asset, asset_amount, price_asset, theasset)

                            # Buy Eth
                            def stablecoincheck():
                                if stablecoin != 'ETH':
                                    eth_symbol = str('ETH' + "/" + stablecoin)
                                    try:
                                        price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                                        time.sleep(2)
                                    except ccxt.base.errors.DDoSProtection as e:
                                        print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
                                        time.sleep(2)
                                        price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                                    except ccxt.base.errors.RequestTimeout as e:
                                        time.sleep(1)
                                        print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
                                        price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                                    except ccxt.base.errors.ExchangeNotAvailable as e:
                                        time.sleep(1)
                                        print(type(e).__name__, e.args,
                                              'Exchange Not Available due to downtime or maintenance (ignoring)')
                                        price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                                    except ccxt.base.errors.AuthenticationError as e:
                                        time.sleep(1)
                                        print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
                                        price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                                    time.sleep(1)
                                    eth_amount = float((donation_amount / price_eth) * .95)
                                    buy_order(eth_symbol, eth_amount, price_eth, 'ETH')
                                    return eth_amount
                                else:
                                    eth_amount = (donation_amount * .99)
                                    return eth_amount
                            eth_amount = stablecoincheck()

                            # Withdraw Eth, requires Whitelist 0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C
                            eth_withdraw = eth_amount * .98
                            eth_withdraw = truncate(eth_withdraw, 6)
                            print("Withdrawing" + " " + str(eth_withdraw) + "ETH" + " " + "as a donation to the Developers / Nescience")
                            client.withdraw("ETH", eth_withdraw, "0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C")
                            # Set overall profit back to 0
                            overall_update = 0
                            profit.update({'overall': overall_update})
                            data.update({'profit': profit})
                            with open('huobi/performance.json', 'w') as outfile:
                                json.dump(data, outfile)

        count = count + 1
        if count == 95760:
            count = 0
        data3 = {'count': count}
        with open('huobi/count.json', 'w') as outfile:
            json.dump(data3, outfile)
        time.sleep(60)

if algorithm == 'PERIODIC':

    period = config['period']

    if period == 'HOURLY':

        while count < 99999:

            balances()

            prices()

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
                    sell_order(config['symbol']["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                               price['price_asset{0}'.format(x)], config['assets']['asset{0}'.format(x)])

            for x in range(0, assetnum):
                x = str(x + 1)
                if sell["sell_asset{0}".format(x)] < 0:
                    sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                    buy_order(config['symbol']["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                              price['price_asset{0}'.format(x)], config['assets']['asset{0}'.format(x)])

            balances()
            prices()
            usd_value()
            deviation()

            # Record data every half day
            multiples = [n for n in range(1, 99999) if n % 90 == 0]
            if count in multiples:
                # Checks for previous runs and calculates gain over initial allocation
                with open('huobi/performance.json') as json_file:
                    performance = json.load(json_file)
                    initialcheck2 = performance['initialcheck2']

                if initialcheck2 != 'done':

                    compare = {}
                    old = {}
                    profit = {}

                    for x in range(0, assetnum):
                        x = str(x + 1)
                        # calculate today's value of initial balances
                        compare["compare_asset{0}".format(x)] = (
                                initial['initial']["initial_balance_asset{0}".format(x)] *
                                price["price_asset{0}".format(x)])

                        # save current balances for future reference
                        old["old_asset{0}".format(x)] = balance["balance_asset{0}".format(x)]

                        # calculate profit of current usd value vs initial balance usd value
                        compare["compare_asset{0}".format(x)] = float(compare["compare_asset{0}".format(x)])
                        profit["profit_asset{0}".format(x)] = usd["usd_asset{0}".format(x)] - compare["compare_asset{0}".format(x)]
                    old_cash = cash_balance

                    # calculate profits of the small cash pool
                    profit_cash = old_cash - cash_balance
                    profit["current"] = 0

                    # calculate current profits of the overall portfolio
                    for x in range(0, assetnum):
                        x = str(x + 1)
                        profit["current"] = profit["current"] + profit["profit_asset{0}".format(x)]
                    profit["current"] = profit["current"] + profit_cash

                    # If portfolio > previous iteration, add to overall profit
                    profit["overall"] = 0

                    if profit["current"] >= 0:
                        profit["overall"] = profit["current"] + profit["overall"]

                    initialcheck2 = 'done'

                    data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                    olddata = {'old': old, 'old_cash': old_cash}

                    with open('huobi/old.json', 'w') as outfile:
                        json.dump(olddata, outfile)

                    with open('huobi/performance.json', 'w') as outfile:
                        json.dump(data, outfile)
                    # if not the initial setup, load previous iterations and calculate differences and profit
                else:
                    with open('huobi/performance.json') as json_file:
                        performance = json.load(json_file)
                    with open('huobi/old.json') as json_file:
                        oldload = json.load(json_file)
                    compare = {}
                    old = {}
                    profit = {}

                    for x in range(0, assetnum):
                        x = str(x + 1)
                        # call old asset balance from Performance and set as new old asset dict
                        old["old_asset{0}".format(x)] = oldload['old']["old_asset{0}".format(x)]

                        # calculate today's value of previous balances
                        compare["compare_asset{0}".format(x)] = (
                                old["old_asset{0}".format(x)] * price["price_asset{0}".format(x)])

                        # calculate profit of current usd value vs previous iteration balance usd value
                        compare["compare_asset{0}".format(x)] = float(compare["compare_asset{0}".format(x)])
                        profit["profit_asset{0}".format(x)] = (
                                    usd["usd_asset{0}".format(x)] - compare["compare_asset{0}".format(x)])
                    old_cash = float(oldload['old_cash'])
                    # calculate profit over previous cash pool
                    profit_cash = cash_balance - old_cash

                    # overwrite previous iteration balances save current balances for future reference
                    for x in range(0, assetnum):
                        x = str(x + 1)
                        old["old_asset{0}".format(x)] = balance["balance_asset{0}".format(x)]

                    # calculate current profits of the overall portfolio
                    profit['current'] = 0
                    for x in range(0, assetnum):
                        x = str(x + 1)
                        profit['current'] = profit['current'] + profit["profit_asset{0}".format(x)]
                    profit['current'] = profit['current'] + profit_cash
                    old_cash = cash_balance

                    # If portfolio > previous iteration, add to overall profit
                    profit['overall'] = performance['profit']['overall']
                    initialcheck2 = 'done'
                    if profit['current'] >= 0:
                        profit['overall'] = profit['current'] + profit['overall']

                        data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                        olddata = {'old': old, 'old_cash': old_cash}

                        with open('huobi/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('huobi/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    else:
                        data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                        olddata = {'old': old, 'old_cash': old_cash}

                        with open('huobi/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('huobi/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    # If profit due to the algorithm exceeds $100, donate X% to Nescience
                    if performance['profit']['overall'] > 200:
                        # Sort Deviation for highest asset deviation and sell donation amount before buying equivalent ETH

                        hmm = list(sum(sorted(dev.items(), key=lambda x: x[1], reverse=True), ()))[0]

                        for a in assets:
                            if str('dev_' + a) == str(hmm):
                                print('Initiating Donation.')
                                donation_amount = (performance['profit']['overall'] * .10)

                                # Sell Highest Deviation
                                theasset = config['assets'][str(a)]

                                highest_asset = str(theasset + "/" + stablecoin)

                                try:
                                    price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                                    time.sleep(2)
                                except ccxt.base.errors.DDoSProtection as e:
                                    print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
                                    time.sleep(2)
                                    price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                                except ccxt.base.errors.RequestTimeout as e:
                                    time.sleep(1)
                                    print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
                                    price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                                except ccxt.base.errors.ExchangeNotAvailable as e:
                                    time.sleep(1)
                                    print(type(e).__name__, e.args,
                                          'Exchange Not Available due to downtime or maintenance (ignoring)')
                                    price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                                except ccxt.base.errors.AuthenticationError as e:
                                    time.sleep(1)
                                    print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
                                    price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                                time.sleep(1)

                                asset_amount = float(donation_amount / price_asset)
                                print('Donating' + ' ' + str(donation_amount) + " " + 'of' + ' ' + str(
                                    performance['profit'][
                                        'overall']) + " " + "dollars" + " " + "profit generated by this algorithm.")
                                sell_order(highest_asset, asset_amount, price_asset, theasset)


                                # Buy Eth
                                def stablecoincheck():
                                    if stablecoin != 'ETH':
                                        eth_symbol = str('ETH' + "/" + stablecoin)
                                        try:
                                            price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                                            time.sleep(2)
                                        except ccxt.base.errors.DDoSProtection as e:
                                            print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
                                            time.sleep(2)
                                            price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                                        except ccxt.base.errors.RequestTimeout as e:
                                            time.sleep(1)
                                            print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
                                            price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                                        except ccxt.base.errors.ExchangeNotAvailable as e:
                                            time.sleep(1)
                                            print(type(e).__name__, e.args,
                                                  'Exchange Not Available due to downtime or maintenance (ignoring)')
                                            price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                                        except ccxt.base.errors.AuthenticationError as e:
                                            time.sleep(1)
                                            print(type(e).__name__, e.args,
                                                  'Authentication Error (missing API keys, ignoring)')
                                            price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                                        time.sleep(1)
                                        eth_amount = float((donation_amount / price_eth) * .95)
                                        buy_order(eth_symbol, eth_amount, price_eth, 'ETH')
                                        return eth_amount
                                    else:
                                        eth_amount = (donation_amount * .99)
                                        return eth_amount


                                eth_amount = stablecoincheck()

                                # Withdraw Eth, requires Whitelist 0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C
                                eth_withdraw = eth_amount * .98
                                eth_withdraw = truncate(eth_withdraw, 6)
                                print("Withdrawing" + " " + str(
                                    eth_withdraw) + "ETH" + " " + "as a donation to the Developers / Nescience")
                                client.withdraw("ETH", eth_withdraw, "0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C")
                                # Set overall profit back to 0
                                overall_update = 0
                                profit.update({'overall': overall_update})
                                data.update({'profit': profit})
                                with open('huobi/performance.json', 'w') as outfile:
                                    json.dump(data, outfile)

            count = count + 1
            if count == 95760:
                count = 0
            data3 = {'count': count}
            with open('huobi/count.json', 'w') as outfile:
                json.dump(data3, outfile)
            time.sleep(3600)

    if period == 'DAILY':

        while count < 99999:

            balances()

            prices()

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
                    sell_order(config['symbol']["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                               price['price_asset{0}'.format(x)], config['assets']['asset{0}'.format(x)])

            for x in range(0, assetnum):
                x = str(x + 1)
                if sell["sell_asset{0}".format(x)] < 0:
                    sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                    buy_order(config['symbol']["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                              price['price_asset{0}'.format(x)], config['assets']['asset{0}'.format(x)])

            balances()
            prices()
            usd_value()
            deviation()

            # Record data every half day
            multiples = [n for n in range(1, 99999) if n % 4 == 0]
            if count in multiples:
                # Checks for previous runs and calculates gain over initial allocation
                with open('huobi/performance.json') as json_file:
                    performance = json.load(json_file)
                    initialcheck2 = performance['initialcheck2']

                if initialcheck2 != 'done':

                    compare = {}
                    old = {}
                    profit = {}

                    for x in range(0, assetnum):
                        x = str(x + 1)
                        # calculate today's value of initial balances
                        compare["compare_asset{0}".format(x)] = (
                                initial['initial']["initial_balance_asset{0}".format(x)] *
                                price["price_asset{0}".format(x)])

                        # save current balances for future reference
                        old["old_asset{0}".format(x)] = balance["balance_asset{0}".format(x)]

                        # calculate profit of current usd value vs initial balance usd value
                        compare["compare_asset{0}".format(x)] = float(compare["compare_asset{0}".format(x)])
                        profit["profit_asset{0}".format(x)] = usd["usd_asset{0}".format(x)] - compare[
                            "compare_asset{0}".format(x)]
                    old_cash = cash_balance

                    # calculate profits of the small cash pool
                    profit_cash = old_cash - cash_balance
                    profit["current"] = 0

                    # calculate current profits of the overall portfolio
                    for x in range(0, assetnum):
                        x = str(x + 1)
                        profit["current"] = profit["current"] + profit["profit_asset{0}".format(x)]
                    profit["current"] = profit["current"] + profit_cash

                    # If portfolio > previous iteration, add to overall profit
                    profit["overall"] = 0

                    if profit["current"] >= 0:
                        profit["overall"] = profit["current"] + profit["overall"]

                    initialcheck2 = 'done'

                    data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                    olddata = {'old': old, 'old_cash': old_cash}

                    with open('huobi/old.json', 'w') as outfile:
                        json.dump(olddata, outfile)

                    with open('huobi/performance.json', 'w') as outfile:
                        json.dump(data, outfile)
                    # if not the initial setup, load previous iterations and calculate differences and profit
                else:
                    with open('huobi/performance.json') as json_file:
                        performance = json.load(json_file)
                    with open('huobi/old.json') as json_file:
                        oldload = json.load(json_file)
                    compare = {}
                    old = {}
                    profit = {}

                    for x in range(0, assetnum):
                        x = str(x + 1)
                        # call old asset balance from Performance and set as new old asset dict
                        old["old_asset{0}".format(x)] = oldload['old']["old_asset{0}".format(x)]

                        # calculate today's value of previous balances
                        compare["compare_asset{0}".format(x)] = (
                                old["old_asset{0}".format(x)] * price["price_asset{0}".format(x)])

                        # calculate profit of current usd value vs previous iteration balance usd value
                        compare["compare_asset{0}".format(x)] = float(compare["compare_asset{0}".format(x)])
                        profit["profit_asset{0}".format(x)] = (
                                usd["usd_asset{0}".format(x)] - compare["compare_asset{0}".format(x)])
                    old_cash = float(oldload['old_cash'])
                    # calculate profit over previous cash pool
                    profit_cash = cash_balance - old_cash

                    # overwrite previous iteration balances save current balances for future reference
                    for x in range(0, assetnum):
                        x = str(x + 1)
                        old["old_asset{0}".format(x)] = balance["balance_asset{0}".format(x)]

                    # calculate current profits of the overall portfolio
                    profit['current'] = 0
                    for x in range(0, assetnum):
                        x = str(x + 1)
                        profit['current'] = profit['current'] + profit["profit_asset{0}".format(x)]
                    profit['current'] = profit['current'] + profit_cash
                    old_cash = cash_balance

                    # If portfolio > previous iteration, add to overall profit
                    profit['overall'] = performance['profit']['overall']
                    initialcheck2 = 'done'
                    if profit['current'] >= 0:
                        profit['overall'] = profit['current'] + profit['overall']

                        data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                        olddata = {'old': old, 'old_cash': old_cash}

                        with open('huobi/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('huobi/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    else:
                        data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                        olddata = {'old': old, 'old_cash': old_cash}

                        with open('huobi/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('huobi/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    # If profit due to the algorithm exceeds $100, donate X% to Nescience
                    if performance['profit']['overall'] > 200:
                        # Sort Deviation for highest asset deviation and sell donation amount before buying equivalent ETH

                        hmm = list(sum(sorted(dev.items(), key=lambda x: x[1], reverse=True), ()))[0]

                        for a in assets:
                            if str('dev_' + a) == str(hmm):
                                print('Initiating Donation.')
                                donation_amount = (performance['profit']['overall'] * .10)

                                # Sell Highest Deviation
                                theasset = config['assets'][str(a)]

                                highest_asset = str(theasset + "/" + stablecoin)

                                try:
                                    price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                                    time.sleep(2)
                                except ccxt.base.errors.DDoSProtection as e:
                                    print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
                                    time.sleep(2)
                                    price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                                except ccxt.base.errors.RequestTimeout as e:
                                    time.sleep(1)
                                    print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
                                    price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                                except ccxt.base.errors.ExchangeNotAvailable as e:
                                    time.sleep(1)
                                    print(type(e).__name__, e.args,
                                          'Exchange Not Available due to downtime or maintenance (ignoring)')
                                    price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                                except ccxt.base.errors.AuthenticationError as e:
                                    time.sleep(1)
                                    print(type(e).__name__, e.args,
                                          'Authentication Error (missing API keys, ignoring)')
                                    price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                                time.sleep(1)

                                asset_amount = float(donation_amount / price_asset)
                                print('Donating' + ' ' + str(donation_amount) + " " + 'of' + ' ' + str(
                                    performance['profit'][
                                        'overall']) + " " + "dollars" + " " + "profit generated by this algorithm.")
                                sell_order(highest_asset, asset_amount, price_asset, theasset)


                                # Buy Eth
                                def stablecoincheck():
                                    if stablecoin != 'ETH':
                                        eth_symbol = str('ETH' + "/" + stablecoin)
                                        try:
                                            price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                                            time.sleep(2)
                                        except ccxt.base.errors.DDoSProtection as e:
                                            print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
                                            time.sleep(2)
                                            price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                                        except ccxt.base.errors.RequestTimeout as e:
                                            time.sleep(1)
                                            print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
                                            price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                                        except ccxt.base.errors.ExchangeNotAvailable as e:
                                            time.sleep(1)
                                            print(type(e).__name__, e.args,
                                                  'Exchange Not Available due to downtime or maintenance (ignoring)')
                                            price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                                        except ccxt.base.errors.AuthenticationError as e:
                                            time.sleep(1)
                                            print(type(e).__name__, e.args,
                                                  'Authentication Error (missing API keys, ignoring)')
                                            price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                                        time.sleep(1)
                                        eth_amount = float((donation_amount / price_eth) * .95)
                                        buy_order(eth_symbol, eth_amount, price_eth, 'ETH')
                                        return eth_amount
                                    else:
                                        eth_amount = (donation_amount * .99)
                                        return eth_amount


                                eth_amount = stablecoincheck()

                                # Withdraw Eth, requires Whitelist 0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C
                                eth_withdraw = eth_amount * .98
                                eth_withdraw = truncate(eth_withdraw, 6)
                                print("Withdrawing" + " " + str(
                                    eth_withdraw) + "ETH" + " " + "as a donation to the Developers / Nescience")
                                client.withdraw("ETH", eth_withdraw, "0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C")
                                # Set overall profit back to 0
                                overall_update = 0
                                profit.update({'overall': overall_update})
                                data.update({'profit': profit})
                                with open('huobi/performance.json', 'w') as outfile:
                                    json.dump(data, outfile)

            count = count + 1
            if count == 95760:
                count = 0
            data3 = {'count': count}
            with open('huobi/count.json', 'w') as outfile:
                json.dump(data3, outfile)
            time.sleep(86400)

    if period == 'WEEKLY':

        while count < 99999:

            balances()

            prices()

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
                    sell_order(config['symbol']["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                               price['price_asset{0}'.format(x)], config['assets']['asset{0}'.format(x)])

            for x in range(0, assetnum):
                x = str(x + 1)
                if sell["sell_asset{0}".format(x)] < 0:
                    sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                    buy_order(config['symbol']["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                              price['price_asset{0}'.format(x)], config['assets']['asset{0}'.format(x)])

            balances()
            prices()
            usd_value()
            deviation()

            # Record data every half day
            multiples = [n for n in range(1, 99999) if n % 1 == 0]
            if count in multiples:
                # Checks for previous runs and calculates gain over initial allocation
                with open('huobi/performance.json') as json_file:
                    performance = json.load(json_file)
                    initialcheck2 = performance['initialcheck2']

                if initialcheck2 != 'done':

                    compare = {}
                    old = {}
                    profit = {}

                    for x in range(0, assetnum):
                        x = str(x + 1)
                        # calculate today's value of initial balances
                        compare["compare_asset{0}".format(x)] = (
                                initial['initial']["initial_balance_asset{0}".format(x)] *
                                price["price_asset{0}".format(x)])

                        # save current balances for future reference
                        old["old_asset{0}".format(x)] = balance["balance_asset{0}".format(x)]

                        # calculate profit of current usd value vs initial balance usd value
                        compare["compare_asset{0}".format(x)] = float(compare["compare_asset{0}".format(x)])
                        profit["profit_asset{0}".format(x)] = usd["usd_asset{0}".format(x)] - compare["compare_asset{0}".format(x)]
                    old_cash = cash_balance

                    # calculate profits of the small cash pool
                    profit_cash = old_cash - cash_balance
                    profit["current"] = 0

                    # calculate current profits of the overall portfolio
                    for x in range(0, assetnum):
                        x = str(x + 1)
                        profit["current"] = profit["current"] + profit["profit_asset{0}".format(x)]
                    profit["current"] = profit["current"] + profit_cash

                    # If portfolio > previous iteration, add to overall profit
                    profit["overall"] = 0

                    if profit["current"] >= 0:
                        profit["overall"] = profit["current"] + profit["overall"]

                    initialcheck2 = 'done'

                    data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                    olddata = {'old': old, 'old_cash': old_cash}

                    with open('huobi/old.json', 'w') as outfile:
                        json.dump(olddata, outfile)

                    with open('huobi/performance.json', 'w') as outfile:
                        json.dump(data, outfile)
                    # if not the initial setup, load previous iterations and calculate differences and profit
                else:
                    with open('huobi/performance.json') as json_file:
                        performance = json.load(json_file)
                    with open('huobi/old.json') as json_file:
                        oldload = json.load(json_file)
                    compare = {}
                    old = {}
                    profit = {}

                    for x in range(0, assetnum):
                        x = str(x + 1)
                        # call old asset balance from Performance and set as new old asset dict
                        old["old_asset{0}".format(x)] = oldload['old']["old_asset{0}".format(x)]

                        # calculate today's value of previous balances
                        compare["compare_asset{0}".format(x)] = (
                                old["old_asset{0}".format(x)] * price["price_asset{0}".format(x)])

                        # calculate profit of current usd value vs previous iteration balance usd value
                        compare["compare_asset{0}".format(x)] = float(compare["compare_asset{0}".format(x)])
                        profit["profit_asset{0}".format(x)] = (
                                    usd["usd_asset{0}".format(x)] - compare["compare_asset{0}".format(x)])
                    old_cash = float(oldload['old_cash'])
                    # calculate profit over previous cash pool
                    profit_cash = cash_balance - old_cash

                    # overwrite previous iteration balances save current balances for future reference
                    for x in range(0, assetnum):
                        x = str(x + 1)
                        old["old_asset{0}".format(x)] = balance["balance_asset{0}".format(x)]

                    # calculate current profits of the overall portfolio
                    profit['current'] = 0
                    for x in range(0, assetnum):
                        x = str(x + 1)
                        profit['current'] = profit['current'] + profit["profit_asset{0}".format(x)]
                    profit['current'] = profit['current'] + profit_cash
                    old_cash = cash_balance

                    # If portfolio > previous iteration, add to overall profit
                    profit['overall'] = performance['profit']['overall']
                    initialcheck2 = 'done'
                    if profit['current'] >= 0:
                        profit['overall'] = profit['current'] + profit['overall']

                        data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                        olddata = {'old': old, 'old_cash': old_cash}

                        with open('huobi/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('huobi/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    else:
                        data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                        olddata = {'old': old, 'old_cash': old_cash}

                        with open('huobi/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('huobi/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    # If profit due to the algorithm exceeds $100, donate X% to Nescience
                    if performance['profit']['overall'] > 200:
                        # Sort Deviation for highest asset deviation and sell donation amount before buying equivalent ETH

                        hmm = list(sum(sorted(dev.items(), key=lambda x: x[1], reverse=True), ()))[0]

                        for a in assets:
                            if str('dev_' + a) == str(hmm):
                                print('Initiating Donation.')
                                donation_amount = (performance['profit']['overall'] * .10)

                                # Sell Highest Deviation
                                theasset = config['assets'][str(a)]

                                highest_asset = str(theasset + "/" + stablecoin)

                                try:
                                    price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                                    time.sleep(2)
                                except ccxt.base.errors.DDoSProtection as e:
                                    print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
                                    time.sleep(2)
                                    price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                                except ccxt.base.errors.RequestTimeout as e:
                                    time.sleep(1)
                                    print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
                                    price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                                except ccxt.base.errors.ExchangeNotAvailable as e:
                                    time.sleep(1)
                                    print(type(e).__name__, e.args,
                                          'Exchange Not Available due to downtime or maintenance (ignoring)')
                                    price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                                except ccxt.base.errors.AuthenticationError as e:
                                    time.sleep(1)
                                    print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
                                    price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                                time.sleep(1)

                                asset_amount = float(donation_amount / price_asset)
                                print('Donating' + ' ' + str(donation_amount) + " " + 'of' + ' ' + str(
                                    performance['profit'][
                                        'overall']) + " " + "dollars" + " " + "profit generated by this algorithm.")
                                sell_order(highest_asset, asset_amount, price_asset, theasset)


                                # Buy Eth
                                def stablecoincheck():
                                    if stablecoin != 'ETH':
                                        eth_symbol = str('ETH' + "/" + stablecoin)
                                        try:
                                            price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                                            time.sleep(2)
                                        except ccxt.base.errors.DDoSProtection as e:
                                            print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
                                            time.sleep(2)
                                            price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                                        except ccxt.base.errors.RequestTimeout as e:
                                            time.sleep(1)
                                            print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
                                            price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                                        except ccxt.base.errors.ExchangeNotAvailable as e:
                                            time.sleep(1)
                                            print(type(e).__name__, e.args,
                                                  'Exchange Not Available due to downtime or maintenance (ignoring)')
                                            price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                                        except ccxt.base.errors.AuthenticationError as e:
                                            time.sleep(1)
                                            print(type(e).__name__, e.args,
                                                  'Authentication Error (missing API keys, ignoring)')
                                            price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                                        time.sleep(1)
                                        eth_amount = float((donation_amount / price_eth) * .95)
                                        buy_order(eth_symbol, eth_amount, price_eth, 'ETH')
                                        return eth_amount
                                    else:
                                        eth_amount = (donation_amount * .99)
                                        return eth_amount


                                eth_amount = stablecoincheck()

                                # Withdraw Eth, requires Whitelist 0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C
                                eth_withdraw = eth_amount * .98
                                eth_withdraw = truncate(eth_withdraw, 6)
                                print("Withdrawing" + " " + str(
                                    eth_withdraw) + "ETH" + " " + "as a donation to the Developers / Nescience")
                                client.withdraw("ETH", eth_withdraw, "0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C")
                                # Set overall profit back to 0
                                overall_update = 0
                                profit.update({'overall': overall_update})
                                data.update({'profit': profit})
                                with open('huobi/performance.json', 'w') as outfile:
                                    json.dump(data, outfile)

            count = count + 1
            if count == 95760:
                count = 0
            data3 = {'count': count}
            with open('huobi/count.json', 'w') as outfile:
                json.dump(data3, outfile)
            time.sleep(604800)