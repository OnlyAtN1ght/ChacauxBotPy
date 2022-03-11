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