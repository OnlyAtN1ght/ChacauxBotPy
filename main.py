import discord
from discord.ext import tasks

from ics import Calendar

import time
import requests
from datetime import datetime, timedelta
import random

from VARIABLES import TOKEN
from rankfinder import rankbot_activation,draven


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
main_channel = 951448999313948712


@client.event
async def on_message(message):
	# Check if the sender is not the bot 
	if message.author != client.user:
		author = str(message.author)
		message_content = str(message.content)

		print("Message de " + author + " in "+ str(message.channel) + " : " + message_content)

		# Changed the channel of the bot
		if message.content == "!change_channel":
			global main_channel
			main_channel = message.channel.id
			print("!change_channel :" + str(main_channel))
			await message.channel.send("Channel Changed")

		if "!cours_demain" in message.content:
			# Check the arguments 
			args = parse_args(message.content)

			events = get_tommorow_event(args)

			if events == None:
				print("!cours_demain : Erreur")
				await message.channel.send("Arrete gros t nul")
			else:
				for e in events:
					print("!cours_demain : " + str(args[0]))
					m = format_event(e)
					await message.channel.send(m)

		if "!wink" in message.content:
			print("!wink")
			await message.channel.send("https://tenor.com/view/simonwink-simon-gif-25014069")

		if "!twitch_prime" in message.content:
			print("!twitch_prime")
			await message.channel.send("connaissez-vous Twitch Prime : https://www.twitch.tv/nonames_tv")

		if "!draven" in message.content:
			print("!draven")
			m = draven()
			await message.channel.send(m)

		if "!francis" in message.content:
			print("!francis")
			await message.channel.send("https://media.discordapp.net/attachments/771107470457307166/938711411314532372/francis.gif")

		if "!bretagne" in message.content:
			print("!bretagne")
			await message.channel.send("https://cdn.discordapp.com/emojis/917430160435843173.webp?size=240&quality=lossless")

		if "!salles_libres" in message.content:
			m = get_salles_libres()
			await message.channel.send(m)

		if "!rank" in message.content:
			username = "".join(parse_args(message.content))
			rank = rankbot_activation(username)
			if rank:
				await message.channel.send("Rank de {username} : {rank}".format(username=username,rank=rank))
			else:
				await message.channel.send("Ereur dans la récupération du rank (summoners doesn't exists or he's unranked (noob ))")

		if "!moudoule" in message.content:
			ran = int(random.random()*100)
			if ran > 10:
				await message.channel.send("https://cdn.discordapp.com/attachments/918506634010046504/951470082180149320/unknown.png")
			else:
				await message.channel.send("https://tenor.com/view/animal-eating-enormous-fat-hello-there-gif-20202771")



		if "!boussole" in message.content:
			await message.channel.send("@EmileButter#7083 ")



		if message.content == "!help":
			await message.channel.send("Commands : \n!change_channel\n!cours_demain (tp1/tp2/cyber)\n!wink (meilleur commande) \n!twitch_prime \n!francis  \n!salles_libres  \n!rank  \n!moudoule  \n!help")


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
	if "Projet système à logiciel prépondérant" in str(event.name):
		return str(event.name) + " à " + heure + "(Inutile)"
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
			first_event_tp1 = get_tommorow_event()[0]
			first_event_tp2 = get_tommorow_event(["tp2"])[0]
			first_event_cyber = get_tommorow_event(["cyber"])[0]

			# Message a envoyer TP1
			message = "Premier cours TP1 : " + format_event(first_event_tp1)
			print("SEND : " + message)
			await message_channel.send(message)

			# Message a envoyer TP2
			message = "Premier cours TP2 : " + format_event(first_event_tp2)
			print("SEND : " + message)
			await message_channel.send(message)

			# Message a envoyer Cyber
			message = "Premier cours cyber : " + format_event(first_event_cyber)
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

	if url == "":
		return None

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

