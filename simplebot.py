#!/usr/bin/env python
#https://github.com/python-telegram-bot/python-telegram-bot#api

# Sergio Tanzilli - sergio@tanzilli.com
 
import RPi.GPIO as GPIO
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
import telegram
import logging
import random

import time
import os				

from usercheck import Check

check=Check()

CANCELLO=4
TASTO=17

codice="XXX"
timeout_codice=0

# We use this var to save the last chat id, so we can reply to it
last_chat_id = 0

# Enable logging
logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=logging.INFO)

logger = logging.getLogger(__name__)

def apri():
	GPIO.output(CANCELLO, 1)
	time.sleep(2)
	GPIO.output(CANCELLO, 0)

def tasto_handler(channel):
	print "Premuto tasto locale"
	GPIO.output(CANCELLO, 1)
	while GPIO.input(TASTO)==0:
		pass
	GPIO.output(CANCELLO, 0)
		
def cmd_start(bot, update):
	keyboard = telegram.ReplyKeyboardMarkup([['APRI']])
	keyboard.one_time_keyboard=False
	keyboard.resize_keyboard=False
	bot.sendMessage(update.message.chat_id, text="Hi %s ! I'm acme_simplebot.\n" % update.message.from_user.username, reply_markup=keyboard)

def cmd_help(bot, update):	
	help_text = (
		"/otp Genera una one time password\n"
		"/userlist Lista utenti\n"
		"/userdel Cancella tutti gli utenti\n"
	)
	user_type= check.user(bot,update)
	
	if user_type!="none":
		bot.sendMessage(update.message.chat_id, help_text)
		return

def echo(bot, update):
	global codice
	global timeout_codice

	user_type= check.user(bot,update)
	
	if user_type=="none":
		bot.sendMessage(update.message.chat_id, "Accesso negato. Contatta @SergioTanzilli.")
		return

	if user_type=="user" or user_type=="su":
		print "----> Mittente: : [" + update.message.from_user.username + "]"
		print "      Testo     : [" + update.message.text + "]"
		print codice
		
		if  update.message.text==codice:
			bot.sendMessage(update.message.chat_id, text="Comando di apertura inviato\n")
			codice="XXX"
			apri()
		else:
			codice = "APRI [%03d]" % (random.random()*999)

			keyboard = telegram.ReplyKeyboardMarkup([[codice]])
			keyboard.one_time_keyboard=False
			keyboard.resize_keyboard=False

			bot.sendMessage(update.message.chat_id, text="Premi ancora per confermare...",reply_markup=keyboard)
			timeout_codice=0	
	
def cmd_exit(bot, update):
	exit()
	
def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():	
	global update_queue
	global codice
	global timeout_codice
	global check
	
	#@acme_simplebot
	updater = Updater("593165043:AAEmuB3MaUwAfOG3q3IEnhAaOLv3dgTFWgo")	
	dispatcher = updater.dispatcher

	
	dispatcher.add_handler(CommandHandler("start", cmd_start))
	dispatcher.add_handler(CommandHandler("exit", cmd_exit))
	dispatcher.add_handler(MessageHandler(Filters.text,echo))
	dispatcher.add_handler(CommandHandler("help",cmd_help))
	check.addTanzoCheckCommandHandler(dispatcher)

	#dispatcher.addErrorHandler(error)

	update_queue = updater.start_polling()

	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	
	GPIO.setup(CANCELLO, GPIO.OUT)	
	GPIO.output(CANCELLO, 0)

	GPIO.setup(TASTO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(TASTO, GPIO.FALLING, tasto_handler, 200)	


	while True:
		time.sleep(1)
		
		if codice<>"XXX":
			timeout_codice+=1

			if timeout_codice==10:
				timeout_codice=0
				print "Codice annullato"
				codice="XXX"


if __name__ == '__main__':
	main()