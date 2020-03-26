import gemini
import time
import datetime
import math
import json
import ctypes
from sys import exit
ctypes.windll.kernel32.SetConsoleTitleW("Gemini")


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

    with open('gemini/config.json') as json_file:
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
            API_KEY = input('API KEY:')
            API_SECRET = input('API SECRET:')

            print("Initializing...")

            configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck,
                             'assetnum': assetnum,
                             'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY,
                             'API_SECRET': API_SECRET,
                             'algorithm': algorithm}
            with open('gemini/config.json', 'w') as outfile:
                json.dump(configuration, outfile)
        if algorithm == 'PERIODIC':
            period = input('Hourly, Daily, or Weekly: ').upper()
            API_KEY = input('API KEY:')
            API_SECRET = input('API SECRET:')

            print("Initializing...")

            configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                             'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY,
                             'API_SECRET': API_SECRET,
                             'algorithm': algorithm}
            with open('gemini/config.json', 'w') as outfile:
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

            print("Loading... This may take a few seconds.")

            client = gemini.PrivateClient(API_KEY, API_SECRET)
            try:
                new_balances = client.get_balance()
            except ConnectionError as e:
                print(e)
                time.sleep(3)
                new_balances = client.get_balance()
            # Get Balances of each previously entered asset
            new_balance = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                for b in new_balances:
                    if b['currency'] == assets["asset{0}".format(x)]:
                        new_balance["balance_asset{0}".format(x)] = [b['amount']][0]
                        new_balance["balance_asset{0}".format(x)] = float(new_balance["balance_asset{0}".format(x)])
                    if "balance_asset{0}".format(x) not in new_balance:
                        new_balance["balance_asset{0}".format(x)] = 0

            def oldcash():
                for b in new_balances:
                    if b['currency'] == stablecoin:
                        old_cash = b['amount']
                        old_cash = float(old_cash)
                        return old_cash
            old_cash = oldcash()

            old = {}

            for x in range(0, assetnum):
                x = str(x + 1)
                try:
                    old['old_asset{0}'.format(x)] = new_balance['balance_asset{0}'.format(x)]
                except:
                    pass
            olddata = {'old': old, 'old_cash': old_cash}

            with open('bitfinex3/old.json', 'w') as outfile:
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
                with open('gemini/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)
            if algorithm == 'PERIODIC':
                period = input('Hourly, Daily, or Weekly: ').upper()

                print("Initializing...")

                configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'algorithm': algorithm}
                with open('gemini/config.json', 'w') as outfile:
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
                symbol["symbol_asset{0}".format(x)] = str(assets["asset{0}".format(x)] + stablecoin)

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
                with open('gemini/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)
            if algorithm == 'PERIODIC':
                period = config['period']

                print("Initializing...")

                configuration = {'assets': assets, 'period': period, 'configcheck': configcheck, 'assetnum': assetnum,
                                 'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY,
                                 'API_SECRET': API_SECRET,
                                 'algorithm': algorithm}
                with open('gemini/config.json', 'w') as outfile:
                    json.dump(configuration, outfile)


def balances():
    # Pull  balance for each selected asset
    global cash_balance
    global balance

    # Balance USD
    attempt = False
    while attempt is False:
        try:
            balances = client.get_balance()
            attempt = True
        except ConnectionError:
            time.sleep(3)
            balances = client.get_balance()
        except ValueError:
            time.sleep(3)
            balances = client.get_balance()
    # Get Balances of each previously entered asset
    balance = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        for b in balances:
            if b['currency'] == assets["asset{0}".format(x)]:
                balance["balance_asset{0}".format(x)] = [b['amount']][0]
                balance["balance_asset{0}".format(x)] = float(balance["balance_asset{0}".format(x)])
            if "balance_asset{0}".format(x) not in balance:
                balance["balance_asset{0}".format(x)] = 0
            if b['currency'] == stablecoin:
                cash_balance = b['amount']
                cash_balance = float(cash_balance)
    # save balances to json
    balance.update({'cash_balance': cash_balance})
    with open('gemini/balance.json', 'w') as outfile:
        json.dump(balance, outfile)


def prices():
    global price
    # Grabs prices from Gemini
    price = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        attempt = False
        while attempt is False:
            try:
                price["price_asset{0}".format(x)] = float(client.get_ticker(symbol["symbol_asset{0}".format(x)])['last'])
                attempt = True
            except ConnectionError:
                time.sleep(3)
                pass
            except ValueError:
                time.sleep(3)
                pass
    # saves to json
    with open('gemini/prices.json', 'w') as outfile:
        json.dump(price, outfile)


def usd_value():
    # Calculates USD value of positions
    global usd
    global total_usd

    with open('gemini/balance.json') as json_file:
        balance = json.load(json_file)

    with open('gemini/prices.json') as json_file:
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


def sell_order(asset, sell_asset, current_price, currency):

    if currency == 'LTC':
        sell_asset = truncate(sell_asset, 2)
    if currency == 'BTC':
        sell_asset = truncate(sell_asset, 5)
    if currency == 'BCH':
        sell_asset = truncate(sell_asset, 3)
    else:
        sell_asset = truncate(sell_asset, 3)
    value = float(client.get_ticker(asset)['last']) * float(sell_asset)
    side = str('sell')
    sell_asset = str(sell_asset)
    asset = str(asset)

    if value >= 10:
        print(
            "Selling" + " " + sell_asset + " " + "of" + " " + asset)
        current_price = (current_price * .5)
        current_price = round(current_price)
        current_price = str(current_price)
        client.new_order(symbol=asset, amount=sell_asset, price=current_price, side=side)
        time.sleep(1)


def buy_order(asset, buy_asset, current_price, currency):

    if currency == 'LTC':
        buy_asset = truncate(buy_asset, 2)
    if currency == 'BTC':
        buy_asset = truncate(buy_asset, 5)
    if currency == 'BCH':
        buy_asset = truncate(buy_asset, 3)
    else:
        buy_asset = truncate(buy_asset, 3)

    value = float(client.get_ticker(asset)['last']) * float(buy_asset)
    side = str('buy')
    buy_asset = str(buy_asset)
    asset = str(asset)
    if value >= 10:
        print(
            "Buying" + " " + buy_asset + " " + "of" + " " + asset)
        current_price = (current_price * 1.05)
        current_price = round(current_price)
        current_price = str(current_price)
        client.new_order(symbol=asset, amount=buy_asset, price=current_price, side=side)
        time.sleep(1)

    # MAIN


setup()

with open('gemini/config.json') as json_file:
    config = json.load(json_file)

api_key = config['API_KEY']
api_private = config['API_SECRET']

client = gemini.PrivateClient(api_key, api_private)

allocation = (.99 / assetnum)

with open('gemini/initial.json') as json_file:
    initial = json.load(json_file)
    initialcheck = initial['initialcheck']

if initialcheck != 'done':
    initial = {}
    balances()
    with open('gemini/balance.json') as json_file:
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

    with open('gemini/count.json', 'w') as outfile:
        json.dump(data2, outfile)

    with open('gemini/initial.json', 'w') as outfile:
        json.dump(data, outfile)

else:
    with open('gemini/count.json') as json_file:
        counts = json.load(json_file)
    count = int(counts['count'])

algorithm = config['algorithm']

if algorithm == 'THRESHOLD':

    threshold = config['threshold']

    while count < 99999:

        balances()

        prices()

        with open('gemini/balance.json') as json_file:
            balance = json.load(json_file)
        with open('gemini/prices.json') as json_file:
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
                for y in range(0, assetnum):
                    y = str(y + 1)
                    usd_value()
                    dif["dif_asset{0}".format(y)] = usd["usd_asset{0}".format(y)] - goal_allocation
                    sell["sell_asset{0}".format(y)] = float(dif["dif_asset{0}".format(y)]) / float(price['price_asset{0}'.format(y)])
                    sell["sell_asset{0}".format(y)] = float(sell["sell_asset{0}".format(y)])

                # Sell order API call
                    if sell["sell_asset{0}".format(y)] > 0:
                        sell_order(symbol["symbol_asset{0}".format(y)], sell["sell_asset{0}".format(y)], price["price_asset{0}".format(y)], config['assets']['asset{0}'.format(y)])
                for y in range(0, assetnum):
                    y = str(y + 1)
                    if sell["sell_asset{0}".format(y)] < 0:
                        sell["sell_asset{0}".format(y)] = (-1 * sell["sell_asset{0}".format(y)])
                        buy_order(symbol["symbol_asset{0}".format(y)], sell["sell_asset{0}".format(y)], price["price_asset{0}".format(y)], config['assets']['asset{0}'.format(y)])

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
                for y in range(0, assetnum):
                    y = str(y + 1)
                    usd_value()
                    dif["dif_asset{0}".format(y)] = usd["usd_asset{0}".format(y)] - goal_allocation
                    buy["buy_asset{0}".format(y)] = float(dif["dif_asset{0}".format(y)]) / float(price['price_asset{0}'.format(y)])
                    buy["buy_asset{0}".format(y)] = float(-1 * buy["buy_asset{0}".format(y)])

                # Buy order API call
                    if buy["buy_asset{0}".format(y)] < 0:
                        sellasset = (-1 * buy["buy_asset{0}".format(y)])
                        sell_order(symbol["symbol_asset{0}".format(y)], sellasset, price["price_asset{0}".format(y)], config['assets']['asset{0}'.format(y)])
                for y in range(0, assetnum):
                    y = str(y + 1)
                    if buy["buy_asset{0}".format(y)] > 0:
                        buy_order(symbol["symbol_asset{0}".format(y)], buy["buy_asset{0}".format(y)], price["price_asset{0}".format(y)], config['assets']['asset{0}'.format(y)])

        time.sleep(3)
        balances()
        prices()
        usd_value()

        # Record data every half day
        multiples = [n for n in range(1, 99999) if n % (1000*assetnum) == 0]
        if count in multiples:
            # Checks for previous runs and calculates gain over initial allocation
            with open('gemini/performance.json') as json_file:
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

                olddata= {'old': old, 'old_cash': old_cash}

                with open('gemini/old.json', 'w') as outfile:
                    json.dump(olddata, outfile)

                with open('gemini/performance.json', 'w') as outfile:
                    json.dump(data, outfile)
                # if not the initial setup, load previous iterations and calculate differences and profit
            if initialcheck2 == 'done':
                with open('gemini/performance.json') as json_file:
                    performance = json.load(json_file)
                with open('gemini/old.json') as json_file:
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
                        old["old_asset{0}".format(x)] = balance['balance']["balance_asset{0}".format(x)]

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

                    with open('gemini/old.json', 'w') as outfile:
                        json.dump(olddata, outfile)

                    with open('gemini/performance.json', 'w') as outfile:
                        json.dump(data, outfile)

                else:
                    data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                    olddata = {'old': old, 'old_cash': old_cash}

                    with open('gemini/old.json', 'w') as outfile:
                        json.dump(olddata, outfile)

                    with open('gemini/performance.json', 'w') as outfile:
                        json.dump(data, outfile)

                # If profit due to the algorithm exceeds $100, donate X% to Nescience
                if performance['profit']['overall'] > 400:
                    # Sort Deviation for highest asset deviation and sell donation amount before buying equivalent ETH

                    highest = list(sum(sorted(dev.items(), key=lambda x: x[1], reverse=True), ()))[0]

                    for a in assets:
                        if str('dev_' + a) == str(highest):
                            print('Initiating Donation.')
                            donation_amount = (performance['profit']['overall'] * .075)

                            # Sell Highest Deviation
                            theasset = config['assets'][str(a)]

                            highest_asset = str(theasset + stablecoin)
                            price_asset = float(client.get_ticker(str(highest_asset))['last'])
                            asset_amount = float(donation_amount / price_asset)
                            print('Donating' + ' ' + str(donation_amount) + " " + 'of' + ' ' + str(
                                performance['profit']['overall']) + " " + "dollars" + " " + "profit generated by this algorithm.")
                            sell_order(highest_asset, asset_amount, price_asset, theasset)

                            # Buy Eth

                            def stablecoincheck():
                                if stablecoin != 'ETH':
                                    eth_symbol = str('ETH' + stablecoin)
                                    price_eth = float(client.get_ticker(eth_symbol)['last'])
                                    eth_amount = float((donation_amount / price_eth) * .95)
                                    buy_order(eth_symbol, eth_amount, price_eth, 'ETH')
                                    return eth_amount
                                else:
                                    eth_amount = (donation_amount * .99)
                                    return eth_amount
                            eth_amount = stablecoincheck()

                            # Withdraw Eth, Must be Whitelisted address and API privelege
                            eth_withdraw = eth_amount * .98
                            eth_withdraw = truncate(eth_withdraw, 5)
                            print("Withdrawing" + " " + str(eth_withdraw) + "ETH" + " " + "as a donation to the Developers / Nescience")
                            withdraw = str(client.withdraw_to_address("ETH", "0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C", str(eth_withdraw)))
                            if 'error' in withdraw:
                                print('Ensure you have whitelisted ETH withdrawals to this address: 0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C')
                                print('If you have not, the AI cannot process donations/payments.')
                                exit(0)
                            # Set overall profit back to 0
                            overall_update = 0
                            profit.update({'overall': overall_update})
                            data.update({'profit': profit})
                            with open('gemini/performance.json', 'w') as outfile:
                                json.dump(data, outfile)

        count = count + 1
        if count == 95760:
            count = 0
        data3 = {'count': count}
        with open('gemini/count.json', 'w') as outfile:
            json.dump(data3, outfile)
        time.sleep(60)

if algorithm == 'PERIODIC':

    period = config['period']

    if period == 'HOURLY':

        while count < 99999:

            balances()

            prices()

            with open('gemini/balance.json') as json_file:
                balance = json.load(json_file)
            with open('gemini/prices.json') as json_file:
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
            for y in range(0, assetnum):
                y = str(y + 1)
                usd_value()
                dif["dif_asset{0}".format(y)] = usd["usd_asset{0}".format(y)] - goal_allocation
                sell["sell_asset{0}".format(y)] = float(dif["dif_asset{0}".format(y)]) / float(
                    price['price_asset{0}'.format(y)])
                sell["sell_asset{0}".format(y)] = float(sell["sell_asset{0}".format(y)])

                # Sell order API call
                if sell["sell_asset{0}".format(y)] > 0:
                    sell_order(symbol["symbol_asset{0}".format(y)], sell["sell_asset{0}".format(y)],
                               price["price_asset{0}".format(y)], config['assets']['asset{0}'.format(y)])
            for y in range(0, assetnum):
                y = str(y + 1)
                if sell["sell_asset{0}".format(y)] < 0:
                    sell["sell_asset{0}".format(y)] = (-1 * sell["sell_asset{0}".format(y)])
                    buy_order(symbol["symbol_asset{0}".format(y)], sell["sell_asset{0}".format(y)],
                              price["price_asset{0}".format(y)], config['assets']['asset{0}'.format(y)])

            time.sleep(3)
            balances()
            prices()
            usd_value()
            deviation()

            # Record data every half day
            multiples = [n for n in range(1, 99999) if n % 90 == 0]
            if count in multiples:
                # Checks for previous runs and calculates gain over initial allocation
                with open('gemini/performance.json') as json_file:
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

                    with open('gemini/old.json', 'w') as outfile:
                        json.dump(olddata, outfile)

                    with open('gemini/performance.json', 'w') as outfile:
                        json.dump(data, outfile)
                    # if not the initial setup, load previous iterations and calculate differences and profit
                if initialcheck2 == 'done':
                    with open('gemini/performance.json') as json_file:
                        performance = json.load(json_file)
                    with open('gemini/old.json') as json_file:
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

                        with open('gemini/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('gemini/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    else:
                        data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                        olddata = {'old': old, 'old_cash': old_cash}

                        with open('gemini/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('gemini/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    # If profit due to the algorithm exceeds $100, donate X% to Nescience
                    if performance['profit']['overall'] > 400:
                        # Sort Deviation for highest asset deviation and sell donation amount before buying equivalent ETH

                        highest = list(sum(sorted(dev.items(), key=lambda x: x[1], reverse=True), ()))[0]

                        for a in assets:
                            if str('dev_' + a) == str(highest):
                                print('Initiating Donation.')
                                donation_amount = (performance['profit']['overall'] * .075)

                                # Sell Highest Deviation
                                theasset = config['assets'][str(a)]

                                highest_asset = str(theasset + stablecoin)
                                price_asset = float(client.get_ticker(str(highest_asset))['last'])
                                asset_amount = float(donation_amount / price_asset)
                                print('Donating' + ' ' + str(donation_amount) + " " + 'of' + ' ' + str(
                                    performance['profit'][
                                        'overall']) + " " + "dollars" + " " + "profit generated by this algorithm.")
                                sell_order(highest_asset, asset_amount, price_asset, theasset)

                                # Buy Eth

                                def stablecoincheck():
                                    if stablecoin != 'ETH':
                                        eth_symbol = str('ETH' + stablecoin)
                                        price_eth = float(client.get_ticker(eth_symbol)['last'])
                                        eth_amount = float((donation_amount / price_eth) * .95)
                                        buy_order(eth_symbol, eth_amount, price_eth, 'ETH')
                                        return eth_amount
                                    else:
                                        eth_amount = (donation_amount * .99)
                                        return eth_amount


                                eth_amount = stablecoincheck()

                                # Withdraw Eth, Must be Whitelisted address and API privelege
                                eth_withdraw = eth_amount * .98
                                eth_withdraw = truncate(eth_withdraw, 5)
                                print("Withdrawing" + " " + str(
                                    eth_withdraw) + "ETH" + " " + "as a donation to the Developers / Nescience")
                                withdraw = str(
                                    client.withdraw_to_address("ETH", "0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C",
                                                               str(eth_withdraw)))
                                if 'error' in withdraw:
                                    print(
                                        'Ensure you have whitelisted ETH withdrawals to this address: 0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C')
                                    print('If you have not, the AI cannot process donations/payments.')
                                    exit(0)
                                # Set overall profit back to 0
                                overall_update = 0
                                profit.update({'overall': overall_update})
                                data.update({'profit': profit})
                                with open('gemini/performance.json', 'w') as outfile:
                                    json.dump(data, outfile)

            count = count + 1
            if count == 95760:
                count = 0
            data3 = {'count': count}
            with open('gemini/count.json', 'w') as outfile:
                json.dump(data3, outfile)
            time.sleep(3600)

    if period == 'DAILY':

        while count < 99999:

            balances()

            prices()

            with open('gemini/balance.json') as json_file:
                balance = json.load(json_file)
            with open('gemini/prices.json') as json_file:
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
            for y in range(0, assetnum):
                y = str(y + 1)
                usd_value()
                dif["dif_asset{0}".format(y)] = usd["usd_asset{0}".format(y)] - goal_allocation
                sell["sell_asset{0}".format(y)] = float(dif["dif_asset{0}".format(y)]) / float(
                    price['price_asset{0}'.format(y)])
                sell["sell_asset{0}".format(y)] = float(sell["sell_asset{0}".format(y)])

                # Sell order API call
                if sell["sell_asset{0}".format(y)] > 0:
                    sell_order(symbol["symbol_asset{0}".format(y)], sell["sell_asset{0}".format(y)],
                               price["price_asset{0}".format(y)], config['assets']['asset{0}'.format(y)])
            for y in range(0, assetnum):
                y = str(y + 1)
                if sell["sell_asset{0}".format(y)] < 0:
                    sell["sell_asset{0}".format(y)] = (-1 * sell["sell_asset{0}".format(y)])
                    buy_order(symbol["symbol_asset{0}".format(y)], sell["sell_asset{0}".format(y)],
                              price["price_asset{0}".format(y)], config['assets']['asset{0}'.format(y)])

            time.sleep(3)
            balances()
            prices()
            usd_value()
            deviation()

            # Record data every half day
            multiples = [n for n in range(1, 99999) if n % 4 == 0]
            if count in multiples:
                # Checks for previous runs and calculates gain over initial allocation
                with open('gemini/performance.json') as json_file:
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

                    with open('gemini/old.json', 'w') as outfile:
                        json.dump(olddata, outfile)

                    with open('gemini/performance.json', 'w') as outfile:
                        json.dump(data, outfile)
                    # if not the initial setup, load previous iterations and calculate differences and profit
                if initialcheck2 == 'done':
                    with open('gemini/performance.json') as json_file:
                        performance = json.load(json_file)
                    with open('gemini/old.json') as json_file:
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

                        with open('gemini/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('gemini/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    else:
                        data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                        olddata = {'old': old, 'old_cash': old_cash}

                        with open('gemini/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('gemini/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    # If profit due to the algorithm exceeds $100, donate X% to Nescience
                    if performance['profit']['overall'] > 400:
                        # Sort Deviation for highest asset deviation and sell donation amount before buying equivalent ETH

                        highest = list(sum(sorted(dev.items(), key=lambda x: x[1], reverse=True), ()))[0]

                        for a in assets:
                            if str('dev_' + a) == str(highest):
                                print('Initiating Donation.')
                                donation_amount = (performance['profit']['overall'] * .075)

                                # Sell Highest Deviation
                                theasset = config['assets'][str(a)]

                                highest_asset = str(theasset + stablecoin)
                                price_asset = float(client.get_ticker(str(highest_asset))['last'])
                                asset_amount = float(donation_amount / price_asset)
                                print('Donating' + ' ' + str(donation_amount) + " " + 'of' + ' ' + str(
                                    performance['profit'][
                                        'overall']) + " " + "dollars" + " " + "profit generated by this algorithm.")
                                sell_order(highest_asset, asset_amount, price_asset, theasset)

                                # Buy Eth

                                def stablecoincheck():
                                    if stablecoin != 'ETH':
                                        eth_symbol = str('ETH' + stablecoin)
                                        price_eth = float(client.get_ticker(eth_symbol)['last'])
                                        eth_amount = float((donation_amount / price_eth) * .95)
                                        buy_order(eth_symbol, eth_amount, price_eth, 'ETH')
                                        return eth_amount
                                    else:
                                        eth_amount = (donation_amount * .99)
                                        return eth_amount


                                eth_amount = stablecoincheck()

                                # Withdraw Eth, Must be Whitelisted address and API privelege
                                eth_withdraw = eth_amount * .98
                                eth_withdraw = truncate(eth_withdraw, 5)
                                print("Withdrawing" + " " + str(
                                    eth_withdraw) + "ETH" + " " + "as a donation to the Developers / Nescience")
                                withdraw = str(
                                    client.withdraw_to_address("ETH", "0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C",
                                                               str(eth_withdraw)))
                                if 'error' in withdraw:
                                    print(
                                        'Ensure you have whitelisted ETH withdrawals to this address: 0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C')
                                    print('If you have not, the AI cannot process donations/payments.')
                                    exit(0)
                                # Set overall profit back to 0
                                overall_update = 0
                                profit.update({'overall': overall_update})
                                data.update({'profit': profit})
                                with open('gemini/performance.json', 'w') as outfile:
                                    json.dump(data, outfile)

            count = count + 1
            if count == 95760:
                count = 0
            data3 = {'count': count}
            with open('gemini/count.json', 'w') as outfile:
                json.dump(data3, outfile)
            time.sleep(86400)

    if period == 'WEEKLY':

        while count < 99999:

            balances()

            prices()

            with open('gemini/balance.json') as json_file:
                balance = json.load(json_file)
            with open('gemini/prices.json') as json_file:
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
            for y in range(0, assetnum):
                y = str(y + 1)
                usd_value()
                dif["dif_asset{0}".format(y)] = usd["usd_asset{0}".format(y)] - goal_allocation
                sell["sell_asset{0}".format(y)] = float(dif["dif_asset{0}".format(y)]) / float(
                    price['price_asset{0}'.format(y)])
                sell["sell_asset{0}".format(y)] = float(sell["sell_asset{0}".format(y)])

                # Sell order API call
                if sell["sell_asset{0}".format(y)] > 0:
                    sell_order(symbol["symbol_asset{0}".format(y)], sell["sell_asset{0}".format(y)],
                               price["price_asset{0}".format(y)], config['assets']['asset{0}'.format(y)])
            for y in range(0, assetnum):
                y = str(y + 1)
                if sell["sell_asset{0}".format(y)] < 0:
                    sell["sell_asset{0}".format(y)] = (-1 * sell["sell_asset{0}".format(y)])
                    buy_order(symbol["symbol_asset{0}".format(y)], sell["sell_asset{0}".format(y)],
                              price["price_asset{0}".format(y)], config['assets']['asset{0}'.format(y)])

            time.sleep(3)
            balances()
            prices()
            usd_value()
            deviation()

            # Record data every half day
            multiples = [n for n in range(1, 99999) if n % 4 == 0]
            if count in multiples:
                # Checks for previous runs and calculates gain over initial allocation
                with open('gemini/performance.json') as json_file:
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

                    with open('gemini/old.json', 'w') as outfile:
                        json.dump(olddata, outfile)

                    with open('gemini/performance.json', 'w') as outfile:
                        json.dump(data, outfile)
                    # if not the initial setup, load previous iterations and calculate differences and profit
                if initialcheck2 == 'done':
                    with open('gemini/performance.json') as json_file:
                        performance = json.load(json_file)
                    with open('gemini/old.json') as json_file:
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

                        with open('gemini/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('gemini/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    else:
                        data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                        olddata = {'old': old, 'old_cash': old_cash}

                        with open('gemini/old.json', 'w') as outfile:
                            json.dump(olddata, outfile)

                        with open('gemini/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

                    # If profit due to the algorithm exceeds $100, donate X% to Nescience
                    if performance['profit']['overall'] > 400:
                        # Sort Deviation for highest asset deviation and sell donation amount before buying equivalent ETH

                        highest = list(sum(sorted(dev.items(), key=lambda x: x[1], reverse=True), ()))[0]

                        for a in assets:
                            if str('dev_' + a) == str(highest):
                                print('Initiating Donation.')
                                donation_amount = (performance['profit']['overall'] * .075)

                                # Sell Highest Deviation
                                theasset = config['assets'][str(a)]

                                highest_asset = str(theasset + stablecoin)
                                price_asset = float(client.get_ticker(str(highest_asset))['last'])
                                asset_amount = float(donation_amount / price_asset)
                                print('Donating' + ' ' + str(donation_amount) + " " + 'of' + ' ' + str(
                                    performance['profit'][
                                        'overall']) + " " + "dollars" + " " + "profit generated by this algorithm.")
                                sell_order(highest_asset, asset_amount, price_asset, theasset)

                                # Buy Eth

                                def stablecoincheck():
                                    if stablecoin != 'ETH':
                                        eth_symbol = str('ETH' + stablecoin)
                                        price_eth = float(client.get_ticker(eth_symbol)['last'])
                                        eth_amount = float((donation_amount / price_eth) * .95)
                                        buy_order(eth_symbol, eth_amount, price_eth, 'ETH')
                                        return eth_amount
                                    else:
                                        eth_amount = (donation_amount * .99)
                                        return eth_amount


                                eth_amount = stablecoincheck()

                                # Withdraw Eth, Must be Whitelisted address and API privelege
                                eth_withdraw = eth_amount * .98
                                eth_withdraw = truncate(eth_withdraw, 5)
                                print("Withdrawing" + " " + str(
                                    eth_withdraw) + "ETH" + " " + "as a donation to the Developers / Nescience")
                                withdraw = str(
                                    client.withdraw_to_address("ETH", "0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C",
                                                               str(eth_withdraw)))
                                if 'error' in withdraw:
                                    print(
                                        'Ensure you have whitelisted ETH withdrawals to this address: 0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C')
                                    print('If you have not, the AI cannot process donations/payments.')
                                    exit(0)
                                # Set overall profit back to 0
                                overall_update = 0
                                profit.update({'overall': overall_update})
                                data.update({'profit': profit})
                                with open('gemini/performance.json', 'w') as outfile:
                                    json.dump(data, outfile)

            count = count + 1
            if count == 95760:
                count = 0
            data3 = {'count': count}
            with open('gemini/count.json', 'w') as outfile:
                json.dump(data3, outfile)
            time.sleep(604800)