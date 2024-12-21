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
pName = 'AkashaHelper'
pVersion = '4.1'
pUrl = 'https://raw.githubusercontent.com/Desha11s/Phbot/main/AkashaHelper.py'

# ______________________________ Initializing ______________________________ #

# Globals
inGame = None
followActivated = False
followPlayer = ''
followDistance = 0

# Graphic user interface
gui = QtBind.init(__name__,pName)
largetong = 0
QtBind.createLabel(gui,'Created by Akasha for Cerberus Online',525,10)
QtBind.createLabel(gui,'If you have more ideas to be added\n      Contact via discord :Ak047',545,260)
QtBind.createLabel(gui,'< All usual known commands are working and these are extra for easier usage >',11,55)
QtBind.createLabel(gui,'- GO : starts bot at current location\n- stop : stops bot and trace\n- trace or t or cmd trace :starts trace\n- nt : Stop trace\n- R : back to town or wake up\n- GO + X Y --> will go to these coords\n- locate : tells you the coords and region\n- rm : makes random movement\n- HWT1 : teleports to HWT beginner\n- HWT2 teleports to HWT Intermidate\n- Q1/Q2/Q3 : known teleports from ZsZc\n- SETR : +radius to set\n- leave : leaves pt\n- R death : reverse to last death point\n- gold : tells you how much gold you have\n- sort : sort your inventory ',10,70)
QtBind.createLabel(gui,'< These are some helpfull shortcuts > \n- DW : tp from bagdad to dw \n- BAG : tp from dw to baghdad\n- ALEX : tp from baghdad to alex(S)\n- regTOWER : register Tower Defend \n- regLMS :    register  Last Man Standing\n- regCLASH :      register  Styria Clash\n- regSOLO :   register  Survival Solo\n- regTLMS:  register  Team Madness\n- regMAD :    register  Madness\n- regTMAD :   register  Madness Team\n- cards : tells you what fgw card you have and shields egy\n- prog : checks custom quest progress\n- check : tells you how many immo+astral you have\n- coins : Tells you how many coins you have\n- quest? : tells you if you have a custom quest or no',260,70)
btnUpdate = QtBind.createButton(gui,'get_npc_id',"  Update Plugin ",400,8)
lvwPlugins = QtBind.createList(gui,11,33,400,20)
lstPluginsData = []
btnCheck = QtBind.createButton(gui,'btnCheck_clicked',"  Check Update  ",300,8)
dwchk = QtBind.createCheckBox(gui, 'CBXDoNothing', 'Donwhang', 10, 10 )
conchk = QtBind.createCheckBox(gui, 'CBXDoNothing', 'Constantinpole', 100, 10 )
btnwep = QtBind.createButton(gui, 'ReverseToCharacter', 'Lucky Hit (Devil S)', 200, 8)
bakborta = ['fare2 el bkbortatttttttttt','ba ka bo rtaaaaaaa']
shtema = ['enta 5awl ','adek tzmr ','anekk t2ol ahhhh ','adek tf7r ','kosomak ','tezak de wla weshk','5ormk aws3 mn 5orm el ozoon','enta 5awl be ro5sa wla mn 8yer','enta fate7 tezak sabeel','enta shayel rasak we 7atet tezak leh ','omak esmha so3ad','7ot 5yara fe tezak','yabo 5ormen ','7a2a esmk loka loka el sharmota']
tbxLeaders = QtBind.createLineEdit(gui,"",525,30,110,20)
lstLeaders = QtBind.createList(gui,525,52,110,111)
btnAddLeader = QtBind.createButton(gui,'btnAddLeader_clicked',"    Add   ",635,30)
btnRemLeader = QtBind.createButton(gui,'btnRemLeader_clicked',"     Remove     ",635,52)
item_name = 'Large tong'
inventory = get_inventory()
current_slot = 0
buy_counter = 0
path = []
path_dict = {}
current_step_index = 0
walk_flag = False

def get_npc_id():
	log("  ss  ")
	npcs = get_npcs()
	log(f"{npcs}")

