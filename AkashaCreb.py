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
pVersion = '2.3'
pUrl = 'https://raw.githubusercontent.com/Desha11s/Phbot/main/AkashaCreb.py'

# ______________________________ Initializing ______________________________ #

# Globals
inGame = None
followActivated = False
followPlayer = ''
followDistance = 0

# Graphic user interface
gui = QtBind.init(__name__,pName)
QtBind.createLabel(gui,'Created by Akasha for Cerberus Online',525,10)
QtBind.createLabel(gui,'If you have more ideas to be added\n      Contact via discord :Ak047',525,260)
QtBind.createLabel(gui,'< All usual known commands are working and these are extra for easier usage >',11,55)
QtBind.createLabel(gui,'- att : starts bot\n- stop : stops bot\n- trace :starts trace\n- notrace : Stop trace\n- RETURN : back to town\n- GO : X Y --> will go to these coords\n- locate : tells you the current location\n- dwq : Take&Deliver dw quests (must be near npc)\n- HWT : teleports to HWT intermidate\n- Q1/Q2/Q3 : known teleports from ZsZc\n- SETR : +radius to set\n- leave : leaves pt\n- R death : reverse to last death point',10,70)
QtBind.createLabel(gui,'< These are some helpfull shortcuts > \n- DW : tp from bagdad to dw \n- BAG : tp from dw to baghdad\n- ALEX : tp from baghdad to alex(S)\n- regtower : register Tower Defend \n- reglms :    register  Last Man Standing\n- regLS :      register  Lottery Silk\n- regmag :   register  Survival Magic\n- regsolo :   register  Survival Solo\n- regmaze:  register  Maze LMS\n- regpvp :    register  Random PvP\n- reguniq :   register  Random Unique',260,70)
btnUpdate = QtBind.createButton(gui,'btnUpdate_clicked',"  Update Plugin ",400,8)
lvwPlugins = QtBind.createList(gui,11,33,400,20)
lstPluginsData = []
btnCheck = QtBind.createButton(gui,'btnCheck_clicked',"  Check Update  ",300,8)
#btn = QtBind.createCheckBox(gui, 'CbxDoNothing', 'Buy', 210, 30)
dwchk = QtBind.createCheckBox(gui, 'CBXDoNothing', 'Donwhang', 10, 10 )
conchk = QtBind.createCheckBox(gui, 'CBXDoNothing', 'Constantinpole', 100, 10 )
btnwep = QtBind.createButton(gui, 'on_wep_click', 'Lucky Hit (Devil S)', 200, 8)
#btnwep = QtBind.createButton(gui, 'dwq', 'DW QUEST', 10, 90)

tbxLeaders = QtBind.createLineEdit(gui,"",525,30,110,20)
lstLeaders = QtBind.createList(gui,525,52,110,111)
btnAddLeader = QtBind.createButton(gui,'btnAddLeader_clicked',"    Add   ",635,30)
btnRemLeader = QtBind.createButton(gui,'btnRemLeader_clicked',"     Remove     ",635,52)

inventory = get_inventory()
current_slot = 0
buy_counter = 0

