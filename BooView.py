
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import math, pygame, sys, json
from pygame.gfxdraw import *
from pygame.locals import *


import socket

import math
import errno
import time


import Assets
import Objects
import KartScreen as KS

import TrackHelper


import threading



import tkinter as tk
from tkinter import *
from tkinter import filedialog

import platform



import threading

if False:
	import pygame._view


#HOST = '127.0.0.1'
HOST = 'localhost'
PORT = 65432

SOCKET_CONN = None


CURR_TIME = 0



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










'''
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
'''


SIDE_FRAME_WIDTH = 100

WINDOW_WIDTH = config["window_size"]
WINDOW_HEIGHT = config["window_size"]



#width = config["window_size"]
#height = config["window_size"]



width = height = 1024



spf = 1.0 / 60.0



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

PREV_SCALE = 1


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


MAP_UPDATE_TIMER = 0
MAP_UPDATE_RATE = 1

demo_byte = 0



NUM_TRAILS = 2000

GHOST_FLASH_TIMER = 0



SPRITE_SCALE = 2


RECORD_MODE = False

SHOW_DEBUG = False

SPRITE_SCALE_VAR = None

in_file_dialogue = False


CURR_TRACK_PALETTE = None
CURR_TRACK_TILES   = None
CURR_TRACK_TILEMAP = None

MAP_UPDATE_BYTES = []

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

def set_in_file_dialogue():
	global in_file_dialogue
	in_file_dialogue = True






















def SEND_DATA(data, send_all=False):

	global SOCKET_CONN

	bytes_left = size = len(data)
	bytes_sent = 0


	while bytes_left > 0:
		try:
			_num_sent = SOCKET_CONN.send(data[bytes_sent:])

			if _num_sent == 0: raise ConnectionResetError("CONNECTION ERROR!")

			bytes_sent += _num_sent
			bytes_left -= _num_sent

		except socket.error as e:

			if e.errno in [errno.EAGAIN, errno.EWOULDBLOCK]:
				if send_all:
					continue
				return data[bytes_sent:]
			else:
				raise e





def RECV_DATA():
	global SOCKET_CONN

	CONN_DAT = ""

	CONN_DAT += SOCKET_CONN.recv(8192).decode("ascii")



	return CONN_DAT




def send_signal(sig):

	if type(sig) == type(0):
		sig = str(sig)

	try:
		sig.decode("utf-8")	# dummy test to see if it is a string or a bytes list
	except AttributeError:
		sig = sig.encode("utf-8")

	if sig[-1:] != b'\n':
		sig = (sig.decode("utf-8") + "\n").encode("utf-8")

	SEND_DATA(sig)



def send_raw_signal(raw): 		send_signal(raw)
def send_frame_signal(): 		send_signal("FRAME")
def send_close_signal(): 		send_signal("close")
def send_ghost_signal(): 		send_signal("DO_GHOST")
def send_ack_signal(): 			send_signal("ack")
def send_pause_signal():		send_signal("PAUSE")
def send_unpause_signal(): 		send_signal("UNPAUSE")
def send_reset_map_signal(): 	send_signal("RESET_MAP")

def send_palette_signal(): send_signal("PALETTE")
def send_tileset_signal(): send_signal("TILES")
def send_tilemap_signal(): send_signal("TRACK")
def send_cp_data_signal(): send_signal("CP_DATA")
def send_flowmap_signal(): send_signal("FLOW")

def send_nonce_signal(): send_signal("nonce")




def send_w_sram_signal(sram_data):

	try:
		while sram_data[0] == " ": sram_data = sram_data[1:]
	except Exception as e:
		pass
	sram_data = " " + sram_data
	send_signal("W_SRAM" + sram_data)



def CLOSE_CONN():
	global SOCKET_CONN

	send_close_signal()
	SOCKET_CONN.close()





def wait_for_sync():
	global SOCKET_CONN

	CONN_DAT = RECV_DATA().split("\n")

	if CONN_DAT[0] == "sync":
		send_ack_signal()
		CONN_DAT = '\n'.join(CONN_DAT[1:])


	else:
		raise ValueError("NOT SYNC: " + CONN_DAT[0])








def do_frame_update(root, CANVAS):

	send_frame_signal()
	update_window(root, CANVAS)
	