def usescroll():
	inventory = get_inventory()
	for slot, item in enumerate(inventory['items']):
		if item:
			if item['name'] == '10% damage increase scroll':
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
			if item['name'] == 'War Elephant':
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
			log('AkashaHelper: Leader added ['+player+']')
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
			log('AkashaHelper: Leader removed ['+selectedItem+']')
			phBotChat.ClientNotice('AkashaHelper: Leader removed ['+selectedItem+']')

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
				log("AkashaHelper: Selecting teleporter ["+source+"]")
				phBotChat.ClientNotice("AkashaHelper: Selecting teleporter ["+source+"]")
				# Teleport found, select it
				inject_joymax(0x7045, struct.pack('<I', key), False)
				# Start a timer to teleport in 2.0 seconds
				Timer(2.0, inject_joymax, (0x705A,struct.pack('<IBI', key, 2, t[1]),False)).start()
				Timer(2.0, log, ("Plugin: Teleporting to ["+destination+"]")).start()
				return
		#log('AkashaHelper: NPC not found. Wrong NPC name or servername')		
	#else:
		#log('AkashaHelper: Teleport data not found. Wrong teleport name or servername')

# Send message, Ex. "All Hello World!" or "private JellyBitz Hi!"
def handleChatCommand(msg):
	# Try to split message
	args = msg.split(' ',1)
	# Check if the format is correct and is not empty
	if len(args) != 2 or not args[0] or not args[1]:
		return
	# Split correctly the message
	t = args[0].lower()
	if t == 'private' or t == 'note':
		# then check message is not empty
		argsExtra = args[1].split(' ',1)
		if len(argsExtra) != 2 or not argsExtra[0] or not argsExtra[1]:
			return
		args.pop(1)
		args += argsExtra
	# Check message type
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
		log('AkashaHelper: Message "'+t+'" sent successfully!')

# Move to a random position from the actual position using a maximum radius
def randomMovement(radiusMax=10):
	# Generating a random new point
	pX = random.uniform(-radiusMax,radiusMax)
	pY = random.uniform(-radiusMax,radiusMax)
	# Mixing with the actual position
	p = get_position()
	pX = pX + p["x"]
	pY = pY + p["y"]
	# Moving to new position
	move_to(pX,pY,p["z"])
	log("AkashaHelper: Random movement to (X:%.1f,Y:%.1f)"%(pX,pY))

# Follow a player using distance. Return success
def start_follow(player,distance):
	if party_player(player):
		global followActivated,followPlayer,followDistance
		followPlayer = player
		followDistance = distance
		followActivated = True
		return True
	return False

# Return True if the player is in the party
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

# Try to summon a vehicle
def MountHorse():
	# search item with similar name or exact server name
	item = GetItemByExpression(lambda n,s: s.startswith('ITEM_COS_C_'),13)
	if item:
		UseItem(item)
		return True
	log('AkashaHelper: Horse not found at your inventory')
	return False

# Try to mount pet by type, return success
def MountPet(petType):
	# just in case
	if petType == 'pick':
		return False
	elif petType == 'horse':
		return MountHorse()
	# get all summoned pets
	pets = get_pets()
	if pets:
		for uid,pet in pets.items():
			if pet['type'] == petType:
				p = b'\x01' # mount flag
				p += struct.pack('I',uid)
				inject_joymax(0x70CB,p, False)
				return True
	return False

# Try to dismount pet by type, return success
def DismountPet(petType):
	petType = petType.lower()
	# just in case
	if petType == 'pick':
		return False
	# get all summoned pets
	pets = get_pets()
	if pets:
		for uid,pet in pets.items():
			if pet['type'] == petType:
				p = b'\x00'
				p += struct.pack('I',uid)
				inject_joymax(0x70CB,p, False)
				return True
	return False

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

# Injects item movement on inventory
def Inject_InventoryMovement(movementType,slotInitial,slotFinal,logItemName,quantity=0):
	p = struct.pack('<B',movementType)
	p += struct.pack('<B',slotInitial)
	p += struct.pack('<B',slotFinal)
	p += struct.pack('<H',quantity)
	log('AkashaHelper: Moving item "'+logItemName+'"...')
	# CLIENT_INVENTORY_ITEM_MOVEMENT
	inject_joymax(0x7034,p,False)

