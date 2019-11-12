exchange = input('What exchange would you like to use:')
exchange = exchange.upper()

if exchange == 'ALPACA':
    import Alpaca_refactored

if exchange == 'UPBIT':
    import UpbitPeriodic

if exchange == 'BINANCE':
    import BinancePeriodic

if exchange == 'BITTREX':
    import BittrexPeriodic

if exchange == 'BITFINEX':
    import BitfinexPeriodic

if exchange == 'GDAX' or exchange == 'COINBASE' or exchange == 'COINBASE.PRO' or exchange == 'COINBASE PRO' or exchange == 'COINBASEPRO':
    import GDAXPeriodic

if exchange == 'GEMINI':
    import GeminiPeriodic

if exchange == 'KUCOIN':
    import KucoinPeriodic

if exchange == 'POLONIEX':
    import PoloniexPeriodic

if exchange == 'HUOBI' or exchange == 'HUOBIPRO':
    import HuobiPeriodic

if exchange == 'KRAKEN':
    import KrakenPeriodic

if exchange == 'LIQUID' or exchange == 'Quoine' or exchange == 'Quoinex' or exchange == 'Qryptos':
    import LiquidPeriodic

if exchange == 'OKEX':
    import OkExPeriodic

else:
    print('Please check the spelling of your exchange.')


