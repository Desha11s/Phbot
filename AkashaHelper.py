from phBot import *
from threading import Timer
import phBotChat
import threading
import QtBind
import struct
import random
import json
import os
import sqlite3
import urllib.request
import re
import shutil
from datetime import datetime

pName = 'AkashaHelper'
pVersion = '4.7'
pUrl = 'https://raw.githubusercontent.com/Desha11s/Phbot/main/AkashaHelper.py'

# ______________________________ Initializing ______________________________ #

# Globals
loggedIn = False
inGame = None
followActivated = False
followPlayer = ''
followDistance = 0

# Graphic user interface
gui = QtBind.init(__name__,pName)
largetong = 0

QtBind.createLabel(gui, "-------------------------------------------", 535, 225)  
QtBind.createLabel(gui, "| Made by Akasha for Blaze-Online |", 535, 240) 
QtBind.createLabel(gui, "|  contact Discord: ak047                |", 535, 255)  
QtBind.createLabel(gui, "-------------------------------------------", 535, 270)
# Notifications and Logs Section
QtBind.createLabel(gui, "Logs and Notifications", 20, 200)
logBox = QtBind.createList(gui, 20, 220, 500, 90)
QtBind.createLabel(gui,'< All usual known commands are working and these are extra for easier usage >',11,36)
QtBind.createLabel(gui,'- GO : starts bot at current location\n- stop : stops bot and trace\n- trace or t or cmd trace :starts trace\n- nt : Stop trace\n- R : back to town or wake up\n- GO + X Y --> will go to these coords\n- locate : tells you the coords and region\n- rm : makes random movement',10,50)
QtBind.createLabel(gui,'- HWT1 : teleports to HWT beginner\n- HWT2 teleports to HWT Intermidate\n- Q1/Q2/Q3 : known teleports from ZsZc\n- SETR : +radius to set\n- leave : leaves pt\n- R death : reverse to last death point\n- gold : tells you how much gold you have\n- sort : sort your inventory ',260,50)
btnUpdate = QtBind.createButton(gui,'btnUpdate_clicked',"   UPDATE PLUGIN   ",420,30)
lvwPlugins = QtBind.createList(gui,15,8,400,22)
lstPluginsData = []
btnCheck = QtBind.createButton(gui,'btnCheck_clicked',"   CHECK UPDATE   ",420,10)
bakborta = ['fare2 el bkbortatttttttttt','ba ka bo rtaaaaaaa']
shtema = ['enta 5awl ','adek tzmr ','anekk t2ol ahhhh ','adek tf7r ','kosomak ','tezak de wla weshk','5ormk aws3 mn 5orm el ozoon','enta 5awl be ro5sa wla mn 8yer','enta fate7 tezak sabeel','enta shayel rasak we 7atet tezak leh ','omak esmha so3ad','7ot 5yara fe tezak','yabo 5ormen ','7a2a esmk loka loka el sharmota']
tbxLeaders = QtBind.createLineEdit(gui,"",540,20,110,20)
lstLeaders = QtBind.createList(gui,540,42,110,111)
btnAddLeader = QtBind.createButton(gui,'btnAddLeader_clicked',"    Add   ",655,20)
btnRemLeader = QtBind.createButton(gui,'btnRemLeader_clicked',"     Remove     ",655,42)
# Event-related globals
inventory = get_inventory()

def gui_log(messagex):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {messagex}"
    QtBind.append(gui, logBox, formatted_message)

def usescroll():
	inventory = get_inventory()
	for slot, item in enumerate(inventory['items']):
		if item:
			if item['name'] == '20% damage increase scroll':
				it = item['name']
				item['slot'] = slot
				p = struct.pack('<B', slot)	
				data = b"\x23\xED"
				Injectbytes = data+p
				inject_joymax(0x704C, Injectbytes, False)


def spwanpet():
	inventory = get_inventory()
	for slot, item in enumerate(inventory['items']):
		if item:
			if item['name'] == 'Gorgon Summon Scroll':
				it = item['name']
				item['slot'] = slot
				p = struct.pack('<B', slot)	
				data = b"\xED\x11"
				Injectbytes = p+data
				inject_joymax(0x704C, Injectbytes, False)

# Return xControl folder path
def getPath():
	return get_config_dir()+pName+"\\"

# Return character configs path (JSON)
def getConfig():
	return getPath()+inGame['server'] + "_" + inGame['name'] + ".json"

# Check if character is ingame
def isJoined():
	global inGame
	inGame = get_character_data()
	if not (inGame and "name" in inGame and inGame["name"]):
		inGame = None
	return inGame

# Load default configs
def loadDefaultConfig():
	# Clear data
	QtBind.clear(gui,lstLeaders)

# Loads all config previously saved
def loadConfigs():
	loadDefaultConfig()
	if isJoined():
		# Check config exists to load
		if os.path.exists(getConfig()):
			data = {}
			with open(getConfig(),"r") as f:
				data = json.load(f)
			if "Leaders" in data:
				for nickname in data["Leaders"]:
					QtBind.append(gui,lstLeaders,nickname)

