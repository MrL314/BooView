
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import math, pygame, sys, json
from pygame.gfxdraw import *
from pygame.locals import *


import socket

import math


import Assets
import Objects
import KartScreen as KS


import threading



import tkinter as tk
from tkinter import *

import platform




#HOST = '127.0.0.1'
HOST = 'localhost'
PORT = 65432



with open('config.json', 'r') as f:
    config = json.load(f)


class character_bytes(object):

	def __init__(self):
		self.c_bytes = []


	def set_bytes(self, b):
		self.c_bytes = b

	def get_bytes(self):
		return self.c_bytes




CH_BYTES = character_bytes()
OBJ_BYTES = character_bytes()
ITEM_BYTES = character_bytes()



SQRT_2 = 2 ** 0.5






width = config["window_width"]
height = config["window_height"]




MAP_NAMES = [
	"MC3",
	"GV2",
	"DP2",
	"BC2",
	"VL2",
	"RR",
	"KB2",
	"MC1",
	"GV3",
	"BC3",
	"CI2",
	"DP3",
	"VL1",
	"KB1",
	"MC4",
	"MC2",
	"GV1",
	"BC1",
	"CI1",
	"DP1",
	"BT3",
	"BT4",
	"BT1",
	"BT2"
]


SIDE_FRAME_WIDTH = 100

WINDOW_WIDTH = width
WINDOW_HEIGHT = height


screen = None
CANVAS = None


def hex_to_int(h):
	return int('0x' + h, 16)


def byte_buffer(buf):
	index = 0

	while index < len(buf):
		yield buf[index]
		index += 1

def next_byte(g):
	b = next(g)

	return hex_to_int(b)

def next_word(g):
	low = next(g)
	high = next(g)
	return hex_to_int(low) + (256 * hex_to_int(high))

def next_word_signed(g):
	val = next_word(g)

	if val > 0x7fff:
		val -= 0x10000

	return val



def map_value(val, map_type=None):

	if map_type == None:
		return val
	elif map_type == 'width':
		return (val * width) / 1024
	elif map_type == 'height':
		return (val * height) / 1024
	elif map_type == 'radians':
		return (val * -2 * math.pi) / 255
	elif map_type == 'degrees':
		return (val * -360) / 255
	else:
		return val


def angle_between(angle_1, angle_2):

	x1 = math.cos(angle_1 * math.pi/180)
	y1 = math.sin(angle_1 * math.pi/180)
	x2 = math.cos(angle_2 * math.pi/180)
	y2 = math.sin(angle_2 * math.pi/180)

	dot = x1*x2 + y1*y2
	det = x1*y2 - y1*x2

	return math.atan2(det, dot) * 180/math.pi



def setup_map(map_name):

	global map_img
	global map_screen
	global screen
	global CANVAS
	global cp_image
	global dir_image
	global cp_screen
	global dir_screen
	global full_map
	global arrow_img
	global scl
	global BG
	global map_cp
	global map_flow


	if map_name[-1] != '/':
		map_name += '/'

	'''
	map_img = pygame.image.load('maps/' + map_name + 'map.png')

	map_screen = pygame.transform.smoothscale(map_img, (width, height))
	CANVAS = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	screen = KS.Screen(map_screen.get_size())
	BG = pygame.Surface((width, height))
	BG.fill((0, 0, 0))

	cp_image = pygame.image.load('maps/' + map_name + 'checkpoints.png')
	dir_image = pygame.image.load('maps/' + map_name + 'directions.png')

	cp_screen  = pygame.transform.smoothscale(cp_image, (width, height))
	dir_screen = pygame.transform.smoothscale(dir_image, (width, height))
	full_map   = pygame.transform.smoothscale(pygame.image.load('maps/' + map_name + 'fullMap.png'), (width, height))

	arrow_img = pygame.transform.smoothscale(pygame.image.load('assets/' + config["sprite"] + '.png'), (width//64, height//64))


	scl = map_img.get_width()/map_screen.get_width()
	'''


	try:
		map_img = pygame.image.load('maps/' + map_name + 'map.png').convert()
	except:
		map_img = pygame.Surface((1, 1))

	map_screen = pygame.transform.smoothscale(map_img, (width, height))
	#map_screen = pygame.transform.scale(map_img, (1024, 1024))
	CANVAS = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	screen = KS.Screen(map_screen.get_size())
	BG = pygame.Surface((width, height))
	BG.fill((0, 0, 0))

	try:
		cp_image = pygame.image.load('maps/' + map_name + 'checkpoints.png')
	except:
		cp_image = pygame.Surface((1, 1))
	try:
		dir_image = pygame.image.load('maps/' + map_name + 'directions.png')
	except:
		dir_image = pygame.Surface((1, 1))

	cp_screen  = pygame.transform.smoothscale(cp_image, (width, height))
	dir_screen = pygame.transform.smoothscale(dir_image, (width, height))

	#cp_screen  = pygame.transform.scale(cp_image, (1024, 1024))
	#dir_screen = pygame.transform.scale(dir_image, (1024, 1024))

	map_cp = map_screen.copy()
	map_cp.blit(cp_screen, (0, 0))

	map_flow = map_screen.copy()
	map_flow.blit(dir_screen, (0, 0))

	'''
	try:
		full_map   = pygame.transform.scale(pygame.image.load('maps/' + map_name + 'fullMap.png'), (width, height))
	except:
		full_map = pygame.Surface((1, 1))
	'''
	full_map = map_cp.copy()
	full_map.blit(dir_screen, (0, 0))
	#arrow_img = pygame.transform.scale(pygame.image.load('assets/' + config["sprite"] + '.png'), (width//64, height//64))


	scl = map_img.get_width()/map_screen.get_width()













# ========================== VARIABLES for general use ==============================








