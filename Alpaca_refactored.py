from time import sleep
from sys import exit
import time
import datetime
import json
import alpaca_trade_api as tradeapi
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
            assets["asset{0}".format(x)] = input('asset' + " " + x + ':')
        threshold = input("Algorithm Threshold= ")
        threshold = float(threshold)
        threshold = (.01 * threshold)
        configcheck = 'configured'
        configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum}
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
                assets["asset{0}".format(x)] = input('asset' + " " + x + ':')
            threshold = input("Algorithm Threshold= ")
            threshold = float(threshold)
            threshold = (.01 * threshold)
            configcheck = 'configured'
            configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum}
            with open('alpaca/config.json', 'w') as outfile:
                json.dump(configuration, outfile)

        else:
            assetnum = config['assetnum']
            assetnum = int(assetnum)
            assets = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                assets["asset{0}".format(x)] = config['assets']["asset{0}".format(x)]
            threshold = config['threshold']
            configcheck = 'configured'
            configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum}
            with open('alpaca/config.json', 'w') as outfile:
                json.dump(configuration, outfile)


def balances():
    # Pull  balance for each selected asset
    global cash_balance
    global balance

    # Balance USD
    cash_balance = alpaca.get_account().cash
    cash_balance = float(cash_balance)
    # Get Balances of each previously entered asset
    balance = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        try:
            balance["balance_asset{0}".format(x)] = round(alpaca.get_position(assets[str('asset' + x)]).qty)
        except:
            balance["balance_asset{0}".format(x)] = 0
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
        price["price_asset{0}".format(x)] = float(alpaca.polygon.last_trade(assets["asset{0}".format(x)]).price)

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
    if market == 'True':
        print("Selling" + " " + str(sell_asset) + " " + "of" + " " + str(asset))
        alpaca.submit_order(
            symbol=asset,
            qty=sell_asset,
            side='sell',
            type='market',
            time_in_force='gtc')


def buy_order(asset, buy_asset):
    # Buy order logic
    buy_asset = round(buy_asset)
    market = str(alpaca.get_clock().is_open)
    if market == 'True':
        print("Buying" + " " + str(buy_asset) + " " + "of" + " " + str(asset))
        alpaca.submit_order(
            symbol=asset,
            qty=buy_asset,
            side='buy',
            type='market',
            time_in_force='gtc')

    # MAIN


API_KEY = "PKH47JEKAPDBW0D74MAY"
API_SECRET = "YbQgI3NpwPLHend0FcKNiXnzmND5euPewKeQfbNV"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

alpaca = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')
# allocation = .99 / len(assets)

with open('alpaca/config.json') as json_file:
    config = json.load(json_file)
    configcheck = config['configcheck']

with open('alpaca/initial.json') as json_file:
    initial = json.load(json_file)
    initialcheck = initial['initialcheck']

with open('alpaca/prices.json') as json_file:
    price = json.load(json_file)

setup()

allocation = (.985 / assetnum)

balances()

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

    usd_value()

    deviation()

    # print date and asset deviations

    print(datetime.datetime.now().time())

    for x in range(0, assetnum):
        x = str(x + 1)
        print(
            "Asset: " + assets["asset{0}".format(x)] + " :::: " + "Current Variation: " + str(dev["dev_asset{0}".format(x)] * 100) + "%")

    # Sell order trade trigger
    for x in range(0, assetnum):
        x = str(x + 1)
        balances()
        usd_value()
        deviation()
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
    time.sleep(3)
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
                    buy["buy_asset{0}".format(x)] = (-1 * buy["buy_asset{0}".format(x)])
                    sell_order(assets["asset{0}".format(x)], buy["buy_asset{0}".format(x)])
            for x in range(0, assetnum):
                x = str(x + 1)
                if buy["buy_asset{0}".format(x)] > 0:
                    buy_order(assets["asset{0}".format(x)], buy["buy_asset{0}".format(x)])

    balances()
    usd_value()
    deviation()
    # Record data every half day
    multiples = [n for n in range(1, 99999) if n % 5040 == 0]
    if count in multiples:
        # Checks for previous runs and calculates gain over initial allocation
        with open('alpaca/performance.json') as json_file:
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
                compare["compare_asset{0}".format(x)] = (initial["initial_balance_asset{0}".format(x)] * price["price_asset{0}".format(x)])

                # save current balances for future reference
                old["old_asset{0}".format(x)] = balance["balance_asset{0}".format(x)]

                # calculate profit of current usd value vs initial balance usd value
                compare["compare_asset{0}".format(x)] = float(compare["compare_asset{0}".format(x)])
                profit["profit_asset{0}".format(x)] = usd["usd_asset{0}".format(x)] - compare["compare_asset{0}".format(x)]
            compare_cash = cash_balance

            # calculate profits of the small cash pool
            profit_cash = compare_cash - cash_balance
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

            data = {'old': old, 'compare': compare, 'profit': profit, 'compare_cash': compare_cash, 'initialcheck2': initialcheck2}

            with open('alpaca/performance.json', 'w') as outfile:
                json.dump(data, outfile)
            # if not the initial setup, load previous iterations and calculate differences and profit
        else:
            with open('alpaca/performance.json') as json_file:
                performance = json.load(json_file)

            compare = {}
            old = {}
            profit = {}

            for x in range(0, assetnum):
                x = str(x + 1)
                # call old asset balance from Performance and set as new old asset dict
                old["old_asset{0}".format(x)] = performance['old']["old_asset{0}".format(x)]

                # calculate today's value of previous balances
                compare["compare_asset{0}".format(x)] = (old["old_asset{0}".format(x)] * price["price_asset{0}".format(x)])

                # calculate profit of current usd value vs previous iteration balance usd value
                compare["compare_asset{0}".format(x)] = float(compare["compare_asset{0}".format(x)])
                profit["profit_asset{0}".format(x)] = (usd["usd_asset{0}".format(x)] - compare["compare_asset{0}".format(x)])

            # calculate profit over previous cash pool
            profit_cash = cash_balance - performance['compare_cash']

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
            compare_cash = cash_balance

            # If portfolio > previous iteration, add to overall profit
            profit['overall'] = performance['profit']['overall']
            initialcheck2 = 'done'
            if profit['current'] >= 0:
                profit['overall'] = profit['current'] + profit['overall']

                data = {'old': old, 'compare': compare, 'profit': profit, 'compare_cash': compare_cash, 'initialcheck2': initialcheck2}

                with open('alpaca/performance.json', 'w') as outfile:
                    json.dump(data, outfile)

            else:
                data = {'old': old, 'compare': compare, 'profit': profit, 'compare_cash': compare_cash, 'initialcheck2': initialcheck2}
                with open('alpaca/performance.json', 'w') as outfile:
                    json.dump(data, outfile)

            # If profit due to the algorithm exceeds $100, donate X% to Nescience
            if performance['profit']['overall'] > 100:
                print('withdraw orders here')

    count = count + 1
    data3 = {'count': count}
    with open('alpaca/count.json', 'w') as outfile:
        json.dump(data3, outfile)
    time.sleep(60)