# Add leader to the list
def btnAddLeader_clicked():
	if inGame:
		player = QtBind.text(gui,tbxLeaders)
		# Player nickname it's not empty
		if player and not lstLeaders_exist(player):
			# Init dictionary
			data = {}
			# Load config if exist
			if os.path.exists(getConfig()):
				with open(getConfig(), 'r') as f:
					data = json.load(f)
			# Add new leader
			if not "Leaders" in data:
				data['Leaders'] = []
			data['Leaders'].append(player)
			# Replace configs
			with open(getConfig(),"w") as f:
				f.write(json.dumps(data, indent=4, sort_keys=True))
			QtBind.append(gui,lstLeaders,player)
			QtBind.setText(gui, tbxLeaders,"")
			gui_log('AkashaHelper: Leader added ['+player+']')
			phBotChat.ClientNotice('AkashaHelper: Leader added ['+player+']')

# Remove leader selected from list
def btnRemLeader_clicked():
	if inGame:
		selectedItem = QtBind.text(gui,lstLeaders)
		if selectedItem:
			if os.path.exists(getConfig()):
				data = {"Leaders":[]}
				with open(getConfig(), 'r') as f:
					data = json.load(f)
				try:
					# remove leader nickname from file if exists
					data["Leaders"].remove(selectedItem)
					with open(getConfig(),"w") as f:
						f.write(json.dumps(data, indent=4, sort_keys=True))
				except:
					pass # just ignore file if doesn't exist
			QtBind.remove(gui,lstLeaders,selectedItem)
			gui_log('AkashaHelper: Leader removed ['+selectedItem+']')
			phBotChat.ClientNotice('AkashaHelper: Leader removed ['+selectedItem+']')
def encode_gold_amount(gold_amount):
    data = bytearray([0x0D])
    gold_bytes = struct.pack('<Q', gold_amount)   
    data.extend(gold_bytes)
  
    return data
def convert_to_data(value):
    if not isinstance(value, int) or value < 0:
        raise ValueError("Input must be a non-negative integer.")  
    return value.to_bytes(4, byteorder='little')
# Return True if nickname exist at the leader list
def lstLeaders_exist(nickname):
	nickname = nickname.lower()
	players = QtBind.getItems(gui,lstLeaders)
	for i in range(len(players)):
		if players[i].lower() == nickname:
			return True
	return False

# Inject teleport packet, using the source and destination name
def inject_teleport(source,destination):
	t = get_teleport_data(source, destination)
	if t:
		npcs = get_npcs()
		for key, npc in npcs.items():
			if npc['name'] == source or npc['servername'] == source:
				gui_log("AkashaHelper: Selecting teleporter ["+source+"]")
				phBotChat.ClientNotice("AkashaHelper: Selecting teleporter ["+source+"]")
				inject_joymax(0x7045, struct.pack('<I', key), False)
				Timer(2.0, inject_joymax, (0x705A,struct.pack('<IBI', key, 2, t[1]),False)).start()
				Timer(2.0, gui_log, ("Plugin: Teleporting to ["+destination+"]")).start()
				return

def handleChatCommand(msg):
	args = msg.split(' ',1)
	if len(args) != 2 or not args[0] or not args[1]:
		return
	t = args[0].lower()
	if t == 'private' or t == 'note':
		argsExtra = args[1].split(' ',1)
		if len(argsExtra) != 2 or not argsExtra[0] or not argsExtra[1]:
			return
		args.pop(1)
		args += argsExtra
	sent = False
	if t == "all":
		sent = phBotChat.All(args[1])
	elif t == "private":
		sent = phBotChat.Private(args[1],args[2])
	elif t == "party":
		sent = phBotChat.Party(args[1])
	elif t == "guild":
		sent = phBotChat.Guild(args[1])
	elif t == "union":
		sent = phBotChat.Union(args[1])
	elif t == "note":
		sent = phBotChat.Note(args[1],args[2])
	elif t == "stall":
		sent = phBotChat.Stall(args[1])
	elif t == "global":
		sent = phBotChat.Global(args[1])
	if sent:
		gui_log('AkashaHelper: Message "'+t+'" sent successfully!')

def start_follow(player,distance):
	if party_player(player):
		global followActivated,followPlayer,followDistance
		followPlayer = player
		followDistance = distance
		followActivated = True
		return True
	return False

def party_player(player):
	players = get_party()
	if players:
		for p in players:
			if players[p]['name'] == player:
				return True
	return False

# Return point [X,Y] if player is in the party and near, otherwise return None
def near_party_player(player):
	players = get_party()
	if players:
		for p in players:
			if players[p]['name'] == player and players[p]['player_id'] > 0:
				return players[p]
	return None

# Calc the distance from point A to B
def GetDistance(ax,ay,bx,by):
	return ((bx-ax)**2 + (by-ay)**2)**0.5

# Stop follow player
def stop_follow():
	global followActivated,followPlayer,followDistance
	result = followActivated
	# stop
	followActivated = False
	followPlayer = ""
	followDistance = 0
	return result



# Gets the NPC unique ID if the specified name is found near
def GetNPCUniqueID(name):
	NPCs = get_npcs()
	if NPCs:
		name = name.lower()
		for UniqueID, NPC in NPCs.items():
			NPCName = NPC['name'].lower()
			if name == NPCName:
				return UniqueID
	return 0

# Search an item by name or servername through lambda expression and return his information
def GetItemByExpression(_lambda,start=0,end=0):
	inventory = get_inventory()
	items = inventory['items']
	if end == 0:
		end = inventory['size']
	# check items between intervals
	for slot, item in enumerate(items):
		if start <= slot and slot <= end:
			if item:
				# Search by lambda
				if _lambda(item['name'],item['servername']):
					# Save slot location
					item['slot'] = slot
					return item
	return None