Racer0 = Objects.Racer(OBJ_ID="racer0", address=0x1000, display_dest=False)
Racer1 = Objects.Racer(OBJ_ID="racer1", address=0x1100)
Racer2 = Objects.Racer(OBJ_ID="racer2", address=0x1200)
Racer3 = Objects.Racer(OBJ_ID="racer3", address=0x1300)
Racer4 = Objects.Racer(OBJ_ID="racer4", address=0x1400)
Racer5 = Objects.Racer(OBJ_ID="racer5", address=0x1500)
Racer6 = Objects.Racer(OBJ_ID="racer6", address=0x1600)
Racer7 = Objects.Racer(OBJ_ID="racer7", address=0x1700)


Obj0 = Objects.Obstacle(OBJ_ID="obj0", address=0x1800)
Obj1 = Objects.Obstacle(OBJ_ID="obj0", address=0x1840)
Obj2 = Objects.Obstacle(OBJ_ID="obj0", address=0x1880)
Obj3 = Objects.Obstacle(OBJ_ID="obj0", address=0x18c0)
Obj4 = Objects.Obstacle(OBJ_ID="obj0", address=0x1900)
Obj5 = Objects.Obstacle(OBJ_ID="obj0", address=0x1940)
Obj6 = Objects.Obstacle(OBJ_ID="obj0", address=0x1980)
Obj7 = Objects.Obstacle(OBJ_ID="obj0", address=0x19c0)


Item0 = Objects.Item(OBJ_ID="item0", address=0x1a00)
Item1 = Objects.Item(OBJ_ID="item1", address=0x1a80)
Item2 = Objects.Item(OBJ_ID="item2", address=0x1b00)
Item3 = Objects.Item(OBJ_ID="item3", address=0x1b80)
Item4 = Objects.Item(OBJ_ID="item4", address=0x1438)
Item5 = Objects.Item(OBJ_ID="item5", address=0x1538)
Item6 = Objects.Item(OBJ_ID="item6", address=0x1638)
Item7 = Objects.Item(OBJ_ID="item7", address=0x1738)

num_racers = 8
num_obstacles = 8
num_items = 8



OBJECTS = [Racer0, Racer1, Racer2, Racer3, Racer4, Racer5, Racer6, Racer7,  Obj0, Obj1, Obj2, Obj3, Obj4, Obj5, Obj6, Obj7,   Item0, Item1, Item2, Item3, Item4, Item5, Item6, Item7]




SCREEN_SCALE = width




mouse = (-1, -1)
mouse_rel = (0, 0)
pressed = (False, False, False)


F = 0


LEFT_PRESSED = False
RIGHT_PRESSED = False




FOLLOW_MODE = False
FOLLOW_MODE_2P = False


TRAIL_LINES = False

grabbed = -1

m_off = (0, 0)



mouse_button_names = ("left", "middle", "right", "scroll_up", "scroll_down")

CURR_FRAME_MOUSE = {
	"left": False,
	"middle": False,
	"right": False,
	"scroll_up": False,
	"scroll_down": False
}

PREV_FRAME_MOUSE = {}
MOUSE_NEW = {}
MOUSE_RELEASED = {}

for m_button in CURR_FRAME_MOUSE:
	PREV_FRAME_MOUSE[m_button] = CURR_FRAME_MOUSE[m_button]
	MOUSE_NEW[m_button] = CURR_FRAME_MOUSE[m_button]
	MOUSE_RELEASED[m_button] = CURR_FRAME_MOUSE[m_button]





KEY_NAMES = {
	pygame.K_1: "1",
	pygame.K_2: "2",
	pygame.K_3: "3",
	pygame.K_4: "4",
	pygame.K_5: "5",
	pygame.K_6: "6",
	pygame.K_7: "7",
	pygame.K_8: "8",
	pygame.K_9: "9",
	pygame.K_0: "0",
	pygame.K_g: "g",
	pygame.K_c: "c",
	pygame.K_f: "f",
	pygame.K_i: "i",
	pygame.K_o: "o",
	pygame.K_t: "l",
	pygame.K_s: "s",
	pygame.K_r: "r",
	pygame.K_d: "d"
	
}



CURR_FRAME_KEYS = {
	"1": False,
	"2": False,
	"3": False,
	"4": False,
	"5": False,
	"6": False,
	"7": False,
	"8": False,
	"9": False,
	"0": False,
	"g": False,
	"c": False,
	"f": False,
	"i": False,
	"o": False,
	"l": False,
	"s": False,
	"r": False,
	"d": False
}


PREV_FRAME_KEYS = {}
KEYS_NEW = {}
KEYS_RELEASED = {}

for k_button in CURR_FRAME_KEYS:
	PREV_FRAME_KEYS[k_button] = CURR_FRAME_KEYS[k_button]
	KEYS_NEW[k_button] = CURR_FRAME_KEYS[k_button]
	KEYS_RELEASED[k_button] = CURR_FRAME_KEYS[k_button]



FOLLOWING = []
racers_to_follow = {
	"racer0": False,
	"racer1": False,
	"racer2": False,
	"racer3": False,
	"racer4": False,
	"racer5": False,
	"racer6": False,
	"racer7": False
}

SHOW_GHOST = True

ghost_mode_byte = 0




ANIM_TIMER = 0
ANIM_TIMER_SWAP = 15


FRAME_SKIP = config["FRAME_SKIP"]

FRAME_NUMBER = 0

demo_byte = 0



NUM_TRAILS = 2000

GHOST_FLASH_TIMER = 0



SPRITE_SCALE = 2


RECORD_MODE = False

SHOW_DEBUG = False

SPRITE_SCALE_VAR = None

# ==================================================================================================








# ==================================================================================================

def toggle_record_mode():
	global RECORD_MODE
	RECORD_MODE = not RECORD_MODE

def toggle_trails():
	global TRAIL_LINES
	TRAIL_LINES = not TRAIL_LINES


def toggle_follow_1():
	global racers_to_follow
	racers_to_follow["racer0"] = not racers_to_follow["racer0"]

def toggle_follow_2():
	global racers_to_follow
	racers_to_follow["racer1"] = not racers_to_follow["racer1"]

