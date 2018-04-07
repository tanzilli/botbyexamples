# simplebot

Very basic Telegram gate remote controller for Raspberry Pi

## Installing

	sudo apt-get update
	sudo apt-get install python-setuptools
	sudo apt-get install git

	git clone https://github.com/python-telegram-bot/python-telegram-bot --recursive
	cd python-telegram-bot
	sudo python setup.py install
	
	cd
	git clone https://github.com/tanzilli/simplebot
	cd simplebot

## Running

Create your bot with Telegram client from <https://telegram.me/BotFather> and replace the
token inside __simplebot.py__ at line:

	#@acme_simplebot
	updater = Updater("593165043:AAEmuB3MaUwAfOG3q3IEnhAaOLv3dgTFWgo")	

Save and launch:
	
	python simplebot.py

## Links

* [python-telegram-bot repository](https://github.com/python-telegram-bot/python-telegram-bot)	
* [python-telegram-bot documentation](https://python-telegram-bot.readthedocs.io/en/stable/index.html)	
	
 