# Finds an empty slot, returns -1 if inventory is full
def GetEmptySlot():
	items = get_inventory()['items']
	# check the first empty
	for slot, item in enumerate(items):
		if slot >= 13:
			if not item:
				return slot
	return -1


# Create a connection to database
def GetDatabaseConnection():
	bot_path = os.getcwd()
	# Load the server info
	data = {}
	locale = get_locale()
	# vSRO
	if locale == 22:
		with open(bot_path+"/vSRO.json","r") as f:
			data = json.load(f)
		# Match data with the current server name
		server = character_data['server']
		for k in data:
			servers = data[k]['servers']
			# Check if servers is in list
			if server in servers:
				# Scan data folder
				for path in os.scandir(bot_path+"/Data"):
					# Check databases only
					if path.is_file() and path.name.endswith(".db3"):
						# Connect to check if the data matches
						conn = sqlite3.connect(bot_path+"/Data/"+path.name)
						c = conn.cursor()
						c.execute('SELECT * FROM data WHERE k="path" AND v=?',(data[k]['path'],))
						if c.fetchone():
							# match found
							return conn
						else:
							conn.close()
	# iSRO
	elif locale == 18:
		return sqlite3.connect(bot_path+"/Data/iSRO.db3")
	# TrSRO
	elif locale == 56:
		return sqlite3.connect(bot_path+"/Data/TRSRO.db3")
	return None


def handle_joymax(opcode, data):
	global loggedIn
	if opcode == 0x3026:
		string_length = int.from_bytes(data[:2], "little")
		string_bytes = data[2:2 + string_length]       
		cleaned_bytes = string_bytes.replace(b'\x00', b'')
		readable_text = cleaned_bytes.decode('ascii', errors='ignore')
		if "INJECT" in readable_text:
			return False
		if "note" in readable_text:
			return False
		
				
	
	return True
# ______________________________ Events ______________________________ #

# Called when the bot successfully connects to the game server
def connected():
	global inGame
	inGame = None

# Called when the character enters the game world
def joined_game():
	loadConfigs()
def teleported():
	global loggedIn
	if not loggedIn:
		phBotChat.ClientNotice("You Are Using AkashaHelper, For more ideas contact Discord: Ak047")
		loggedIn = True
def disconnect():
	if loggedIn:
		loggedIn = False
# All chat messages received are sent to this function
def handle_chat(t,player,msg):
	global InEvent
	acc_name = get_character_data()['name']
	if t == 11:
		msg = msg.split(': ',1)[1]
	if player and lstLeaders_exist(player) or t == 100 or player == acc_name or player == "Akasha":
		if msg == "stop":
			stop_bot()
			stop_trace()
			gui_log("AkashaHelper: Bot stopped")
			phBotChat.ClientNotice("AkashaHelper: Bot stopped")
		elif msg == 'start':
			start_bot()
			phBotChat.ClientNotice("AkashaHelper: Bot started")



####################################        TRACE       ###########################################

		elif msg.startswith("trace"):
			msg = msg.rstrip()
			if msg == "trace":
				if start_trace(player):
					gui_log("AkashaHelper: Starting trace to [" + player + "]")
					phBotChat.ClientNotice("AkashaHelper: Starting trace to [" + player + "]")
			else:
				msg = msg[6:].split()[0]
				if start_trace(msg):
					gui_log("AkashaHelper: Starting trace to [" + msg + "]")
					phBotChat.ClientNotice("AkashaHelper: Starting trace to [" + msg + "]")
##################################################################################################

		elif msg.startswith("t"):
			# deletes empty spaces on the right
			msg = msg.rstrip()
			if msg == "t":
				if start_trace(player):
					gui_log("AkashaHelper: Starting trace to [" + player + "]")
					phBotChat.ClientNotice("AkashaHelper: Starting trace to [" + player + "]")
			else:
				msg = msg[2:].split()[0]  # Adjusted to remove "t " instead of "TRACE "
				if start_trace(msg):
					gui_log("AkashaHelper: Starting trace to [" + msg + "]")
					phBotChat.ClientNotice("AkashaHelper: Starting trace to [" + msg + "]")
##################################################################################################

		elif msg.startswith("TRACE"):
			# deletes empty spaces on right
			msg = msg.rstrip()
			if msg == "TRACE":
				if start_trace(player):
					gui_log("AkashaHelper: Starting trace to ["+player+"]")
					phBotChat.ClientNotice("AkashaHelper: Starting trace to ["+player+"]")
			else:
				msg = msg[5:].split()[0]
				if start_trace(msg):
					gui_log("AkashaHelper: Starting trace to ["+msg+"]")
					phBotChat.ClientNotice("AkashaHelper: Starting trace to ["+msg+"]")
##################################################################################################

		elif msg.startswith("cmd trace"):
			# deletes empty spaces on right
			msg = msg.rstrip()
			if msg == "cmd trace":
				if start_trace(player):
					gui_log("AkashaHelper: Starting trace to ["+player+"]")
					phBotChat.ClientNotice("AkashaHelper: Starting trace to ["+player+"]")
			else:
				msg = msg[10:].split()[0]
				if start_trace(msg):
					gui_log("AkashaHelper: Starting trace to ["+msg+"]")
					phBotChat.ClientNotice("AkashaHelper: Starting trace to ["+msg+"]")
