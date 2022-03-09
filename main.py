import discord
from discord.ext import tasks

from ics import Calendar

import time
import requests
from datetime import datetime, timedelta


# Token discord
TOKEN = "OTUxMTA3Njg4MDQ0MDQwMjYz.YiiqDw.0SmbEv8fsfN0z5NQRpr9foh-Leg"

# Heure d'envoi du message
HOUR,MINUTES = 20,00

# Current_day so that the message is only send once 
current_day = 0

# Url planning
url = "https://planning.univ-ubs.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214370536b50fcc57df324cfcf2e9e6b4356213d7c347ee7c2df43b49ed91b3cccdb0db0d7caf18783a6e383fe55999af1e19541e84f90735ed6e8504f9d2b878bb69711e591f527eea"

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


# Client is ready
@client.event
async def on_ready():
	print("Le bot est prêt !")

# Change the current day
def set_day():
	global current_day
	current_day = datetime.now().day

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

			# String de l'heure du premier cours
			heure = str(int(str(events[0].begin)[11:13]) + 1) + ":" + str(events[0].begin)[14:16]
			# Message a envoyer
			message = "Premier cours : " + str(events[0].name) + " à " + heure
			print("SEND : " + message)
			await message_channel.send(message)


# Get the events from tommorrow 
def get_tommorow_event():
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






