import time
import datetime
import math
import json
import cbpro
import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("Coinbase")


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

    with open('GDAX/config.json') as json_file:
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
            API_PASSWORD = input('API PASSPHRASE:')

            print("Initializing...")

            configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum,
                             'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY, 'API_SECRET': API_SECRET,
                             'API_PASSWORD': API_PASSWORD, 'algorithm': algorithm}
            with open('GDAX/config.json', 'w') as outfile:
                json.dump(configuration, outfile)
        if algorithm == 'PERIODIC':
            period = input('Hourly, Daily, or Weekly: ').upper()
            API_KEY = input('API KEY:')
            API_SECRET = input('API SECRET:')
            API_PASSWORD = input('API PASSPHRASE:')

            print("Initializing...")

            configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                             'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY, 'API_SECRET': API_SECRET,
                             'API_PASSWORD': API_PASSWORD, 'algorithm': algorithm}
            with open('GDAX/config.json', 'w') as outfile:
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
            API_PASSWORD = input('API PASSPHRASE:')
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

            client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, API_PASSWORD)

            try:
                new_balances = client.get_accounts()
            except ValueError:
                time.sleep(2)
                new_balances = client.get_accounts()
            except OSError:
                time.sleep(3)
                new_balances = client.get_accounts()
            # Get Balances of each previously entered asset
            new_balance = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                for b in new_balances:
                    if b['currency'] == assets["asset{0}".format(x)]:
                        new_balance['balance_asset{0}'.format(x)] = b['balance']
                        new_balance["balance_asset{0}".format(x)] = float(new_balance["balance_asset{0}".format(x)])
                    if "balance_asset{0}".format(x) not in new_balance:
                        new_balance["balance_asset{0}".format(x)] = 0
                    if b['currency'] == stablecoin:
                        new_balance["cash_balance"] = b['balance']
                        old_cash = float(new_balance['cash_balance'])
                    if "cash_balance" not in new_balance:
                        old_cash = 0

            old = {}

            for x in range(0, assetnum):
                x = str(x + 1)
                try:
                    old['old_asset{0}'.format(x)] = new_balance['balance_asset{0}'.format(x)]
                except:
                    pass
            olddata = {'old': old, 'old_cash': old_cash}

            with open('GDAX/old.json', 'w') as outfile:
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
                                 'API_PASSWORD': API_PASSWORD, 'algorithm': algorithm}
                with open('GDAX/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)
            if algorithm == 'PERIODIC':
                period = input('Hourly, Daily, or Weekly: ').upper()

                print("Initializing...")

                configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'API_PASSWORD': API_PASSWORD, 'algorithm': algorithm}
                with open('GDAX/config.json', 'w') as outfile:
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
            API_PASSWORD = config['API_PASSWORD']
            for x in range(0, assetnum):
                x = str(x + 1)
                assets["asset{0}".format(x)] = config['assets']["asset{0}".format(x)]
                assets["asset{0}".format(x)] = assets["asset{0}".format(x)].upper()

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
                                 'API_PASSWORD': API_PASSWORD, 'algorithm': algorithm}
                with open('GDAX/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)
            if algorithm == 'PERIODIC':
                period = config['period']

                print("Initializing...")

                configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'API_PASSWORD': API_PASSWORD, 'algorithm': algorithm}
                with open('GDAX/config.json', 'w') as outfile:
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
        except ValueError:
            time.sleep(2)
            pass
        except OSError:
            time.sleep(2)
            pass
    # Get Balances of each previously entered asset
    balance = {}
    try:
        for x in range(0, assetnum):
            x = str(x + 1)
            for b in balances:
                if b['currency'] == assets["asset{0}".format(x)]:
                    balance['balance_asset{0}'.format(x)] = b['balance']
                    balance["balance_asset{0}".format(x)] = float(balance["balance_asset{0}".format(x)])
                if "balance_asset{0}".format(x) not in balance:
                    balance["balance_asset{0}".format(x)] = 0
                if b['currency'] == stablecoin:
                    balance["cash_balance"] = b['balance']
                    cash_balance = float(balance['cash_balance'])
                if "cash_balance" not in balance:
                    cash_balance = 0
    except Exception as e:
        print(e)
        pass
    # save balances to json
    balance.update({'cash_balance': cash_balance})
    with open('GDAX/balance.json', 'w') as outfile:
        json.dump(balance, outfile)


