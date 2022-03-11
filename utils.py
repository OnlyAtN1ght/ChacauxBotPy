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