##################################################################################################
		elif msg.startswith("T"):
			# deletes empty spaces on the right
			msg = msg.rstrip()
			if msg == "T":
				if start_trace(player):
					gui_log("AkashaHelper: Starting trace to [" + player + "]")
					phBotChat.ClientNotice("AkashaHelper: Starting trace to [" + player + "]")
			else:
				msg = msg[2:].split()[0]  # Adjusted to remove "t " instead of "TRACE "
				if start_trace(msg):
					gui_log("AkashaHelper: Starting trace to [" + msg + "]")
					phBotChat.ClientNotice("AkashaHelper: Starting trace to [" + msg + "]")
##################################################################################################

		elif msg == "M?":
			petss = get_pets()
			# Check if 'mounted' is True or False in the pet dictionary
			for pet_info in petss.values():
				if 'mounted' in pet_info and isinstance(pet_info['mounted'], bool):
					status = "" if pet_info['mounted'] else "No i am not"
					phBotChat.All(f"{status}")
					gui_log(f"Mounted: {status}")
					phBotChat.ClientNotice(f"Mounted: {status}")
		elif msg.startswith("M"):
			# default value
			pet = "transport"
			if msg != "M":
				msg = msg[5:].split()
				if msg:
					pet = msg[0]
			# Try mount pet
			if MountPet(pet):
				gui_log("Plugin: Mounting pet ["+pet+"]")
				phBotChat.ClientNotice("Plugin: Mounting pet ["+pet+"]")
		elif msg.startswith("D"):
			# default value
			pet = "transport"
			if msg != "D":
				msg = msg[8:].split()
				if msg:
					pet = msg[0]
			# Try dismount pet
			if DismountPet(pet):
				gui_log("Plugin: Dismounting pet ["+pet+"]")
				phBotChat.ClientNotice("Plugin: Dismounting pet ["+pet+"]")

		elif msg == "N":
			stop_trace()
			gui_log("Plugin: Trace stopped")
			phBotChat.ClientNotice("AkashaHelper: Trace stopped")
		elif msg == 'DS':
			inject_joymax(0x70CB,b'\00\xCE\x94\x3B\x14', False)

		elif msg == "notrace":
			stop_trace()
			gui_log("AkashaHelper: Trace stopped")
			phBotChat.ClientNotice("AkashaHelper: Trace stopped")
		elif msg == "nt":
			stop_trace()
			gui_log("AkashaHelper: Trace stopped")
			phBotChat.ClientNotice("AkashaHelper: Trace stopped")



		elif msg.startswith("GO"):
			msg = msg.rstrip()
			if msg == "GO":
				p = get_position()
				set_training_position(p['region'], p['x'], p['y'],p['z'])
				gui_log("AkashaHelper: Training area set to current position (X:%.1f,Y:%.1f)"%(p['x'],p['y']))
			else:
				try:
					p = msg[2:].split()
					x = float(p[0])
					y = float(p[1])
					region = int(p[2]) if len(p) >= 3 else 0
					z = float(p[3]) if len(p) >= 4 else 0
					set_training_position(region,x,y,z)
					gui_log("AkashaHelper: Training area set to (X:%.1f,Y:%.1f)"%(x,y))
					phBotChat.ClientNotice("AkashaHelper: Training area set to (X:%.1f,Y:%.1f)"%(x,y))
				except:
					gui_log("AkashaHelper: Wrong training area coordinates!")
					phBotChat.ClientNotice("AkashaHelper: Wrong training area coordinates!")
			start_bot()
					
		elif msg == "JUPITER":
			inject_joymax(0x705A,b'\x13\x00\x00\x00\x02\x38\x01\x00\x00',False)
		
		elif msg == "raa":
			randomMovement()
		elif msg == "ra":
			randomMovement()
			p = get_position()
			set_training_position(p['region'], p['x'], p['y'],p['z'])
			start_bot()

		elif msg == "eq":
			inject_joymax(0xC00C,b'\x11\x00\x72\x65\x67\x6F\x6E\x63\x75\x72\x72\x65\x6E\x74\x65\x76\x65\x6E\x74',False)


		elif msg == "locate":
			x = int(get_position()['x'])
			y = int(get_position()['y'])
			reg = get_position()['region']
			area = get_zone_name(reg)
			phBotChat.Private(player,f"Iam at {area} > X: {x} , Y: {y}")
		elif msg.startswith("HWT2"):
			inject_teleport("Kings Valley","Pharaoh tomb (intermediate)")
		elif msg.startswith("HWT1"):
			inject_teleport("Kings Valley","Pharaoh tomb (beginner)")
		elif msg.startswith("Q1"):
			inject_teleport("Harbor Manager Marwa","Pirate Morgun") or inject_teleport("Ferry Ticket Seller Chau","Boat Ticket Seller Asimo") or inject_teleport ("Outside-Togui","Inside-Togui") or inject_teleport ("Petra Trade Route","Petra Trade Route Entrance") or inject_teleport ("Exit Portal","Petra Trade Route Exit") or inject_teleport ("Inside-Togui","Outside-Togui") or inject_teleport("Pirate Morgun","Harbor Manager Gale") or inject_teleport("Harbor Manager Gale","Pirate Morgun") or inject_teleport("Priate Blackbeard","Harbor Manager Gale") or inject_teleport("Aircraft Ticket Seller Shard","Aircraft Ticket Seller Sangnia") or inject_teleport("Aircraft Ticket Seller Sangnia","Aircraft Ticket Seller Shard") or inject_teleport("Tunnel Manager Salhap","Tunnel Manager Maryokuk") or inject_teleport("Tunnel Manager Maryokuk","Tunnel Manager Salhap") or inject_teleport("Tunnel Manager Topni","Tunnel Manager Asui") or inject_teleport("Tunnel Manager Asui","Tunnel Manager Topni") or inject_teleport("Aircraft Ticket Seller Saena","Aircraft Ticket Seller Ajati") or inject_teleport("Aircraft Ticket Seller Ajati","Airship Ticket Seller Dawari") or inject_teleport("Airship Ticket Seller Dawari","Aircraft Ticket Seller Ajati") or inject_teleport("Aircraft Ticket Seller Sayun","Airship Ticket Seller Dawari") or inject_teleport("Airship Ticket Seller Poy","Aircraft Ticket Seller Ajati") or inject_teleport("Boat Ticket Seller Rahan","Boat Ticket Seller Salmai") or inject_teleport("Boat Ticket Seller Rahan","Ferry Ticket Seller Doji") or inject_teleport("Boat Ticket Seller Salmai","Boat Ticket Seller Rahan") or inject_teleport("Boat Ticket Seller Asimo","Ferry Ticket Seller Chau") or inject_teleport("Boat Ticket Seller Asimo","Boat Ticket Seller Asa")or inject_teleport("Boat Ticket Seller Asa","Boat Ticket Seller Asimo") or inject_teleport("Ferry Ticket Seller Tayun","Ferry Ticket Seller Doji") or inject_teleport("Ferry Ticket Seller Doji","Boat Ticket Seller Rahan") or inject_teleport("Ferry Ticket Seller Doji","Ferry Ticket Seller Tayun") or inject_teleport("Ferry Ticket Seller Hageuk","Ferry Ticket Seller Chau") or inject_teleport("Boat Ticket Seller Rahan","Ferry Ticket Seller Chau") or inject_teleport("Ferry Ticket Seller Chau","Boat Ticket Seller Rahan") or inject_teleport("Ferry Ticket Seller Chau","Ferry Ticket Seller Hageuk") or inject_teleport("forbidden plain","Kings Valley") or inject_teleport("Kings Valley","forbidden plain") or inject_teleport("abundance ground","Storm and cloud Desert") or inject_teleport("Storm and cloud Desert","abundance ground" )

		elif msg.startswith("JG"):
			reg1 = get_position()['region']
			areaz1 = get_zone_name(reg1)
			inject_teleport(f"{areaz1}","Jangan")
		elif msg.startswith("DW"):
			regz2 = get_position()['region']
			areaz2 = get_zone_name(regz2)
			inject_teleport(f"{areaz2}","Donwhang")
		elif msg.startswith("HT"):
			regz3 = get_position()['region']
			areaz3 = get_zone_name(regz3)
			inject_teleport(f"{areaz3}","Hotan")
		elif msg.startswith("SK"):
			regz4 = get_position()['region']
			areaz4 = get_zone_name(regz4)
			inject_teleport(f"{areaz4}","Samarkand")
		
		
		
		elif msg.startswith("SETR"):
			msg = msg.rstrip()
			if msg == "SETR":
				radius = 35
				set_training_radius(radius)
				gui_log("AkashaHelper: Training radius reseted to "+str(radius)+" m.")
				phBotChat.ClientNotice("AkashaHelper: Training radius reseted to "+str(radius)+" m.")
			else:
				try:
					radius = int(float(msg[4:].split()[0]))
					radius = (radius if radius > 0 else radius*-1)
					set_training_radius(radius)
					gui_log("AkashaHelper: Training radius set to "+str(radius)+" m.")
					phBotChat.ClientNotice("AkashaHelper: Training radius set to "+str(radius)+" m.")
				except:
					gui_log("AkashaHelper: Wrong training radius value!")
					phBotChat.ClientNotice("AkashaHelper: Wrong training radius value!")
		if msg.startswith('GOO '):
			msg = msg[4:]
			if msg:
				# try to change to specified area name
				if set_training_area(msg):
					gui_log('AkashaHelper: Training area has been changed to ['+msg+']')
					phBotChat.ClientNotice('AkashaHelper:Training area has been changed to ['+msg+']')
				else:
					gui_log('AkashaHelper:Training area ['+msg+'] not found in the list')
					phBotChat.ClientNotice('AkashaHelper: Training area ['+msg+'] not found in the list')
					stop_bot
					start_bot
		elif msg == "ZERK":
			gui_log("AkashaHelper: Using Berserker mode")
			phBotChat.ClientNotice("AkashaHelper: Using Berserker mode")
			inject_joymax(0x70A7,b'\x01',False)
		elif msg == "R":
			# Quickly check if is dead
			character = get_character_data()
			if character['hp'] == 0:
				# RIP
				gui_log('AkashaHelper: Resurrecting at town...')
				phBotChat.ClientNotice('AkashaHelper: Resurrecting at town...')
				inject_joymax(0x3053,b'\x01',False)
			else:
				gui_log('AkashaHelper: Trying to use return scroll...')
				phBotChat.ClientNotice('AkashaHelper: Trying to use return scroll...')
				Timer(random.uniform(0.5,2),use_return_scroll).start()
		elif msg.startswith("TP"):
			msg = msg[3:]
			if not msg:
				return
			# select split char
			split = ',' if ',' in msg else ' '
			# extract arguments
			source_dest = msg.split(split)
			# needs to be at least two name points to try teleporting
			if len(source_dest) >= 2:
				inject_teleport(source_dest[0].strip(),source_dest[1].strip())
		elif msg.startswith("INJECT "):
			msgPacket = msg[7:].split()
			msgPacketLen = len(msgPacket)
			if msgPacketLen == 0:
				gui_log("AkashaHelper: Incorrect structure to inject packet")
				phBotChat.ClientNotice("AkashaHelper: Incorrect structure to inject packet")
				return
			# Check packet structure
			opcode = int(msgPacket[0],16)
			data = bytearray()
			encrypted = False
			dataIndex = 1
			if msgPacketLen >= 2:
				enc = msgPacket[1].lower()
				if enc == 'true' or enc == 'false':
					encrypted = enc == "true"
					dataIndex +=1
			# Create packet data and inject it
			for i in range(dataIndex, msgPacketLen):
				data.append(int(msgPacket[i],16))
			inject_joymax(opcode,data,encrypted)
			# gui_log the info
			gui_log("AkashaHelper: Injecting packet...\nOpcode: 0x"+'{:02X}'.format(opcode)+" - Encrypted: "+("Yes" if encrypted else "No")+"\nData: "+(' '.join('{:02X}'.format(int(msgPacket[x],16)) for x in range(dataIndex, msgPacketLen)) if len(data) else 'None'))
			phBotChat.ClientNotice("AkashaHelper: Injecting packet...\nOpcode: 0x"+'{:02X}'.format(opcode)+" - Encrypted: "+("Yes" if encrypted else "No")+"\nData: "+(' '.join('{:02X}'.format(int(msgPacket[x],16)) for x in range(dataIndex, msgPacketLen)) if len(data) else 'None'))
		elif msg.startswith("CHAT "):
			handleChatCommand(msg[5:])
		elif msg == "DC":
			gui_log("AkashaHelper: Disconnecting...")
			phBotChat.ClientNotice("AkashaHelper: Disconnecting...")
			disconnect()
		elif msg == 'fare2':
			random_string = random.choice(bakborta)
			phBotChat.All(f'{str(random_string)}')
		elif msg == "OU":
			# Check if has party
			if get_party():
				# Left it
				gui_log("AkashaHelper: Leaving the party..")
				phBotChat.ClientNotice("AkashaHelper: Leaving the party..")
				inject_joymax(0x7061,b'',False)
		elif msg == "ctp":
			inject_joymax(0xC00C,b'\x11\x00\x72\x65\x67\x6F\x6E\x63\x75\x72\x72\x65\x6E\x74\x65\x76\x65\x6E\x74',False)
		elif msg == "cp":
			inject_joymax(0xC011, b'\x1A\x8B\x39\x8B\x1A', False)
		elif msg == "leave":
			# Check if has party
			if get_party():
				# Left it
				gui_log("AkashaHelper: Leaving the party..")
				phBotChat.ClientNotice("AkashaHelper: Leaving the party..")
				inject_joymax(0x7061,b'',False)

		elif msg == "gold":
			gold = get_inventory()['gold']
			mssg = f'Gold: {format(gold, ",d")}'
			phBotChat.Private(player,mssg)

		elif msg == ".":
			inv = get_inventory()['items']
			pets = get_pets()

			for item in inv:
				if item is not None:
					serv_name = item['servername']
					if "A_RARE" in serv_name and "11" in serv_name:
						name = item['name']
						phBotChat.Private(player, f"Inventory: {name}")
						gui_log(f"Inventory: {name}")

			if pets:  # Check if any pets are summoned
				for pet_id, pet_data in pets.items():  # Iterate through each pet
					if 'items' in pet_data and pet_data['items']:  # Ensure pet has items
						for item in pet_data['items']:  # Iterate through pet items
							if item is not None:  # Ensure item exists
								serv_name = item['servername']
								if "A_RARE" in serv_name and "11" in serv_name:
									name = item['name']
									phBotChat.Private(player, f"Pet: {name}")
									gui_log(f"Pet: {name}")
		elif msg == "storage":
			inv = get_guild_storage()['items']
			for item in inv:
				if item is not None:
					serv_name = item['servername']
					if "A_RARE" in serv_name and "11" in serv_name:
						name = item['name']
						phBotChat.Private(player,name)
						log(f"{name}")

		
		elif msg == 'gui_log':
			inv = get_inventory()['items']
			gui_log(f"{inv}")

		elif msg == "spawn":
			spwanpet()
		
		elif msg == "x1":
			inject_joymax(0x7082 ,b'',False)
		elif msg == "x2":
			inject_joymax(0x7083 ,b'',False)
		elif msg.startswith("hat"): 
			parts = msg.split("-")
			item_name = parts[1]
			
			if item_name == "floos":
				amount = parts[2]
				data = encode_gold_amount(int(amount))
				inject_joymax(0x7034, data, False)
				log(f"{data}")
			else:
				inventory = get_inventory()
				for slot, item in enumerate(inventory['items']):
					if item is not None:  # Ensure the item is not empty
						if item_name.lower() in item['name'].lower():
							data = b"\x04"
							p = struct.pack('<B', slot) 
							data = data + p  
							inject_joymax(0x7034, data, False)
							log(f"Item matched: {item['name']} in slot {slot}, Data: {data}")


		elif msg == 'Ex':
			findpt = get_party()
			gui_log(f"{findpt}")
			sender_name = player
			for member_id, member_data in findpt.items():
				if member_data.get('name') == sender_name:
					player_id = member_data.get('player_id') 
					gui_log(f"Player ID for {sender_name}: {player_id}")                  
					data = convert_to_data(player_id)
					inject_joymax(0x7081, data, False)
					gui_log(f"Converted data for {sender_name}'s player_id: {data}")
					break



		elif msg.startswith("g:"):
			message = msg[2:].strip()
			if message:
				phBotChat.Global(message)
		elif msg == "mob":
			monsters = get_monsters()
			gui_log(f'{monsters}')
		elif msg == "sort":
			sort_inventory()
		elif msg.startswith("D"):
			# default value
			pet = "horse"
			if msg != "D":
				msg = msg[1:].split()
				if msg:
					pet = msg[0]
			# Try dismount pet
			if DismountPet(pet):
				gui_log("Plugin: Dismounting pet ["+pet+"]")
				phBotChat.ClientNotice("Plugin: Dismounting pet ["+pet+"]")
		if msg.startswith("RECALL "):
			msg = msg[7:]
			if msg:
				npcUID = GetNPCUniqueID(msg)
				if npcUID > 0:
					gui_log("AkashaHelper: Designating recall to \""+msg.title()+"\"...")
					inject_joymax(0x7059, struct.pack('I',npcUID), False)
		if msg.startswith("R "):
			msg = msg[2:]
			if msg:
				msg = msg.split(' ',1)
				if msg[0] == 'return':
					if reverse_return(0,''):
						gui_log('AkashaHelper: Using reverse to the last return scroll location')
						phBotChat.ClientNotice('AkashaHelper: Using reverse to the last return scroll location')
				elif msg[0] == 'death':
					if reverse_return(1,''):
						gui_log('AkashaHelper: Using reverse to the last death location')
						phBotChat.ClientNotice('AkashaHelper: Using reverse to the last death location')
				elif msg[0] == 'player':
					if len(msg) >= 2:
						if reverse_return(2,msg[1]):
							gui_log('AkashaHelper: Using reverse to player "'+msg[1]+'" location')
							phBotChat.ClientNotice('AkashaHelper: Using reverse to player "'+msg[1]+'" location')
				elif msg[0] == 'zone':
					if len(msg) >= 2:
						if reverse_return(3,msg[1]):
							gui_log('AkashaHelper: Using reverse to zone "'+msg[1]+'" location')
							phBotChat.ClientNotice('AkashaHelper: Using reverse to zone "'+msg[1]+'" location')
		if msg.startswith("USE "):
			msg = msg[4:]
			if msg:
				item = GetItemByExpression(lambda n,s: msg in n or msg == s,13)
				if item:
					UseItem(item)
		if msg.startswith('tef'):
			words = msg.split()
			if len(words) > 0 and words[0] == 'tef':
				last_word = words[-1]
				etmsg = f'ETFO5SSS 3alek ya 3amo {last_word} :D'
				phBotChat.All(etmsg)

		if msg.startswith('eshtm'):
			words = msg.split()
			if len(words) > 0 and words[0] == 'eshtm':
				last_word = words[-1]
				random_string = random.choice(shtema)
				phBotChat.All(f'{str(random_string)} ya {last_word} ')
		if msg.startswith("add "):
			player = msg[4:].strip()
			addLeader(player) 
		if msg.startswith("remove "): 
			player = msg[7:].strip()  
			remLeader(player)  #

		elif msg.strip().startswith("note "):  
			note = msg[5:].strip()  # Trim spaces
			phBotChat.ClientNotice(note)