def dwq():
	inject_joymax(0x7045,b'\x2A\x01\x00\x00',False)
	inject_joymax(0x7046,b'\x2A\x01\x00\x00\x02',False)
	inject_joymax(0x30D4,b'\x0A',False)
	inject_joymax(0x30D4,b'\x05',False)
	inject_joymax(0x30D4,b'\x05',False)

	inject_joymax(0x7045,b'\x2A\x01\x00\x00',False)
	inject_joymax(0x7046,b'\x2A\x01\x00\x00\x02',False)
	inject_joymax(0x30D4,b'\x07',False)
	inject_joymax(0x30D4,b'\x05',False)
	inject_joymax(0x30D4,b'\x05',False)

	inject_joymax(0x7045,b'\x2A\x01\x00\x00',False)
	inject_joymax(0x7046,b'\x2A\x01\x00\x00\x02',False)
	inject_joymax(0x30D4,b'\x08',False)
	inject_joymax(0x30D4,b'\x05',False)
	inject_joymax(0x30D4,b'\x05',False)

	inject_joymax(0x7045,b'\x2A\x01\x00\x00',False)
	inject_joymax(0x7046,b'\x2A\x01\x00\x00\x02',False)
	inject_joymax(0x30D4,b'\x09',False)
	inject_joymax(0x30D4,b'\x05',False)
	inject_joymax(0x30D4,b'\x05',False)

	inject_joymax(0x7045,b'\x2A\x01\x00\x00',False)
	inject_joymax(0x7046,b'\x2A\x01\x00\x00\x02',False)
	inject_joymax(0x30D4,b'\x0B',False)
	inject_joymax(0x30D4,b'\x05',False)
	inject_joymax(0x30D4,b'\x05',False)

	inject_joymax(0x7045,b'\x2A\x01\x00\x00',False)
	inject_joymax(0x7046,b'\x2A\x01\x00\x00\x02',False)
	inject_joymax(0x30D4,b'\x0C',False)
	inject_joymax(0x30D4,b'\x05',False)
	inject_joymax(0x30D4,b'\x05',False)

	inject_joymax(0x7045,b'\x2A\x01\x00\x00',False)
	inject_joymax(0x7046,b'\x2A\x01\x00\x00\x02',False)
	inject_joymax(0x30D4,b'\x0E',False)
	inject_joymax(0x30D4,b'\x05',False)
	inject_joymax(0x30D4,b'\x05',False)
#devil s
def kawep():
	global current_slot
	# Find the next slot with a "Magic POP Card"
	for slot, item in enumerate(inventory['items']):
		if slot > current_slot and item and item['name'] == "Magic POP Card":
			item['slot'] = slot
			slot_hex = hex(slot)[2:].zfill(2)
			slot_byte = bytes.fromhex(slot_hex)
			op = 0x7118
			if QtBind.isChecked(gui, dwchk):
				da = b'\xEF\x00\x00\x00\x11\x13\x00\x00'
				data = da + slot_byte
				inject_joymax(op, data, False)
				log(f'Injecting {data.hex()} - Trying on Devil S')
				current_slot = slot
				threading.Timer(0.50, kawep).start()
				break
			else:
				log('Magic Pop plugin: Please choose a town first')
			if QtBind.isChecked(gui, conchk):
				da = b'\xEF\x00\x00\x00\x11\x13\x00\x00'
				data = da + slot_byte
				inject_joymax(op, data, False)
				log(f'Injecting {data.hex()} - Trying on Devil S')
				current_slot = slot
				threading.Timer(0.50, kawep).start()
				break
			else:
				log('Magic Pop plugin: Please choose a town first')
	else:
		pass
#Functions to call the fusing function of each elixir when the button is clicked.
def on_wep_click():
	global current_slot
	for slot, item in enumerate(inventory['items']):
		if slot > current_slot and item and item['name'] == "Magic POP Card":
			threading.Timer(0.15, kawep).start()
			current_slot = slot
			break
#mainloop function to support the buying operation.
def event_loop():
	global buy_counter
	global counter
	if QtBind.isChecked(gui, btn):
		inv = get_inventory()
		none_slots = sum(item is None for item in inv['items'])
		if buy_counter <= none_slots -1:
			inject_joymax(0x7034, b'\x18\x1B\x04\x02\x00\x0B\x1C\x00\x50\x41\x43\x4B\x41\x47\x45\x5F\x49\x54\x45\x4D\x5F\x4D\x41\x4C\x4C\x5F\x47\x41\x43\x48\x41\x5F\x43\x41\x52\x44\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x37\x02\x00\x00', False)
			log(f'Buying a card - filled {buy_counter} slot out of {none_slots} so far...')
			buy_counter += 1
		else:
			buy_counter = 0  # Reset the counter back to 0
			log(f'Filled all of the {none_slots} empty slot(s) - {buy_counter} remaining slots left.')
			if buy_counter == 0:
				pass


