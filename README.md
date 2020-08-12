![Project Image](https://nescience.io/wp-content/uploads/2020/01/Official.png)

> Software Solutions for Alpha Seeking Portfolio Management

---

### [Whitepaper](https://nescience.io/wp-content/uploads/2019/11/Nescience_Rebalance_Whitepaper.pdf)

---

### Table of Contents

- [Description](#description)
- [Setup](#how-to-use)
- [Further Operation](#further-operation)
- [Build Instructions](#build)
- [Company Information](#nescience-software--capital-llc)


---

## Description

With our open-source portfolio management tool, an investor with no previous experience can apply a variety of automated portfolio rebalancing strategies to their portfolio. Further, due to our entirely client side application, we are able to ensure transaction security and offer the most secure portfolio management tool available at no upfront cost to our users. 

A demo of our tool can be found operating 24/7 on our twitch channel: [NescienceSoftware](https://www.twitch.tv/nesciencesoftware)

#### Media

- [Mission Statement](https://nescience.io/wp-content/uploads/2019/11/Nescience_Cover.pdf)
- [Rebalancing Whitepaper](https://nescience.io/wp-content/uploads/2019/11/Nescience_Rebalance_Whitepaper.pdf)
- [Demo](https://www.twitch.tv/nesciencesoftware)


---

## Setup

Compatable with Windows 64-bit.

#### Installation

Installation in the form of an executable is relatively straightforward. Download the most recent release, unzip the file, and run "Nescience_Rebalance.exe".

Alternatively, if one feels the need to verify the integrity of a release, follow the [build](#build) guide provided below.

#### API Configuration

To properly set up the tool the first step is to create an API key and enable proper key authorizations. 

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
- [Luno](#Luno)
- [OkEx](#Okex)
- [Poloniex](#Poloniex)
- [Upbit](#Upbit)

- [Ally](#Ally)
- [Alpaca](#Alpaca) 
- [Robinhood](#Robinhood) 

NOTE: For legal reasons we do not provide the same level of support to those utilizing traditional market clearinghouses/brokers, use of our product does not constitute liability.

---

## Operation

1. Start up "Nescience_Rebalance.exe" in the folder "Nescience_Rebalance

*Note: If a message questions the origin of the exe, do not worry, we will be getting a proper microsoft liscence ASAP.*

2. When prompted, types your exchange selection.

3. Determine and enter the number of assets in your rebalancing portfolio.

4. Determine what currency you wish to trade against (e.g. BTC: (X/BTC) , USDT: (X/USDT) , ETH: (X/ETH) )

5. Input your asset selections based on Symbol (e.g. Bitcoin: BTC, Tether: USDT, OmiseGo: OMG)

6. Select either Periodic Rebalancing or Threshold Rebalancing.

7. Depending on your selection, determine your Threshold (e.g. 15% = 15) or your period (e.g. Daily = daily).

8. Enter your API Key and API Secret when prompted.

9. Done! After you enter your threshold/period the algorithm will query your balances and begin allocation maitenence!

[Back To The Top](#table-of-contents)

---

## API Setup

#### Binance

###### API Instructions
1. Go to your Dashboard

2. Click Settings

3. Go to Api Management

4. Name your API Key, click create, and enter your 2-factor-authentication key.

5. Approve the API creation in your email.

6. Edit the restrictions on the next page that pops up.

7. Enable IP whitelisting, google "My IP address", and copy paste your IP address into the whitelist. This will ensure that only your IP address will be able to use the API key.

8. Enable API withdrawals.

9. Save your Key/Secret somewhere safe.

[Back To The Top](#table-of-contents)

---

#### Bitfinex

###### API Instructions

1. Nagivate to your Account page.

2. Navigate to "</> API".

3. Click "Create New Key".

4. Ensure all account privileges are enabled, importantly read/write capabilities for orders, wallets, and withdrawals.

5. Name your API Key, click generate and confirm API Key creation using the link sent to your email.

6. When navigated to your API Key page, save your API Key and API Secret somewhere safe.

[Back To The Top](#table-of-contents)

---

#### Bittrex

###### API Instructions
1. Go to your Account Page

2. Under "Site Settings" click "Api Keys"

3. Click "New Key"

4. Ensure all account privileges are enabled, read & trade.

5. Click save and enter your 2-factor-authentication key.

6. Save your key/secret somewhere safe.

[Back To The Top](#table-of-contents)

---

#### Coinbase.Pro
This configuration works with coinbase.pro (GDAX) and coinbase.prime.

###### API Instructions
1. Go to your profile.

2. Go to "API Settings".

3. Click "New API Key" in the upper right.

4. Ensure all account privileges are enabled, view, trade, and transfer enabled.

6. Create and save your API "password".

7. Google "My IP address" and copy/paste your IP address into the whitelist. This will ensure your API key can only be accessed from your IP.

8. Click save and enter your 2-factor-authentication key.

9. You API secret will then pop up with your API key on the main API page, save your secret/key/password somewhere safe.

[Back To The Top](#table-of-contents)

---

#### Gemini

###### API Instructions
1. Click on "My Account" in the upper right. 

2. Under My account, click on "API Settings".

3. Under a primary account, click "Create a New Api Key"

4. Enter your 2-factor-authentication key.

4. Ensure proper account privileges are enabled, fund management and trading.

6. Save your secret/key somewhere safe.

[Back To The Top](#table-of-contents)

---

#### Huobi

###### API Instructions

1. In the upper right corner, while hovering over your profile and click "API Management".

2. On the left side click "API Management".

3. Name the key in "notes" and enable all API privileges, read, withdraw, and trade.

4. Google "My IP Address" and copy/paste your IP address into the IP bind field. This will ensure your API Key can only be accessed using your IP address.

5. Click "Create" to create your API Key.

6. Click "Send Code" and enter the code sent to your email, in addition to your 2-factor-authentication key.

7. Save your API Key and Api Secret somewhere safe.

[Back To The Top](#table-of-contents)

---

#### Kraken

###### API Instructions

1. In the upper right corner, hover over your account name and click "Settings".

2. Under settings, click "API".

3. Click "Generate New Key".

4. Name your API Key and enable all privileges for funds control and trading. (Including withdrawals)

5. Save your API Key and Api Secret somewhere safe.


[Back To The Top](#table-of-contents)

---

#### Kucoin

###### API Instructions

1. Go to your user profile.

2. On the left side click "API Management".

3. Click "Create API".

4. Chose and save your API name and API password.

5. Enter your trading password (Note that this is not your login or API password, but the 6 digit password required to make trades).

6. Click "Send Code" and enter the code sent to your email, in addition to your 2-factor-authentication key below.

7. Once the API key has been created, click "Change" right above the API Key.

8. Ensure proper account privileges are enabled, general & trade.

9. Google "My IP address", enable IP whitelisting, and copy paste your IP address into the whitelist. This will ensure your API key can only be accessed using your IP address.

[Back To The Top](#table-of-contents)

---

#### Liquid

###### API Instructions

1. Go to your user profile.

2. Under your profile, navigate to "API Tokens".

3. Under IP Whitelist, click "Add IP Address"

4. Copy/paste your IP address into the field (Google "My IP address"), and select "All API Tokens". This will ensure your API key can only be accessed using your IP address.

5. Enter your 2-factor-authentication key.

6. Back on your API Tokens page, click "Create API Token".

7. Ensure all account privilege are enabled, both read and write.

8. Enter your 2-factor-authentication key and click "Create Token"

9. Save your API Key (ID), and API Secret in a safe place.

---

#### Luno

Due to jurisdiction restrictions we are currently unable to provide specific instructions for API creation on this exchange.

[Back To The Top](#table-of-contents)

---

#### OkEx

Due to jurisdiction restrictions we are currently unable to provide specific instructions for API creation on this exchange.

[Back To The Top](#table-of-contents)

---

#### Poloniex

###### API Instructions

1. In the upper right corner, hover over the wrench and click "API Keys".

2. If you have not already enabled API access, click "Enable" and confirm using your 2fa and/or the link sent to your email.

3. Next, once back on the "API Keys" page, click "Create New Key" and again confirm using your 2fa and/or the link sent to your email.

4. Save your API Key and Api Secret somewhere safe.

5. Enable Withdrawals, again confirming using the link sent to your email.

6. For added safety, you will want to enable IP Restrictions. This will ensure your API key can only be accessed using your IP address.

  7. Use the drop down and enable IP Restriction, confirming using your 2fa and/or the link sent to your email.

  8. Copy paste the IP address provided into the field and click save, again confirming using your 2fa and/or the link sent to your email.

[Back To The Top](#table-of-contents)

---

#### Upbit

Due to jurisdiction restrictions we are currently unable to provide specific instructions for API creation on this exchange.

[Back To The Top](#table-of-contents)

---

#### Ally

Ally has a unique API key schema, requiring 2 different API Key/Secret pairs.

###### API Instructions

1. Log in to your Ally invest portfolio.

2. In the bar at the top, click "Tools"

3. Select "API".

4. Once navigating to the API page, click, "Create a new application"

5. Select personal application and enter your information, with the application name being "Nescience Indexing Tool".

6. Click "Create".

7. Back on your API page, click the Nescience Indexing Tool under "Developer Applications"

8. Copy all four API Keys/Secrets and save them in a safe place.

---

#### Alpaca

The Alpaca exchange is a clearinghouse for traditional equities that primarily supports algorithmic trading. 

If interested, https://docs.alpaca.markets/ 

Remember to save your API Key and API Secret somewhere safe!

[Back To The Top](#table-of-contents)

-----------------------------------------

#### Robinhood

Robinhood allows users to take advantage of fractional shares, allowing precise maitenence of a given index or portfolio.

Unlike other exchanges, Robinhood does not authenticate using API keys, but using traditional Username/Password schemas.

[Back To The Top](#table-of-contents)

-----------------------------------------
## Further Operation

Once set up, the AI/tool will operate until stopped. This can be done by either stopping the application with a keyboard command (Ctrl-C) or by exiting the application. (Command provides the safest shutdown)

The AI/tool can be run in multiple instances under the same executable, provided there is only one instance per exchange.

Should there be a need for multiple instances on the same exchange, there need to be unique installations of the AI/tool.

**IMPORTANT**

_When adding money to a portfolio that has already been configured, ensure that you "reconfigure" your algorithm._

**If you do not, the built in profit tracking will not be able to detect the new deposit and will instead think that it is profit generated by the algorithm, resulting in unnecessary donations. Reconfiguring ensures that a new baseline is established.**

Any issues or inquiries can be directed to support@nescience.io

[Back To The Top](#table-of-contents)

----------------------------
## Build

To ensure that the most recent release is genuine, check that the PGP-signature in "Signature.txt.gpg" is that of Nescience Software & Capital. Our fingerprint will always be available on our website's home page.

Further, the best way to validate a new release is to build/compile the application yourself based on the Python scripts provided in the "Scripts" folder, while inspecting any new changes. This requires Python 3.5+ and a number of dependencies, and can be done following the steps below:

  1. If you do not already have Python 3.5+ install an appropriate version as can be found here. (https://www.python.org/downloads/)
  
  2. Open a command prompt and using these commands, download and install pip (pythons package installation tool).
  
    
    
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    
    python get-pip.py
    
    
  3. Ensure each dependency listed in "Dependencies.txt" are installed using pip.
  
    
    
    pip install 'package==version"
    
    
    
  4. For each exchange you would like to use, in your "Scripts" folder generate an additional folder with the name of the exchange.
     (Coinbase= "GDAX", Binance = "Binance", Kucoin= "Kucoin", Kraken= "Kraken", etc.)
     
  5. In each folder, create 3 JSON files with the following titles and the following content:
  
----------------------  
  
1. Title: "Config"

    Content:   
    ```
    {"configcheck": ""}
    ```
2. Title: "Initial"

    Content:
    ```
    {"initialcheck": ""}
    ```
    
3. Title: "Performance"
    
    Content:
    ```
    {"initialcheck2": ""}
    ```

----------------------  

__At this point, the scripts will function if called using Python, run "Nescience_rebalance.py" and chose your exchange!__
    
    
__If you would like a complete executable follow the one of the guides below__
    
  The steps to do so are different depending on system specifics and the packaging tool chosen. 
  
  Pyinstaller : https://pyinstaller.readthedocs.io/en/stable/
  
  CxFreeze : https://cx-freeze.readthedocs.io/en/latest/
  
  Py2Exe : https://python101.pythonlibrary.org/chapter40_py2exe.html
  
   __NOTE:__
   
   Using the packaging tool of your choice, target the MAIN script, "Nescience_Rebalance" as the script to be compiled.
  
   If the tool chosen does not recursively search for modules, ensure each script in the "Scripts" folder is included. 

   If the folders you created are not included, ensure that they are located in the same folder as your Nescience_Rebalance python  script or executable. 

   If using Pyinstaller, we have found that strptime.py is commonly not imported, if you run into this issue simply add strptime.py to the data field of the spec file.

[Back To The Top](#table-of-contents)

-----------------------------------

## Nescience Software & Capital, LLC

Nescience Software & Capital is a portfolio management firm focused on advanced cryptocurrency portfolio management tools, facilitating investment with significantly reduced risk and more consistent long-term growth.


- Website - [Nescience Software & Capital, LLC](https://nescience.io)
- Twitch - [NescienceSoftware](https://www.twitch.tv/nesciencesoftware)
- Twitter - [@NescienceSC](https://twitter.com/jamesqquick)
- Facebook - [@NescienceSoftware](https://www.facebook.com/NescienceSoftware)
- Reddit - [Nescience](https://www.reddit.com/r/Nescience)

[Back To The Top](#table-of-contents)