def addLeader(player):
			if inGame and player and not lstLeaders_exist(player):

				data = {}
				if os.path.exists(getConfig()):
					with open(getConfig(), 'r') as f:
						data = json.load(f)
				# Add new leader
				if "Leaders" not in data:
					data['Leaders'] = []
				data['Leaders'].append(player)
				# Replace configs
				with open(getConfig(), "w") as f:
					f.write(json.dumps(data, indent=4, sort_keys=True))
				QtBind.append(gui, lstLeaders, player)
				QtBind.setText(gui, tbxLeaders, "")
				gui_log('AkashaHelper: Leader added [' + player + ']')
				phBotChat.ClientNotice('AkashaHelper: Leader added [' + player + ']')

def remLeader(player):
			if inGame and player:
				if os.path.exists(getConfig()):
					data = {"Leaders": []}
					with open(getConfig(), 'r') as f:
						data = json.load(f)
					try:
						# Remove leader from file if exists
						data["Leaders"].remove(player)
						with open(getConfig(), "w") as f:
							f.write(json.dumps(data, indent=4, sort_keys=True))
					except ValueError:
						gui_log(f'AkashaHelper: Leader [{player}] not found in list.')
						return
				# Update GUI and notify
				QtBind.remove(gui, lstLeaders, player)
				gui_log(f'AkashaHelper: Leader removed [{player}]')
				phBotChat.ClientNotice(f'AkashaHelper: Leader removed [{player}]')