def toggle_follow_3():
	global racers_to_follow
	racers_to_follow["racer2"] = not racers_to_follow["racer2"]

def toggle_follow_4():
	global racers_to_follow
	racers_to_follow["racer3"] = not racers_to_follow["racer3"]

def toggle_follow_5():
	global racers_to_follow
	racers_to_follow["racer4"] = not racers_to_follow["racer4"]

def toggle_follow_6():
	global racers_to_follow
	racers_to_follow["racer5"] = not racers_to_follow["racer5"]

def toggle_follow_7():
	global racers_to_follow
	racers_to_follow["racer6"] = not racers_to_follow["racer6"]

def toggle_follow_8():
	global racers_to_follow
	racers_to_follow["racer7"] = not racers_to_follow["racer7"]

def toggle_cp():
	global show_checkpoints
	show_checkpoints = not show_checkpoints

def toggle_flow():
	global show_directions
	show_directions = not show_directions


# ==================================================================================================




print("#==================================================#")
print("#       Welcome to BooView by MrL314 (v0.4)!       #")
print("#==================================================#")


data = b''
while True:
	print("\n# Please connect socket via BizHawk's Lua Console. #")
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		#print("Listening for connection on port %d..." % (PORT,))
		conn, addr = s.accept()
		BYTES_AS_LIST = []


		with conn:
			try:
				print('Connected by', addr[0])


				# Pygame setup

				conn.send(b"FRAME\n")





				#pygame.display.set_caption("DetaSMK")
				#pygame.display.set_icon(pygame.image.load('assets/icon.png'))


				root = tk.Tk()
				embed = tk.Frame(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
				embed.grid(columnspan = (width), rowspan = height)   # check and fix?
				embed.pack(side=LEFT)

				os.environ['SDL_WINDOWID'] = str(embed.winfo_id())

				if platform.system == "Windows":
					os.environ['SDL_VIDEODRIVER'] = 'windib'


				root.title("BooView")
				root.iconphoto(False, PhotoImage(file='assets/icon.png'))

				pygame.init()



				font = pygame.font.Font(pygame.font.get_default_font(), 12)

				#clock = pygame.time.Clock()

				setup_map("MC3")

				
				prev_gamemode = 0x02
				prev_track_number = 0xff


				done = False
				show_checkpoints = False
				show_directions = False






				# ============================ Tkinter setup stuff ================================

				button_width = 50
				button_height = 50

				Assets.create_tk_images()

				

				SIDE_FRAME = tk.Frame(root, width=SIDE_FRAME_WIDTH, height=WINDOW_HEIGHT)



				REPLAY_BUTTON = tk.Button(SIDE_FRAME, text="Replay\nGhost", command=toggle_record_mode)
				TRAIL_BUTTON  = tk.Button(SIDE_FRAME, text="Show\nTrails", command=toggle_trails)

				CP_BUTTON   = tk.Button(SIDE_FRAME, text="Show\nZones", command=toggle_cp)
				FLOW_BUTTON = tk.Button(SIDE_FRAME, text="Show\nFlows", command=toggle_flow)

				#FOLLOW_TEXT = tk.Text(SIDE_FRAME, text=)

				FOLLOW_FRAME = tk.LabelFrame(SIDE_FRAME, relief=GROOVE, text="FOLLOW RACER")

				FOLLOW_1_BUTTON = tk.Button(FOLLOW_FRAME, image=Assets.EMPTY_TK, command=toggle_follow_1, width=button_width, height=button_height, relief=FLAT)
				FOLLOW_2_BUTTON = tk.Button(FOLLOW_FRAME, image=Assets.EMPTY_TK, command=toggle_follow_2, width=button_width, height=button_height, relief=FLAT)
				FOLLOW_3_BUTTON = tk.Button(FOLLOW_FRAME, image=Assets.EMPTY_TK, command=toggle_follow_3, width=button_width, height=button_height, relief=FLAT)
				FOLLOW_4_BUTTON = tk.Button(FOLLOW_FRAME, image=Assets.EMPTY_TK, command=toggle_follow_4, width=button_width, height=button_height, relief=FLAT)
				FOLLOW_5_BUTTON = tk.Button(FOLLOW_FRAME, image=Assets.EMPTY_TK, command=toggle_follow_5, width=button_width, height=button_height, relief=FLAT)
				FOLLOW_6_BUTTON = tk.Button(FOLLOW_FRAME, image=Assets.EMPTY_TK, command=toggle_follow_6, width=button_width, height=button_height, relief=FLAT)
				FOLLOW_7_BUTTON = tk.Button(FOLLOW_FRAME, image=Assets.EMPTY_TK, command=toggle_follow_7, width=button_width, height=button_height, relief=FLAT)
				FOLLOW_8_BUTTON = tk.Button(FOLLOW_FRAME, image=Assets.EMPTY_TK, command=toggle_follow_8, width=button_width, height=button_height, relief=FLAT)

				FOLLOW_BUTTONS = [FOLLOW_1_BUTTON, FOLLOW_2_BUTTON, FOLLOW_3_BUTTON, FOLLOW_4_BUTTON, FOLLOW_5_BUTTON, FOLLOW_6_BUTTON, FOLLOW_7_BUTTON, FOLLOW_8_BUTTON]

				
				SPRITE_SIZE_FRAME = tk.LabelFrame(SIDE_FRAME, relief=GROOVE, text="SPRITE SCALE")

				SPRITE_SCALE_VAR = StringVar(root)

				SPRITE_SIZE_WIDGET = tk.Spinbox(SPRITE_SIZE_FRAME, increment=1, from_=1, to=4, state='readonly', width=4 , justify=RIGHT, textvariable=SPRITE_SCALE_VAR)
				SPRITE_SIZE_WIDGET.pack(side=TOP, fill=X)

				SPRITE_SCALE_VAR.set("2")



				SIDE_TABLE = [
					[REPLAY_BUTTON, TRAIL_BUTTON],
					[CP_BUTTON, FLOW_BUTTON],
					[(FOLLOW_FRAME, 2)],
					[(SPRITE_SIZE_FRAME, 2)]
					]

				
				FOLLOW_TABLE = [
					[FOLLOW_1_BUTTON, FOLLOW_2_BUTTON],
					[FOLLOW_3_BUTTON, FOLLOW_4_BUTTON],
					[FOLLOW_5_BUTTON, FOLLOW_6_BUTTON],
					[FOLLOW_7_BUTTON, FOLLOW_8_BUTTON]
				]

				row = 0
				for button_row in FOLLOW_TABLE:
					col = 0
					for b in button_row:
						if type(b) == type(tuple()):
							b[0].grid(column = col, row = row, columnspan=b[1], sticky="NEWS")
						else:
							b.grid(column = col, row = row, sticky="NEWS")

						col += 1

					row += 1




				row = 0
				for button_row in SIDE_TABLE:
					col = 0
					for b in button_row:
						if type(b) == type(tuple()):
							b[0].grid(column = col, row = row, columnspan=b[1], sticky="NEWS")
						else:
							b.grid(column = col, row = row, sticky="NEWS")

						col += 1

					row += 1


				SIDE_FRAME.pack(side=LEFT)

				# =================================================================================








				# main loop

				while done == False:


					#print(SPRITE_SIZE_SLIDER.get())

					#SCROLL_UP = False
					#SCROLL_DOWN = False

					PRESSED_RELIEF = SUNKEN




					# =======================================    Button Display    ========================================


					for i in range(8):

						if racers_to_follow["racer" + str(i)]: FOLLOW_BUTTONS[i].config(bg="#c8c8c8")
						else: FOLLOW_BUTTONS[i].config(bg="#f0f0f0")


					if show_checkpoints: CP_BUTTON.config(relief=PRESSED_RELIEF)
					else:  CP_BUTTON.config(relief=RAISED)

					if show_directions: FLOW_BUTTON.config(relief=PRESSED_RELIEF)
					else:  FLOW_BUTTON.config(relief=RAISED)


					if RECORD_MODE: REPLAY_BUTTON.config(relief=PRESSED_RELIEF)
					else:  REPLAY_BUTTON.config(relief=RAISED)

					if TRAIL_LINES: TRAIL_BUTTON.config(relief=PRESSED_RELIEF)
					else:  TRAIL_BUTTON.config(relief=RAISED)






					# ======================================================================================================











					

					# ======================================================================================================
					# Get pygame event values and setup
					

					# pre-polling clear
					#for m_button in CURR_FRAME_MOUSE:
					#	CURR_FRAME_MOUSE[m_button] = False

					#for k_button in CURR_FRAME_KEYS:
					#	CURR_FRAME_KEYS[k_button] = False
					CURR_FRAME_MOUSE["scroll_up"] = False
					CURR_FRAME_MOUSE["scroll_down"] = False

					ANIM_TIMER += 1
					FRAME_NUMBER += 1
					if ANIM_TIMER > (ANIM_TIMER_SWAP * 4) - 1:
						ANIM_TIMER = 0

					SPRITE_SCALE = int(SPRITE_SCALE_VAR.get())

					

					for event in pygame.event.get():
						if event.type == QUIT: 
							done = True
							root.destroy()

						elif event.type == pygame.MOUSEBUTTONDOWN:

							if event.button >= 1 and event.button <= 5:
								CURR_FRAME_MOUSE[mouse_button_names[event.button - 1]] = True

					

						elif event.type == pygame.MOUSEBUTTONUP:

							if event.button >= 1 and event.button <= 3:
								CURR_FRAME_MOUSE[mouse_button_names[event.button - 1]] = False

						elif event.type == pygame.MOUSEWHEEL:

							if event.y < 0:
								CURR_FRAME_MOUSE["scroll_down"] = True
							elif event.y > 0:
								CURR_FRAME_MOUSE["scroll_up"] = True


						elif event.type == pygame.MOUSEMOTION:
							#mouse_rel = pygame.mouse.get_rel()
							pass

						elif event.type == pygame.KEYDOWN:
							#parse keys pressed here
							if event.key in KEY_NAMES:
								CURR_FRAME_KEYS[KEY_NAMES[event.key]] = True

						elif event.type == pygame.KEYUP:
							#parse keys released here
							if event.key in KEY_NAMES:
								CURR_FRAME_KEYS[KEY_NAMES[event.key]] = False






					## SET UP "CLICKED/RELEASED" OBJECTS

					for m_button in CURR_FRAME_MOUSE:

						if CURR_FRAME_MOUSE[m_button] == True:
							if PREV_FRAME_MOUSE[m_button] == True:
								MOUSE_NEW[m_button] = False
							elif PREV_FRAME_MOUSE[m_button] == False:
								MOUSE_NEW[m_button] = True

						elif CURR_FRAME_MOUSE[m_button] == False:
							if PREV_FRAME_MOUSE[m_button] == True:
								MOUSE_RELEASED[m_button] = True
							elif PREV_FRAME_MOUSE[m_button] == False:
								MOUSE_RELEASED[m_button] = False


					for k_button in CURR_FRAME_KEYS:

						if CURR_FRAME_KEYS[k_button] == True:
							if PREV_FRAME_KEYS[k_button] == True:
								KEYS_NEW[k_button] = False
							elif PREV_FRAME_KEYS[k_button] == False:
								KEYS_NEW[k_button] = True

						elif CURR_FRAME_KEYS[k_button] == False:
							if PREV_FRAME_KEYS[k_button] == True:
								KEYS_RELEASED[k_button] = True
							elif PREV_FRAME_KEYS[k_button] == False:
								KEYS_RELEASED[k_button] = False

					
					# ======================================================================================================

					#if KEYS_NEW["g"] == True: SHOW_GHOST = not SHOW_GHOST

					try:

						data = conn.recv(4096)
								
						if not data:
							conn.send(b"close\n")
							conn.close()
							break

						
						CH_BYTES.set_bytes([])
						OBJ_BYTES.set_bytes([])
						ITEM_BYTES.set_bytes([])

						if data == b"sync" or data == b"sync\n":
							conn.send(b"ack\n")
						else:

							while data[:5] == b"sync\n":
								if len(data) > 5:
									data = data[5:]
								else:
									data = b""


							

							if data == b"close" or data == b"close\n" or data.decode("utf-8")[:5] == "close":
								break

							elif data[:7] == b'CH_DATA':

								data = data[7:]
								

								raw_bytes = data.decode('ascii').split("\n")

								#print(raw_bytes)



								byte_list = [raw_bytes[0][i:i+2] for i in range(0, len(raw_bytes[0]), 2)]
								
								CH_BYTES.set_bytes(byte_list)

								#conn.send(b"received data\n")

								raw_bytes = raw_bytes[1:]
								
								byte_list = [raw_bytes[0][i:i+2] for i in range(0, len(raw_bytes[0]), 2)]
								OBJ_BYTES.set_bytes(byte_list)

								#conn.send(b"received data\n")
								raw_bytes = raw_bytes[1:]
								
								#print(raw_bytes)
								byte_list = [raw_bytes[0][i:i+2] for i in range(0, len(raw_bytes[0]), 2)]
								ITEM_BYTES.set_bytes(byte_list)

								raw_bytes = raw_bytes[1:]

								conn.send(b"received data\n")


							else:
								#print(data[:9])
								conn.send(b"received data\n")

								



						BYTES_AS_LIST = CH_BYTES.get_bytes()

						if BYTES_AS_LIST != []:

							ch_bytes = byte_buffer([x for x in BYTES_AS_LIST])
							obj_bytes = byte_buffer([x for x in OBJ_BYTES.get_bytes()])
							item_bytes = byte_buffer([x for x in ITEM_BYTES.get_bytes()])

							gamemode = next_byte(ch_bytes)

							ghost_mode_byte = next_byte(ch_bytes)

							

							demo_byte = next_byte(ch_bytes)

							if ghost_mode_byte == 0x02 and demo_byte == 0:
								REPLAY_BUTTON.config(state="normal")

								if RECORD_MODE:
									SHOW_GHOST = True
									TRAIL_LINES = True
									SPRITE_SCALE = 2
									SPRITE_SCALE_VAR.set("2")
									SPRITE_SIZE_WIDGET.config(state='disabled')

								SHOW_GHOST = True
							else:
								SHOW_GHOST = False
								RECORD_MODE = False
								REPLAY_BUTTON.config(state="disabled")

								#print("HERE")
								#print(ghost_mode_byte)





							# do not try to update stuff if not in a right gamemode
							if not (gamemode == 0x02 or gamemode == 0x0e):
								for i in range(8):

									racers_to_follow["racer" + str(i)] = False

									
									FOLLOW_BUTTONS[i].config(image=Assets.EMPTY_TK)
									FOLLOW_BUTTONS[i].config(state="disabled")

								REPLAY_BUTTON.config(state="disabled")
								RECORD_MODE = False

								CANVAS.blit(BG, (0, 0))
								conn.send(b"FRAME\n")
								pygame.display.update(CANVAS.get_rect()) #pygame.display.flip()
								root.update()

								for m_button in CURR_FRAME_MOUSE:
									PREV_FRAME_MOUSE[m_button] = CURR_FRAME_MOUSE[m_button]

								for k_button in CURR_FRAME_KEYS:
									PREV_FRAME_KEYS[k_button] = CURR_FRAME_KEYS[k_button]

								## set up prev values
								prev_gamemode = gamemode
								prev_track_number = -1

								continue

							gametype = next_byte(ch_bytes)



							###### Control what map should be displayed 
							display_overlay = True
							if not (gamemode == 0x02 or gamemode == 0x0e):
								if prev_gamemode == 0x02 or prev_gamemode == 0x0e:
									#setup_map("NULL_MAP")
									raise ZeroDivisionError()
								display_overlay = False

								for i in range(8):
									OBJECTS[i].reset_trail()

									racers_to_follow["racer" + str(i)] = False

									
									FOLLOW_BUTTONS[i].config(image=Assets.EMPTY_TK)
									FOLLOW_BUTTONS[i].config(state="disabled")



							else:
								current_track_number = next_byte(ch_bytes)

								if current_track_number != prev_track_number:
									setup_map(MAP_NAMES[current_track_number])

									for i in range(8):
										OBJECTS[i].reset_trail()

										racers_to_follow["racer" + str(i)] = False

										
										FOLLOW_BUTTONS[i].config(image=Assets.EMPTY_TK)
										FOLLOW_BUTTONS[i].config(state="disabled")


							#print(current_track_number)





							###### DISPLAY MAP ######			
							if show_checkpoints:
								if show_directions:
									screen.blit(full_map, (0, 0))
								else:
									screen.blit(map_cp, (0, 0))
							else:				
								if show_directions:
									screen.blit(map_flow, (0, 0))
								else:
									screen.blit(map_screen, (0, 0))
							'''
							if not (show_checkpoints and show_directions):
								screen.blit(map_screen, (0, 0))
								if show_checkpoints == True:
									screen.blit(cp_screen, (0, 0))

								if show_directions == True:
									screen.blit(dir_screen, (0, 0))
							else:
								screen.blit(full_map, (0, 0))
							'''


							camera_angle = map_value(next_byte(ch_bytes), "degrees") + 90

							
							## DISPLAY OVERLAY DATA OVER TRACK
							if display_overlay:

								# Racer object data setting
								for i in range(8):
									OBJECTS[i].surface = CANVAS

									
									
										


									########### PARSE RECIEVED DATA PER CHARACTER ##############

									OBJECTS[i].ch_num = next_byte(ch_bytes)

									X = map_value(next_word(ch_bytes), "width")
									Y = map_value(next_word(ch_bytes), "height")

									if (gametype == 0) or (gametype == 2 and i < 2) or (gametype == 4 and (i == 0 or   (i == 1 and (not RECORD_MODE) and SHOW_GHOST )))  or (gametype == 6 and i < 2):
										
										FOLLOW_BUTTONS[i].config(image=Assets.CHARACTERS_TK[OBJECTS[i].ch_num // 2])
										FOLLOW_BUTTONS[i].config(state="normal")
										

									else:
										X = -100
										Y = -100
										OBJECTS[i].reset_trail()

										racers_to_follow["racer" + str(i)] = False

										
										FOLLOW_BUTTONS[i].config(image=Assets.EMPTY_TK)
										FOLLOW_BUTTONS[i].config(state="disabled")


									

									OBJECTS[i].x = X
									OBJECTS[i].y = Y
									OBJECTS[i].z = next_word(ch_bytes)

									OBJECTS[i].angle = map_value(next_byte(ch_bytes), "degrees")

									OBJECTS[i].vel = (map_value(next_word_signed(ch_bytes)/4, "width"), 
										              map_value(next_word_signed(ch_bytes)/4, "height"))

									OBJECTS[i].dest = (map_value(next_word(ch_bytes), "width"),
										               map_value(next_word(ch_bytes), "height"))

									




								#Obstacle object data
								for i in range(8):

									OBJECTS[num_racers + i].surface = CANVAS

									#obj_addr = next_word(obj_bytes)
									OBJECTS[num_racers + i].address = next_word(obj_bytes)

									OBJECTS[num_racers + i].x = map_value(next_word(obj_bytes), "width")
									OBJECTS[num_racers + i].y = map_value(next_word(obj_bytes), "height")
									OBJECTS[num_racers + i].z = next_word(obj_bytes)


									if gametype != 6:
										OBJECTS[num_racers + i].ch_num = (current_track_number * 4) + (ANIM_TIMER // ANIM_TIMER_SWAP) # dummy
									else:
										OBJECTS[num_racers + i].ch_num = (current_track_number * 4) + (i // 3)

										#print("Object", i, ": ", format(obj_addr, "04x"))



								
								# Item object data
								for i in range(8):

									if (gametype == 0 and i < 2) or (gametype == 2) or (gametype == 6 and i < 6):
										OBJECTS[num_racers + num_obstacles + i].surface = CANVAS


										########### PARSE RECIEVED DATA PER ITEM ##############

										OBJECTS[num_racers + num_obstacles + i].address = next_word(item_bytes)

										alive = next_byte(item_bytes)

										if alive < 0x80:
											OBJECTS[num_racers + num_obstacles + i].is_alive = False
										else:
											OBJECTS[num_racers + num_obstacles + i].is_alive = True

										ch_num_1 = next_byte(item_bytes)
										ch_num_2 = next_byte(item_bytes)
										#print(format(ch_num_1, "02x"), format(ch_num_2, "02x"))
										OBJECTS[num_racers + num_obstacles + i].ch_num = (ch_num_2 * 8) + ch_num_1

										#if MOUSE_NEW["left"]:
										#	print(format(OBJECTS[num_racers + num_obstacles + i].ch_num, "02x"))

										
										OBJECTS[num_racers + num_obstacles + i].x = map_value(next_word(item_bytes), "width")
										OBJECTS[num_racers + num_obstacles + i].y = map_value(next_word(item_bytes), "height")
										OBJECTS[num_racers + num_obstacles + i].z = next_word(item_bytes)
								
									
								
								


								#UPDATING


								#==============================================================================================================
								#
								#    MAIN UPDATING ROUTINE
								#
								#==============================================================================================================




								if True:
									m_x, m_y = pygame.mouse.get_pos()
									mouse = (m_x, m_y)
									m_x = screen.INV_SCALE*(-screen.x + m_x) * 1024/screen.DEFAULT_WIDTH
									m_y = screen.INV_SCALE*(-screen.y + m_y) * 1024/screen.DEFAULT_HEIGHT
									

									mouse_rel = pygame.mouse.get_rel()







								if MOUSE_NEW["left"]:
									
									for i in range(len(OBJECTS)):

										OBJ = OBJECTS[i]

										O_x = OBJ.x * 1024/screen.DEFAULT_WIDTH
										O_y = OBJ.y * 1024/screen.DEFAULT_HEIGHT

										

										if abs(O_x - m_x) < 5 * SPRITE_SCALE:
											if abs(O_y - m_y) < 5 * SPRITE_SCALE:
												grabbed = i
												m_off = (O_x - m_x, O_y - m_y)
												break




							
								if CURR_FRAME_MOUSE["left"]:
									
									if grabbed != -1:
										

										X_COORD = int(m_x + m_off[0])
										Y_COORD = int(m_y + m_off[1])

									

										OBJECTS[grabbed].x = (X_COORD * screen.DEFAULT_WIDTH/1024)
										OBJECTS[grabbed].y = (Y_COORD * screen.DEFAULT_HEIGHT/1024)

										ADDR = OBJECTS[grabbed].address

									
										if F == 1:
											F = 0
											
											
											
											part1 = "W_BYTES addr" + " " + str(ADDR + 0x18) + " " + "bytes" + " " + str(X_COORD & 0xff) + " " + str((X_COORD>>8 & 0xff)) + " 00 00 " + str(Y_COORD & 0xff) + " " + str((Y_COORD>>8 & 0xff)) + " 00 00 05 " + "\n"
											conn.send(part1.encode("utf-8"))

										F += 1

								else:
									if grabbed != -1:
										ADDR = OBJECTS[grabbed].address
										ground_instr = "W_BYTES addr" + " " + str(ADDR + 0x1e) + " " + "bytes" + " " + "00 00 00 00" + "\n"
										conn.send(ground_instr.encode("utf-8"))

									grabbed = -1
											







								














								#if KEYS_NEW["1"] == True: racers_to_follow["racer0"] = not racers_to_follow["racer0"]
								#if KEYS_NEW["2"] == True: racers_to_follow["racer1"] = not racers_to_follow["racer1"]
								#if KEYS_NEW["3"] == True: racers_to_follow["racer2"] = not racers_to_follow["racer2"]
								#if KEYS_NEW["4"] == True: racers_to_follow["racer3"] = not racers_to_follow["racer3"]
								#if KEYS_NEW["5"] == True: racers_to_follow["racer4"] = not racers_to_follow["racer4"]
								#if KEYS_NEW["6"] == True: racers_to_follow["racer5"] = not racers_to_follow["racer5"]
								#if KEYS_NEW["7"] == True: racers_to_follow["racer6"] = not racers_to_follow["racer6"]
								#if KEYS_NEW["8"] == True: racers_to_follow["racer7"] = not racers_to_follow["racer7"]

								#if KEYS_NEW["c"] == True: show_checkpoints = not show_checkpoints
								#if KEYS_NEW["f"] == True: show_directions  = not show_directions

								#if KEYS_NEW["r"] == True: RECORD_MODE = not RECORD_MODE

								#if KEYS_NEW["d"] == True: SHOW_DEBUG = not SHOW_DEBUG


								#if KEYS_NEW["l"] == True: TRAIL_LINES = not TRAIL_LINES
								'''
								if KEYS_NEW["s"] == True: 
									if not RECORD_MODE:
										SPRITE_SCALE += 1

									if SPRITE_SCALE > 4:
										SPRITE_SCALE = 1
								'''


								if RECORD_MODE and gametype == 4 and demo_byte == 0:

									'''
									X_COORD = math.floor(OBJECTS[1].x) * 2
									Y_COORD = math.floor(OBJECTS[1].y) * 2
									Z_COORD = math.floor(OBJECTS[1].z)
									H_COORD = math.floor(OBJECTS[1].angle * 255 / -360)
									ghost_instr = "W_BYTES addr" + " " + str(0x1018) + " " + "bytes" + " " + str(X_COORD & 0xff) + " " + str((X_COORD>>8) & 0xff) + "\n"
									conn.send(ghost_instr.encode("utf-8"))
									ghost_instr = "W_BYTES addr" + " " + str(0x101C) + " " + "bytes" + " " + str(Y_COORD & 0xff) + " " + str((Y_COORD>>8) & 0xff) + "\n"
									conn.send(ghost_instr.encode("utf-8"))
									ghost_instr = "W_BYTES addr" + " " + str(0x101F) + " " + "bytes" + " " + str(Z_COORD & 0xff) + " " + str((Z_COORD>>8) & 0xff) + "\n"
									conn.send(ghost_instr.encode("utf-8"))
									ghost_instr = "W_BYTES addr" + " " + str(0x102B) + " " + "bytes" + " " + str(H_COORD & 0xff) + "\n"
									conn.send(ghost_instr.encode("utf-8"))
									'''
									conn.send(b'DO_GHOST\n')
									racers_to_follow["racer0"] = True



								FOLLOWING = []

								for racer in racers_to_follow:
									if racers_to_follow[racer] == True:
										FOLLOWING.append(int(racer[-1])) # cheap but dirty way to add the racer number in
								






								'''
								if SCROLL_UP:
									screen.zoom(mouse, 1.1)

								elif SCROLL_DOWN:
									screen.zoom(mouse, 0.9)
								'''

															
								if CURR_FRAME_MOUSE["scroll_up"]:
									screen.zoom(mouse, 1.1)
								elif CURR_FRAME_MOUSE["scroll_down"]:
									screen.zoom(mouse, 0.9)
								

								'''
								if CURR_FRAME_KEYS["i"]:
									screen.zoom(mouse, 1.1)
								elif CURR_FRAME_KEYS["o"]:
									screen.zoom(mouse, 0.9)
								'''
							


								
								if CURR_FRAME_MOUSE["right"]:
									screen.x = screen.x + mouse_rel[0]
									screen.y = screen.y + mouse_rel[1]



								if len(FOLLOWING) > 0:
									# if following at least 1 racer

									CENTER_X = OBJECTS[FOLLOWING[0]].x
									CENTER_Y = OBJECTS[FOLLOWING[0]].y


									if len(FOLLOWING) > 1:
										left_x = 0x5000
										right_x = -1

										top_y = 0x5000
										bottom_y = -1

										for racer_id in FOLLOWING:
											O_x = OBJECTS[racer_id].x
											O_y = OBJECTS[racer_id].y

											if O_x < left_x: left_x = O_x
											if O_x > right_x: right_x = O_x

											if O_y < top_y: top_y = O_y
											if O_y > bottom_y: bottom_y = O_y


										'''
										# for zoom amount (if necessary)
										diff_x = (abs(right_x - left_x) * screen.DEFAULT_WIDTH / 1024) + 3
										diff_y = (abs(bottom_y - top_y) * screen.DEFAULT_WIDTH / 1024) + 3



										zoom_amount = (diff_x**2 + diff_y**2)**0.5

										if zoom_amount < 600:
											zoom_amount = 600
										'''


										CENTER_X = math.floor((left_x + right_x)/2)
										CENTER_Y = math.floor((top_y + bottom_y)/2)


									screen.center_x = CENTER_X
									screen.center_y = CENTER_Y







								
								"""  OBSOLETE CODE, KEEP JUST IN CASE
								if FOLLOW_MODE:
									screen.center_x = OBJECTS[0].x
									screen.center_y = OBJECTS[0].y


								if FOLLOW_MODE_2P:
								

									diff_x = (abs(OBJECTS[0].x - OBJECTS[1].x) * screen.DEFAULT_WIDTH / 1024) + 3
									diff_y = (abs(OBJECTS[0].y - OBJECTS[1].y) * screen.DEFAULT_HEIGHT / 1024) + 3

									'''
									if diff_x < 100:
										diff_x = 100

									if diff_y < 100:
										diff_y = 100

									zoom_amount = diff_x
									if diff_y > zoom_amount:
										zoom_amount = diff_y
									'''
									zoom_amount = (diff_x**2 + diff_y**2)**0.5

									if zoom_amount < 200:
										zoom_amount = 200

									#screen.zoom((screen.DEFAULT_WIDTH//2, screen.DEFAULT_HEIGHT//2), 0.001)

									screen.w = (screen.DEFAULT_WIDTH**2 / zoom_amount) * 0.4
									screen.h = (screen.DEFAULT_HEIGHT**2 / zoom_amount) * 0.4


									screen.center_x = (OBJECTS[0].x + OBJECTS[1].x)//2
									screen.center_y = (OBJECTS[0].y + OBJECTS[1].y)//2

									#screen.zoom((screen.DEFAULT_WIDTH//2, screen.DEFAULT_HEIGHT//2), (zoom_amount / screen.DEFAULT_WIDTH) * 0.8)


								if FOLLOW_MODE:
									screen.center_x = OBJECTS[0].x
									screen.center_y = OBJECTS[0].y

								#print(screen.center_x)
								"""


								#==============================================================================================================


								#DISPLAY
								if TRAIL_LINES == False:
									NUM_TRAILS = 0
								elif gametype == 4:
									NUM_TRAILS = 2000
								else:
									NUM_TRAILS = 200


								if FRAME_NUMBER > FRAME_SKIP:
									
									FRAME_NUMBER = 0

									CANVAS.blit(BG, (0, 0))
									#CANVAS.blit(screen.canvas, (screen.x, screen.y))
									CANVAS.blit(screen.canvas, (0, 0))

									# racers
									for i in range(7, -1, -1):
										OBJ = OBJECTS[i]
										if (gametype == 0) or (gametype == 2 and i < 2) or (gametype == 4 and i < 2) or (gametype == 6 and i < 2):
											#print(i)
											OBJ.scl = math.floor(screen.SCALE * width//128 * SQRT_2 * SPRITE_SCALE)
											OBJ.disp_x = OBJ.x*screen.SCALE + screen.x
											OBJ.disp_y = OBJ.y*screen.SCALE + screen.y
											if RECORD_MODE and i == 1 and gametype == 4:
												#OBJ.display(screen, trails=False)
												pass
											else:
												if (gametype == 4 and i == 1):
													GHOST_FLASH_TIMER += 1
													if GHOST_FLASH_TIMER == 2:
														GHOST_FLASH_TIMER = 0
													if GHOST_FLASH_TIMER % 2 == 0:
														OBJ.display(screen, trails=NUM_TRAILS)
													else:
														OBJ.display(screen, trails=NUM_TRAILS, ghost=True)
													
												else:
													OBJ.display(screen, trails=NUM_TRAILS)

									# obstacles
									for i in range(7, -1, -1):
										j = num_racers + i
										OBJ = OBJECTS[j]
										OBJ.scl = math.floor(screen.SCALE * width//128 * SPRITE_SCALE)
										OBJ.disp_x = OBJ.x*screen.SCALE + screen.x
										OBJ.disp_y = OBJ.y*screen.SCALE + screen.y
										OBJ.display()

									#items
									for i in range(7, -1, -1):
										j = num_racers + num_obstacles + i
										OBJ = OBJECTS[j]
										if (gametype == 0 and i < 2) or (gametype == 2) or (gametype == 6 and i < 6):
											if OBJ.is_alive:
												OBJ.scl = math.floor(screen.SCALE * width//256 * SPRITE_SCALE)
												OBJ.disp_x = OBJ.x*screen.SCALE + screen.x
												OBJ.disp_y = OBJ.y*screen.SCALE + screen.y
												OBJ.display()





									if SHOW_DEBUG:

										DEBUG_LIST = [
											"RECORD_MODE: " + str(RECORD_MODE),
											"NUM_TRAILS: " + str(NUM_TRAILS),
											"SPRITE_SCALE: " + str(SPRITE_SCALE),
											"FOLLOWING: " + str([x + 1 for x in FOLLOWING])
										]

										D_LINE = 0
										for DEBUG_TEXT in DEBUG_LIST:
											text_surface = font.render(DEBUG_TEXT, True, (255, 255, 255))
											CANVAS.blit(text_surface, dest=(0, D_LINE * 14))
											D_LINE += 1
										pass




								
								



							else:
								pass
							
							




							#threading.Thread(target=pygame.display.flip).start()
							conn.send(b"FRAME\n")
							pygame.display.update(CANVAS.get_rect()) #pygame.display.flip()
							root.update()
							

							




							# SET UP "PREV" VALUES

							for m_button in CURR_FRAME_MOUSE:
								PREV_FRAME_MOUSE[m_button] = CURR_FRAME_MOUSE[m_button]

							for k_button in CURR_FRAME_KEYS:
								PREV_FRAME_KEYS[k_button] = CURR_FRAME_KEYS[k_button]



							## set up prev values
							prev_gamemode = gamemode
							prev_track_number = current_track_number
					except ZeroDivisionError:
						conn.send(b"FRAME\n")
						pygame.display.update(CANVAS.get_rect()) #pygame.display.flip()
						root.update()


						#clock.tick(fps)
					except:
						#print(BYTES_AS_LIST)
						conn.send(b"close\n")
						conn.close()
						raise ValueError("eh")
						break

					#P_LEFT_PRESSED = LEFT_PRESSED
					#P_RIGHT_PRESSED = RIGHT_PRESSED

			except TclError as e:
				pass
			except Exception as e:
				print(e)

				

			pygame.quit()

			print(addr[0], "disconnected.", end="")
			printed_reason = False

			if data == b"close" or data == b"close\n" or data.decode("utf-8")[:5] == "close":
				if len(data.decode("utf-8")) > 6:
					print("  Reason: ", data.decode("utf-8")[6:])
					printed_reason = True

			if not printed_reason:
				print("  Reason: Server Script Forcibly Stopped")

			conn.send(b"close\n")
			conn.close()
		