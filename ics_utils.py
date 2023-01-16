from datetime import datetime, timedelta
import requests

from ics import Calendar



url_grp1_log = "https://planning.univ-ubs.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=bee217e04f058c8c788b0060b8b122d336205b94d7d29e90e2f5dfbb8890033330a5f72847b0c2c00c79892a4ff650a7dbca700d54ae6afea732ccd5c1a19334906c5f5c262adb7d79b0a1769c62d692,1"
url_grp2_log = "https://planning.univ-ubs.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc38732002148cfdfac49402f5b4e0fa50826f0818af4a82a8fde6ce3f14906f45af276f59ae8fac93f781e86152b11da73a3d6d4343f9d4d7095cee5623c2973627c2eb073b6eaee4862e984e828d3f4109b6629391"
url_tp4_cyber = "https://planning.univ-ubs.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214e659a3a5a28a8ccfe0fa50826f0818af4a82a8fde6ce3f14906f45af276f59ae8fac93f781e86152b11da73a3d6d4343f9d4d7095cee5623c2973627c2eb073be3b599defae53fd98d3f4109b6629391"


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