#!/usr/bin/env python
#https://github.com/python-telegram-bot/python-telegram-bot#api

# Sergio Tanzilli - sergio@tanzilli.com
 
import RPi.GPIO as GPIO
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import logging
import random

import time
import os				

P1=22
P2=27
P3=17
P4=4

job_queue=None
chat_ids=[]

def cmd_start(bot, update):
	global chat_ids

	chat_ids+=[update.message.chat_id]
	bot.sendMessage(update.message.chat_id, text="Hello\n")
	print "Ricevuto /start"

def echo(bot, update):
	print "Mittente: : [" + update.message.from_user.username + "]"
	print "Testo     : [" + update.message.text + "]"

	bot.sendMessage(update.message.chat_id, text="Ricevuto")
	

def p1_handler(channel):
	global job_queue
	global chat_ids

	if len(chat_ids)>=0:
		for chat_id in chat_ids:
			job_queue.bot.sendMessage(chat_id, text="Pressed P1")

	print "Pressed P1"

def p2_handler(channel):
	print "Pressed P2"

def p3_handler(channel):
	print "Pressed P1"

def p4_handler(channel):
	print "Pressed P4"

updater = Updater("589601197:AAEWx0L_9G4l3TqDo8YKLgI3PsBu8Xetsm4")	
job_queue = updater.job_queue

dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", cmd_start))
dispatcher.add_handler(MessageHandler(Filters.text,echo))

update_queue = updater.start_polling()
print "Started. Type ctrl-C to exit"		

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(P1, GPIO.IN, pull_up_down=GPIO.PUD_UP)	
GPIO.setup(P2, GPIO.IN, pull_up_down=GPIO.PUD_UP)	
GPIO.setup(P3, GPIO.IN, pull_up_down=GPIO.PUD_UP)	
GPIO.setup(P4, GPIO.IN, pull_up_down=GPIO.PUD_UP)	

GPIO.add_event_detect(P1, GPIO.FALLING,p1_handler,200)	
GPIO.add_event_detect(P2, GPIO.FALLING,p2_handler,200)	
GPIO.add_event_detect(P3, GPIO.FALLING,p3_handler,200)	
GPIO.add_event_detect(P4, GPIO.FALLING,p4_handler,200)	

try:
	counter=0
	while True:
		time.sleep(1)
		counter=counter+1
		print counter
finally:
	print "\nExit in 10 seconds"		
	updater.stop()
	GPIO.cleanup()
	exit()

		
	