def prices():
    global price
    # Grabs prices from Coinbase Pro
    price = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        attempt = False
        while attempt is False:
            try:
                price["price_asset{0}".format(x)] = float(client.get_product_ticker(symbol["symbol_asset{0}".format(x)])['price'])
                attempt = True
            except ValueError:
                time.sleep(2)
                pass
            except OSError:
                time.sleep(3)
                pass
    # saves to json
    with open('GDAX/prices.json', 'w') as outfile:
        json.dump(price, outfile)


def usd_value():
    # Calculates USD value of positions
    global usd
    global total_usd

    with open('GDAX/balance.json') as json_file:
        balance = json.load(json_file)

    with open('GDAX/prices.json') as json_file:
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


def sell_order(pair, sell_asset, current_price):

    value = current_price * sell_asset
    if value >= 10:
        try:
            currencies = client.get_products()
        except ValueError:
            time.sleep(2)
            currencies = client.get_products()

        def minimums():
            for c in currencies:
                if c['id'] == pair:
                    return float(c['base_min_size'])
        minimum = minimums()

        if minimum < .001:
            sell_asset = truncate(sell_asset, 4)
        else:
            if minimum < .01:
                sell_asset = truncate(sell_asset, 3)
            else:
                if minimum < .1:
                    sell_asset = truncate(sell_asset, 2)
                else:
                    if minimum < 1:
                        sell_asset = truncate(sell_asset, 1)
                    else:
                        if minimum == 1:
                            sell_asset = round(sell_asset)
        print("Selling" + " " + str(sell_asset) + " " + "of" + " " + pair)
        try:
            client.place_market_order(product_id=pair,
                                      side='sell',
                                      size=sell_asset)
            time.sleep(1)
        except ValueError:
            time.sleep(2)
            client.place_market_order(product_id=pair,
                                      side='sell',
                                      size=sell_asset)


def buy_order(pair, buy_asset, current_price):

    value = current_price * buy_asset
    if value >= 10:
        try:
            currencies = client.get_products()
        except ValueError:
            time.sleep(2)
            currencies = client.get_products()

        def minimums():
            for c in currencies:
                if c['id'] == pair:
                    return float(c['base_min_size'])
        minimum = minimums()

        if minimum < .001:
            buy_asset = truncate(buy_asset, 4)
        else:
            if minimum < .01:
                buy_asset = truncate(buy_asset, 3)
            else:
                if minimum < .1:
                    buy_asset = truncate(buy_asset, 2)
                else:
                    if minimum < 1:
                        buy_asset = truncate(buy_asset, 1)
                    else:
                        if minimum == 1:
                            buy_asset = round(buy_asset)
        print("Buying" + " " + str(buy_asset) + " " + "of" + " " + pair)
        try:
            client.place_market_order(product_id=pair,
                                      side='buy',
                                      size=buy_asset)
            time.sleep(1)
        except ValueError:
            time.sleep(2)
            client.place_market_order(product_id=pair,
                                      side='buy',
                                      size=buy_asset)

    # MAIN


setup()

with open('GDAX/config.json') as json_file:
    config = json.load(json_file)

api_key = config['API_KEY']
api_secret = config['API_SECRET']
api_passphrase = config['API_PASSWORD']

client = cbpro.AuthenticatedClient(api_key, api_secret, api_passphrase)

allocation = (.99 / assetnum)

with open('GDAX/initial.json') as json_file:
    initial = json.load(json_file)
    initialcheck = initial['initialcheck']

if initialcheck != 'done':
    initial = {}
    balances()
    with open('GDAX/balance.json') as json_file:
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

    with open('GDAX/count.json', 'w') as outfile:
        json.dump(data2, outfile)

    with open('GDAX/initial.json', 'w') as outfile:
        json.dump(data, outfile)

else:
    with open('GDAX/count.json') as json_file:
        counts = json.load(json_file)
    count = int(counts['count'])

algorithm = config['algorithm']

