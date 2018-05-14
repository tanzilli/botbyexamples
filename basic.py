#!/usr/bin/env python
#https://github.com/python-telegram-bot/python-telegram-bot#api

# Sergio Tanzilli - sergio@tanzilli.com
 
import RPi.GPIO as GPIO
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram,time,os,json

mytoken="your token here"

#Alarm line (PIO22 pin 15)

Alarm_in=22

job_queue=None
chat_ids=[]
chat_ids_filename="chat_ids.json"
alarm_counter=0

#Add a chat id
def addChatIds(chat_id):
	global chat_ids

	if chat_id not in chat_ids:
		chat_ids.append(chat_id)

#Delete a chat id
def removeChatIds(chat_id):
	global chat_ids

	chat_ids.remove(chat_id)

#Save on chat_ids.json file the chat id list
def saveChatIds():
	global chat_ids
	global chat_ids_filename

	with open(chat_ids_filename, 'wb') as fp:
		json.dump(chat_ids, fp)
		fp.close()	

#Load from chat_ids.json file the chat id list
def loadChatIds():
	global chat_ids
	global chat_ids_filename

	if not os.path.isfile(chat_ids_filename):
		chat_ids=[]
		return

	with open(chat_ids_filename, 'r') as fp:
		chat_ids=json.load(fp)
		fp.close()	

#/start command handler
def cmd_start(bot, update):
	bot.sendMessage(update.message.chat_id, text="Welcome !\n")
	print "Received: /start"
	
	#Save the chad id received to use to send alarm
	addChatIds(update.message.chat_id)
	saveChatIds()

#/stop command handler
def cmd_stop(bot, update):
	bot.sendMessage(update.message.chat_id, text="Bye, bye\n")
	print "Received: /stop"

	#Delete the chat id from the list to avoid to send alarms
	removeChatIds(update.message.chat_id)
	saveChatIds()

#Normal message handler
def echo(bot, update):
	print "User:   : [" + update.message.from_user.username + "]"
	print "Text    : [" + update.message.text + "]"
	bot.sendMessage(update.message.chat_id, text="Riceived")

	#Save the chad id received to use to send alarm
	addChatIds(update.message.chat_id)
	saveChatIds()

#Open a link to Telegram using the Token Assigned
updater = Updater(mytoken)	
job_queue = updater.job_queue

dispatcher = updater.dispatcher

#Handler definition
dispatcher.add_handler(CommandHandler("start", cmd_start))
dispatcher.add_handler(CommandHandler("stop", cmd_stop))
dispatcher.add_handler(MessageHandler(Filters.text,echo))

# Load the chat id list
loadChatIds()

# Start the updater
update_queue = updater.start_polling()
print "Started. Type ctrl-C to exit"		

#Alarm line setup (0=alarm active)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(P1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Forever loop
try:
	while True:

		#Check the alarm line
		if GPIO.input(P1)==0:
			alarm_counter=alarm_counter+1
			print "Alarm # %d !" % alarm_counter

			#Send the alarm message to all the chat id saved
			if len(chat_ids)>=0:
				for chat_id in chat_ids:
					job_queue.bot.sendMessage(chat_id, text="Allarme # %d!!" % alarm_counter)

			while GPIO.input(P1)==0:
				time.sleep(0.2)
				pass
	
		time.sleep(0.2)

finally:
	print "\nExit in 10 seconds"		
	updater.stop()
	GPIO.cleanup()
	exit()
