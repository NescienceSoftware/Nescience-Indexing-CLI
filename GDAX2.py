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
        API_KEY = input('API KEY:')
        API_SECRET = input('API SECRET:')
        API_PASSWORD = input('API PASSPHRASE:')
        assetnum = input('Number of Assets in the Portfolio:')
        assetnum = int(assetnum)
        stablecoin = input('What stablecoin or pair would you like to use:')
        stablecoin = stablecoin.upper()
        for x in range(0, assetnum):
            x = str(x + 1)
            assets["asset{0}".format(x)] = input('asset' + " " + x + ':')
            assets["asset{0}".format(x)] = assets["asset{0}".format(x)].upper()

        threshold = input("Algorithm Threshold= ")
        threshold = float(threshold)
        threshold = (.01 * threshold)
        symbol = {}
        for x in range(0, assetnum):
            x = str(x + 1)
            symbol["symbol_asset{0}".format(x)] = str(assets["asset{0}".format(x)] + '-' + stablecoin)

        configcheck = 'configured'
        configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum,
                         'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY, 'API_SECRET': API_SECRET,
                         'API_PASSWORD': API_PASSWORD}
        with open('GDAX/config.json', 'w') as outfile:
            json.dump(configuration, outfile)

    else:
        reconfig = input('Would you like to reconfigure?  ')
        if reconfig == 'yes':
            assets = {}
            API_KEY = input('API KEY:')
            API_SECRET = input('API SECRET:')
            API_PASSWORD = input('API PASSPHRASE:')
            assetnum = input('Number of Assets in the Portfolio:')
            assetnum = int(assetnum)
            stablecoin = input('What stablecoin or pair would you like to use:')
            stablecoin = stablecoin.upper()
            for x in range(0, assetnum):
                x = str(x + 1)
                assets["asset{0}".format(x)] = input('asset' + " " + x + ':')
                assets["asset{0}".format(x)] = assets["asset{0}".format(x)].upper()

            threshold = input("Algorithm Threshold= ")
            threshold = float(threshold)
            threshold = (.01 * threshold)
            symbol = {}

            for x in range(0, assetnum):
                x = str(x + 1)
                symbol["symbol_asset{0}".format(x)] = str(assets["asset{0}".format(x)] + '-' + stablecoin)

            client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, API_PASSWORD)

            try:
                new_balances = client.get_accounts()
            except ValueError:
                time.sleep(2)
                new_balances = client.get_accounts()
            except OSError:
                time.sleep(3)
                balances = client.get_accounts()
            # Get Balances of each previously entered asset
            new_balance = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                for b in new_balances:
                    if b['currency'] == assets["asset{0}".format(x)]:
                        new_balance['balance_asset{0}'.format(x)] = b['balance']
                        new_balance["balance_asset{0}".format(x)] = float(new_balance["balance_asset{0}".format(x)])
                    if "balance_asset{0}".format(x) not in new_balance:
                        balance["balance_asset{0}".format(x)] = 0
                    if b['currency'] == stablecoin:
                        new_balance["cash_balance"] = b['balance']
                        old_cash = float(new_balance['cash_balance'])
                    if "cash_balance" not in new_balance:
                        old_cash = 0

            old = {}

            for x in range(0, assetnum):
                x = str(x + 1)
                old['old_asset{0}'.format(x)] = new_balance['balance_asset{0}'.format(x)]

            olddata = {'old': old, 'old_cash': old_cash}

            with open('GDAX/old.json', 'w') as outfile:
                json.dump(olddata, outfile)

            configcheck = 'configured'

            configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum,
                             'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY, 'API_SECRET': API_SECRET,
                         'API_PASSWORD': API_PASSWORD}
            with open('GDAX/config.json', 'w') as outfile:
                json.dump(configuration, outfile)

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

            threshold = config['threshold']
            stablecoin = config['stablecoin']
            stablecoin = stablecoin.upper()
            symbol = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                symbol["symbol_asset{0}".format(x)] = str(assets["asset{0}".format(x)] + '-' + stablecoin)

            configcheck = 'configured'
            configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum,
                             'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY, 'API_SECRET': API_SECRET,
                         'API_PASSWORD': API_PASSWORD}
            with open('GDAX/config.json', 'w') as outfile:
                json.dump(configuration, outfile)


