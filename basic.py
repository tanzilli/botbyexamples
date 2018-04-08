#!/usr/bin/env python
#https://github.com/python-telegram-bot/python-telegram-bot#api

# Sergio Tanzilli - sergio@tanzilli.com
 
import RPi.GPIO as GPIO
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram,time,os,json

#GPIO usato per generale l'allarme da inviare via Telegram (Pin 15)
P1=22

job_queue=None
chat_ids=[]
chat_ids_filename="chat_ids.json"
alarm_counter=0

#Aggiunge una chat id all'elenco in ram
def addChatIds(chat_id):
	global chat_ids

	if chat_id not in chat_ids:
		chat_ids.append(chat_id)

#Rimuove una chat id all'elenco in ram
def removeChatIds(chat_id):
	global chat_ids

	chat_ids.remove(chat_id)

#Salva l'elenco delle chat_id sul file chat_ids.json
def saveChatIds():
	global chat_ids
	global chat_ids_filename

	with open(chat_ids_filename, 'wb') as fp:
		json.dump(chat_ids, fp)
		fp.close()	

#Carica l'elenco delle chat_id dal file chat:ids.json
def loadChatIds():
	global chat_ids
	global chat_ids_filename

	if not os.path.isfile(chat_ids_filename):
		chat_ids=[]
		return

	with open(chat_ids_filename, 'r') as fp:
		chat_ids=json.load(fp)
		fp.close()	

#Handler del comando /start ricevuto da Telegram
#Il comando /start viene inviato quando da cellulare
#ci si registra ad un bot
def cmd_start(bot, update):
	bot.sendMessage(update.message.chat_id, text="Welcome message\n")
	print "Ricevuto /start"
	
	#Salva la chat id del messaggio in arrivo per poter
	#poi usarla per inviare allarmi
	addChatIds(update.message.chat_id)
	saveChatIds()

#Handler del comando /stop ricevuto da Telegram
#Il comando /stop viene inviato quando da cellulare
#ci si cancella ad un bot
def cmd_stop(bot, update):
	bot.sendMessage(update.message.chat_id, text="Bye, bye\n")
	print "Ricevuto /stop"

	#Cancella la chat id del messaggio in arrivo per poter
	#evitare di inviare messaggi di allarme in futuro
	removeChatIds(update.message.chat_id)
	saveChatIds()

#Handler di gestione dei messaggi liberi in arrivo
def echo(bot, update):
	print "User:   : [" + update.message.from_user.username + "]"
	print "Text    : [" + update.message.text + "]"
	bot.sendMessage(update.message.chat_id, text="Ricevuto")

	#Salva la chat id del messaggio in arrivo per poter
	#poi usarla per inviare allarmi
	addChatIds(update.message.chat_id)
	saveChatIds()

#Si registra a Telegram con il Token del bot
updater = Updater("Inserisci il Token")	
job_queue = updater.job_queue

dispatcher = updater.dispatcher

#Registra gli handler
dispatcher.add_handler(CommandHandler("start", cmd_start))
dispatcher.add_handler(CommandHandler("stop", cmd_stop))
dispatcher.add_handler(MessageHandler(Filters.text,echo))

# Carica l'elenco delle chat telegram aperte
loadChatIds()

# Fa partire il gestore dei messaggi Telegram
update_queue = updater.start_polling()
print "Started. Type ctrl-C to exit"		

#Configura il pin di allarme (Se a 0 manda l'allarme)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(P1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Loop infinito 
try:
	while True:

		#Controlla se e' stato premuto il tasto di allarme 
		if GPIO.input(P1)==0:
			alarm_counter=alarm_counter+1
			print "Allarme %d" % alarm_counter

			#Invia l'allarme a tutti i cellulari che si sono collegati al bot
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