if algorithm == 'THRESHOLD':

    threshold = config['threshold']

    while count < 99999:

        balances()

        prices()

        with open('GDAX/balance.json') as json_file:
            balance = json.load(json_file)
        with open('GDAX/prices.json') as json_file:
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
                            sell_order(config['symbol']["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                                       price['price_asset{0}'.format(x)])
                for x in range(0, assetnum):
                    x = str(x + 1)
                    if sell["sell_asset{0}".format(x)] < 0:
                            sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                            buy_order(config['symbol']["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                                       price['price_asset{0}'.format(x)])

        # Buy order trade trigger
        negative_threshold = (-1 * config['threshold'])
        for x in range(0, assetnum):
            x = str(x + 1)
            balances()
            usd_value()
            deviation()
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
                            sellasset = (-1 * buy["buy_asset{0}".format(x)])
                            sell_order(config['symbol']["symbol_asset{0}".format(x)], sellasset,
                                      price['price_asset{0}'.format(x)])
                for x in range(0, assetnum):
                    x = str(x + 1)
                    if buy["buy_asset{0}".format(x)] > 0:
                            buy_order(config['symbol']["symbol_asset{0}".format(x)], buy["buy_asset{0}".format(x)],
                                      price['price_asset{0}'.format(x)])

        time.sleep(3)
        balances()
        deviation()
        prices()
        usd_value()

        # Record data every half day
        multiples = [n for n in range(1, 99999) if n % (1000*assetnum) == 0]
        if count in multiples:
            # Checks for previous runs and calculates gain over initial allocation
            with open('GDAX/performance.json') as json_file:
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

                if profit["current"] > 0:
                    profit["overall"] = profit["current"] + profit["overall"]

                initialcheck2 = 'done'

                data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                olddata = {'old': old, 'old_cash': old_cash}

                with open('GDAX/old.json', 'w') as outfile:
                    json.dump(olddata, outfile)

                with open('GDAX/performance.json', 'w') as outfile:
                    json.dump(data, outfile)
                # if not the initial setup, load previous iterations and calculate differences and profit
            else:
                with open('GDAX/performance.json') as json_file:
                    performance = json.load(json_file)

                with open('GDAX/old.json') as json_file:
                    oldload = json.load(json_file)

                compare = {}
                old = {}
                profit = {}

                for x in range(0, assetnum):
                    x = str(x + 1)
                    # call old asset balance from Performance and set as new old asset dict
                    try:
                        old["old_asset{0}".format(x)] = oldload['old']["old_asset{0}".format(x)]
                    except:
                        old["old_asset{0}".format(x)] = balance["balance_asset{0}".format(x)]

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

                    with open('GDAX/old.json', 'w') as outfile:
                        json.dump(olddata, outfile)

                    with open('GDAX/performance.json', 'w') as outfile:
                        json.dump(data, outfile)

                else:
                    data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                    olddata = {'old': old, 'old_cash': old_cash}

                    with open('GDAX/old.json', 'w') as outfile:
                        json.dump(olddata, outfile)

                    with open('GDAX/performance.json', 'w') as outfile:
                        json.dump(data, outfile)

                # If profit due to the algorithm exceeds $200, donate X% to Nescience
                if performance['profit']['overall'] > 400:

                    # Sort Deviation for highest asset deviation and sell donation amount before buying equivalent ETH

                    highest = list(sum(sorted(dev.items(), key=lambda x: x[1], reverse=True), ()))[0]

                    for a in assets:
                        if str('dev_' + a) == str(highest):
                            print('Initiating Donation.')
                            donation_amount = (performance['profit']['overall'] * .075)

                            # Sell Highest Deviation
                            theasset = config['assets'][str(a)]

                            highest_asset = str(theasset + "-" + stablecoin)

                            price_asset = float(client.get_product_ticker(str(highest_asset))['price'])
                            asset_amount = float(donation_amount / price_asset)
                            print('Donating' + ' ' + str(donation_amount) + " " + 'of' + ' ' + str(performance['profit']['overall']) + " " + "dollars" + " " + "profit generated by this algorithm.")
                            sell_order(highest_asset, asset_amount, price_asset)

                            # Buy Eth

                            def stablecoincheck():
                                if stablecoin != 'ETH':
                                    eth_symbol = str('ETH' + '-' + stablecoin)
                                    price_eth = float(client.get_product_ticker(eth_symbol)['price'])
                                    eth_amount = float((donation_amount / price_eth) * .98)
                                    buy_order(eth_symbol, eth_amount, price_eth)
                                    return eth_amount
                                else:
                                    eth_amount = (donation_amount * .99)
                                    return eth_amount
                            eth_amount = stablecoincheck()

                            # Withdraw Eth
                            eth_withdraw = eth_amount * .98
                            eth_withdraw = truncate(eth_withdraw, 5)
                            print("Withdrawing" + " " + str(eth_withdraw) + "ETH" + " " + "as a donation to the Developers / Nescience")
                            withdraw = client.crypto_withdraw(eth_withdraw, "ETH", "0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C")
                            # Set overall profit back to 0
                            overall_update = 0
                            profit.update({'overall': overall_update})
                            data.update({'profit': profit})
                            with open('GDAX/performance.json', 'w') as outfile:
                                json.dump(data, outfile)

        count = count + 1
        if count == 95760:
            count = 0
        data3 = {'count': count}
        with open('GDAX/count.json', 'w') as outfile:
            json.dump(data3, outfile)
        time.sleep(60)

if algorithm == 'PERIODIC':

    period = config['period']

    if period == 'HOURLY':
        while count < 99999:

            balances()

            prices()

            with open('GDAX/balance.json') as json_file:
                balance = json.load(json_file)
            with open('GDAX/prices.json') as json_file:
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
                    sell_order(config['symbol']["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                               price['price_asset{0}'.format(x)])
            for x in range(0, assetnum):
                x = str(x + 1)
                if sell["sell_asset{0}".format(x)] < 0:
                    sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                    buy_order(config['symbol']["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                              price['price_asset{0}'.format(x)])

            time.sleep(3)
            balances()
            deviation()
            prices()
            usd_value()

            # Record data every half day
            multiples = [n for n in range(1, 99999) if n % 35555 == 0]
            if count in multiples:
                # Checks for previous runs and calculates gain over initial allocation
                with open('GDAX/performance.json') as json_file:
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

                    if profit["current"] > 0:
                        profit["overall"] = profit["current"] + profit["overall"]

                    initialcheck2 = 'done'

                    data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                    olddata = {'old': old, 'old_cash': old_cash}

                    with open('GDAX/old.json', 'w') as outfile:
                        json.dump(olddata, outfile)

                    with open('GDAX/performance.json', 'w') as outfile:
                        json.dump(data, outfile)
                    # if not the initial setup, load previous iterations and calculate differences and profit
                else:
                    with open('GDAX/performance.json') as json_file:
                        performance = json.load(json_file)

                    with open('GDAX/old.json') as json_file:
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

                        with open('GDAX/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('GDAX/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    else:
                        data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                        olddata = {'old': old, 'old_cash': old_cash}

                        with open('GDAX/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('GDAX/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    # If profit due to the algorithm exceeds $200, donate X% to Nescience
                    if performance['profit']['overall'] > 400:

                        # Sort Deviation for highest asset deviation and sell donation amount before buying equivalent ETH

                        highest = list(sum(sorted(dev.items(), key=lambda x: x[1], reverse=True), ()))[0]

                        for a in assets:
                            if str('dev_' + a) == str(highest):
                                print('Initiating Donation.')
                                donation_amount = (performance['profit']['overall'] * .075)

                                # Sell Highest Deviation
                                theasset = config['assets'][str(a)]

                                highest_asset = str(theasset + "-" + stablecoin)

                                price_asset = float(client.get_product_ticker(str(highest_asset))['price'])
                                asset_amount = float(donation_amount / price_asset)
                                print('Donating' + ' ' + str(donation_amount) + " " + 'of' + ' ' + str(
                                    performance['profit'][
                                        'overall']) + " " + "dollars" + " " + "profit generated by this algorithm.")
                                sell_order(highest_asset, asset_amount, price_asset)

                                # Buy Eth

                                def stablecoincheck():
                                    if stablecoin != 'ETH':
                                        eth_symbol = str('ETH' + '-' + stablecoin)
                                        price_eth = float(client.get_product_ticker(eth_symbol)['price'])
                                        eth_amount = float((donation_amount / price_eth) * .98)
                                        buy_order(eth_symbol, eth_amount, price_eth)
                                        return eth_amount
                                    else:
                                        eth_amount = (donation_amount * .99)
                                        return eth_amount


                                eth_amount = stablecoincheck()

                                # Withdraw Eth
                                eth_withdraw = eth_amount * .98
                                eth_withdraw = truncate(eth_withdraw, 5)
                                print("Withdrawing" + " " + str(
                                    eth_withdraw) + "ETH" + " " + "as a donation to the Developers / Nescience")
                                withdraw = client.crypto_withdraw(eth_withdraw, "ETH",
                                                                  "0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C")
                                # Set overall profit back to 0
                                overall_update = 0
                                profit.update({'overall': overall_update})
                                data.update({'profit': profit})
                                with open('GDAX/performance.json', 'w') as outfile:
                                    json.dump(data, outfile)

            count = count + 1
            if count == 95760:
                count = 0
            data3 = {'count': count}
            with open('GDAX/count.json', 'w') as outfile:
                json.dump(data3, outfile)
            time.sleep(3600)

    if period == 'DAILY':
        while count < 99999:

            balances()

            prices()

            with open('GDAX/balance.json') as json_file:
                balance = json.load(json_file)
            with open('GDAX/prices.json') as json_file:
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
                    sell_order(config['symbol']["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                               price['price_asset{0}'.format(x)])
            for x in range(0, assetnum):
                x = str(x + 1)
                if sell["sell_asset{0}".format(x)] < 0:
                    sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                    buy_order(config['symbol']["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                              price['price_asset{0}'.format(x)])

            time.sleep(3)
            balances()
            deviation()
            prices()
            usd_value()

            # Record data every half day
            multiples = [n for n in range(1, 99999) if n % 35555 == 0]
            if count in multiples:
                # Checks for previous runs and calculates gain over initial allocation
                with open('GDAX/performance.json') as json_file:
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

                    if profit["current"] > 0:
                        profit["overall"] = profit["current"] + profit["overall"]

                    initialcheck2 = 'done'

                    data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                    olddata = {'old': old, 'old_cash': old_cash}

                    with open('GDAX/old.json', 'w') as outfile:
                        json.dump(olddata, outfile)

                    with open('GDAX/performance.json', 'w') as outfile:
                        json.dump(data, outfile)
                    # if not the initial setup, load previous iterations and calculate differences and profit
                else:
                    with open('GDAX/performance.json') as json_file:
                        performance = json.load(json_file)

                    with open('GDAX/old.json') as json_file:
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

                        with open('GDAX/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('GDAX/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    else:
                        data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                        olddata = {'old': old, 'old_cash': old_cash}

                        with open('GDAX/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('GDAX/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    # If profit due to the algorithm exceeds $200, donate X% to Nescience
                    if performance['profit']['overall'] > 400:

                        # Sort Deviation for highest asset deviation and sell donation amount before buying equivalent ETH

                        highest = list(sum(sorted(dev.items(), key=lambda x: x[1], reverse=True), ()))[0]

                        for a in assets:
                            if str('dev_' + a) == str(highest):
                                print('Initiating Donation.')
                                donation_amount = (performance['profit']['overall'] * .075)

                                # Sell Highest Deviation
                                theasset = config['assets'][str(a)]

                                highest_asset = str(theasset + "-" + stablecoin)

                                price_asset = float(client.get_product_ticker(str(highest_asset))['price'])
                                asset_amount = float(donation_amount / price_asset)
                                print('Donating' + ' ' + str(donation_amount) + " " + 'of' + ' ' + str(
                                    performance['profit'][
                                        'overall']) + " " + "dollars" + " " + "profit generated by this algorithm.")
                                sell_order(highest_asset, asset_amount, price_asset)

                                # Buy Eth

                                def stablecoincheck():
                                    if stablecoin != 'ETH':
                                        eth_symbol = str('ETH' + '-' + stablecoin)
                                        price_eth = float(client.get_product_ticker(eth_symbol)['price'])
                                        eth_amount = float((donation_amount / price_eth) * .98)
                                        buy_order(eth_symbol, eth_amount, price_eth)
                                        return eth_amount
                                    else:
                                        eth_amount = (donation_amount * .99)
                                        return eth_amount


                                eth_amount = stablecoincheck()

                                # Withdraw Eth
                                eth_withdraw = eth_amount * .98
                                eth_withdraw = truncate(eth_withdraw, 5)
                                print("Withdrawing" + " " + str(
                                    eth_withdraw) + "ETH" + " " + "as a donation to the Developers / Nescience")
                                withdraw = client.crypto_withdraw(eth_withdraw, "ETH",
                                                                  "0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C")
                                # Set overall profit back to 0
                                overall_update = 0
                                profit.update({'overall': overall_update})
                                data.update({'profit': profit})
                                with open('GDAX/performance.json', 'w') as outfile:
                                    json.dump(data, outfile)

            count = count + 1
            if count == 95760:
                count = 0
            data3 = {'count': count}
            with open('GDAX/count.json', 'w') as outfile:
                json.dump(data3, outfile)
            time.sleep(86400)

    if period == 'WEEKLY':
        while count < 99999:

            balances()

            prices()

            with open('GDAX/balance.json') as json_file:
                balance = json.load(json_file)
            with open('GDAX/prices.json') as json_file:
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
                    sell_order(config['symbol']["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                               price['price_asset{0}'.format(x)])
            for x in range(0, assetnum):
                x = str(x + 1)
                if sell["sell_asset{0}".format(x)] < 0:
                    sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                    buy_order(config['symbol']["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                              price['price_asset{0}'.format(x)])

            time.sleep(3)
            balances()
            deviation()
            prices()
            usd_value()

            # Record data every half day
            multiples = [n for n in range(1, 99999) if n % 35555 == 0]
            if count in multiples:
                # Checks for previous runs and calculates gain over initial allocation
                with open('GDAX/performance.json') as json_file:
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

                    if profit["current"] > 0:
                        profit["overall"] = profit["current"] + profit["overall"]

                    initialcheck2 = 'done'

                    data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                    olddata = {'old': old, 'old_cash': old_cash}

                    with open('GDAX/old.json', 'w') as outfile:
                        json.dump(olddata, outfile)

                    with open('GDAX/performance.json', 'w') as outfile:
                        json.dump(data, outfile)
                    # if not the initial setup, load previous iterations and calculate differences and profit
                else:
                    with open('GDAX/performance.json') as json_file:
                        performance = json.load(json_file)

                    with open('GDAX/old.json') as json_file:
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

                        with open('GDAX/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('GDAX/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    else:
                        data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                        olddata = {'old': old, 'old_cash': old_cash}

                        with open('GDAX/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('GDAX/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    # If profit due to the algorithm exceeds $200, donate X% to Nescience
                    if performance['profit']['overall'] > 400:

                        # Sort Deviation for highest asset deviation and sell donation amount before buying equivalent ETH

                        highest = list(sum(sorted(dev.items(), key=lambda x: x[1], reverse=True), ()))[0]

                        for a in assets:
                            if str('dev_' + a) == str(highest):
                                print('Initiating Donation.')
                                donation_amount = (performance['profit']['overall'] * .075)

                                # Sell Highest Deviation
                                theasset = config['assets'][str(a)]

                                highest_asset = str(theasset + "-" + stablecoin)

                                price_asset = float(client.get_product_ticker(str(highest_asset))['price'])
                                asset_amount = float(donation_amount / price_asset)
                                print('Donating' + ' ' + str(donation_amount) + " " + 'of' + ' ' + str(
                                    performance['profit'][
                                        'overall']) + " " + "dollars" + " " + "profit generated by this algorithm.")
                                sell_order(highest_asset, asset_amount, price_asset)

                                # Buy Eth

                                def stablecoincheck():
                                    if stablecoin != 'ETH':
                                        eth_symbol = str('ETH' + '-' + stablecoin)
                                        price_eth = float(client.get_product_ticker(eth_symbol)['price'])
                                        eth_amount = float((donation_amount / price_eth) * .98)
                                        buy_order(eth_symbol, eth_amount, price_eth)
                                        return eth_amount
                                    else:
                                        eth_amount = (donation_amount * .99)
                                        return eth_amount


                                eth_amount = stablecoincheck()

                                # Withdraw Eth
                                eth_withdraw = eth_amount * .98
                                eth_withdraw = truncate(eth_withdraw, 5)
                                print("Withdrawing" + " " + str(
                                    eth_withdraw) + "ETH" + " " + "as a donation to the Developers / Nescience")
                                withdraw = client.crypto_withdraw(eth_withdraw, "ETH",
                                                                  "0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C")
                                # Set overall profit back to 0
                                overall_update = 0
                                profit.update({'overall': overall_update})
                                data.update({'profit': profit})
                                with open('GDAX/performance.json', 'w') as outfile:
                                    json.dump(data, outfile)

            count = count + 1
            if count == 95760:
                count = 0
            data3 = {'count': count}
            with open('GDAX/count.json', 'w') as outfile:
                json.dump(data3, outfile)
            time.sleep(604800)
