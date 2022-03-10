import discord
from discord.ext import tasks

from ics import Calendar

import time
import requests
from datetime import datetime, timedelta

from VARIABLES import TOKEN


# Heure d'envoi du message
HOUR,MINUTES = 20,00

# Current_day so that the message is only send once 
current_day = 0


url_grp1_log = "https://planning.univ-ubs.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214370536b50fcc57df324cfcf2e9e6b4356213d7c347ee7c2df43b49ed91b3cccdb0db0d7caf18783a6e383fe55999af1e19541e84f90735ed6e8504f9d2b878bb69711e591f527eea"
url_grp2_log = "https://planning.univ-ubs.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc38732002148cfdfac49402f5b4e0fa50826f0818af4a82a8fde6ce3f14906f45af276f59ae8fac93f781e86152b11da73a3d6d4343f9d4d7095cee5623c2973627c2eb073b6eaee4862e984e828d3f4109b6629391"
url_tp4_cyber = "https://planning.univ-ubs.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214e659a3a5a28a8ccfe0fa50826f0818af4a82a8fde6ce3f14906f45af276f59ae8fac93f781e86152b11da73a3d6d4343f9d4d7095cee5623c2973627c2eb073be3b599defae53fd98d3f4109b6629391"

# Client discord
client = discord.Client()

# Id channel to send message to
main_channel = 0


@client.event
async def on_message(message):
	# Changed the channel of the bot
	if message.content == "!change_channel":
		global main_channel
		main_channel = message.channel.id
		print("CHANGED MAIN CHANNEL :" + str(main_channel))
		await message.channel.send("Channel Changed")

	if "!cours_demain" in message.content:
		# Check the arguments 
		args = parse_args(message.content)

		events = get_tommorow_event(args)

		for e in events:
			m = format_event(e)
			await message.channel.send(m)

	if message.content == "!help":
		await message.channel.send("Commands : \n!change_channel\n!cours_demain (tp1/tp2/cyber)\n!help")


# Client is ready
@client.event
async def on_ready():
	print("Le bot est prêt !")

# Change the current day
def set_day():
	global current_day
	current_day = datetime.now().day

# Format an event from ics to a readable string
def format_event(event):
	heure = str(int(str(event.begin)[11:13]) + 1) + ":" + str(event.begin)[14:16]
	return str(event.name) + " à " + heure


# Get the args of the command of the format : !cmd args1 args2 ....
# Return a list
def parse_args(message):
	return message.split(" ")[1:]
	


# Loop every day
@tasks.loop(seconds=30)
async def called_once_a_day():
	# Check if the hour and minutes is good
	# Check if the day is good
	# Check if the channel is setup
	if datetime.now().hour == HOUR and datetime.now().minute == MINUTES and datetime.now().day != current_day and main_channel != 0:
		set_day()

		# get the channel
		message_channel = client.get_channel(main_channel)
		if message_channel != None:
			# Get all events
			events = get_tommorow_event()

			# Message a envoyer
			message = "Premier cours : " + format_event(events[0])
			print("SEND : " + message)
			await message_channel.send(message)


# Get the events from tommorrow 
def get_tommorow_event(groupe):
	print("Getting cours demain for " + str(groupe))
	url = ""
	if groupe == []:
		url = url_grp1_log
	elif groupe[0] == "cyber":
		url = url_tp4_cyber
	elif groupe[0] == "tp2":
		url = url_grp2_log
	elif groupe[0] == "tp1":
		url = url_grp1_log

	# Get the data from the planning 
	c = Calendar(requests.get(url).text)

	l = []
	for e in list(c.timeline):
		# Tommorow date 
		tommorow = datetime.now() + timedelta(days=1)
		month = str(tommorow.month).zfill(2)
		day = str(tommorow.day).zfill(2)

		# Date of the event e
		date = str(e.begin)

		# Check if the date of the event e is tommorow 
		if date[5:7] == month and date[8:10] == day:
			# add it to the list
			l.append(e)
	return l

# Start the loop
called_once_a_day.start()

# Start the bot
client.run(TOKEN)