def update_window(root, CANVAS):
	pygame.display.update(CANVAS.get_rect())
	root.update()

	wait_for_sync()

	sync_frame()


def sync_frame():
	global CURR_TIME


	time_left = spf - (time.clock() - CURR_TIME)

	#if time_left < -0.001:
	#	print(int(-10000 * time_left))

	while time.clock() - CURR_TIME < spf * 0.9:
		i = 1 # dummy

	CURR_TIME = time.clock()



def wait(t):
	now = time.clock()

	while time.clock() < now + t:
		i = 1 # dummy










M7_TILES = None
TILEMAP = None



def make_map_images(m_data, t_data, p_data, c_data, f_data):
	
	global map_screen
	global cp_screen
	global dir_screen


	global map_screen_SMALL
	global cp_screen_SMALL
	global dir_screen_SMALL


	global M7_TILES
	global TILEMAP
	global map_ready



	resize_size = (512, 512)
	#small_size = (1024, 1024)


	TILEMAP, M7_TILES = TrackHelper.get_tilemap_from_data(
														m_data,		# tilemap data 
														t_data, 	# tileset image data
														p_data)		# palette data


	map_screen = TILEMAP.copy()
	map_screen_SMALL = pygame.transform.smoothscale(
											TILEMAP, 			# 1024x1024 Mode7 Image
											resize_size)		# size to resize to


	cp, flow = TrackHelper.get_cpmap_flowmap_from_data(
													c_data, 	# checkpoint bound data
													f_data)		# flowmap data

	cp_screen = cp.copy()
	dir_screen = flow.copy()

	cp_screen_SMALL = pygame.transform.smoothscale(cp, resize_size)
	dir_screen_SMALL = pygame.transform.smoothscale(flow, resize_size)


	update_map_images()

	map_ready = True



def update_map_images():

	global map_screen
	global cp_screen
	global dir_screen

	global full_map
	global map_cp
	global map_flow

	global map_screen_SMALL
	global cp_screen_SMALL
	global dir_screen_SMALL

	global full_map_SMALL
	global map_cp_SMALL
	global map_flow_SMALL



	#map_screen = pygame.transform.smoothscale(TILEMAP, (width, height))

	map_cp = map_screen.copy()
	map_cp.blit(cp_screen, (0, 0))

	map_flow = map_screen.copy()
	map_flow.blit(dir_screen, (0, 0))

	full_map = map_cp.copy()
	full_map.blit(dir_screen, (0, 0))


	map_cp_SMALL = map_screen_SMALL.copy()
	map_cp_SMALL.blit(cp_screen_SMALL, (0, 0))

	map_flow_SMALL = map_screen_SMALL.copy()
	map_flow_SMALL.blit(dir_screen_SMALL, (0, 0))

	full_map_SMALL = map_cp_SMALL.copy()
	full_map_SMALL.blit(dir_screen_SMALL, (0, 0))





MAP_SCALE = 1024 / width


def update_map_data(update_data):

	global TILEMAP
	global map_screen
	global map_screen_SMALL



	for offs, val in update_data:
		#print(offs, val)
		
		TILE_X = offs % 128
		TILE_Y = offs // 128

		TILE = M7_TILES[val]

		map_screen.blit(
			pygame.transform.smoothscale(
				TILE,	# tile image 
				(8, 8)	# image size
			), 
			(round(TILE_X*8), round(TILE_Y*8))	# position to blit
		)

		map_screen_SMALL.blit(
			pygame.transform.smoothscale(
				TILE,	# tile image 
				(4, 4)	# image size
			), 
			(round(TILE_X*4), round(TILE_Y*4))	# position to blit
		)
		

	if update_data != []: update_map_images()	# only update map if updates happen
		
	