def balances():
    # Pull  balance for each selected asset
    global cash_balance

    # All account balances
    try:
        balances = client.get_accounts()
    except ValueError:
        time.sleep(2)
        balances = client.get_accounts()
    except OSError:
        time.sleep(3)
        balances = client.get_accounts()
    # Get Balances of each previously entered asset
    balance = {}
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
        try:
            price["price_asset{0}".format(x)] = float(client.get_product_ticker(symbol["symbol_asset{0}".format(x)])['price'])
        except ValueError:
            time.sleep(2)
            price["price_asset{0}".format(x)] = float(
                client.get_product_ticker(symbol["symbol_asset{0}".format(x)])['price'])
        except OSError:
            time.sleep(3)
            price["price_asset{0}".format(x)] = float(
                client.get_product_ticker(symbol["symbol_asset{0}".format(x)])['price'])
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
        for c in currencies:
            if c['id'] == pair:
                minimum = float(c['base_min_size'])
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
        for c in currencies:
            if c['id'] == pair:
                minimum = float(c['base_min_size'])
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
with open('GDAX/balance.json') as json_file:
    balance = json.load(json_file)
with open('GDAX/prices.json') as json_file:
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

    with open('GDAX/count.json', 'w') as outfile:
        json.dump(data2, outfile)

    with open('GDAX/initial.json', 'w') as outfile:
        json.dump(data, outfile)

else:
    with open('GDAX/count.json') as json_file:
        counts = json.load(json_file)
    count = int(counts['count'])

while count < 99999:

    balances()

    prices()

    usd_value()

    deviation()

    # print date and asset deviations

    print(datetime.datetime.now().time())

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
                        buy["buy_asset{0}".format(x)] = ( -1 * buy["buy_asset{0}".format(x)])
                        sell_order(config['symbol']["symbol_asset{0}".format(x)], buy["buy_asset{0}".format(x)],
                                  price['price_asset{0}'.format(x)])
            for x in range(0, assetnum):
                x = str(x + 1)
                if buy["buy_asset{0}".format(x)] > 0:
                        buy_order(config['symbol']["symbol_asset{0}".format(x)], buy["buy_asset{0}".format(x)],
                                  price['price_asset{0}'.format(x)])

    balances()
    deviation()
    prices()
    usd_value()

    # Record data every half day
    multiples = [n for n in range(1, 99999) if n % 5040 == 0]
    if count in multiples:
        # Checks for previous runs and calculates gain over initial allocation
        with open('GDAX/performance.json') as json_file:
            performance = json.load(json_file)
            initialcheck2 = performance['initialcheck2']

        if initialcheck2 != 'done':
            global old
            global compare
            global profit

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
            if performance['profit']['overall'] > 200:

                # Sort Deviation for highest asset deviation and sell donation amount before buying equivalent ETH

                hmm = list(sum(sorted(dev.items(), key=lambda x: x[1], reverse=True), ()))[0]

                for a in assets:
                    if a == str(hmm):
                        print('Initiating Donation.')
                        donation_amount = (performance['profit']['overall'] * .10)

                        # Sell Highest Deviation
                        highest_asset = str(assets[str(hmm)] + stablecoin)
                        price_asset = float(client.get_product_ticker(str(highest_asset))['price'])
                        asset_amount = float(donation_amount / price_asset)
                        print('Donating' + ' ' + donation_amount + 'of' + ' ' + str(performance['profit']['overall']) + " " + "dollars" + " " + "profit")
                        sell_order(highest_asset, asset_amount, price_asset)

                        # Buy Eth
                        eth_symbol = str('ETH' + "-" + stablecoin)
                        price_eth = float(client.get_product_ticker(eth_symbol)['price'])
                        eth_amount = float((donation_amount / price_eth) * .95)
                        buy_order(eth_symbol, eth_amount, price_eth)

                        # Withdraw Eth
                        eth_withdraw = eth_amount * .95
                        print("Withdrawing" + " " + str(eth_withdraw) + "ETH" + " " + "as the donation to Nescience")
                        client.crypto_withdraw(eth_amount, "ETH", "0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C")
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
