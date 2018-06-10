#!/usr/bin/env python
#https://github.com/python-telegram-bot/python-telegram-bot#api

# Sergio Tanzilli - sergio@tanzilli.com
 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import time
import os

mytoken="token of your bot"

#/start command handler
def cmd_start(bot, update):
	bot.sendMessage(update.message.chat_id, text="Send your video !\n")
	print "Received: /start"	

def echo(bot, update):
	print "Received a video"	
	#print update.message
	
	user = update.message.from_user
	#print "User:", user
	#print "Video:", update.message.video.file_id
		
	video_file = bot.get_file(update.message.video.file_id)
	video_file.download('video.mp4')

	os.system("sudo ~/rpi-rgb-led-matrix/utils/video-viewer --led-chain=5 --led-parallel=3  --led-pixel-mapper='U-mapper;Rotate:270' video.mp4");

#Open a link to Telegram using the Token Assigned
updater = Updater(mytoken)	
job_queue = updater.job_queue

dispatcher = updater.dispatcher

#Handler definition
dispatcher.add_handler(CommandHandler("start", cmd_start))
dispatcher.add_handler(MessageHandler(Filters.video, echo))

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
	GPIO.cleanup()
	exit()
