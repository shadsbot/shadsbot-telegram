from users import *
import re
import json
import requests
import urllib
import time

def mtgtext(cardn, text):
	if text is True:
		isCreature = False
		msg = ""
		try:
			response = requests.get('https://api.deckbrew.com/mtg/cards?name=%s' % (cardn))
			data = response.json()
			msg += "%s \n" % (data[0]['name'])
			for m in data[0]['cost']:
				go = True
				if m == '{' or m == '}':
					go = False
				if go == True:
					msg += m
			msg += "\n"
			for ctype in data[0]['types']:
				msg += "%s " % ctype.title()
				if ctype == 'creature':
					isCreature = True
			if isCreature:
				msg += "-- "
				for stype in data[0]['subtypes']:
					msg += "%s " % stype.title()
			msg += "\n\n"
			msg += data[0]['text']
			msg += "\n"

			if isCreature:
				msg += "\n%s/%s" % (data[0]['power'], data[0]['toughness'])
		except:
			if msg == "":
				msg += "Couldn't find that card. Check your spelling and try again."
		return msg
	response = requests.get('https://api.deckbrew.com/mtg/cards?name=%s' % (cardn))
	data = response.json()
	picurl = data[0]['editions'][1]['image_url']
	return picurl

def checkcmd(command, chat_id, bot, colin,julian,jake):
	print('Command: %s' % command)
	print('From: %s' % chat_id)
	# Handle actual commands here
	if command == '/based':
		bot.sendMessage(chat_id, 'Based Orlando has heard your plea, and it has been denied.')
	if '/math' in command:
		# Parse because this is dangerous!
		doThis = command[5:]
		doThis = re.sub(r'([A-Z]|[a-z])|[!|,|@|#|$|&|\\|;|<|>|"|\'|_|?|:|=]','',doThis)
		doThis = doThis.replace(" ","")
		# print("Debug: " + doThis)
		try:
			bot.sendMessage(chat_id, '%.2f' % eval(doThis))
		except:
			bot.sendMessage(chat_id, "This only accepts mathematical statements.")
	if command == '/trutru':
		pic = open('934.jpg', 'rb')
		bot.sendPhoto(chat_id, pic)
	if command == '/test':
		bot.sendMessage(chat_id, "This bot is recieving commands and is able to respond.")
	if command == '/furriest':
		bot.sendMessage(chat_id, '''Here are the current standings:
Current Mascot: Jake
Most Posted: Julian
Most Adorable: Colin
Biggest Furry: Jake''')
	if command == '/sam':
		bot.sendMessage(chat_id, 'Your mother was a hamster and your father smelled of elder berries.')
	if command == '/holyshit':
		bot.sendMessage(chat_id, 'A talking cat')
	if '/powerlevel' in command:
		message = ''
		if 'jake' in command or 'Jake' in command:
			message += 'Jake\'s powerlevel: %(jake)i' %{"jake": jake.powerlevel()} + '\n'
		if 'julian' in command or 'Julian' in command:
			message += 'Julian\'s powerlevel: %(julian)i' %{"julian": julian.powerlevel()} + '\n'
		if 'colin' in command or 'Colin' in command:
			message += 'Colin\'s powerlevel: %(colin)i' % {"colin": colin.powerlevel()} + '\n'
		bot.sendMessage(chat_id, message)
	if '/addpower' in command:
		if 'jake' in command or 'Jake' in command:
			jake.addpl()
		if 'julian' in command or 'Julian' in command:
			julian.addpl()
		if 'colin' in command or 'Colin' in command:
			colin.addpl()
	if '/mtg ' in command:
		cardn = command[5:]
		msg = mtgtext(cardn, True)
		bot.sendMessage(chat_id,msg)
	if '/mtgp' in command:
		cardn = command[6:]
		picurl = mtgtext(cardn, False)
		pic = urllib.request.urlretrieve(picurl, 'mtg.jpg')
		bot.sendPhoto(chat_id, 'mtg.jpg')
	if '/def' in command:
		word = command[5:]
		msg = word
		msg += "\n\n"
		try:
			response = requests.get('http://dictionaryapi.net/api/definition/%s' % (word))
			data = response.json()
			for defin in data:
				msg += "*"
				msg += defin['PartOfSpeech']
				msg += "* - "
				for mdefin in defin['Definitions']:
					msg += mdefin
					msg += "\n\n"
				#msg += defin['Definitions'][0]
				msg += "\n\n"
		except:
			msg = "Couldn't find that word. Check the spelling and try again."
		bot.sendMessage(chat_id,msg, parse_mode='Markdown')