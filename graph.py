#!/usr/bin/env python
#https://github.com/python-telegram-bot/python-telegram-bot#api

# Sergio Tanzilli - sergio@tanzilli.com
 
from telegram.ext import Updater, CommandHandler
import time
import random
import pygal

mytoken="your token here"

#/start command handler
def cmd_start(bot, update):
	print "Received: /start"	
	bot.sendMessage(update.message.chat_id, text="Random graph...\n")

	for i in range(24):
		indoor[i]=random.random()*24

	line_chart = pygal.Line()
	line_chart.title = 'Temperatures'
	line_chart.x_labels = map(str, range(0, 23))
	line_chart.add('Indoor', indoor)
	line_chart.add('Outdoor',[24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1])
	line_chart.render_to_png('graph.png')

	bot.sendPhoto(update.message.chat_id,open('graph.png'))
	

#Open a link to Telegram using the Token Assigned
updater = Updater(mytoken)	
job_queue = updater.job_queue

dispatcher = updater.dispatcher

#Handler definition
dispatcher.add_handler(CommandHandler("start", cmd_start))

# Start the updater
update_queue = updater.start_polling()
print "Started. Type ctrl-C to exit"		

#Forever loop
try:
	while True:
		time.sleep(1)

finally:
	print "\nExit in 10 seconds"		
	updater.stop()
	exit()