# Try to equip item
def EquipItem(item):
	itemData = get_item(item['model'])
	# Check equipables only
	if itemData['tid1'] != 1:
		log('AkashaHelper: '+item['name']+' cannot be equiped!')
		return
	# Check equipable type
	t = itemData['tid2']
	# garment, protector, armor, robe, light, heavy
	if t == 1 or t == 2 or t == 3 or t == 9 or t == 10 or t == 11:
		t = itemData['tid3']
		# head
		if t == 1:
			Inject_InventoryMovement(0,item['slot'],0,item['name'])
		# shoulders
		elif t == 2:
			Inject_InventoryMovement(0,item['slot'],2,item['name'])
		# chest
		elif t == 3:
			Inject_InventoryMovement(0,item['slot'],1,item['name'])
		# pants
		elif t == 4:
			Inject_InventoryMovement(0,item['slot'],4,item['name'])
		# gloves
		elif t == 5:
			Inject_InventoryMovement(0,item['slot'],3,item['name'])
		# boots
		elif t == 6:
			Inject_InventoryMovement(0,item['slot'],5,item['name'])
	# shields
	elif t == 4:
		Inject_InventoryMovement(0,item['slot'],7,item['name'])
	# accesories ch/eu
	elif t == 5 or t == 12:
		t = itemData['tid3']
		# earring
		if t == 1:
			Inject_InventoryMovement(0,item['slot'],9,item['name'])
		# necklace
		elif t == 2:
			Inject_InventoryMovement(0,item['slot'],10,item['name'])
		# ring
		elif t == 3:
			# Check if second ring slot is empty
			if not GetItemByExpression(lambda s,n: True,11):
				Inject_InventoryMovement(0,item['slot'],12,item['name'])
			else:
				Inject_InventoryMovement(0,item['slot'],11,item['name'])
	# weapon ch/eu
	elif t == 6:
		Inject_InventoryMovement(0,item['slot'],6,item['name'])
	# job
	elif t == 7:
		Inject_InventoryMovement(0,item['slot'],8,item['name'])
	# avatar
	elif t == 13:
		t = itemData['tid3']
		# hat
		if t == 1:
			Inject_InventoryMovement(36,item['slot'],0,item['name'])
		# dress
		elif t == 2:
			Inject_InventoryMovement(36,item['slot'],1,item['name'])
		# accesory
		elif t == 3:
			Inject_InventoryMovement(36,item['slot'],2,item['name'])
		# flag
		elif t == 4:
			Inject_InventoryMovement(36,item['slot'],3,item['name'])
	# devil spirit
	elif t == 14:
		Inject_InventoryMovement(36,item['slot'],4,item['name'])

# Try to unequip item
def UnequipItem(item):
	# find an empty slot
	slot = GetEmptySlot()
	if slot != -1:
		Inject_InventoryMovement(0,item['slot'],slot,item['name'])

# Try to use the item specified
def UseItem(item):
	# Create packet and inject it
	p = struct.pack('<B',item['slot'])
	loc = get_locale()

	tid = GetTIDFromItem(item['model'])
	if loc == 22: # vsro
		p += struct.pack('<H',tid)
	else:
		p += struct.pack('<I',tid)

	log('AkashaHelper0 Using item "'+item['name']+'"...')
	# CLIENT_INVENTORY_ITEM_USE
	inject_joymax(0x704C,p,True)

# Get Type ID from item
def GetTIDFromItem(itemId):
	conn = GetDatabaseConnection()
	c = conn.cursor()
	c.execute('SELECT cash_item, tid1, tid2, tid3 FROM items WHERE id=?',(itemId,))
	result = c.fetchone()
	# calculate TID
	result = result[0] + (3 * 4) + (result[1] * 32) + (result[2] * 128) + (result[3] * 2048)
	conn.close()
	return result

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

# ______________________________ Events ______________________________ #

# Called when the bot successfully connects to the game server
def connected():
	global inGame
	inGame = None

# Called when the character enters the game world
def joined_game():
	loadConfigs()
	

