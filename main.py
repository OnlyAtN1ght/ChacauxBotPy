import discord
from discord.ext import tasks
from discord.ext import commands #Module python

import random
from datetime import datetime, timedelta


from VARIABLES import TOKEN
from rankfinder import rankbot_activation,draven
from utils import format_event, parse_args,add_command,get_new_commands
from ics_utils import get_tommorow_event,get_salles_libres


# Heure d'envoi du message
HOUR,MINUTES = 20,00

# Current_day so that the message is only send once 
current_day = 0


url_grp1_log = "https://planning.univ-ubs.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214370536b50fcc57df324cfcf2e9e6b4356213d7c347ee7c2df43b49ed91b3cccdb0db0d7caf18783a6e383fe55999af1e19541e84f90735ed6e8504f9d2b878bb69711e591f527eea"
url_grp2_log = "https://planning.univ-ubs.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc38732002148cfdfac49402f5b4e0fa50826f0818af4a82a8fde6ce3f14906f45af276f59ae8fac93f781e86152b11da73a3d6d4343f9d4d7095cee5623c2973627c2eb073b6eaee4862e984e828d3f4109b6629391"
url_tp4_cyber = "https://planning.univ-ubs.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214e659a3a5a28a8ccfe0fa50826f0818af4a82a8fde6ce3f14906f45af276f59ae8fac93f781e86152b11da73a3d6d4343f9d4d7095cee5623c2973627c2eb073be3b599defae53fd98d3f4109b6629391"

# Client discord
intents = discord.Intents.default()
client = discord.Client(intents=intents)
#client = commands.Bot(command_prefix= "!",help_command=None , description = "ChacauxBot", intents= discord.Intents.all()) #prefix du bot + Commande help 


# Id channel to send message to
main_channel = 951448999313948712


@client.event
async def on_message(message):
	# Check if the sender is not the bot 
	
	if message.author != client.user:
		author = str(message.author)
		print(message.author.id)
		message_content = str(message.content)
		print(message)
		print(message.id)
		print(message.content)

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
				if args:
					s = "!cours_demain : " + str(args[0])
				else:
					s = "!cours_demain : TP1"
				print(s)
				for e in events:
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

		if "!wide" in message.content:
			await message.channel.send("https://tenor.com/view/ensibs-wide-thomas-widethomas-gif-25094179")

		if "!a 2 doigts de ban le bot" in message.content:
			await message.channel.send("NON")

		if "!munster" in message.content:
			await message.channel.send("https://tenor.com/view/munster-fromage-vall%C3%A9e-de-munster-vall%C3%A9e-alsace-gif-23983641")

		if '!random' in message.content:
			print("r")
			url_list = ["https://tenor.com/view/ensibs-wide-thomas-widethomas-gif-25094179","https://cdn.discordapp.com/attachments/918506634010046504/951470082180149320/unknown.png","https://media.discordapp.net/attachments/771107470457307166/938711411314532372/francis.gif","https://tenor.com/view/simonwink-simon-gif-25014069"]
			m = random.choice(url_list)
			print(m)
			await message.channel.send(m)

		#if "!escorte_vannes" in message.content:
			#await message.channel

		if "!add_command" in message.content:
			args = parse_args(message.content)
			new_command = " ".join(args)
			add_command(new_command)
			await message.channel.send("New Command : " + new_command)

		if "!see_new_commands" in message.content:
			all_commands = get_new_commands()
			for command in all_commands:
				await message.channel.send(command)

		if message.content == "!help":
			await message.channel.send("Commands : \n!change_channel\n!cours_demain (tp1/tp2/cyber)\n!wink (meilleur commande) \n!twitch_prime \n!francis  \n!salles_libres  \n!rank  \n!moudoule  \n!add_command \n!see_new_commands\n!help")


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







def start_bot():
	# Start the loop
	called_once_a_day.start()

	# Start the bot
	client.run(TOKEN)

start_bot()



