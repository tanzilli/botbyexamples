#!/usr/bin/env python
#https://github.com/python-telegram-bot/python-telegram-bot#api

# Sergio Tanzilli - sergio@tanzilli.com
 
import RPi.GPIO as GPIO
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import time

mytoken="insert your token here"

#Led line (GPIO 23 pin 11)

led=22

#/start command handler
def cmd_start(bot, update):
	led_keyboard = ReplyKeyboardMarkup([[ '/on', '/off' ]])
	led_keyboard.one_time_keyboard=False
	led_keyboard.resize_keyboard=True

	bot.sendMessage(update.message.chat_id, text="Welcome !\n", reply_markup=led_keyboard)
	print "Received: /start"	

#/on command handler
def cmd_on(bot, update):
	bot.sendMessage(update.message.chat_id, text="Led ON !\n")
	print "Received: /on"	
	GPIO.output(led,True)

#/off command handler
def cmd_off(bot, update):
	bot.sendMessage(update.message.chat_id, text="Led OFF !\n")
	print "Received: /off"	
	GPIO.output(led,False)

#Open a link to Telegram using the Token Assigned
updater = Updater(mytoken)	
job_queue = updater.job_queue

dispatcher = updater.dispatcher

#Handler definition
dispatcher.add_handler(CommandHandler("start", cmd_start))
dispatcher.add_handler(CommandHandler("on", cmd_on))
dispatcher.add_handler(CommandHandler("off", cmd_off))

# Start the updater
update_queue = updater.start_polling()
print "Started. Type ctrl-C to exit"		

#Alarm line setup (0=alarm active)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led, GPIO.OUT)

#Forever loop
try:
	while True:
		time.sleep(1)

finally:
	print "\nExit in 10 seconds"		
	updater.stop()
	GPIO.cleanup()
	exit()