# ______________________________ Methods ______________________________ #

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
			log('Plugin: Leader added ['+player+']')

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
			log('Plugin: Leader removed ['+selectedItem+']')

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
				log("Plugin: Selecting teleporter ["+source+"]")
				# Teleport found, select it
				inject_joymax(0x7045, struct.pack('<I', key), False)
				# Start a timer to teleport in 2.0 seconds
				Timer(2.0, inject_joymax, (0x705A,struct.pack('<IBI', key, 2, t[1]),False)).start()
				Timer(2.0, log, ("Plugin: Teleporting to ["+destination+"]")).start()
				return
		log('Plugin: NPC not found. Wrong NPC name or servername')
	else:
		log('Plugin: Teleport data not found. Wrong teleport name or servername')

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
		log('Plugin: Message "'+t+'" sent successfully!')

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
	log("Plugin: Random movement to (X:%.1f,Y:%.1f)"%(pX,pY))

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
	log('Plugin: Horse not found at your inventory')
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
	log('Plugin: Moving item "'+logItemName+'"...')
	# CLIENT_INVENTORY_ITEM_MOVEMENT
	inject_joymax(0x7034,p,False)

# Try to equip item
def EquipItem(item):
	itemData = get_item(item['model'])
	# Check equipables only
	if itemData['tid1'] != 1:
		log('Plugin: '+item['name']+' cannot be equiped!')
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

	log('Plugin: Using item "'+item['name']+'"...')
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
	# Remove guild name from union chat messages
	if t == 11:
		msg = msg.split(': ',1)[1]
	# Check player at leader list or a Discord message
	if player and lstLeaders_exist(player) or t == 100:
		# Parsing message command
		if msg == 'HELP':
			if acc_name == 'Devilhug':
				inject_joymax(0xA459,b'\x06\x00\x41\x6B\x73\x68\x61\x4E\x11',False)
			if acc_name == '_AkshaN_':
				inject_joymax(0xA459,b'\x06\x00\x41\x6B\x73\x68\x61\x4E\x0F',False)
			if acc_name == '__AkshaN__':
				inject_joymax(0xA459,b'\x06\x00\x41\x6B\x73\x68\x61\x4E\x10',False)
			if acc_name == 'MarOoZ':
				inject_joymax(0xA459,b'\x06\x00\x41\x6B\x73\x68\x61\x4E\x15',False)
			if acc_name == 'Painful':
				inject_joymax(0xA459,b'\x06\x00\x41\x6B\x73\x68\x61\x4E\x14',False)
			if acc_name == 'Veigor':
				inject_joymax(0xA459,b'\x06\x00\x41\x6B\x73\x68\x61\x4E\x0F',False)
			if acc_name == 'xXAkshaNXx':
				inject_joymax(0xA459,b'\x06\x00\x41\x6B\x73\x68\x61\x4E\x14',False)
		elif msg == 'regtower':
			inject_joymax(0xC006,b'\x00\x10\x00\x44\x65\x66\x65\x6E\x64\x20\x54\x68\x65\x20\x54\x6F\x77\x65\x72',False)
		elif msg == 'reglms':
			inject_joymax(0xC006,b'\x00\x11\x00\x4C\x61\x73\x74\x20\x4D\x61\x6E\x20\x53\x74\x61\x6E\x64\x69\x6E\x67',False)
		elif msg == 'regLS':
			inject_joymax(0xC006,b'\x00\x0C\x00\x4C\x6F\x74\x74\x65\x72\x79\x20\x53\x69\x6C\x6B',False)
		elif msg == 'regmag':
			inject_joymax(0xC006,b'\x00\x10\x00\x53\x75\x72\x76\x69\x76\x61\x6C\x20\x28\x4D\x61\x67\x69\x63\x29',False)
		elif msg == 'regsolo':
			inject_joymax(0xC006,b'\x00\x0F\x00\x53\x75\x72\x76\x69\x76\x61\x6C\x20\x28\x53\x6F\x6C\x6F\x29',False)
		elif msg == 'regmaze':
			inject_joymax(0xC006,b'\x00\x08\x00\x4D\x61\x7A\x65\x20\x4C\x4D\x53',False)
		elif msg == 'reguniq':
			inject_joymax(0xC006,b'\x00\x0F\x00\x55\x6E\x69\x71\x75\x65\x20\x4D\x61\x74\x63\x68\x69\x6E\x67',False)
		elif msg == 'regpvp':
			inject_joymax(0xC006,b'\x00\x0C\x00\x50\x56\x50\x20\x4D\x61\x74\x63\x68\x69\x6Ex67',False)
		elif msg == 'att':
			start_bot()
			log("Plugin: Bot started")
		elif msg == "stop":
			stop_bot()
			log("Plugin: Bot stopped")
		elif msg.startswith("trace"):
			# deletes empty spaces on right
			msg = msg.rstrip()
		if msg == "trace":
			if start_trace(player):
				log("Plugin: Starting trace to ["+player+"]")
			else:
				msg = msg[5:].split()[0]
				if start_trace(msg):
					log("Plugin: Starting trace to ["+msg+"]")
		elif msg.startswith("t"):
			# deletes empty spaces on right
			msg = msg.rstrip()
		if msg == "t":
			if start_trace(player):
				log("Plugin: Starting trace to ["+player+"]")
			else:
				msg = msg[1:].split()[0]
				if start_trace(msg):
					log("Plugin: Starting trace to ["+msg+"]")
		elif msg.startswith("TRACE"):
			# deletes empty spaces on right
			msg = msg.rstrip()
			if msg == "TRACE":
				if start_trace(player):
					log("Plugin: Starting trace to ["+player+"]")
			else:
				msg = msg[5:].split()[0]
				if start_trace(msg):
					log("Plugin: Starting trace to ["+msg+"]")
		elif msg.startswith("cmd trace"):
			# deletes empty spaces on right
			msg = msg.rstrip()
			if msg == "cmd trace":
				if start_trace(player):
					log("Plugin: Starting trace to ["+player+"]")
			else:
				msg = msg[9:].split()[0]
				if start_trace(msg):
					log("Plugin: Starting trace to ["+msg+"]")
		elif msg == "notrace":
			stop_trace()
			log("Plugin: Trace stopped")
		elif msg == "nt":
			stop_trace()
			log("Plugin: Trace stopped")
		elif msg == 'BAG':
			inject_joymax(0x705A,b'\x02\x00\x00\x00\x02\x15\x01\x00\x00',False)
		elif msg == 'DW':
			inject_joymax(0x705A,b'\x04\x00\x00\x00\x02\x02\x00\x00\x00',False)
		elif msg == 'ALEX':
			inject_joymax(0x705A,b'\x04\x00\x00\x00\x02\xAF\x00\x00\x00',False)
		elif msg.startswith("GO"):
			# deletes empty spaces on right
			msg = msg.rstrip()
			if msg == "GO":
				p = get_position()
				set_training_position(p['region'], p['x'], p['y'],p['z'])
				log("Plugin: Training area set to current position (X:%.1f,Y:%.1f)"%(p['x'],p['y']))
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
					log("Plugin: Training area set to (X:%.1f,Y:%.1f)"%(x,y))
				except:
					log("Plugin: Wrong training area coordinates!")
			start_bot()
		elif msg == "dwq":
			#A Falling star
			inject_joymax(0x7045,b'\x25\x01\x00\x00',False)
			inject_joymax(0x7046,b'\x25\x01\x00\x00\x02',False)
			inject_joymax(0x30D4,b'\x05',False)
			inject_joymax(0x30D4,b'\x05',False)
			inject_joymax(0x30D4,b'\x05',False)
			#quest lv 60
			inject_joymax(0x7045,b'\x25\x01\x00\x00',False)
			inject_joymax(0x7046,b'\x25\x01\x00\x00\x02',False)
			inject_joymax(0x30D4,b'\x06',False)
			inject_joymax(0x30D4,b'\x05',False)
			inject_joymax(0x30D4,b'\x05',False)
			#quest lv 75
			inject_joymax(0x7045,b'\x25\x01\x00\x00',False)
			inject_joymax(0x7046,b'\x25\x01\x00\x00\x02',False)
			inject_joymax(0x30D4,b'\x07',False)
			inject_joymax(0x30D4,b'\x05',False)
			inject_joymax(0x30D4,b'\x05',False)
			#quest lv 85
			inject_joymax(0x7045,b'\x25\x01\x00\x00',False)
			inject_joymax(0x7046,b'\x25\x01\x00\x00\x02',False)
			inject_joymax(0x30D4,b'\x08',False)
			inject_joymax(0x30D4,b'\x05',False)
			inject_joymax(0x30D4,b'\x05',False)
			inject_joymax(0x7045,b'\x25\x01\x00\x00',False)
			inject_joymax(0x7046,b'\x25\x01\x00\x00\x02',False)
			inject_joymax(0x30D4,b'\x09',False)
			inject_joymax(0x30D4,b'\x05',False)
			inject_joymax(0x30D4,b'\x05',False)
			#quest job 101+
			inject_joymax(0x7045,b'\x25\x01\x00\x00',False)
			inject_joymax(0x7046,b'\x25\x01\x00\x00\x02',False)
			inject_joymax(0x30D4,b'\x0A',False)
			inject_joymax(0x30D4,b'\x05',False)
			inject_joymax(0x30D4,b'\x05',False)
			#quest garden
			inject_joymax(0x7045,b'\x25\x01\x00\x00',False)
			inject_joymax(0x7046,b'\x25\x01\x00\x00\x02',False)
			inject_joymax(0x30D4,b'\x0B',False)
			inject_joymax(0x30D4,b'\x05',False)
			inject_joymax(0x30D4,b'\x05',False)			
		elif msg == 'locate':
			# Check current position
			pos = get_position()
			phBotChat.Private(player,'mkany (X:%.1f,Y:%.1f,Z:%1f,Region:%d)'%(pos['x'],pos['y'],pos['z'],pos['region']))
		elif msg.startswith("HWT2"):
			inject_teleport("Kings Valley","Pharaoh tomb (intermediate)")
		elif msg.startswith("HWT1"):
			inject_teleport("Kings Valley","Pharaoh tomb (beginner)")
		elif msg.startswith("Q1"):
			inject_teleport("Harbor Manager Marwa","Pirate Morgun") or inject_teleport("Pirate Morgun","Harbor Manager Gale") or inject_teleport("Harbor Manager Gale","Pirate Morgun") or inject_teleport("Priate Blackbeard","Harbor Manager Gale") or inject_teleport("Aircraft Ticket Seller Shard","Aircraft Ticket Seller Sangnia") or inject_teleport("Aircraft Ticket Seller Sangnia","Aircraft Ticket Seller Shard") or inject_teleport("Tunnel Manager Salhap","Tunnel Manager Maryokuk") or inject_teleport("Tunnel Manager Maryokuk","Tunnel Manager Salhap") or inject_teleport("Tunnel Manager Topni","Tunnel Manager Asui") or inject_teleport("Tunnel Manager Asui","Tunnel Manager Topni") or inject_teleport("Aircraft Ticket Seller Saena","Aircraft Ticket Seller Ajati") or inject_teleport("Aircraft Ticket Seller Ajati","Airship Ticket Seller Dawari") or inject_teleport("Airship Ticket Seller Dawari","Aircraft Ticket Seller Ajati") or inject_teleport("Aircraft Ticket Seller Sayun","Airship Ticket Seller Dawari") or inject_teleport("Airship Ticket Seller Poy","Aircraft Ticket Seller Ajati") or inject_teleport("Boat Ticket Seller Rahan","Boat Ticket Seller Salmai") or inject_teleport("Boat Ticket Seller Salmai","Boat Ticket Seller Rahan") or inject_teleport("Boat Ticket Seller Asimo","Boat Ticket Seller Asa") or inject_teleport("Boat Ticket Seller Asa","Boat Ticket Seller Asimo") or inject_teleport("Ferry Ticket Seller Tayun","Ferry Ticket Seller Doji") or inject_teleport("Ferry Ticket Seller Doji","Ferry Ticket Seller Tayun") or inject_teleport("Ferry Ticket Seller Hageuk","Ferry Ticket Seller Chau") or inject_teleport("Ferry Ticket Seller Chau","Ferry Ticket Seller Hageuk") or inject_teleport("forbidden plain","Kings Valley") or inject_teleport("Kings Valley","forbidden plain") or inject_teleport("abundance ground","Storm and cloud Desert") or inject_teleport("Storm and cloud Desert","abundance ground")
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
				log("Plugin: Training radius reseted to "+str(radius)+" m.")
			else:
				try:
					# split and parse movement radius
					radius = int(float(msg[4:].split()[0]))
					# to absolute
					radius = (radius if radius > 0 else radius*-1)
					set_training_radius(radius)
					log("Plugin: Training radius set to "+str(radius)+" m.")
				except:
					log("Plugin: Wrong training radius value!")
		elif msg.startswith('SETAREA '):
			# deletes empty spaces on right
			msg = msg[8:]
			if msg:
				# try to change to specified area name
				if set_training_area(msg):
					log('Plugin: Training area has been changed to ['+msg+']')
				else:
					log('Plugin: Training area ['+msg+'] not found in the list')
		elif msg == "ZERK":
			log("Plugin: Using Berserker mode")
			inject_joymax(0x70A7,b'\x01',False)
		elif msg == "RETURN":
			# Quickly check if is dead
			character = get_character_data()
			if character['hp'] == 0:
				# RIP
				log('Plugin: Resurrecting at town...')
				inject_joymax(0x3053,b'\x01',False)
			else:
				log('Plugin: Trying to use return scroll...')
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
				log("Plugin: Incorrect structure to inject packet")
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
			log("Plugin: Injecting packet...\nOpcode: 0x"+'{:02X}'.format(opcode)+" - Encrypted: "+("Yes" if encrypted else "No")+"\nData: "+(' '.join('{:02X}'.format(int(msgPacket[x],16)) for x in range(dataIndex, msgPacketLen)) if len(data) else 'None'))
		elif msg.startswith("CHAT "):
			handleChatCommand(msg[5:])
		elif msg == "DC":
			log("Plugin: Disconnecting...")
			disconnect()
		elif msg == "leave":
			# Check if has party
			if get_party():
				# Left it
				log("Plugin: Leaving the party..")
				inject_joymax(0x7061,b'',False)
		elif msg.startswith("RECALL "):
			msg = msg[7:]
			if msg:
				npcUID = GetNPCUniqueID(msg)
				if npcUID > 0:
					log("Plugin: Designating recall to \""+msg.title()+"\"...")
					inject_joymax(0x7059, struct.pack('I',npcUID), False)
		elif msg.startswith("EQUIP "):
			msg = msg[6:]
			if msg:
				# search item with similar name or exact server name
				item = GetItemByExpression(lambda n,s: msg in n or msg == s,13)
				if item:
					EquipItem(item)
		
		elif msg.startswith("UNEQUIP "):
			msg = msg[8:]
			if msg:
				# search item with similar name or exact server name
				item = GetItemByExpression(lambda n,s: msg in n or msg == s,0,12)
				if item:
					UnequipItem(item)
		elif msg.startswith("R "):
			# remove command
			msg = msg[2:]
			if msg:
				# check params
				msg = msg.split(' ',1)
				# param type
				if msg[0] == 'return':
					# try to use it
					if reverse_return(0,''):
						log('Plugin: Using reverse to the last return scroll location')
				elif msg[0] == 'death':
					# try to use it
					if reverse_return(1,''):
						log('Plugin: Using reverse to the last death location')
				elif msg[0] == 'player':
					# Check existing name
					if len(msg) >= 2:
						# try to use it
						if reverse_return(2,msg[1]):
							log('Plugin: Using reverse to player "'+msg[1]+'" location')
				elif msg[0] == 'zone':
					# Check existing zone
					if len(msg) >= 2:
						# try to use it
						if reverse_return(3,msg[1]):
							log('Plugin: Using reverse to zone "'+msg[1]+'" location')
		elif msg.startswith("USE "):
			# remove command
			msg = msg[4:]
			if msg:
				# search item with similar name or exact server name
				item = GetItemByExpression(lambda n,s: msg in n or msg == s,13)
				if item:
					UseItem(item)

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
					log('Plugin: "'+pyData['pName']+'" plugin has been successfully updated')
			except:
				log("Plugin: Error updating your plugin. Try again later..")









# Plugin loaded
log("Plugin: "+pName+" v"+pVersion+" successfully loaded")

if os.path.exists(getPath()):
	# Adding RELOAD plugin support
	loadConfigs()
else:
	# Creating configs folder
	os.makedirs(getPath())
	log('Plugin: '+pName+' folder has been created')