def get_salles_libres():
	url = "https://planning.univ-ubs.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc387320021403ea5a409591dbc3327ebf4d37fa3b8893e504f8fb4328d223791f3efcb060cd7408538e9571ec0fcc0329252e070fa6673c4282646e5f54395d07bffeaee1d7324cfcf2e9e6b4356213d7c347ee7c2df43b49ed91b3cccdb0db0d7caf18783a6e383fe55999af1e19541e84f90735ed6e8504f9d2b878bb4a000f664cf02e57"
	c = Calendar(requests.get(url).text)

	sallesOccupées = []
	heures_fin = {}
	heures_libre = {}
	all_salles = ['V-TO-ENSIBS-A106', 'V-TO-ENSIBS-D009', 'V-TO-ENSIBS-D003', 'V-TO-ENSIBS-D113', 'V-TO-ENSIbs - B001 amphi', 'V-TO-ENSIbs-A105-107', 'V-TO-ENSIBS-D010', 'V-TO-ENSIbs-A103', 'V-TO-ENSIBS-D005', 'V-TO-ENSIbs-A102 TBI', 'V-TO-ENSIbs-D001', 'V-TO-ENSIBS-A104', 'V-TO-ENSIBS-D105']
	for e in list(c.timeline):
		date_start = str(e.begin)
		date_end = str(e.end)
		#print(date_start)
		#print(date_start[10:12])

		cours_start_month = date_start[5:7]
		cours_start_day = date_start[8:10]

		today = datetime.now()
		current_month = str(today.month).zfill(2)
		current_day = str(today.day).zfill(2)

		#print(cours_start_month,cours_start_day,current_month,current_day)
		if (cours_start_month == current_month and cours_start_day == current_day):
			#print(e)

			current_hour = today.hour
			current_minutes = today.minute

			cours_debut_hour = int(date_start[11:13])
			cours_debut_minutes = int(date_start[14:16])

			cours_fin_hour = int(date_end[11:13])
			cours_fin_minutes = int(date_end[14:16])

			# L'event est avant l'heure actuelle
			if (cours_debut_hour < current_hour or (cours_debut_hour == current_hour and cours_debut_minutes < current_minutes)):
				# L'event fin est après l'heure actuelle 
				# => Un cours a lieu en ce moment
				if (cours_fin_hour > current_hour or (cours_fin_hour == current_hour and cours_fin_minutes > current_minutes)):
					sallesOccupées.append(str(e.location))
					heures_fin[str(e.location)] = str(cours_fin_hour)+ ":" + str(cours_fin_minutes)
				elif (cours_debut_hour > current_hour or (cours_debut_hour == current_hour and cours_debut_minutes > current_minutes)):
					# Check s'il y a deja une entrée
					# => Que le cours est après l'entrée deja dans le tableau 
					if str(e.location) not in heures_libre:
						heures_libre[str(e.location)] = str(cours_debut_hour)+ ":" + str(cours_debut_minutes)



	# Final string
	# Add the salles occupees and the end of the current course
	message = "Salles Occupées : " + ", ".join([s + " -> " + heures_fin[s] for s in sallesOccupées if s in all_salles])

	libres = [salle for salle in all_salles if salle not in sallesOccupées]

	# Add the salles libres and the start of the next course in the final stirng
	message += "\nSalles Libres : "
	for s in libres:
		message += s + " -> "
		if s in heures_libre:
			message += heures_libre[s]
		else:
			message += "Demain"
		message += ", "

	# Remove the last ",""
	message = message[:-2]

	# Replace all 
	message = message.replace("V-TO-ENSIBS-","").replace("V-TO-ENSIbs - ","").replace("V-TO-ENSIbs-","").replace("amphi","").replace(" TBI","")
	# <3 Arthur
	message += "\n©️ Athur Pêtre"
	return message



def start_bot():
	# Start the loop
	called_once_a_day.start()

	# Start the bot
	client.run(TOKEN)

start_bot()



