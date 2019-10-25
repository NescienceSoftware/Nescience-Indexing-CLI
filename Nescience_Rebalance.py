exchange = input('What exchange would you like to use:')
exchange = exchange.upper()

if exchange == 'ALPACA':
    import Alpaca_refactored

if exchange == 'UPBIT':
    import Upbit2

if exchange == 'BINANCE':
    import Binance2

if exchange == 'BITTREX':
    import Bittrex2

if exchange == 'BITFINEX':
    import Bitfinex3

if exchange == 'GDAX' or exchange == 'COINBASE' or exchange == 'COINBASE.PRO' or exchange == 'COINBASE PRO' or exchange == 'COINBASEPRO':
    import GDAX2

if exchange == 'GEMINI':
    import Gemini2

if exchange == 'IDEX':
    import IDEX2

if exchange == 'KUCOIN':
    import Kucoin2

if exchange == 'POLONIEX':
    import Poloniex2

if exchange == 'HUOBI' or exchange == 'HUOBIPRO':
    import Huobi2

if exchange == 'KRAKEN':
    import Kraken

if exchange == 'BIBOX':
    import Bibox2

else:
    print('Please check the spelling of your exchange.')