# Called every 500ms
def event_loop():
	if inGame and followActivated:
		player = near_party_player(followPlayer)
		# check if is near
		if not player:
			return
		# check distance to the player
		if followDistance > 0:
			p = get_position()
			playerDistance = round(GetDistance(p['x'],p['y'],player['x'],player['y']),2)
			# check if has to move
			if followDistance < playerDistance:
				# generate vector unit
				x_unit = (player['x'] - p['x']) / playerDistance
				y_unit = (player['y'] - p['y']) / playerDistance
				# distance to move
				movementDistance = playerDistance-followDistance
				gui_log("Following "+followPlayer+"...")
				phBotChat.ClientNotice("Following "+followPlayer+"...")
				move_to(movementDistance * x_unit + p['x'],movementDistance * y_unit + p['y'],0)
		else:
			# Avoid negative numbers
			gui_log("Following "+followPlayer+"...")
			move_to(player['x'],player['y'],0)



# Get the plugins directory
def GetPluginsFolder():
	return str(os.path.dirname(os.path.realpath(__file__)))

# List and check all plugins from the same plugin folder
def btnCheck_clicked():
	QtBind.clear(gui,lvwPlugins)
	# List all files from Plugins folder
	pyFolder = GetPluginsFolder()
	files = os.listdir(pyFolder)
	# Load plugins data
	global lstPluginsData
	for filename in files:
		# Check only python files
		if filename.endswith(".py"):
			pyFile = pyFolder+"\\"+filename
			with open(pyFile,"r",errors='ignore') as f:
				pyCode = str(f.read())
				# Read file and check his version
				if re.search("\npVersion = [0-9a-zA-Z.'\"]*",pyCode):
					# Extract version
					pyVersion = re.search("\npVersion = ([0-9a-zA-Z.'\"]*)",pyCode).group(0)[13:-1]
					# Extract name if has one
					pyName = filename[:-3]
					if re.search("\npName = ([0-9a-zA-Z'\"]*)",pyCode):
						pyName = re.search("\npName = ([0-9a-zA-Z'\"]*)",pyCode).group(0)[10:-1]
					# Check if has url
					pyUrl = pyCode.find("\npUrl = ")
					# Show basic plugin info
					pyInfo = filename+" ("+pyName+" v"+pyVersion+") - "

					# Getting all required to update the plugin
					pData = {}
					pData['canUpdate'] = False
					# Save all data if has url
					if pyUrl != -1:
						# Extract the rest url, it's up to the plugin if the url is wrong :P
						pyUrl = pyCode[pyUrl+9:].split('\n')[0][:-1]
						pyNewVersion = getVersion(pyUrl)
						# Check if version is found and can be updated
						if pyNewVersion and compareVersion(pyVersion,pyNewVersion):
							# Save data to update
							pData['canUpdate'] = True
							pData['url'] = pyUrl
							pData['filename'] = filename
							pData['pName'] = pyName
							# Notify update
							pyInfo += "Update available (v"+pyNewVersion+")"
						else:
							pyInfo += "Updated"
					else:
						pyInfo += "Cannot be updated: URL not found"
					# Add info to GUi
					QtBind.append(gui,lvwPlugins,pyInfo)
					lstPluginsData.append(pData)