# All chat messages received are sent to this function
def handle_chat(t,player,msg):
	
	acc_name = get_character_data()['name']
	# Remove guild name from union chat messages
	if t == 11:
		msg = msg.split(': ',1)[1]
	# Check player at leader list or a Discord message
	if player and lstLeaders_exist(player) or t == 100 or player == acc_name or player == "Akasha":

		# Parsing message command
		if msg == "regSOLO":
			inject_joymax(0xC006,b'\x00\x0F\x00\x53\x75\x72\x76\x69\x76\x61\x6C\x20\x28\x53\x6F\x6C\x6F\x29',False)
			phBotChat.ClientNotice('AkashaHelper: Done you are registed to Survival Solo. ENJOY <3')
		elif msg == "regTOWER":
			inject_joymax(0xC006,b'\x00\x10\x00\x44\x65\x66\x65\x6E\x64\x20\x54\x68\x65\x20\x54\x6F\x77\x65\x72',False)
			phBotChat.ClientNotice('AkashaHelper: Done you are registed to Defend Tower. ENJOY <3')
		elif msg == "regANGEL":
			inject_joymax(0xC006,b'\x00\x10\x00\x41\x6E\x67\x65\x6C\x73\x20\x56\x73\x20\x44\x65\x76\x69\x6C\x73',False)
			phBotChat.ClientNotice('AkashaHelper: Done you are registed to Angel vs Devil. ENJOY <3')
		elif msg == "regCLASH":
			inject_joymax(0xC006,b'\x00\x0C\x00\x53\x74\x79\x72\x69\x61\x20\x43\x6C\x61\x73\x68',False)
			phBotChat.ClientNotice('AkashaHelper: Done you are registed to Styria Clash. ENJOY <3')
		elif msg == "regLMS":
			inject_joymax(0xC006,b'\x00\x11\x00\x4C\x61\x73\x74\x20\x4D\x61\x6E\x20\x53\x74\x61\x6E\x64\x69\x6E\x67',False)
			phBotChat.ClientNotice('AkashaHelper: Done you are registed to Last Man Standing. ENJOY <3')
		elif msg == "regTLMS":
			inject_joymax(0xC006,b'\x00\x12\x00\x4C\x61\x73\x74\x20\x54\x65\x61\x6D\x20\x53\x74\x61\x6E\x64\x69\x6E\x67',False)
			phBotChat.ClientNotice('AkashaHelper: Done you are registed to Team Last Man Standing. ENJOY <3')
		elif msg == "regMAD":
			inject_joymax(0xC006,b'\x00\x07\x00\x4D\x61\x64\x6E\x65\x73\x73',False)
			phBotChat.ClientNotice('AkashaHelper: Done you are registed to Madness. ENJOY <3')
		elif msg == "regTMAD":
			inject_joymax(0xC006,b'\x00\x17\x00\x4D\x61\x64\x6E\x65\x73\x73\x20\x28\x54\x65\x61\x6D\x20\x2D\x20\x52\x61\x6E\x64\x6F\x6D\x29',False)
			phBotChat.ClientNotice('AkashaHelper: Done you are registed to Team Madness. ENJOY <3')
		elif msg == "stop":
			stop_bot()
			stop_trace()
			log("AkashaHelper: Bot stopped")
			phBotChat.ClientNotice("AkashaHelper: Bot stopped")
		elif msg == 'start':
			start_bot()
			phBotChat.ClientNotice("AkashaHelper: Bot started")



####################################        TRACE       ###########################################

		elif msg.startswith("trace"):
			# deletes empty spaces on the right
			msg = msg.rstrip()
			if msg == "trace":
				if start_trace(player):
					log("AkashaHelper: Starting trace to [" + player + "]")
					phBotChat.ClientNotice("AkashaHelper: Starting trace to [" + player + "]")
			else:
				msg = msg[6:].split()[0]  # Adjusted to remove "t " instead of "TRACE "
				if start_trace(msg):
					log("AkashaHelper: Starting trace to [" + msg + "]")
					phBotChat.ClientNotice("AkashaHelper: Starting trace to [" + msg + "]")
##################################################################################################

		elif msg.startswith("t"):
			# deletes empty spaces on the right
			msg = msg.rstrip()
			if msg == "t":
				if start_trace(player):
					log("AkashaHelper: Starting trace to [" + player + "]")
					phBotChat.ClientNotice("AkashaHelper: Starting trace to [" + player + "]")
			else:
				msg = msg[2:].split()[0]  # Adjusted to remove "t " instead of "TRACE "
				if start_trace(msg):
					log("AkashaHelper: Starting trace to [" + msg + "]")
					phBotChat.ClientNotice("AkashaHelper: Starting trace to [" + msg + "]")
##################################################################################################

		elif msg.startswith("TRACE"):
			# deletes empty spaces on right
			msg = msg.rstrip()
			if msg == "TRACE":
				if start_trace(player):
					log("AkashaHelper: Starting trace to ["+player+"]")
					phBotChat.ClientNotice("AkashaHelper: Starting trace to ["+player+"]")
			else:
				msg = msg[5:].split()[0]
				if start_trace(msg):
					log("AkashaHelper: Starting trace to ["+msg+"]")
					phBotChat.ClientNotice("AkashaHelper: Starting trace to ["+msg+"]")