def setup_map_socket():
	global map_screen
	global cp_screen
	global dir_screen

	global full_map
	global map_cp
	global map_flow
	global map_ready

	

	# PALETTE DATA
	#conn.send(b"PALETTE\n")
	send_palette_signal()

	CONN_DAT = RECV_DATA().split("\n")
	

	P_DAT  = CONN_DAT[0]
	p_data = [int("0x" + P_DAT[i*2:(i+1)*2], 16) for i in range(len(P_DAT)//2)]

	#print("Finished palette")
	#print("Pal len: ", format(len(p_data), "04x"))







	# TILE DATA 
	#conn.send(b"TILES\n")
	send_tileset_signal()
	#print("in Tiles")
	#conn.recv(8192)
	T_DAT = ""

	for i in range(16):

		T_DAT += RECV_DATA().split("\n")[0]
		#conn.send(b"nonce\n")
		send_nonce_signal()

	'''
	T_DAT  = conn.recv(8192).decode("ascii").split("\n")[0]
	conn.send(b"nonce\n")
	T_DAT += conn.recv(8192).decode("ascii").split("\n")[0]
	conn.send(b"nonce\n")
	T_DAT += conn.recv(8192).decode("ascii").split("\n")[0]
	conn.send(b"nonce\n")
	T_DAT += conn.recv(8192).decode("ascii").split("\n")[0]
	'''

	t_data = [int("0x" + T_DAT[i*2:(i+1)*2], 16) for i in range(len(T_DAT)//2)][1::2]

	#print("Finished tiles")
	#print("Tile len: ", format(len(t_data), "04x"))








	# MAP DATA
	#conn.send(b"TRACK\n")
	send_tilemap_signal()
	#print("in Track")
	#conn.recv(8192)


	M_DAT = ""

	for i in range(8):

		M_DAT += RECV_DATA().split("\n")[0]
		send_nonce_signal()

	m_data = [int("0x" + M_DAT[i*2:(i+1)*2], 16) for i in range(len(M_DAT)//2)]






	# CP DATA
	#conn.send(b"CP_DATA\n")
	send_cp_data_signal()

	C_DAT = ""

	for i in range(2):
		C_DAT += RECV_DATA().split("\n")[0]
		#conn.send(b"nonce\n")
		send_nonce_signal()

	c_data = [int("0x" + C_DAT[i*2:(i+1)*2], 16) for i in range(len(C_DAT)//2)]



	# FLOW DATA
	#conn.send(b"FLOW\n")
	send_flowmap_signal()

	F_DAT = ""

	for i in range(2):
		F_DAT += RECV_DATA().split("\n")[0]
		#conn.send(b"nonce\n")
		send_nonce_signal()

	f_data = [int("0x" + F_DAT[i*2:(i+1)*2], 16) for i in range(len(F_DAT)//2)]




	map_ready = False
	map_thread = threading.Thread(target=make_map_images, args=(m_data, t_data, p_data, c_data, f_data))
	map_thread.start()



	













# ==================================================================================================




print("#==================================================#")
print("#       Welcome to BooView by MrL314 (v1.0)!       #")
print("#==================================================#")

root = None


WINDOW_SCALE = 1

data = b''
while True:
	print("\n# Please connect socket via BizHawk's Lua Console. #")
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		#print("Listening for connection on port %d..." % (PORT,))
		conn, addr = s.accept()

		SOCKET_CONN = conn

		BYTES_AS_LIST = []


		with conn:
			#conn.settimeout(10)
			try:
				print('Connected by', addr[0])


				# Pygame setup

				send_frame_signal()	# call "frame" once to set up
				wait_for_sync()

				CURR_TIME = time.clock()
				



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
				root.resizable(False, False)

				pygame.init()

				font = None
				
				#font = pygame.font.Font("./assets/freesansbold.ttf", 12)


				#clock = pygame.time.Clock()



				# ======== default screen =========
				map_img = pygame.Surface((1, 1))
				map_screen = pygame.transform.scale(map_img, (width, height))
				map_screen_SMALL = pygame.transform.scale(map_img, (512, 512))

				CANVAS = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
				
				#screen = KS.Screen(map_screen.get_size())
				#screen = KS.Screen((1024, 1024))
				###screen = KS.Screen((width, height))
				screen = KS.Screen((512, 512))
				#screen = KS.Screen((WINDOW_WIDTH, WINDOW_HEIGHT))

				#WINDOW_SCALE = screen.DEFAULT_WIDTH / WINDOW_WIDTH
				#WINDOW_SCALE = WINDOW_WIDTH / screen.DEFAULT_WIDTH
				
				BG = pygame.Surface((width, height))
				BG.fill((0, 0, 0))

				cp_image = pygame.Surface((1, 1))
				dir_image = pygame.Surface((1, 1))


				
				cp_screen  = pygame.transform.scale(cp_image, (width, height))
				dir_screen = pygame.transform.scale(dir_image, (width, height))

				map_cp = map_screen.copy()
				map_cp.blit(cp_screen, (0, 0))

				map_flow = map_screen.copy()
				map_flow.blit(dir_screen, (0, 0))

				full_map = map_cp.copy()
				full_map.blit(dir_screen, (0, 0))



				cp_screen_SMALL  = pygame.transform.scale(cp_image, (512, 512))
				dir_screen_SMALL = pygame.transform.scale(dir_image, (512, 512))

				map_cp_SMALL = map_screen_SMALL.copy()
				map_cp_SMALL.blit(cp_screen_SMALL, (0, 0))

				map_flow_SMALL = map_screen_SMALL.copy()
				map_flow_SMALL.blit(dir_screen_SMALL, (0, 0))

				full_map_SMALL = map_cp_SMALL.copy()
				full_map_SMALL.blit(dir_screen_SMALL, (0, 0))




				scl = map_img.get_width()/map_screen.get_width()
				map_ready = False
				# =================================

				
				prev_gamemode = 0x02
				prev_track_number = 0xff


				done = False
				show_checkpoints = False
				show_directions = False

				in_file_dialogue = False




				

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



				SRAM_UPLOAD_BUTTON = tk.Button(SIDE_FRAME, text="Load SRAM File", command=set_in_file_dialogue)



				SIDE_TABLE = [
					[REPLAY_BUTTON, TRAIL_BUTTON],
					[CP_BUTTON, FLOW_BUTTON],
					[(FOLLOW_FRAME, 2)],
					[(SPRITE_SIZE_FRAME, 2)],
					[(SRAM_UPLOAD_BUTTON, 2)]
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

						
						CH_BYTES.set_bytes([])
						OBJ_BYTES.set_bytes([])
						ITEM_BYTES.set_bytes([])


						data = RECV_DATA()


								
						if not data:
							#conn.send(b"close\n")
							#conn.close()
							CLOSE_CONN()
							break


						

						if data == "close" or data == "close\n": # or data.decode("utf-8")[:5] == "close":
							break

						elif data[:7] == 'CH_DATA':

							#print(len(data))

							data = data[7:]
							

							raw_bytes = data.split("\n")

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



							# map update bytes
							MAP_UPDATE_BYTES = [raw_bytes[0][i:i+2] for i in range(0, len(raw_bytes[0]), 2)]
							
							raw_bytes = raw_bytes[1:]

							#conn.send(b"received data\n")

						else:
							#print(data[:9])
							#conn.send(b"received data\n")
							pass





						if in_file_dialogue:


							#conn.send(b"PAUSE\n")

							send_pause_signal()
							
							#print("Paused")\
							#nonce = RECV_DATA()

							def update_while_open():
								global _unpaused
								_unpaused = False
								while not _unpaused:
									send_raw_signal("nonce")
									sync_frame()
								#print("EXITING THREAD")
							
							threading.Thread(target=update_while_open).start()
							sync_frame()

							file_path = tk.filedialog.askopenfilename()

							#conn.send(b"UNPAUSE\n")
							#nonce = RECV_DATA()
							_unpaused = True
							sync_frame()
							send_unpause_signal()
							

							if file_path != "": 
								
								SRM_DATA = []
								with open(file_path, "rb") as SRM_FILE:
									SRM_DATA = SRM_FILE.read()

								srm_send = ""
								for d in SRM_DATA:
									srm_send += " " + str(d)

								#conn.send(("W_SRAM" + srm_send + "\n").encode("utf-8"))
								send_w_sram_signal(srm_send)

								print("Wrote data from ", file_path)


							in_file_dialogue = False

							do_frame_update(root, CANVAS)
							

							continue

								



						BYTES_AS_LIST = CH_BYTES.get_bytes()

						if BYTES_AS_LIST != []:

							ch_bytes = byte_buffer([x for x in BYTES_AS_LIST])
							obj_bytes = byte_buffer([x for x in OBJ_BYTES.get_bytes()])
							item_bytes = byte_buffer([x for x in ITEM_BYTES.get_bytes()])

							gamemode = next_byte(ch_bytes)

							ghost_mode_byte = next_byte(ch_bytes)

							

							demo_byte = next_byte(ch_bytes)

							SPRITE_SIZE_WIDGET.config(state='normal')

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

								





							# do not try to update stuff if not in a right gamemode
							if not (gamemode == 0x02 or gamemode == 0x0e):
								for i in range(8):

									racers_to_follow["racer" + str(i)] = False

									
									FOLLOW_BUTTONS[i].config(image=Assets.EMPTY_TK)
									FOLLOW_BUTTONS[i].config(state="disabled")

								REPLAY_BUTTON.config(state="disabled")
								RECORD_MODE = False

								CANVAS.blit(BG, (0, 0))


								do_frame_update(root, CANVAS)


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
									raise ZeroDivisionError()
								display_overlay = False

								for i in range(8):
									OBJECTS[i].reset_trail()

									racers_to_follow["racer" + str(i)] = False

									
									FOLLOW_BUTTONS[i].config(image=Assets.EMPTY_TK)
									FOLLOW_BUTTONS[i].config(state="disabled")



							else:
								current_track_number = next_byte(ch_bytes)

								current_theme_number = next_byte(ch_bytes)
								current_theme_object = next_byte(ch_bytes)

								#print(current_theme_object)



								if current_track_number != prev_track_number:

									send_reset_map_signal()

									
									RECV_DATA() # nonce

									setup_map_socket()


									for i in range(8):
										OBJECTS[i].reset_trail()

										racers_to_follow["racer" + str(i)] = False

										
										FOLLOW_BUTTONS[i].config(image=Assets.EMPTY_TK)
										FOLLOW_BUTTONS[i].config(state="disabled")

								else:

									#conn.send(b"UPDATE_MAP\n")

									#print("UPDATE_MAP")

									#raw_bytes = RECV_DATA().split("\n")


									#raw_bytes = data.decode('ascii').split("\n")
									#byte_list = [int("0x" + raw_bytes[0][i:i+2], 16) for i in range(0, len(raw_bytes[0]), 2)]

									
									# if MAP_UPDATE_BYTES != []: print(MAP_UPDATE_BYTES)
									

									byte_list = [int("0x" + x, 16) for x in MAP_UPDATE_BYTES]

									map_updates = []

									while len(byte_list) >= 3:

										offs = byte_list[0] + (byte_list[1] * 256)
										val = byte_list[2]

										map_updates.append((offs, val))

										byte_list = byte_list[3:]

									update_map_data(map_updates)
									
									








							





							
							if map_ready:

								###### DISPLAY MAP ######
								if show_checkpoints:
									if show_directions:
										screen.blit(full_map_SMALL, (0, 0))
									else:
										screen.blit(map_cp_SMALL, (0, 0))
								else:				
									if show_directions:
										screen.blit(map_flow_SMALL, (0, 0))
									else:
										screen.blit(map_screen_SMALL, (0, 0))




								camera_angle = map_value(next_byte(ch_bytes), "degrees") + 90

								
								## DISPLAY OVERLAY DATA OVER TRACK
								if display_overlay:

									# Racer object data setting
									for i in range(8):
										OBJECTS[i].surface = CANVAS

										
										
											


										########### PARSE RECIEVED DATA PER CHARACTER ##############

										OBJECTS[i].ch_num = next_byte(ch_bytes)

										X_coord = map_value(next_word(ch_bytes), "width")
										Y_coord = map_value(next_word(ch_bytes), "height")

										if (gametype == 0) or (gametype == 2 and i < 2) or (gametype == 4 and (i == 0 or   (i == 1 and (not RECORD_MODE) and SHOW_GHOST )))  or (gametype == 6 and i < 2):
											
											FOLLOW_BUTTONS[i].config(image=Assets.CHARACTERS_TK[OBJECTS[i].ch_num // 2])
											FOLLOW_BUTTONS[i].config(state="normal")
											

										else:
											X_coord = -100
											Y_coord = -100
											OBJECTS[i].reset_trail()

											racers_to_follow["racer" + str(i)] = False

											
											FOLLOW_BUTTONS[i].config(image=Assets.EMPTY_TK)
											FOLLOW_BUTTONS[i].config(state="disabled")


										

										OBJECTS[i].x = X_coord
										OBJECTS[i].y = Y_coord
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
											#OBJECTS[num_racers + i].ch_num = (current_track_number * 4) + (ANIM_TIMER // ANIM_TIMER_SWAP) # dummy
											#print(((current_theme_object//2) * 4))
											OBJECTS[num_racers + i].ch_num = ((current_theme_object//2) * 4) + (ANIM_TIMER // ANIM_TIMER_SWAP) # dummy

										else:
											#OBJECTS[num_racers + i].ch_num = (current_track_number * 4) + (i // 3)
											OBJECTS[num_racers + i].ch_num = 28 + (i // 3)


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
											

											X_COORD = int((m_x + m_off[0])/2)
											Y_COORD = int((m_y + m_off[1] + 4)/2)

										

											OBJECTS[grabbed].x = (X_COORD * screen.DEFAULT_WIDTH/1024) * 2
											OBJECTS[grabbed].y = (Y_COORD * screen.DEFAULT_HEIGHT/1024) * 2

											ADDR = OBJECTS[grabbed].address

										
											if F == 1:
												F = 0
												
												
												
												part1 = "W_BYTES addr" + " " + str(ADDR + 0x18) + " " + "bytes" + " " + str(X_COORD & 0xff) + " " + str((X_COORD>>8 & 0xff)) + " 00 00 " + str(Y_COORD & 0xff) + " " + str((Y_COORD>>8 & 0xff)) + " 00 00 05 " + "\n"
												#conn.send(part1.encode("utf-8"))
												send_raw_signal(part1)

											F += 1

									else:
										if grabbed != -1:
											ADDR = OBJECTS[grabbed].address
											ground_instr = "W_BYTES addr" + " " + str(ADDR + 0x1e) + " " + "bytes" + " " + "00 00 00 00" + "\n"
											#conn.send(ground_instr.encode("utf-8"))
											send_raw_signal(ground_instr)

										grabbed = -1
												







									














									


									if RECORD_MODE and gametype == 4 and demo_byte == 0:

										
										send_ghost_signal()
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


											


											CENTER_X = math.floor((left_x + right_x)/2)
											CENTER_Y = math.floor((top_y + bottom_y)/2)


										screen.center_x = CENTER_X
										screen.center_y = CENTER_Y







									
									


									#==============================================================================================================


									#DISPLAY
									if TRAIL_LINES == False:
										NUM_TRAILS = 0
									elif gametype == 4:
										NUM_TRAILS = 2000
									else:
										NUM_TRAILS = 100


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



										'''

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
										'''



								
								



							else:
								pass
							
							




							#threading.Thread(target=pygame.display.flip).start()
							do_frame_update(root, CANVAS)
							'''
							send_frame_signal()
							pygame.display.update(CANVAS.get_rect()) #pygame.display.flip()
							root.update()
							'''
							

							




							# SET UP "PREV" VALUES

							for m_button in CURR_FRAME_MOUSE:
								PREV_FRAME_MOUSE[m_button] = CURR_FRAME_MOUSE[m_button]

							for k_button in CURR_FRAME_KEYS:
								PREV_FRAME_KEYS[k_button] = CURR_FRAME_KEYS[k_button]



							## set up prev values
							prev_gamemode = gamemode
							prev_track_number = current_track_number
					except ZeroDivisionError:

						do_frame_update(root, CANVAS)
						'''
						send_frame_signal()
						pygame.display.update(CANVAS.get_rect()) #pygame.display.flip()
						root.update()
						'''


						#clock.tick(fps)
					except Exception as e:

						#print(BYTES_AS_LIST)
						#conn.send(b"close\n")
						#conn.close()
						CLOSE_CONN()
						raise
						

					#P_LEFT_PRESSED = LEFT_PRESSED
					#P_RIGHT_PRESSED = RIGHT_PRESSED

			except TclError as e:
				#print(e)
				pass
			except Exception as e:
				print(e)

				

			pygame.quit()

			if root != None:
				try:
					root.destroy()
					root = None
				except Exception:
					pass

			print(addr[0], "disconnected.", end="")
			printed_reason = False

			if data == "close" or data == "close\n": # or data.decode("utf-8")[:5] == "close":
				if len(data) > 6:
					print("  Reason: ", data[6:])
					printed_reason = True

			if not printed_reason:
				print("  Reason: Server Script Forcibly Stopped")

			try:
				#conn.send(b"close\n")
				#conn.close()
				CLOSE_CONN()
			except ConnectionResetError:
				pass
			except OSError:
				pass


	
		