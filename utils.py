# Format an event from ics to a readable string
def format_event(event):
	heure_debut = str(int(str(event.begin)[11:13]) + 1) + ":" + str(event.begin)[14:16]
	heure_fin = str(int(str(event.end)[11:13]) + 1) + ":" + str(event.end)[14:16]
	base_string = str(event.name) + " de " + heure_debut + " à " + heure_fin
	if "Projet système à logiciel prépondérant" in str(event.name):
		return base_string + "(Inutile)"
	return base_string


# Get the args of the command of the format : !cmd args1 args2 ....
# Return a list
def parse_args(message):
	return message.split(" ")[1:]

# Add a lign to the file "data/new_commands.txt" containing the new command
def add_command(message):
	with open("data/new_commands.txt","a") as f:
		f.write(message)
		f.write("\n")
		f.close()

def get_new_commands():
	with open("data/new_commands.txt","r") as f:
		return f.read().split("\n")

if __name__ == '__main__':
	print(get_new_commands())