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
        API_KEY = input('API KEY:')
        API_SECRET = input('API SECRET:')
        API_PASSPHRASE = input('API PASSPHRASE:')
        assetnum = input('Number of Assets in the Portfolio:')
        assetnum = int(assetnum)
        stablecoin = input('What currency would you like to trade against: ')
        stablecoin = stablecoin.upper()
        for x in range(0, assetnum):
            x = str(x + 1)
            assets["asset{0}".format(x)] = input('asset' + " " + x + ':')
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
            configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum,
                             'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY, 'API_SECRET': API_SECRET,
                             'algorithm': algorithm, 'API PASSPHRASE': API_PASSPHRASE}
            with open('kucoin/config.json', 'w') as outfile:
                json.dump(configuration, outfile)
        if algorithm == 'PERIODIC':
            period = input('Hourly, Daily, or Weekly: ').upper()
            configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                             'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY, 'API_SECRET': API_SECRET,
                             'algorithm': algorithm, 'API PASSPHRASE': API_PASSPHRASE}
            with open('kucoin/config.json', 'w') as outfile:
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
            API_PASSPHRASE = input('API PASSPHRASE:')
            assetnum = input('Number of Assets in the Portfolio:')
            assetnum = int(assetnum)
            stablecoin = input('What currency would you like to trade against: ')
            stablecoin = stablecoin.upper()

            for x in range(0, assetnum):
                x = str(x + 1)
                assets["asset{0}".format(x)] = input('asset' + " " + x + ':')
                assets["asset{0}".format(x)] = assets["asset{0}".format(x)].upper()

            symbol = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                symbol["symbol_asset{0}".format(x)] = str(assets["asset{0}".format(x)] + '-' + stablecoin)

            client = Client(API_KEY, API_SECRET, API_PASSPHRASE)

            try:
                new_balances = client.get_accounts()
            except OSError:
                time.sleep(2)
                new_balances = client.get_accounts()

            # Balance USD

            def oldcash():
                cash = {}
                for b in new_balances:
                    if b['currency'] == stablecoin and b['type'] == 'trade':
                        cash['old_cash'] = [b['balance']][0]
                        old_cash = float(cash['old_cash'])
                        return old_cash
                    if stablecoin not in cash:
                        old_cash = 0
                        return old_cash
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
                old['old_asset{0}'.format(x)] = new_balance['balance_asset{0}'.format(x)]

            olddata = {'old': old, 'old_cash': old_cash}

            with open('kucoin/old.json', 'w') as outfile:
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
                                 'algorithm': algorithm, 'API PASSPHRASE': API_PASSPHRASE}
                with open('kucoin/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)
            if algorithm == 'PERIODIC':
                period = input('Hourly, Daily, or Weekly: ').upper()
                configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'algorithm': algorithm, 'API PASSPHRASE': API_PASSPHRASE}
                with open('kucoin/config.json', 'w') as outfile:
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
                configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck,
                                 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'algorithm': algorithm, 'API PASSPHRASE': API_PASSPHRASE}
                with open('kucoin/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)
            if algorithm == 'PERIODIC':
                period = config['period']
                configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'algorithm': algorithm, 'API PASSPHRASE': API_PASSPHRASE}
                with open('kucoin/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)


def balances():
    # Pull  balance for each selected asset
    global cash_balance

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
    cash = {}
    for b in balances:
        if b['currency'] == stablecoin and b['type'] == 'trade':
            cash['cash_balance'] = [b['balance']][0]
            cash_balance = float(cash['cash_balance'])
        if stablecoin not in cash:
            cash_balance = 0
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
    total_balance = {'balance': balance, 'cash_balance': cash_balance}
    with open('kucoin/balance.json', 'w') as outfile:
        json.dump(total_balance, outfile)


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
        usd["usd_asset{0}".format(x)] = float(balance['balance']["balance_asset{0}".format(x)]) * float(price["price_asset{0}".format(x)])

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
with open('Kucoin/balance.json') as json_file:
    balance = json.load(json_file)
with open('Kucoin/prices.json') as json_file:
    price = json.load(json_file)

if initialcheck != 'done':
    initial = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        initial["initial_balance_asset{0}".format(x)] = float(balance['balance']["balance_asset{0}".format(x)])
    initialcheck = 'done'
    count = 0
    data = {'initial': initial,
            'initialcheck': initialcheck}
    data2 = {'count': count}

    with open('kucoin/count.json', 'w') as outfile:
        json.dump(data2, outfile)

    with open('kucoin/initial.json', 'w') as outfile:
        json.dump(data, outfile)

else:
    with open('kucoin/count.json') as json_file:
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

        # Record data every half day
        multiples = [n for n in range(1, 99999) if n % 4000 == 0]
        if count in multiples:
            # Checks for previous runs and calculates gain over initial allocation
            with open('kucoin/performance.json') as json_file:
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
                    old["old_asset{0}".format(x)] = balance['balance']["balance_asset{0}".format(x)]

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

                with open('kucoin/old.json', 'w') as outfile:
                    json.dump(olddata, outfile)

                with open('kucoin/performance.json', 'w') as outfile:
                    json.dump(data, outfile)
                # if not the initial setup, load previous iterations and calculate differences and profit
            else:
                with open('kucoin/performance.json') as json_file:
                    performance = json.load(json_file)
                with open('kucoin/old.json') as json_file:
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
                    old["old_asset{0}".format(x)] = balance['balance']["balance_asset{0}".format(x)]

                # calculate current profits of the overall portfolio
                profit['current'] = 0
                for x in range(0, assetnum):
                    x = str(x + 1)
                    profit['current'] = profit['current'] + profit["profit_asset{0}".format(x)]
                profit['current'] = profit['current'] + profit_cash
                old_cash = balance['cash_balance']

                # If portfolio > previous iteration, add to overall profit
                profit['overall'] = performance['profit']['overall']
                initialcheck2 = 'done'
                if profit['current'] >= 0:
                    profit['overall'] = profit['current'] + profit['overall']

                    data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                    olddata = {'old': old, 'old_cash': old_cash}

                    with open('kucoin/old.json', 'w') as outfile:
                        json.dump(olddata, outfile)

                    with open('kucoin/performance.json', 'w') as outfile:
                        json.dump(data, outfile)

                else:
                    data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                    olddata = {'old': old, 'old_cash': old_cash}

                    with open('kucoin/old.json', 'w') as outfile:
                        json.dump(olddata, outfile)

                    with open('kucoin/performance.json', 'w') as outfile:
                        json.dump(data, outfile)

                # If profit due to the algorithm exceeds $100, donate X% to Nescience
                if profit['overall'] > 200:

                    # Sort Deviation for highest asset deviation and sell donation amount  in that asset before buying equivalent ETH

                    hmm = list(sum(sorted(dev.items(), key=lambda x: x[1], reverse=True), ()))[0]

                    assets = config['assets']

                    for a in assets:
                        if str('dev_'+a) == str(hmm):
                            print('Initiating Donation.')
                            donation_amount = (performance['profit']['overall'] * .10)

                            # Sell Highest Deviation
                            the_asset = config['assets'][str(a)]
                            highest_asset = str(the_asset + '-' + stablecoin)
                            print(highest_asset)
                            price_asset = float(client.get_ticker(symbol=highest_asset)['price'])
                            asset_amount = float(donation_amount / price_asset)
                            print('Donating' + ' ' + str(donation_amount) + 'of' + ' ' + str(
                                profit['overall']) + " " + "dollars" + " " + "profit generated by this algorithm.")
                            sell_order(highest_asset, asset_amount, price_asset, highest_asset)

                            # Buy Eth
                            def stablecoincheck():
                                if stablecoin != 'ETH':
                                    eth_symbol = str('ETH' + '-' + stablecoin)
                                    price_eth = float(client.get_ticker(symbol=eth_symbol)['price'])
                                    eth_amount = float((donation_amount / price_eth) * .98)
                                    buy_order(eth_symbol, eth_amount, price_eth)
                                    return eth_amount
                                else:
                                    eth_amount = (donation_amount * .99)
                                    return eth_amount
                            eth_amount = stablecoincheck()

                            # Withdrawal amount final
                            eth_withdraw = eth_amount * .98
                            eth_withdraw = truncate(eth_withdraw, 6)

                            # Transfer to Main Wallet
                            accounts = client.get_accounts()

                            def tradeaccount():
                                for a in accounts:
                                    if a['type'] == 'trade' and a['currency'] == 'ETH':
                                        return a['id']

                            tradeacc = tradeaccount()

                            def mainaccount():
                                for a in accounts:
                                    if a['type'] == 'main' and a['currency'] == 'ETH':
                                        return a['id']

                            mainacc = mainaccount()

                            client.create_inner_transfer(str(tradeacc), str(mainacc), eth_withdraw)

                            # Withdraw Eth
                            print("Withdrawing" + " " + str(eth_withdraw) + "ETH" + " " + "as a donation to the Developers / Nescience")
                            try:
                                withdrawal = client.create_withdrawal('ETH', eth_withdraw, '0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C')

                            except OSError:
                                time.sleep(5)
                                withdrawal = client.create_withdrawal('ETH', eth_withdraw,
                                                                      '0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C')
                            # Set overall profit back to 0
                            overall_update = 0
                            profit.update({'overall': overall_update})
                            data.update({'profit': profit})
                            with open('kucoin/performance.json', 'w') as outfile:
                                json.dump(data, outfile)

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

            # Record data every half day
            multiples = [n for n in range(1, 99999) if n % 90 == 0]
            if count in multiples:
                # Checks for previous runs and calculates gain over initial allocation
                with open('kucoin/performance.json') as json_file:
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
                        old["old_asset{0}".format(x)] = balance['balance']["balance_asset{0}".format(x)]

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

                    with open('kucoin/old.json', 'w') as outfile:
                        json.dump(olddata, outfile)

                    with open('kucoin/performance.json', 'w') as outfile:
                        json.dump(data, outfile)
                    # if not the initial setup, load previous iterations and calculate differences and profit
                else:
                    with open('kucoin/performance.json') as json_file:
                        performance = json.load(json_file)
                    with open('kucoin/old.json') as json_file:
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
                        old["old_asset{0}".format(x)] = balance['balance']["balance_asset{0}".format(x)]

                    # calculate current profits of the overall portfolio
                    profit['current'] = 0
                    for x in range(0, assetnum):
                        x = str(x + 1)
                        profit['current'] = profit['current'] + profit["profit_asset{0}".format(x)]
                    profit['current'] = profit['current'] + profit_cash
                    old_cash = balance['cash_balance']

                    # If portfolio > previous iteration, add to overall profit
                    profit['overall'] = performance['profit']['overall']
                    initialcheck2 = 'done'
                    if profit['current'] >= 0:
                        profit['overall'] = profit['current'] + profit['overall']

                        data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                        olddata = {'old': old, 'old_cash': old_cash}

                        with open('kucoin/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('kucoin/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    else:
                        data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                        olddata = {'old': old, 'old_cash': old_cash}

                        with open('kucoin/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('kucoin/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    # If profit due to the algorithm exceeds $100, donate X% to Nescience
                    if profit['overall'] > 200:

                        # Sort Deviation for highest asset deviation and sell donation amount  in that asset before buying equivalent ETH

                        hmm = list(sum(sorted(dev.items(), key=lambda x: x[1], reverse=True), ()))[0]

                        assets = config['assets']

                        for a in assets:
                            if str('dev_' + a) == str(hmm):
                                print('Initiating Donation.')
                                donation_amount = (performance['profit']['overall'] * .10)

                                # Sell Highest Deviation
                                the_asset = config['assets'][str(a)]
                                highest_asset = str(the_asset + '-' + stablecoin)
                                print(highest_asset)
                                price_asset = float(client.get_ticker(symbol=highest_asset)['price'])
                                asset_amount = float(donation_amount / price_asset)
                                print('Donating' + ' ' + str(donation_amount) + 'of' + ' ' + str(
                                    profit['overall']) + " " + "dollars" + " " + "profit generated by this algorithm.")
                                sell_order(highest_asset, asset_amount, price_asset, highest_asset)

                                # Buy Eth
                                def stablecoincheck():
                                    if stablecoin != 'ETH':
                                        eth_symbol = str('ETH' + '-' + stablecoin)
                                        price_eth = float(client.get_ticker(symbol=eth_symbol)['price'])
                                        eth_amount = float((donation_amount / price_eth) * .98)
                                        buy_order(eth_symbol, eth_amount, price_eth)
                                        return eth_amount
                                    else:
                                        eth_amount = (donation_amount * .99)
                                        return eth_amount


                                eth_amount = stablecoincheck()

                                # Withdrawal amount final
                                eth_withdraw = eth_amount * .98
                                eth_withdraw = truncate(eth_withdraw, 6)

                                # Transfer to Main Wallet
                                accounts = client.get_accounts()


                                def tradeaccount():
                                    for a in accounts:
                                        if a['type'] == 'trade' and a['currency'] == 'ETH':
                                            return a['id']


                                tradeacc = tradeaccount()


                                def mainaccount():
                                    for a in accounts:
                                        if a['type'] == 'main' and a['currency'] == 'ETH':
                                            return a['id']


                                mainacc = mainaccount()

                                client.create_inner_transfer(str(tradeacc), str(mainacc), eth_withdraw)

                                # Withdraw Eth
                                print("Withdrawing" + " " + str(
                                    eth_withdraw) + "ETH" + " " + "as a donation to the Developers / Nescience")
                                try:
                                    withdrawal = client.create_withdrawal('ETH', eth_withdraw,
                                                                          '0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C')

                                except OSError:
                                    time.sleep(5)
                                    withdrawal = client.create_withdrawal('ETH', eth_withdraw,
                                                                          '0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C')
                                # Set overall profit back to 0
                                overall_update = 0
                                profit.update({'overall': overall_update})
                                data.update({'profit': profit})
                                with open('kucoin/performance.json', 'w') as outfile:
                                    json.dump(data, outfile)

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

            # Record data every half day
            multiples = [n for n in range(1, 99999) if n % 4 == 0]
            if count in multiples:
                # Checks for previous runs and calculates gain over initial allocation
                with open('kucoin/performance.json') as json_file:
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
                        old["old_asset{0}".format(x)] = balance['balance']["balance_asset{0}".format(x)]

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

                    with open('kucoin/old.json', 'w') as outfile:
                        json.dump(olddata, outfile)

                    with open('kucoin/performance.json', 'w') as outfile:
                        json.dump(data, outfile)
                    # if not the initial setup, load previous iterations and calculate differences and profit
                else:
                    with open('kucoin/performance.json') as json_file:
                        performance = json.load(json_file)
                    with open('kucoin/old.json') as json_file:
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
                        old["old_asset{0}".format(x)] = balance['balance']["balance_asset{0}".format(x)]

                    # calculate current profits of the overall portfolio
                    profit['current'] = 0
                    for x in range(0, assetnum):
                        x = str(x + 1)
                        profit['current'] = profit['current'] + profit["profit_asset{0}".format(x)]
                    profit['current'] = profit['current'] + profit_cash
                    old_cash = balance['cash_balance']

                    # If portfolio > previous iteration, add to overall profit
                    profit['overall'] = performance['profit']['overall']
                    initialcheck2 = 'done'
                    if profit['current'] >= 0:
                        profit['overall'] = profit['current'] + profit['overall']

                        data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                        olddata = {'old': old, 'old_cash': old_cash}

                        with open('kucoin/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('kucoin/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    else:
                        data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                        olddata = {'old': old, 'old_cash': old_cash}

                        with open('kucoin/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('kucoin/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    # If profit due to the algorithm exceeds $100, donate X% to Nescience
                    if profit['overall'] > 200:

                        # Sort Deviation for highest asset deviation and sell donation amount  in that asset before buying equivalent ETH

                        hmm = list(sum(sorted(dev.items(), key=lambda x: x[1], reverse=True), ()))[0]

                        assets = config['assets']

                        for a in assets:
                            if str('dev_' + a) == str(hmm):
                                print('Initiating Donation.')
                                donation_amount = (performance['profit']['overall'] * .10)

                                # Sell Highest Deviation
                                the_asset = config['assets'][str(a)]
                                highest_asset = str(the_asset + '-' + stablecoin)
                                print(highest_asset)
                                price_asset = float(client.get_ticker(symbol=highest_asset)['price'])
                                asset_amount = float(donation_amount / price_asset)
                                print('Donating' + ' ' + str(donation_amount) + 'of' + ' ' + str(
                                    profit['overall']) + " " + "dollars" + " " + "profit generated by this algorithm.")
                                sell_order(highest_asset, asset_amount, price_asset, highest_asset)


                                # Buy Eth
                                def stablecoincheck():
                                    if stablecoin != 'ETH':
                                        eth_symbol = str('ETH' + '-' + stablecoin)
                                        price_eth = float(client.get_ticker(symbol=eth_symbol)['price'])
                                        eth_amount = float((donation_amount / price_eth) * .98)
                                        buy_order(eth_symbol, eth_amount, price_eth)
                                        return eth_amount
                                    else:
                                        eth_amount = (donation_amount * .99)
                                        return eth_amount


                                eth_amount = stablecoincheck()

                                # Withdrawal amount final
                                eth_withdraw = eth_amount * .98
                                eth_withdraw = truncate(eth_withdraw, 6)

                                # Transfer to Main Wallet
                                accounts = client.get_accounts()


                                def tradeaccount():
                                    for a in accounts:
                                        if a['type'] == 'trade' and a['currency'] == 'ETH':
                                            return a['id']


                                tradeacc = tradeaccount()


                                def mainaccount():
                                    for a in accounts:
                                        if a['type'] == 'main' and a['currency'] == 'ETH':
                                            return a['id']


                                mainacc = mainaccount()

                                client.create_inner_transfer(str(tradeacc), str(mainacc), eth_withdraw)

                                # Withdraw Eth
                                print("Withdrawing" + " " + str(
                                    eth_withdraw) + "ETH" + " " + "as a donation to the Developers / Nescience")
                                try:
                                    withdrawal = client.create_withdrawal('ETH', eth_withdraw,
                                                                          '0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C')

                                except OSError:
                                    time.sleep(5)
                                    withdrawal = client.create_withdrawal('ETH', eth_withdraw,
                                                                          '0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C')
                                # Set overall profit back to 0
                                overall_update = 0
                                profit.update({'overall': overall_update})
                                data.update({'profit': profit})
                                with open('kucoin/performance.json', 'w') as outfile:
                                    json.dump(data, outfile)

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

            # Record data every half day
            multiples = [n for n in range(1, 99999) if n % 1 == 0]
            if count in multiples:
                # Checks for previous runs and calculates gain over initial allocation
                with open('kucoin/performance.json') as json_file:
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
                        old["old_asset{0}".format(x)] = balance['balance']["balance_asset{0}".format(x)]

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

                    with open('kucoin/old.json', 'w') as outfile:
                        json.dump(olddata, outfile)

                    with open('kucoin/performance.json', 'w') as outfile:
                        json.dump(data, outfile)
                    # if not the initial setup, load previous iterations and calculate differences and profit
                else:
                    with open('kucoin/performance.json') as json_file:
                        performance = json.load(json_file)
                    with open('kucoin/old.json') as json_file:
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
                        old["old_asset{0}".format(x)] = balance['balance']["balance_asset{0}".format(x)]

                    # calculate current profits of the overall portfolio
                    profit['current'] = 0
                    for x in range(0, assetnum):
                        x = str(x + 1)
                        profit['current'] = profit['current'] + profit["profit_asset{0}".format(x)]
                    profit['current'] = profit['current'] + profit_cash
                    old_cash = balance['cash_balance']

                    # If portfolio > previous iteration, add to overall profit
                    profit['overall'] = performance['profit']['overall']
                    initialcheck2 = 'done'
                    if profit['current'] >= 0:
                        profit['overall'] = profit['current'] + profit['overall']

                        data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                        olddata = {'old': old, 'old_cash': old_cash}

                        with open('kucoin/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('kucoin/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    else:
                        data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                        olddata = {'old': old, 'old_cash': old_cash}

                        with open('kucoin/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('kucoin/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    # If profit due to the algorithm exceeds $100, donate X% to Nescience
                    if profit['overall'] > 200:

                        # Sort Deviation for highest asset deviation and sell donation amount  in that asset before buying equivalent ETH

                        hmm = list(sum(sorted(dev.items(), key=lambda x: x[1], reverse=True), ()))[0]

                        assets = config['assets']

                        for a in assets:
                            if str('dev_' + a) == str(hmm):
                                print('Initiating Donation.')
                                donation_amount = (performance['profit']['overall'] * .10)

                                # Sell Highest Deviation
                                the_asset = config['assets'][str(a)]
                                highest_asset = str(the_asset + '-' + stablecoin)
                                print(highest_asset)
                                price_asset = float(client.get_ticker(symbol=highest_asset)['price'])
                                asset_amount = float(donation_amount / price_asset)
                                print('Donating' + ' ' + str(donation_amount) + 'of' + ' ' + str(
                                    profit['overall']) + " " + "dollars" + " " + "profit generated by this algorithm.")
                                sell_order(highest_asset, asset_amount, price_asset, highest_asset)


                                # Buy Eth
                                def stablecoincheck():
                                    if stablecoin != 'ETH':
                                        eth_symbol = str('ETH' + '-' + stablecoin)
                                        price_eth = float(client.get_ticker(symbol=eth_symbol)['price'])
                                        eth_amount = float((donation_amount / price_eth) * .98)
                                        buy_order(eth_symbol, eth_amount, price_eth)
                                        return eth_amount
                                    else:
                                        eth_amount = (donation_amount * .99)
                                        return eth_amount


                                eth_amount = stablecoincheck()

                                # Withdrawal amount final
                                eth_withdraw = eth_amount * .98
                                eth_withdraw = truncate(eth_withdraw, 6)

                                # Transfer to Main Wallet
                                accounts = client.get_accounts()


                                def tradeaccount():
                                    for a in accounts:
                                        if a['type'] == 'trade' and a['currency'] == 'ETH':
                                            return a['id']


                                tradeacc = tradeaccount()


                                def mainaccount():
                                    for a in accounts:
                                        if a['type'] == 'main' and a['currency'] == 'ETH':
                                            return a['id']


                                mainacc = mainaccount()

                                client.create_inner_transfer(str(tradeacc), str(mainacc), eth_withdraw)

                                # Withdraw Eth
                                print("Withdrawing" + " " + str(
                                    eth_withdraw) + "ETH" + " " + "as a donation to the Developers / Nescience")
                                try:
                                    withdrawal = client.create_withdrawal('ETH', eth_withdraw,
                                                                          '0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C')

                                except OSError:
                                    time.sleep(5)
                                    withdrawal = client.create_withdrawal('ETH', eth_withdraw,
                                                                          '0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C')
                                # Set overall profit back to 0
                                overall_update = 0
                                profit.update({'overall': overall_update})
                                data.update({'profit': profit})
                                with open('kucoin/performance.json', 'w') as outfile:
                                    json.dump(data, outfile)

            count = count + 1
            if count == 95760:
                count = 0
            data3 = {'count': count}
            with open('kucoin/count.json', 'w') as outfile:
                json.dump(data3, outfile)
            time.sleep(604800)