# simplebot

Very basic Telegram gate remote controller for Raspberry Pi

## Installing

	sudo apt-get update
	sudo apt-get install python-setuptools
	sudo apt-get install git

	git clone https://github.com/python-telegram-bot/python-telegram-bot --recursive
	cd python-telegram-bot
	sudo python setup.py install

Clone the whole repository with:
	
	cd
	git clone https://github.com/tanzilli/simplebot
	cd simplebot

or copy only the source you need.

## Running

Create your bot with Telegram client from <https://telegram.me/BotFather> and replace the
token inside the bot source you are using::


	updater = Updater("insert your token here")	

The bot examples are:

* basic.py very basic example that send an alarm to all the Telegram client 
* simplebot.py simple remote control for your gate

## Links

* [python-telegram-bot repository](https://github.com/python-telegram-bot/python-telegram-bot)	
* [python-telegram-bot documentation](https://python-telegram-bot.readthedocs.io/en/stable/index.html)	
	
 
