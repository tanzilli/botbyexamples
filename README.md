# Bot by examples

<img src="https://telegram.org/file/811140058/2/7GzMJk4Ij54/a1649c56fa9f805828">

Examples of Telegram bot written in Python

## Installing

	sudo apt-get update
	sudo apt-get install python-pip
	sudo apt-get install build-essential libssl-dev libffi-dev python-dev
	sudo apt-get install git
	pip install python-telegram-bot

Clone the whole repository with:
	
	cd
	git clone https://github.com/tanzilli/botbyexamples
	cd botbyexamples

or copy only the source you need.

## Running

Create your own bot with <https://telegram.me/BotFather> using your Telegram
client then use the token you got inside the bot source example:

	mytoken="token of your bot"	

### Bot examples

Example of Bot that send an alarm to all the Telegram client linked 

* [chatid.py](/chatid.py) 

Example of Bot than controls a led state using a Telegram keyboard

* [keyboard.py](/keyboard.py) 

Example of Bot than send a graph

* [graph.py](/graph.py) CHat a __/start__ from your phone to get a random graph

To use this example install these packages:

	sudo apt-get install python-pip
	sudo pip install pygal
	sudo pip install tinycss
	sudo apt-get install python-cairosvg
	sudo apt-get install python-lxml
	sudo apt-get install python-cssselect

Example of Bot that receive a video and shows it on 
a RGB led Panel using the [HAT-A3 adapter](https://www.acmesystems.it/HAT-A3):

* [telegram_video.py](/telegram_video.py) 


## Links

* [python-telegram-bot repository](https://github.com/python-telegram-bot/python-telegram-bot)	
* [python-telegram-bot documentation](https://python-telegram-bot.readthedocs.io/en/stable/index.html)	
	
 