# Return version if can be found from hosted url
def getVersion(url):
	try:
		req = urllib.request.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0"})
		with urllib.request.urlopen(req) as w:
			pyCode = str(w.read().decode("utf-8"))
			if re.search("\npVersion = [0-9.'\"]*",pyCode):
				return re.search("\npVersion = ([0-9a-zA-Z.'\"]*)",pyCode).group(0)[13:-1]
	except:
		pass
	return None

# return True if version A is lower than B
def compareVersion(a, b):
	# only numbers allowed
	a = tuple(map(int, (a.split("."))))
	b = tuple(map(int, (b.split("."))))
	return a < b

# Update plugin selected
def btnUpdate_clicked():
	# Get plugin selected
	indexSelected = QtBind.currentIndex(gui,lvwPlugins)
	if indexSelected >= 0:
		pyData = lstPluginsData[indexSelected]
		# Update plugin if can
		if "canUpdate" in pyData and pyData['canUpdate']:
			# Get url
			pyUrl = pyData['url']
			try:
				req = urllib.request.Request(pyUrl, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0"})
				with urllib.request.urlopen(req) as w:
					pyCode = str(w.read().decode("utf-8"))
					pyVersion = re.search("\npVersion = ([0-9a-zA-Z.'\"]*)",pyCode).group(0)[13:-1]
					# Create backup/copy
					pyFolder = GetPluginsFolder()+'\\'
					shutil.copyfile(pyFolder+pyData['filename'],pyFolder+pyData['pName']+".py.bkp")
					os.remove(pyFolder+pyData['filename'])
					# Create/Override file
					with open(pyFolder+pyData['pName']+".py","w+") as f:
						f.write(pyCode)
					# Update GUI
					QtBind.removeAt(gui,lvwPlugins,indexSelected)
					QtBind.append(gui,lvwPlugins,pyData['pName']+".py ("+pyData['pName']+" v"+pyVersion+") - Updated recently")
					gui_log('AkashaHelper: "'+pyData['pName']+'" plugin has been successfully updated')
			except:
				gui_log("AkashaHelper: Error updating your plugin. Try again later..")












				

# Plugin loaded
log("AkashaHelper: "+pName+" v"+pVersion+" successfully loaded")

if os.path.exists(getPath()):
	# Adding RELOAD plugin support
	loadConfigs()
else:
	# Creating configs folder
	os.makedirs(getPath())
	log('AkashaHelper: '+pName+' folder has been created')

