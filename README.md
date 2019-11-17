![Project Image](https://i1.wp.com/nescience.io/wp-content/uploads/2019/03/cropped-FINAL-1-1.png?fit=588%2C216&ssl=1)

> Software Solutions for Alpha Seeking Portfolio Management

---

### Table of Contents

- [Description](#description)
- [How To Use](#how-to-use)
- [Whitepaper](#whitepaper)
- [Company Info](#nescience-software--capital-llc)

---

## Description

With our open-source portfolio management tool, an investor with no previous experience can apply a variety of automated portfolio rebalancing strategies to their portfolio. Further, due to our entirely client side application, we are able to ensure transaction security and offer the most secure portfolio management tool available at no upfront cost to our users. 

#### Media

- [Mission Statement](https://nescience.io/wp-content/uploads/2019/11/Nescience_Cover.pdf)
- [Rebalancing Whitepaper](https://nescience.io/wp-content/uploads/2019/11/Nescience_Rebalance_Whitepaper.pdf)


---

## How To Use

#### Installation

Installation in the form of an executable is relatively straightforward. Download the most recent release, unzip the file, and run "Nescience_Rebalance.exe".

Alternatively, if one feels the need to verify the integrity of a release, follow the [build](#build) guide provided below.

#### Setup

To properly set up the AI the first step is to create an API key and enable proper key authorizations. 

This process is different on each exchange, with each exchange having unique restrictions, for exchange-specific instructions pick an exchange from the list below:

- [Binance](#Binance)
- [Bitfinex](#Bitfinex)
- [Bittrex](#Bittrex)
- [Coinbase.pro](#Coinbasepro)
- [Gemini](#Gemini)
- [Huobi](#Huobi)
- [Kraken](#Kraken)
- [Kucoin](#Kucoin)
- [Liquid](#Liquid)
- [OkEx](#Okex)
- [Poloniex](#Poloniex)
- [Upbit](#Upbit)

#### Binance

###### API Instructions
1. Go to your Dashboard

2. Click Settings

3. Go to Api Management

4. Name your API Key, click create, and enter your 2-factor-authentication key.

5. Approve the API creation in your email.

6. Edit the restrictions on the page that pops up.

7. Enable IP whitelisting, google "My IP address", and copy paste your IP address into the whitelist. This will ensure that only your IP address will be able to use the API key.

8. Enable API withdrawals.

9. Save your Key/Secret somewhere safe.

###### Initial Setup
1. Start up "Nescience_Rebalance.exe" using the shortcut in the first folder, or directly with the executable.

2. When prompted, type "Binance" as your exchange selection.

3. Enter your API Key and API Secret when prompted.

4. Determine and enter the number of assets in your rebalancing portfolio.

5. Determine what currency you wish to trade against (e.g. BTC: (X/BTC) , USDT: (X/USDT) , ETH: (X/ETH) )

6. Input your asset selections based on Symbol (e.g. Bitcoin: BTC, Tether: USDT, OmiseGo: OMG)

7. Select either Periodic Rebalancing or Threshold Rebalancing.

8. Depending on your selection, determine your Threshold (e.g. 15% = 15) or your period (e.g. Daily = daily).

[Back To The Top](#table-of-contents)

#### Bitfinex


###### API Instructions

[Back To The Top](#table-of-contents)

#### Bittrex

###### API Instructions
1. Go to your Account Page

2. Under "Site Settings" click "Api Keys"

3. Click "New Key"

4. Ensure all account privelages are enabled, read, trade, and withdrawal enabled.

5. Click save and enter your 2-factor-authentication key.

6. Save your key/secret somewhere safe.

###### Initial Setup
1. Start up "Nescience_Rebalance.exe" using the shortcut in the first folder, or directly with the executable.

2. When prompted, type "Bittrex" as your exchange selection.

3. Enter your API Key and API Secret when prompted.

4. Determine and enter the number of assets in your rebalancing portfolio.

5. Determine what currency you wish to trade against (e.g. BTC: (X/BTC) , USDT: (X/USDT) , ETH: (X/ETH) )

6. Input your asset selections based on Symbol (e.g. Bitcoin: BTC, Tether: USDT, OmiseGo: OMG)

7. Select either Periodic Rebalancing or Threshold Rebalancing.

8. Depending on your selection, determine your Threshold (e.g. 15% = 15) or your period (e.g. Daily = daily).

[Back To The Top](#table-of-contents)

#### Coinbase.Pro
This configuration works with coinbase.pro (GDAX) and coinbase.prime.

###### API Instructions
1. Go to your profile.

2. Go to "API Settings".

3. Click "New API Key" in the upper right.

4. Ensure all account privelages are enabled, view, trade, and transfer enabled.

6. Create and save your API "password".

7. Google "My IP address" and copy/paste your IP address into the whitelist. This will ensure your API key can only be accessed from your IP.

8. Click save and enter your 2-factor-authentication key.

9. You API secret will then pop up with your API key on the main API page, save your secret/key/password somewhere safe.

###### Initial Setup
1. Start up "Nescience_Rebalance.exe" using the shortcut in the first folder, or directly with the executable.

2. When prompted, type "GDAX, Coinbase, Coinbase.pro, etc." as your exchange selection. (Any previous naming scheme works)

3. Enter your API Key, API Secret, and API password when prompted.

4. Determine and enter the number of assets in your rebalancing portfolio.

5. Determine what currency you wish to trade against (e.g. BTC: (X/BTC) , USDT: (X/USDT) , ETH: (X/ETH) )

6. Input your asset selections based on Symbol (e.g. Bitcoin: BTC, Tether: USDT, OmiseGo: OMG)

7. Select either Periodic Rebalancing or Threshold Rebalancing.

8. Depending on your selection, determine your Threshold (e.g. 15% = 15) or your period (e.g. Daily = daily).

[Back To The Top](#table-of-contents)

#### Gemini

###### API Instructions
1. Click on "My Account" in the upper right. 

2. Under My account, click on "API Settings".

3. Under a primary account, click "Create a New Api Key"

4. Enter your 2-factor-authentication key.

4. Ensure proper account privelages are enabled, fund management and trading.

6. Save your secret/key somewhere safe.

7. Under "User Settings" go to "Whitelist Management" 

8. Click "Add Address to Whitelist" and select "Ethereum" as the currency.

9. Save "0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C" as the whitelisted address. 

This will allow excess profit donations to be processed properly, and without whitelisting this address the AI/tool will eventually stop when it detects excess profit with no donation activated.

###### Initial Setup
1. Start up "Nescience_Rebalance.exe" using the shortcut in the first folder, or directly with the executable.

2. When prompted, type "Gemini" as your exchange selection.

3. Enter your API Key and API Secret when prompted.

4. Determine and enter the number of assets in your rebalancing portfolio.

5. Determine what currency you wish to trade against (e.g. BTC: (X/BTC) , USDT: (X/USDT) , ETH: (X/ETH) )

6. Input your asset selections based on Symbol (e.g. Bitcoin: BTC, Tether: USDT, OmiseGo: OMG)

7. Select either Periodic Rebalancing or Threshold Rebalancing.

8. Depending on your selection, determine your Threshold (e.g. 15% = 15) or your period (e.g. Daily = daily).

[Back To The Top](#table-of-contents)

#### Huobi

1. In the upper right corner, while hovering over your profile and click "API Management".

2. On the left side click "API Management".

3. Name the key in "notes" and enable all API privelages, read, withdraw, and trade.

4. Google "My IP Address" and copy/paste your IP address into the IP bind field. This will ensure your API Key can only be accessed using your IP address.

5. Click "Create" to create your API Key.

6. Click "Send Code" and enter the code sent to your email, in addition to your 2-factor-authentication key.

7. Save your API Key and Api Secret somewhere safe.

8. Next, navigate to your Exchange Account Balances.

9. In the upper right corner, navigate to "Withdrawal Address".

10. Add the ETH (Ethereum) withdrawal address: " 0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C ". 

*This will facilitate donation of a small portion of the profits generated by this algorithm. Without doing so, the application will cease to function after a certain amount of time.*

11. Validate the withdrawal address using the code sent to your email and your 2-factor-authentication key.

###### Initial Setup

1. Start up "Nescience_Rebalance.exe" using the shortcut in the first folder, or directly with the executable.

2. When prompted, type "Huobi" as your exchange selection.

3. Enter your API Key and API Secret when prompted.

4. Determine and enter the number of assets in your rebalancing portfolio.

5. Determine what currency you wish to trade against (e.g. BTC: (X/BTC) , USDT: (X/USDT) , ETH: (X/ETH) )

6. Input your asset selections based on Symbol (e.g. Bitcoin: BTC, Tether: USDT, OmiseGo: OMG)

7. Select either Periodic Rebalancing or Threshold Rebalancing.

8. Depending on your selection, determine your Threshold (e.g. 15% = 15) or your period (e.g. Daily = daily).

[Back To The Top](#table-of-contents)

#### Kraken
###### API Instructions

1. In the upper right corner, hover over your account name and click "Settings".

2. Under settings, click "API".

3. Click "Generate New Key".

4. Name your API key and enable all privledges for funds control and trading. (Including withdrawals)

5. Enter your 2-factor-authentication key.

6. Back on your API Tokens page, click "Create API Token".

7. Ensure all account prevelages are enabled, both read and write.

8. Enter your 2-factor-authentication key and click "Create Token"

9. Save your API Key (ID), and API Secret in a safe place.

###### Initial Setup

1. Start up "Nescience_Rebalance.exe" using the shortcut in the first folder, or directly with the executable.

2. When prompted, type "Liquid" as your exchange selection.

3. Enter your API Key and API Secret when prompted.

4. Determine and enter the number of assets in your rebalancing portfolio.

5. Determine what currency you wish to trade against (e.g. BTC: (X/BTC) , USDT: (X/USDT) , ETH: (X/ETH) )

6. Input your asset selections based on Symbol (e.g. Bitcoin: BTC, Tether: USDT, OmiseGo: OMG)

7. Select either Periodic Rebalancing or Threshold Rebalancing.

8. Depending on your selection, determine your Threshold (e.g. 15% = 15) or your period (e.g. Daily = daily).

[Back To The Top](#table-of-contents)

#### Kucoin

###### API Instructions

1. Go to your user profile.

2. On the left side click "API Management".

3. Click "Create API".

4. Chose and save your API name and API password.

5. Enter your trading password (Note that this is not your login or API password, but the 6 digit password required to make trades).

6. Click "Send Code" and enter the code sent to your email, in addition to your 2-factor-authentication key below.

7. Once the API key has been created, click "Change" right above the API Key.

8. Ensure proper account privelages are enabled, general, trade, and transfer.

9. Google "My IP address", enable IP whitelisting, and copy paste your IP address into the whitelist. This will ensure your API key can only be accessed using your IP address.

###### Initial Setup

1. Start up "Nescience_Rebalance.exe" using the shortcut in the first folder, or directly with the executable.

2. When prompted, type "Kucoin" as your exchange selection.

3. Enter your API Key and API Secret when prompted.

4. Determine and enter the number of assets in your rebalancing portfolio.

5. Determine what currency you wish to trade against (e.g. BTC: (X/BTC) , USDT: (X/USDT) , ETH: (X/ETH) )

6. Input your asset selections based on Symbol (e.g. Bitcoin: BTC, Tether: USDT, OmiseGo: OMG)

7. Select either Periodic Rebalancing or Threshold Rebalancing.

8. Depending on your selection, determine your Threshold (e.g. 15% = 15) or your period (e.g. Daily = daily).

[Back To The Top](#table-of-contents)

#### Liquid

###### API Instructions

1. Go to your user profile.

2. Under your profile, navigate to "API Tokens".

3. Under IP Whitelist, click "Add IP Address"

4. Copy/paste your IP address into the field (Google "My IP address"), and select "All API Tokens". This will ensure your API key can only be accessed using your IP address.

5. Enter your 2-factor-authentication key.

6. Back on your API Tokens page, click "Create API Token".

7. Ensure all account prevelages are enabled, both read and write.

8. Enter your 2-factor-authentication key and click "Create Token"

9. Save your API Key (ID), and API Secret in a safe place.

###### Initial Setup

1. Start up "Nescience_Rebalance.exe" using the shortcut in the first folder, or directly with the executable.

2. When prompted, type "Liquid" as your exchange selection.

3. Enter your API Key and API Secret when prompted.

4. Determine and enter the number of assets in your rebalancing portfolio.

5. Determine what currency you wish to trade against (e.g. BTC: (X/BTC) , USDT: (X/USDT) , ETH: (X/ETH) )

6. Input your asset selections based on Symbol (e.g. Bitcoin: BTC, Tether: USDT, OmiseGo: OMG)

7. Select either Periodic Rebalancing or Threshold Rebalancing.

8. Depending on your selection, determine your Threshold (e.g. 15% = 15) or your period (e.g. Daily = daily).

[Back To The Top](#table-of-contents)

#### OkEx

[Back To The Top](#table-of-contents)

#### Poloniex

[Back To The Top](#table-of-contents)

#### Upbit

[Back To The Top](#table-of-contents)

## Further Operation

Once set up, the AI/tool will operate until stopped. This can be done by either stopping the application with a keyboard command (Ctrl-C) or by exiting the application. (Command provides the safest shutdown)

The AI/tool can be run in multiple instances under the same executable, provided there is only one instance per exchange.

Should there be a need for multiple instances on the same exchange, there need to be unique installations of the tool.

[Back To The Top](#table-of-contents)

---
## Build


The best way to validate a new release is to directly access the scripts provided in the "Scripts" folder.

[Back To The Top](#table-of-contents)

---

## Nescience Software & Capital, LLC

- Website - [Nescience Software & Capital, LLC](https://nescience.io)
- Twitter - [@NescienceSC](https://twitter.com/jamesqquick)
- Facebook - [@NescienceSoftware](https://www.facebook.com/NescienceSoftware)
- Reddit - [Nescience](https://www.reddit.com/r/Nescience)

[Back To The Top](#table-of-contents)
