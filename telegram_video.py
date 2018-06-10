#!/usr/bin/env python
#https://github.com/python-telegram-bot/python-telegram-bot#api

# Sergio Tanzilli - sergio@tanzilli.com
 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import threading
import time
import os

mytoken="insert your token here"

#Play video thread
class PlayerVideo(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.exit_flag=False
		self.video_flag=False
		
	def run(self):
		while self.exit_flag==False:
			if self.video_flag==True:
				# Video orientation (0,90,180,270)
				rotate=270 
				# Launch video-viever.
				os.system("sudo ~/rpi-rgb-led-matrix/utils/video-viewer --led-chain=5 --led-parallel=3 --led-pixel-mapper='U-mapper;Rotate:%d' video.mp4" % rotate);
			else:
				os.system("sudo pkill video-viewer");
			
		os.system("sudo pkill video-viewer");

	def play(self):
		print "Play"
		self.video_flag=True		

	def stop(self):
		print "Stop"
		os.system("sudo pkill video-viewer");
		self.video_flag=False		

	def exit(self):
		print "Exit"
		self.exit_flag=True


#/start command handler
def cmd_start(bot, update):	
	play_keyboard = ReplyKeyboardMarkup([[ '/play', '/stop' ]])
	play_keyboard.one_time_keyboard=False
	play_keyboard.resize_keyboard=True

	bot.sendMessage(update.message.chat_id, text="Send your video !\n", reply_markup=play_keyboard)
	print "Received: /start"	

#/play
def cmd_play(bot, update):	
	PlayerVideoThread.play()
	bot.sendMessage(update.message.chat_id, text="Play on\n")
	print "Received: /play"	

#/stop
def cmd_stop(bot, update):	
	PlayerVideoThread.stop()
	bot.sendMessage(update.message.chat_id, text="Stop\n")
	print "Received: /stop"	

def echo(bot, update):
	print "Received a video"	
	#print update.message
	
	user = update.message.from_user
	#print "User:", user
	#print "Video:", update.message.video.file_id
	
	PlayerVideoThread.stop()
		
	video_file = bot.get_file(update.message.video.file_id)
	video_file.download('video.mp4')

	PlayerVideoThread.play()

#Open a link to Telegram using the Token Assigned
updater = Updater(mytoken)	
job_queue = updater.job_queue

dispatcher = updater.dispatcher

#Handler definition
dispatcher.add_handler(CommandHandler("start", cmd_start))
dispatcher.add_handler(CommandHandler("play", cmd_play))
dispatcher.add_handler(CommandHandler("stop", cmd_stop))
dispatcher.add_handler(MessageHandler(Filters.video, echo))

# Start the updater
update_queue = updater.start_polling()

# Start the video player
PlayerVideoThread=PlayerVideo()
PlayerVideoThread.start()

print "Started. Type ctrl-C to exit"		

#Forever loop
try:
	while True:
		time.sleep(1)

finally:
	print "\nWait 10 seconds please..."		
	PlayerVideoThread.exit()
	PlayerVideoThread.join()
	
	updater.stop()
	exit()
