#!/usr/bin/env python
#https://github.com/python-telegram-bot/python-telegram-bot#api

# Sergio Tanzilli - sergio@tanzilli.com
 
from telegram.ext import Updater, CommandHandler
import time
import random
import pygal

mytoken="token of your bot"

#/start command handler
def cmd_start(bot, update):
	print "Received: /start"	
	bot.sendMessage(update.message.chat_id, text="Random temp graph...\n")

	# Create a random set of indoor temperatures
	indoor=[]
	print "Indoor"
	for i in range(24):
		indoor.append(round(random.random()*5+18,0))

	# Create a random set of outdoor temperatures
	outdoor=[]
	print "Outdoor"
	for i in range(24):
		outdoor.append(round(random.random()*10+12,0))


	# Create the line chart
	# http://pygal.org/en/stable/documentation/types/line.html	
	print "Prepare graph"
	line_chart = pygal.Line()
	line_chart.title = 'Temperatures'
	line_chart.x_labels = map(str, range(0, 23))
	line_chart.add('Indoor', indoor)
	line_chart.add('Outdoor', outdoor)
	line_chart.render_to_png('/tmp/graph.png')

	print "Send graph"
	bot.sendPhoto(update.message.chat_id,photo=open('/tmp/graph.png'))
	
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