##################################################################################################

		elif msg.startswith("cmd trace"):
			# deletes empty spaces on right
			msg = msg.rstrip()
			if msg == "cmd trace":
				if start_trace(player):
					log("AkashaHelper: Starting trace to ["+player+"]")
					phBotChat.ClientNotice("AkashaHelper: Starting trace to ["+player+"]")
			else:
				msg = msg[10:].split()[0]
				if start_trace(msg):
					log("AkashaHelper: Starting trace to ["+msg+"]")
					phBotChat.ClientNotice("AkashaHelper: Starting trace to ["+msg+"]")
##################################################################################################
		elif msg.startswith("T"):
			# deletes empty spaces on the right
			msg = msg.rstrip()
			if msg == "T":
				if start_trace(player):
					log("AkashaHelper: Starting trace to [" + player + "]")
					phBotChat.ClientNotice("AkashaHelper: Starting trace to [" + player + "]")
			else:
				msg = msg[2:].split()[0]  # Adjusted to remove "t " instead of "TRACE "
				if start_trace(msg):
					log("AkashaHelper: Starting trace to [" + msg + "]")
					phBotChat.ClientNotice("AkashaHelper: Starting trace to [" + msg + "]")
##################################################################################################

		elif msg == "M?":
			petss = get_pets()
			# Check if 'mounted' is True or False in the pet dictionary
			for pet_info in petss.values():
				if 'mounted' in pet_info and isinstance(pet_info['mounted'], bool):
					status = "" if pet_info['mounted'] else "No i am not"
					phBotChat.All(f"{status}")
					log(f"Mounted: {status}")
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
				log("Plugin: Mounting pet ["+pet+"]")
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
				log("Plugin: Dismounting pet ["+pet+"]")
				phBotChat.ClientNotice("Plugin: Dismounting pet ["+pet+"]")

		elif msg == "N":
			stop_trace()
			log("Plugin: Trace stopped")
			phBotChat.ClientNotice("AkashaHelper: Trace stopped")
		elif msg == 'DS':
			inject_joymax(0x70CB,b'\00\xCE\x94\x3B\x14', False)
		elif msg == "prog": #CHECK PROGRESS QUEST NAME
			quests = get_quests()    
			for quest_id, quest_data in quests.items():
				quest_name = quest_data['name']
				if quest_name == "Hunt 10,000 Sylakenth":
					quest_prog = quest_data['objectives'][0]['progress']
					phBotChat.Private(player,f"prog {quest_prog}/10,000")
		elif msg == "notrace":
			stop_trace()
			log("AkashaHelper: Trace stopped")
			phBotChat.ClientNotice("AkashaHelper: Trace stopped")
		elif msg == "nt":
			stop_trace()
			log("AkashaHelper: Trace stopped")
			phBotChat.ClientNotice("AkashaHelper: Trace stopped")
		elif msg == 'BAG':
			inject_joymax(0x705A,b'\x02\x00\x00\x00\x02\x15\x01\x00\x00',False)

		elif msg == 'rdw':
			inject_joymax(0x7059,b'\x02\x00\x00\x00',False)
		elif msg.startswith("GO"):
			# deletes empty spaces on right
			msg = msg.rstrip()
			if msg == "GO":
				p = get_position()
				set_training_position(p['region'], p['x'], p['y'],p['z'])
				log("AkashaHelper: Training area set to current position (X:%.1f,Y:%.1f)"%(p['x'],p['y']))
			else:
				try:
					# check arguments
					p = msg[2:].split()
					x = float(p[0])
					y = float(p[1])
					# auto calculated if is not specified
					region = int(p[2]) if len(p) >= 3 else 0
					z = float(p[3]) if len(p) >= 4 else 0
					set_training_position(region,x,y,z)
					log("AkashaHelper: Training area set to (X:%.1f,Y:%.1f)"%(x,y))
					phBotChat.ClientNotice("AkashaHelper: Training area set to (X:%.1f,Y:%.1f)"%(x,y))
				except:
					log("AkashaHelper: Wrong training area coordinates!")
					phBotChat.ClientNotice("AkashaHelper: Wrong training area coordinates!")
			start_bot()
					

		elif msg == "raa":
			randomMovement()
		elif msg == "ra":
			randomMovement()
			p = get_position()
			set_training_position(p['region'], p['x'], p['y'],p['z'])
			start_bot()

		elif msg == "eq":
			inject_joymax(0xC00C ,b'\x02\x00\x61\x71',False)

		elif msg == "job":
			inject_joymax(0x704C,b'\x0F\xEC\x19\x07\x30\x00\x00\x00',False)
		elif msg == "jobin":
			inject_joymax(0x705A,b'\03\x00\x00\x00\x02\xAD\x00\x00\x00',False)
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
		elif msg.startswith("Q2"):
			inject_teleport("Harbor Manager Marwa","Priate Blackbeard") or inject_teleport("Harbor Manager Gale","Priate Blackbeard") or inject_teleport("Pirate Morgun","Harbor Manager Marwa") or inject_teleport("Priate Blackbeard","Harbor Manager Marwa") or inject_teleport("Aircraft Ticket Seller Saena","Airship Ticket Seller Dawari") or inject_teleport("Airship Ticket Seller Dawari","Aircraft Ticket Seller Sayun") or inject_teleport("Aircraft Ticket Seller Sayun","Airship Ticket Seller Poy") or inject_teleport("Airship Ticket Seller Poy","Aircraft Ticket Seller Sayun") or inject_teleport("Aircraft Ticket Seller Ajati","Airship Ticket Seller Poy")
		elif msg.startswith("Q3"):
			inject_teleport("Harbor Manager Marwa","Harbor Manager Gale") or inject_teleport("Harbor Manager Gale","Harbor Manager Marwa") or inject_teleport("Aircraft Ticket Seller Ajati","Aircraft Ticket Seller Saena") or inject_teleport("Airship Ticket Seller Dawari","Aircraft Ticket Seller Saena")
		elif msg.startswith("SETR"):
			# deletes empty spaces on right
			msg = msg.rstrip()
			if msg == "SETR":
				# set default radius
				radius = 35
				set_training_radius(radius)
				log("AkashaHelper: Training radius reseted to "+str(radius)+" m.")
				phBotChat.ClientNotice("AkashaHelper: Training radius reseted to "+str(radius)+" m.")
			else:
				try:
					# split and parse movement radius
					radius = int(float(msg[4:].split()[0]))
					# to absolute
					radius = (radius if radius > 0 else radius*-1)
					set_training_radius(radius)
					log("AkashaHelper: Training radius set to "+str(radius)+" m.")
					phBotChat.ClientNotice("AkashaHelper: Training radius set to "+str(radius)+" m.")
				except:
					log("AkashaHelper: Wrong training radius value!")
					phBotChat.ClientNotice("AkashaHelper: Wrong training radius value!")
		if msg.startswith('GOO '):
			# deletes empty spaces on right
			msg = msg[4:]
			if msg:
				# try to change to specified area name
				if set_training_area(msg):
					log('AkashaHelper: Training area has been changed to ['+msg+']')
					phBotChat.ClientNotice('AkashaHelper:Training area has been changed to ['+msg+']')
				else:
					log('AkashaHelper:Training area ['+msg+'] not found in the list')
					phBotChat.ClientNotice('AkashaHelper: Training area ['+msg+'] not found in the list')
					stop_bot
					start_bot
		elif msg == "ZERK":
			log("AkashaHelper: Using Berserker mode")
			phBotChat.ClientNotice("AkashaHelper: Using Berserker mode")
			inject_joymax(0x70A7,b'\x01',False)
		elif msg == "R":
			# Quickly check if is dead
			character = get_character_data()
			if character['hp'] == 0:
				# RIP
				log('AkashaHelper: Resurrecting at town...')
				phBotChat.ClientNotice('AkashaHelper: Resurrecting at town...')
				inject_joymax(0x3053,b'\x01',False)
			else:
				log('AkashaHelper: Trying to use return scroll...')
				phBotChat.ClientNotice('AkashaHelper: Trying to use return scroll...')
				# Avoid high CPU usage with too many chars at the same time
				Timer(random.uniform(0.5,2),use_return_scroll).start()
		elif msg.startswith("TP"):
			# deletes command header and whatever used as separator
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
				log("AkashaHelper: Incorrect structure to inject packet")
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
			# Log the info
			log("AkashaHelper: Injecting packet...\nOpcode: 0x"+'{:02X}'.format(opcode)+" - Encrypted: "+("Yes" if encrypted else "No")+"\nData: "+(' '.join('{:02X}'.format(int(msgPacket[x],16)) for x in range(dataIndex, msgPacketLen)) if len(data) else 'None'))
			phBotChat.ClientNotice("AkashaHelper: Injecting packet...\nOpcode: 0x"+'{:02X}'.format(opcode)+" - Encrypted: "+("Yes" if encrypted else "No")+"\nData: "+(' '.join('{:02X}'.format(int(msgPacket[x],16)) for x in range(dataIndex, msgPacketLen)) if len(data) else 'None'))
		elif msg.startswith("CHAT "):
			handleChatCommand(msg[5:])
		elif msg == "DC":
			log("AkashaHelper: Disconnecting...")
			phBotChat.ClientNotice("AkashaHelper: Disconnecting...")
			disconnect()
		elif msg == 'fare2':
			random_string = random.choice(bakborta)
			phBotChat.All(f'{str(random_string)}')
		elif msg == "OU":
			# Check if has party
			if get_party():
				# Left it
				log("AkashaHelper: Leaving the party..")
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
				log("AkashaHelper: Leaving the party..")
				phBotChat.ClientNotice("AkashaHelper: Leaving the party..")
				inject_joymax(0x7061,b'',False)
		elif msg == "gold":
			gold = get_inventory()['gold']
			mssg = f'Gold: {format(gold, ",d")}'
			phBotChat.Private(player,mssg)
		elif msg == 'cards':
			items = get_inventory()['items']
			if items != []:
				for item in items:
					sort_inventory()
					if item != None and "Large" in item['name'] and "tong" in item['name']:
						msg = f"largetong = {item['quantity']}"
						phBotChat.Private(player,msg)
					if item != None and "Phantom" in item['name'] and "harp" in item['name']:
						msg2 = f"phantom harp = {item['quantity']}"
						phBotChat.Private(player,msg2)
					if item != None and "Vindictive" in item['name']:
						msg3 = f"Vindictive  = {item['quantity']}"
						phBotChat.Private(player,msg3)
					if item != None and "Hook" in item['name'] and "hand" in item['name']:
						msg4 = f"Hook hand = {item['quantity']}"
						phBotChat.Private(player,msg4)
					if item != None and "Evil's heart" in item['name']:
						msg5 = f"evils heart = {item['quantity']}"
						phBotChat.Private(player,msg5)
					if item != None and "Broken" in item['name'] and "key" in item['name']:
						msg6 = f"Broken Key = {item['quantity']}"
						phBotChat.Private(player,msg6)
					if item != None and "Commander's patch" in item['name']:
						msg7 = f"Commander's Patch = {item['quantity']}"
						phBotChat.Private(player,msg7)
					if item != None and "Sereness's tears" in item['name']:
						msg8 = f"Sereness = {item['quantity']}"
						phBotChat.Private(player,msg8)
					if item != None and "Sedon" in item['name']:
						msg11 = f"i have egy chin = {item['quantity']}"
						phBotChat.Private(player,msg11)
					if item != None and "Bratoom" in item ['name']:
						msg12 = f" i have egy eu shield"
						phBotChat.Private(player,msg12)
		elif msg == "npz":
			npcs = get_npcs()
			log(f"{npcs}")
		elif msg == 'check':
			items = get_inventory()['items']
			if items != []:
				for item in items:
					sort_inventory()
					if item != None and "Magic stone of immortal(Lvl.11) (Untrade)" in item['name']:
						msg9 = f"untradable immo = {item['quantity']}"
						phBotChat.Private(player,msg9)
					if item != None and "Magic stone of immortal(Lvl.11)" in item['name']:
						msg10 = f"immo stones = {item['quantity']}"
						phBotChat.Private(player,msg10)
					if item != None and "Silk Scroll (25)" in item['name']:
						msg22 = f"silk = {item['quantity']}"
						phBotChat.Private(player,msg22)
		elif msg == "sox":
			inv = get_inventory()['items']
			for item in inv:
				if item is not None:
					serv_name = item['servername']
					if "A_RARE" in serv_name and "11" in serv_name:
						name = item['name']
						phBotChat.Private(player,name)
						log(f"{name}")

		elif msg == 'log':
			inv = get_inventory()['items']
			log(f"{inv}")

		elif msg == "spawn":
			spwanpet()
		




		elif msg == 'coins':
			items = get_inventory()['items']
			if items != []:
				for item in items:
					sort_inventory()
					if item != None and "Gold Coin" in item ['name']:
						msg18 = f"Gold Coins = {item['quantity']}"
						phBotChat.Private(player,msg18)
					if item != None and "Silver Coin" in item ['name']:
						msg19 = f"Silver Coins = {item['quantity']}"
						phBotChat.Private(player,msg19)
					if item != None and "Arena Coin" in item ['name']:
						msg20 = f"Arena Coins = {item['quantity']}"
						phBotChat.Private(player,msg20)
		elif msg.startswith("g:"):
			message = msg[2:].strip()
			if message:
				phBotChat.Global(message)
		elif msg == "mob":
			monsters = get_monsters()
			log(f'{monsters}')
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
				log("Plugin: Dismounting pet ["+pet+"]")
				phBotChat.ClientNotice("Plugin: Dismounting pet ["+pet+"]")
		if msg.startswith("RECALL "):
			msg = msg[7:]
			if msg:
				npcUID = GetNPCUniqueID(msg)
				if npcUID > 0:
					log("AkashaHelper: Designating recall to \""+msg.title()+"\"...")
					inject_joymax(0x7059, struct.pack('I',npcUID), False)
		if msg.startswith("R "):
			# remove command
			msg = msg[2:]
			if msg:
				# check params
				msg = msg.split(' ',1)
				# param type
				if msg[0] == 'return':
					# try to use it
					if reverse_return(0,''):
						log('AkashaHelper: Using reverse to the last return scroll location')
						phBotChat.ClientNotice('AkashaHelper: Using reverse to the last return scroll location')
				elif msg[0] == 'death':
					# try to use it
					if reverse_return(1,''):
						log('AkashaHelper: Using reverse to the last death location')
						phBotChat.ClientNotice('AkashaHelper: Using reverse to the last death location')
				elif msg[0] == 'player':
					# Check existing name
					if len(msg) >= 2:
						# try to use it
						if reverse_return(2,msg[1]):
							log('AkashaHelper: Using reverse to player "'+msg[1]+'" location')
							phBotChat.ClientNotice('AkashaHelper: Using reverse to player "'+msg[1]+'" location')
				elif msg[0] == 'zone':
					# Check existing zone
					if len(msg) >= 2:
						# try to use it
						if reverse_return(3,msg[1]):
							log('AkashaHelper: Using reverse to zone "'+msg[1]+'" location')
							phBotChat.ClientNotice('AkashaHelper: Using reverse to zone "'+msg[1]+'" location')
		if msg.startswith("USE "):
			# remove command
			msg = msg[4:]
			if msg:
				# search item with similar name or exact server name
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
		if msg.startswith("add "):  # Check if the message starts with "add "
			player = msg[4:].strip()  # Extract the part after "add "
			addLeader(player)  # Call the function to add the player
		if msg.startswith("remove "):  # Check if message starts with "remove"
			player = msg[7:].strip()  # Extract player name after "remove"
			remLeader(player)  # Call the function to remove the player
def addLeader(player):
			if inGame and player and not lstLeaders_exist(player):
				# Init dictionary
				data = {}
				# Load config if exists
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
				log('AkashaHelper: Leader added [' + player + ']')
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
						log(f'AkashaHelper: Leader [{player}] not found in list.')
						return
				# Update GUI and notify
				QtBind.remove(gui, lstLeaders, player)
				log(f'AkashaHelper: Leader removed [{player}]')
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
				log("Following "+followPlayer+"...")
				phBotChat.ClientNotice("Following "+followPlayer+"...")
				move_to(movementDistance * x_unit + p['x'],movementDistance * y_unit + p['y'],0)
		else:
			# Avoid negative numbers
			log("Following "+followPlayer+"...")
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
					log('AkashaHelper: "'+pyData['pName']+'" plugin has been successfully updated')
			except:
				log("AkashaHelper: Error updating your plugin. Try again later..")












				

# Plugin loaded
log("AkashaHelper: "+pName+" v"+pVersion+" successfully loaded")

if os.path.exists(getPath()):
	# Adding RELOAD plugin support
	loadConfigs()
else:
	# Creating configs folder
	os.makedirs(getPath())
	log('AkashaHelper: '+pName+' folder has been created')

