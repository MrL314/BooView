
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import math, pygame, sys, json, OpenGL, numpy
from pygame.gfxdraw import *
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLU import *

from ctypes import *

import socket

import math
import errno
import time

from collections import deque


if False:
	import pygame._view

#pygame.init()
#pygame.display.set_mode((1, 1), pygame.NOFRAME)
import Assets
#pygame.quit()



import Objects
import KartScreen as KS

import TrackHelper

import BVmain



import threading



import tkinter as tk
from tkinter import *
from tkinter import filedialog

import platform



import threading

import traceback




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





PY_VERSION_NUMBER = "2.1"
LUA_VERSION_NUMBER = "2.1"

CH_BYTES = character_bytes()
OBJ_BYTES = character_bytes()
ITEM_BYTES = character_bytes()



SQRT_2 = 2 ** 0.5











WINDOW_WIDTH = config["window_size"]
WINDOW_HEIGHT = config["window_size"]

MAX_TRAILS_CONFIG = config["max_trail_length"]

TRAIL_FREQ_CONFIG = config["trail_log_rate"]

#width = config["window_size"]
#height = config["window_size"]



width = height = 1024
MAP_W = MAP_H = 1024



spf = 1.0 / 60.0



screen = None


def hex_to_int(h):
	return int(h, 16)


def byte_buffer(buf):
	index = 0

	while index < len(buf):
		yield buf[index]
		index += 1

def next_byte(g):
	return next(g)
	

def next_word(g):
	L = next(g)
	H = next(g)
	return L + (H << 8)

def next_word_signed(g):
	val = next_word(g)
	if val > 0x7fff: val -= 0x10000
	return val

def next_long(g):
	L = next(g)
	M = next(g)
	H = next(g)
	return L + (M << 8) + (H << 16)

def next_double(g):
	L1 = next(g)
	L2 = next(g)
	H1 = next(g)
	H2 = next(g)
	return ((L1 + (L2 << 8))/65536) + (H1 + (H2 << 8))

def next_double_signed(g):
	val = next_double(g)
	if val > 0x7fff: val -= 0x10000
	return val




MAP_SCLS = {
	'width': width / 1024,
	'height': height / 1024,
	'radians': -2 * math.pi / 255,
	'degrees': -360 / 255,
}


def map_value(val, map_type=None):
	try: return val * MAP_SCLS[map_type]
	except: return val



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








mouse = (-1, -1)
mouse_rel = (0, 0)
###pressed = (False, False, False)


F = 0


LEFT_PRESSED = False
RIGHT_PRESSED = False




FOLLOW_MODE = False
FOLLOW_MODE_2P = False




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




ghost_mode_byte = 0




ANIM_TIMER = 0
ANIM_TIMER_SWAP = 15


FRAME_SKIP = config["FRAME_SKIP"]

FRAME_NUMBER = 0



demo_byte = 0




GHOST_FLASH_TIMER = 0



SPRITE_SCALE = 2




SHOW_DEBUG = False






MAP_UPDATE_BYTES = []

# ==================================================================================================








# ==================================================================================================





SOCKET_DEBUG = False





def print_socket(d):
	if SOCKET_DEBUG:
		print("[DEBUG]", d)










def SEND_DATA(data, send_all=False):

	global SOCKET_CONN

	bytes_left = size = len(data)
	bytes_sent = 0


	while bytes_left > 0:
		try:
			b = data[bytes_sent:]

			#print_socket(">>>" + b.decode("ascii"))

			_num_sent = SOCKET_CONN.send(b)

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





def RECV_DATA(block=True):
	global SOCKET_CONN

	if SOCKET_CONN.gettimeout() == None:
		if block == False:
			SOCKET_CONN.settimeout(2)

	CONN_DAT = ""

	CONN_DAT += SOCKET_CONN.recv(8192).decode("ascii")

	#print_socket("<<< " + CONN_DAT)


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
def send_ghost_off_signal():    send_signal("GHOST_OFF")
def send_ack_signal(): 			send_signal("ack")
def send_pause_signal():		send_signal("PAUSE")
def send_unpause_signal(): 		send_signal("UNPAUSE")
def send_yield_signal():		send_signal("YIELD")
def send_unyield_signal(): 		send_signal("UNYIELD")
def send_reset_map_signal(): 	send_signal("RESET_MAP")

def send_palette_signal(): send_signal("PALETTE")
def send_tileset_signal(): send_signal("TILES")
def send_tilemap_signal(): send_signal("TRACK")
def send_zonemap_signal(): send_signal("ZONE")
def send_flowmap_signal(): send_signal("FLOW")
def send_cp_data_signal(): send_signal("CP_DATA")

def send_id_signal(): send_signal("ID_BVPY_" + PY_VERSION_NUMBER)

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





def wait_for_sync(initial_sync=False):
	global SOCKET_CONN

	while True:

		if initial_sync:
			SOCKET_CONN.settimeout(0.5)
		else:
			SOCKET_CONN.settimeout(10)
		
		failed = False
		try:
			CONN_DAT = RECV_DATA(block=True).split("\n")
		except socket.timeout:
			failed = True

		if failed: 
			SOCKET_CONN.settimeout(None)
			raise Exception("Socket took too long to respond.")

		if CONN_DAT[0] == "sync":
			send_ack_signal()
			CONN_DAT = '\n'.join(CONN_DAT[1:])
			break

		#else:
		#	raise ValueError("NOT SYNC: " + CONN_DAT[0])

	SOCKET_CONN.settimeout(None)




def match_lua_id(lua_version=LUA_VERSION_NUMBER):

	global SOCKET_CONN

	e_what = ""


	send_id_signal()

	d = ""
	try:
		SOCKET_CONN.settimeout(0.1)
		d += RECV_DATA().split('\n')[0]
	except Exception as e:
		e_what = str(e)

	if e_what != "": raise Exception(e_what)

	SOCKET_CONN.settimeout(None)

	if d != "ID_BVLUA_" + lua_version: raise ZeroDivisionError()

	return d






#def toGL_X(x):
#	return x/(WINDOW_WIDTH/2) - 0.5
#def toGL_Y(y):
#	return -y/(WINDOW_HEIGHT/2) + 0.5



def cnvGL_X(x): return (x*2)-1
def cnvGL_Y(y): return -(y*2)+1

def glb2GL_X(x): return cnvGL_X(x/WINDOW_WIDTH)
def glb2GL_Y(y): return cnvGL_Y(y/WINDOW_HEIGHT)
def glb2GL_W(w): return (w/WINDOW_WIDTH)*2
def glb2GL_H(h): return (h/WINDOW_HEIGHT)*-2


def map2disp_X(m_x): return screen.x + screen.SCALE * (m_x * screen.DEFAULT_WIDTH/MAP_W)
def map2disp_Y(m_y): return screen.y + screen.SCALE * (m_y * screen.DEFAULT_HEIGHT/MAP_H)


def disp2map_X(m_x): return screen.INV_SCALE*(-screen.x + m_x) * MAP_W/screen.DEFAULT_WIDTH
def disp2map_Y(m_y): return screen.INV_SCALE*(-screen.y + m_y) * MAP_H/screen.DEFAULT_HEIGHT


def map2GL_X(x): return glb2GL_X(map2disp_X(x))
def map2GL_Y(y): return glb2GL_Y(map2disp_Y(y))











def renderSurface(surf, pos=None, dim=None, rot=None, centered=False):	# SHOULD NEVER NEED TO BE USED ANYMORE!!
	#global GL_CNV_ID

	if pos == None:
		_x = 0
		_y = 0
	else:
		_x,_y = pos

	if dim == None:
		r = surf.get_rect()
		_w = r.width
		_h = r.height
	else:
		_w,_h = dim

	if rot == None:
		_a1 = 0
		_a2 = 0
		_a3 = 0
	else:
		_a1, _a2, _a3 = rot

	Assets.surfToGLTex(surf)

	renderTexture(Assets.GL_CNV_ID, (_x,_y), (_w,_h), (_a1, _a2, _a3), centered=centered)





def renderTexture(texID, pos=None, dim=None, rot=None, centered=False):

	if pos == None:
		_x = 0
		_y = 0
	else:
		_x,_y = pos

	if dim == None:
		_w = WINDOW_WIDTH
		_h = WINDOW_HEIGHT
	else:
		_w,_h = dim

	if rot == None:
		_a1 = 0
		_a2 = 0
		_a3 = 0
	else:
		_a1, _a2, _a3 = rot


	

	c_x = _x
	c_y = _y


	if not centered:
		c_x += _w/2
		c_y += _h/2

	glDisable(GL_LIGHTING)
	glEnable(GL_TEXTURE_2D)


	glMatrixMode(GL_MODELVIEW)

	glPushMatrix()

	#glOrtho(0, WINDOW_WIDTH, WINDOW_HEIGHT, 0, -1, 1);
	
	
	
	glLoadIdentity()

	glTranslatef(glb2GL_X(c_x), glb2GL_Y(c_y), 0)

	#glRotatef(_a1, 1, 0, 0)
	#glRotatef(_a2, 0, 1, 0)
	glRotatef(_a3, 0, 0, 1)

	glTranslatef(glb2GL_W(WINDOW_WIDTH/2),  glb2GL_H(WINDOW_HEIGHT/2), 0)

	glBindTexture(GL_TEXTURE_2D, texID)
	
	
	glBegin(GL_QUADS)
	

	if centered:
		glTexCoord2f(0, 0); glVertex2f(glb2GL_X(0-_w/2), glb2GL_Y(0-_h/2)) # top-left
		glTexCoord2f(0, 1); glVertex2f(glb2GL_X(0-_w/2), glb2GL_Y(0+_h/2)) # bottom-left
		glTexCoord2f(1, 1); glVertex2f(glb2GL_X(0+_w/2), glb2GL_Y(0+_h/2)) # bottom-right
		glTexCoord2f(1, 0); glVertex2f(glb2GL_X(0+_w/2), glb2GL_Y(0-_h/2)) # top-right
	else:
		glTexCoord2f(0, 0); glVertex2f(glb2GL_W(0-_w/2), glb2GL_H(0-_h/2)) # top-left
		glTexCoord2f(0, 1); glVertex2f(glb2GL_W(0-_w/2), glb2GL_H(0+_h/2)) # bottom-left
		glTexCoord2f(1, 1); glVertex2f(glb2GL_W(0+_w/2), glb2GL_H(0+_h/2)) # bottom-right
		glTexCoord2f(1, 0); glVertex2f(glb2GL_W(0+_w/2), glb2GL_H(0-_h/2)) # top-right

	glEnd()

	glPopMatrix()

	glDisable(GL_TEXTURE_2D)





def renderObject(texID, pos=None, dim=None, rot=None, centered=True):
	renderTexture(texID, pos=pos, dim=dim, rot=rot, centered=centered)





def do_frame_update():
	send_frame_signal()
	update_window()
	


def update_window():
	

	#T = time.perf_counter()
	
	# ============================
	BV.root.update() 




	glBindFramebuffer(GL_FRAMEBUFFER, 0)
	glDisable(GL_DEPTH_TEST)



	glDrawBuffer(GL_FRONT)
		
	glClearColor(1.0, 1.0, 1.0, 1.0)
	glClear(GL_COLOR_BUFFER_BIT)
	glLoadIdentity()

	glUseProgram(SCREEN_SHADER)
	glBindVertexArray(SCREEN_VAO)
	glBindTexture(GL_TEXTURE_2D, FBO_TEX)
	glDrawArrays(GL_TRIANGLES, 0, 6)
	glUseProgram(0)


	glFlush()

	glDrawBuffer(GL_BACK)


	glBindFramebuffer(GL_FRAMEBUFFER, FBO_0)




	glClearColor(0.0, 0.0, 0.0, 0.0)
	glClear(GL_COLOR_BUFFER_BIT)
	glLoadIdentity()

	
	# ============================

	#T = time.perf_counter()

	wait_for_sync()

	#T_0 = time.perf_counter() - T

	#print(100 * T_0 * 60)
	
	











M7_TILES = None
TILEMAP = None

TILEMAP_TEX = None
CPMAP_TEX = None
FLOWMAP_TEX = None

ZONE_SCL = 1
FLOW_SCL = config["flowmap_quality"]



def make_map_textures(m_data, t_data, p_data, z_data, f_data, c_data, THREADED=False):
	
	global M7_TILES
	global TILEMAP
	global ZONEMAP
	global FLOWMAP
	global map_ready

	global TILESET_IMAGE
	global TILEMAP_IMAGE
	global ZONEMAP_IMAGE
	global FLOWMAP_IMAGE


	TrackHelper.set_render_quality(
		zone_scl=ZONE_SCL,	# scale factor for zone map, for crispier zones!
		flow_scl=FLOW_SCL	# scale factor for flow map, for crispier arrows!
	)



	TILEMAP, M7_TILES = TrackHelper.get_tilemap_from_data(
		m_data,		# tilemap data 
		t_data, 	# tileset image data
		p_data		# palette data
	)

	ZONEMAP, FLOWMAP = TrackHelper.get_cpmap_flowmap_from_data(
		z_data, 	# checkpoint bound data
		f_data,		# flowmap data
		c_data		# checkpoint attribute data
	)

	update_map_textures(THREADED=THREADED)

	map_ready = True

	#pygame.image.save(create_surface_from_buff(TILEMAP, (1024, 1024), ALPHA=False), "TRACK/TILEMAP.png")
	#pygame.image.save(create_surface_from_buff(ZONEMAP, (1024*ZONE_SCL, 1024*ZONE_SCL)), "TRACK/ZONEMAP.png")
	#pygame.image.save(create_surface_from_buff(FLOWMAP, (1024*FLOW_SCL, 1024*FLOW_SCL)), "TRACK/FLOWMAP.png")









def create_surface_from_buff(buff, in_dim=(0, 0), ALPHA=True):


	frmt = "RGB"
	if ALPHA: frmt = "RGBA"

	return pygame.image.frombuffer(buff, in_dim, frmt)










def update_map_textures(THREADED=False):

	if not THREADED: update_tilemap()


def update_tilemap():
	global TILEMAP_TEX
	
	TILEMAP_TEX = Assets.buffToGLTex(TILEMAP, (1024, 1024), TILEMAP_TEX, ALPHA=False)


def update_zone_flow():
	global ZONEMAP_TEX
	global FLOWMAP_TEX

	ZONEMAP_TEX = Assets.buffToGLTex(ZONEMAP, (1024*ZONE_SCL, 1024*ZONE_SCL), ZONEMAP_TEX, ALPHA=True)
	FLOWMAP_TEX = Assets.buffToGLTex(FLOWMAP, (1024*FLOW_SCL, 1024*FLOW_SCL), FLOWMAP_TEX, ALPHA=True)







def update_map_data(update_data):
	"""Updates the texture data for the map given a list of tile offsets and tile values""" 

	for offs, val in update_data: update_map_tile(offs % 128, offs // 128, val)

	if update_data != []: update_map_textures()	# only update map if updates happen
		




def update_map_tile(TILE_X, TILE_Y, TILE_NUM):
	"""Updates the texture data for the map for a given tile. DOES NOT UPDATE THE TEXTURE ITSELF!!"""

	global TILEMAP


	M7_TILE_DATA = M7_TILES[TILE_NUM]

	for j in range(8):
		TM_Y = TILE_Y*8 + j
		TL_Y = j

		for i in range(8):
			TM_X = TILE_X*8 + i
			TL_X = i
			for p in range(3): #RGB
				TILEMAP[((TM_Y * 1024) + TM_X)*3 + p] = M7_TILE_DATA[((TL_Y * 8) + TL_X)*3 + p]







def setup_map_socket():

	global map_ready


	#T = time.perf_counter()

	#T0 = time.perf_counter() - T

	#print("TIME:", 60 * T0 * 100)



	# PALETTE DATA
	
	send_palette_signal()
	CONN_DAT = RECV_DATA().split("\n")


	P_DAT  = CONN_DAT[0]
	p_data = bytes.fromhex(P_DAT)





	

	# TILE DATA 
	
	send_tileset_signal()
	T_DAT = ""

	for i in range(8):
		T_DAT += RECV_DATA().split("\n")[0]
		send_nonce_signal()

	t_data = bytes.fromhex(T_DAT)





	# MAP DATA
	
	send_tilemap_signal()
	M_DAT = ""

	for i in range(8):
		M_DAT += RECV_DATA().split("\n")[0]
		send_nonce_signal()

	m_data = bytes.fromhex(M_DAT)





	# ZONE DATA

	send_zonemap_signal()
	Z_DAT = ""

	for i in range(2):
		Z_DAT += RECV_DATA().split("\n")[0]
		send_nonce_signal()

	z_data = bytes.fromhex(Z_DAT)




	# FLOW DATA

	send_flowmap_signal()
	F_DAT = ""

	for i in range(2):
		F_DAT += RECV_DATA().split("\n")[0]
		send_nonce_signal()

	f_data = bytes.fromhex(F_DAT)



	# ZONE ATTRIBUTES

	send_cp_data_signal()
	C_DAT = RECV_DATA().split("\n")[0]
	c_data = bytes.fromhex(C_DAT)








	map_ready = False
	map_thread = threading.Thread(target=make_map_textures, args=(m_data, t_data, p_data, z_data, f_data, c_data, True))
	map_thread.start()




	



def elapsed_time(reset=False):
	global _TIME

	t = time.perf_counter()
	e = t - _TIME

	if reset: _TIME = time.perf_counter()

	return e








def GENERATE_TEXTURES():
	global TILEMAP_TEX
	global ZONEMAP_TEX
	global FLOWMAP_TEX


	#global GL_CNV_ID

	TILEMAP_TEX = glGenTextures(1)
	ZONEMAP_TEX = glGenTextures(1)
	FLOWMAP_TEX = glGenTextures(1)

	
	#GL_CNV_ID = glGenTextures(1)



	Assets.create_GL_textures()



def GEN_VBO():
	global VBO1
	global VBO2

	global VAO1

	VBO1 = glGenBuffers(1)
	VBO2 = glGenBuffers(1)

	VAO1 = glGenVertexArrays(1)


def GEN_FBO():
	global FBO_TEX
	global FBO_0
	global RBO_0


	global SCREEN_VAO
	global SCREEN_VERTS

	
	SCREEN_TRI_COORDS = [
		-1, 1, 
		-1, -1, 
		1, -1,

		-1, 1, 
		1, -1, 
		1, 1
	]

	SCREEN_TEX_COORDS = [
		0, 1, 
		0, 0, 
		1, 0,
		
		0, 1, 
		1, 0, 
		1, 1
	]	

	SCREEN_VAO = glGenVertexArrays(1)
	SCREEN_VBO1 = glGenBuffers(1)
	SCREEN_VBO2 = glGenBuffers(1)

	glBindVertexArray(SCREEN_VAO)
	glBindBuffer(GL_ARRAY_BUFFER, SCREEN_VBO1)
	glBufferData(GL_ARRAY_BUFFER, len(SCREEN_TRI_COORDS)*4, (c_float*len(SCREEN_TRI_COORDS))(*SCREEN_TRI_COORDS), GL_STATIC_DRAW)
	glEnableVertexAttribArray(0)
	glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
	glBindBuffer(GL_ARRAY_BUFFER, SCREEN_VBO2)
	glBufferData(GL_ARRAY_BUFFER, len(SCREEN_TEX_COORDS)*4, (c_float*len(SCREEN_TEX_COORDS))(*SCREEN_TEX_COORDS), GL_STATIC_DRAW)
	glEnableVertexAttribArray(1)
	glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)


	FBO_0 = glGenFramebuffers(1)
	glBindFramebuffer(GL_FRAMEBUFFER, FBO_0)

	FBO_TEX = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, FBO_TEX)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, WINDOW_WIDTH, WINDOW_HEIGHT, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, FBO_TEX, 0)

	
	RBO_0 = glGenRenderbuffers(1)
	glBindRenderbuffer(GL_RENDERBUFFER, RBO_0)
	glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, WINDOW_WIDTH, WINDOW_HEIGHT)
	glBindRenderbuffer(GL_RENDERBUFFER, 0)
	glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, RBO_0)

	if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE: print("[WARNING] GL FRAMEBUFFER NOT COMPLETE")

	glBindFramebuffer(GL_FRAMEBUFFER, 0)
	#glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

	glUseProgram(SCREEN_SHADER)
	glUniform1i(screen_tex_screenTexture, 0) # ?
	glUseProgram(0)




def GEN_RBO():
	global RBO_0

	#RBO_0 = glGenRenderbuffers(1)
	pass



def GEN_SHADERS():
	###################################################################################
	##### TRAIL SHADER
	###################################################################################
	global TRAIL_VERTEX_SHADER
	global TRAIL_FRAGMENT_SHADER
	global TRAIL_SHADER
	###################################################################################
	
	TRAIL_VERTEX_SHADER = shaders.compileShader("""
		#version 460

		layout(std430, binding = 0) buffer TVertex
		{
		   float vert_data[];
		};

		uniform float S_w;
		uniform float S_h;
		uniform float S_x;
		uniform float S_y;
		uniform float W_w;
		uniform float W_h;

		uniform float spd_min;
		uniform float spd_max;

		uniform float line_width;

		out vec3 vout_color;



		float toGL_X(float x)
		{
			return 2 * ((S_x + S_w * x) / W_w) - 1;
		}

		float toGL_Y(float y)
		{
			return -1 * (2 * ((S_y + S_h * y) / W_h) - 1);
		}



		void main()
		{

			int line_i = gl_VertexID / 6;
			int tri_i = gl_VertexID % 6;



			vec4 va[4];
			int line_ind = line_i * 3;

			va[0] = vec4(toGL_X(vert_data[line_ind+0]), toGL_Y(vert_data[line_ind+1]), 0.0f, 1.0f);
			va[1] = vec4(toGL_X(vert_data[line_ind+3]), toGL_Y(vert_data[line_ind+4]), 0.0f, 1.0f);
			va[2] = vec4(toGL_X(vert_data[line_ind+6]), toGL_Y(vert_data[line_ind+7]), 0.0f, 1.0f);
			va[3] = vec4(toGL_X(vert_data[line_ind+9]), toGL_Y(vert_data[line_ind+10]), 0.0f, 1.0f);


			vec2 v_line  = normalize(va[2].xy - va[1].xy);
		    vec2 nv_line = vec2(-v_line.y, v_line.x);


			vec4 pos;
			float col;

			
			if (tri_i == 0 || tri_i == 1 || tri_i == 3)
			{
			    vec2 v_pred  = normalize(va[1].xy - va[0].xy);
			    vec2 v_miter = normalize(nv_line + vec2(-v_pred.y, v_pred.x));

			    pos = va[1];
			    pos.xy += v_miter * line_width * 2 * (tri_i == 1 ? -0.5 : 0.5) / dot(v_miter, nv_line);

			    col = vert_data[line_ind+5];
			}
			else
			{
			    vec2 v_succ  = normalize(va[3].xy - va[2].xy);
			    vec2 v_miter = normalize(nv_line + vec2(-v_succ.y, v_succ.x));

			    pos = va[2];
			    pos.xy += v_miter * line_width * 2 * (tri_i == 5 ? 0.5 : -0.5) / dot(v_miter, nv_line);

			    col = vert_data[line_ind+8];
			}


		    gl_Position = pos;


		    // color calculation
		    float max2 = spd_max - spd_min;

			col = (clamp(col, spd_min, spd_max) - spd_min) / max2;

			col = clamp(col, 0.1, 0.9);

			// set hue
			vec3 c = vec3((1 - col) / 3, 1.0f, 1.0f);

			// hsv to rgb
			vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
			vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);

		    vout_color = c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
		}
		""", GL_VERTEX_SHADER)

	TRAIL_FRAGMENT_SHADER = shaders.compileShader("""
		#version 460
		
		in vec3 vout_color;
		out vec4 fragColor;

		void main()
		{
		    fragColor = vec4(vout_color, 1.0);
		}
		""", GL_FRAGMENT_SHADER)


	TRAIL_SHADER = shaders.compileProgram(TRAIL_VERTEX_SHADER, TRAIL_FRAGMENT_SHADER)
	###################################################################################
	global trail_S_w
	global trail_S_h
	global trail_S_x
	global trail_S_y
	global trail_W_w
	global trail_W_h

	global trail_spd_min
	global trail_spd_max
	global trail_line_width

	trail_S_w = glGetUniformLocation(TRAIL_SHADER, "S_w")
	trail_S_h = glGetUniformLocation(TRAIL_SHADER, "S_h")
	trail_S_x = glGetUniformLocation(TRAIL_SHADER, "S_x")
	trail_S_y = glGetUniformLocation(TRAIL_SHADER, "S_y")
	trail_W_w = glGetUniformLocation(TRAIL_SHADER, "W_w")
	trail_W_h = glGetUniformLocation(TRAIL_SHADER, "W_h")

	trail_spd_min = glGetUniformLocation(TRAIL_SHADER, "spd_min")
	trail_spd_max = glGetUniformLocation(TRAIL_SHADER, "spd_max")
	trail_line_width = glGetUniformLocation(TRAIL_SHADER, "line_width")
	###################################################################################



	###################################################################################
	##### LINE SETS SHADER
	###################################################################################
	global LINESET_VERTEX_SHADER
	global LINESET_FRAGMENT_SHADER
	global LINESET_SHADER
	###################################################################################
	LINESET_VERTEX_SHADER = shaders.compileShader("""
		#version 460

		in vec2 vin_pos;
		in vec4 vin_col;

		uniform float S_w;
		uniform float S_h;
		uniform float S_x;
		uniform float S_y;
		uniform float W_w;
		uniform float W_h;

		out vec4 vout_col;


		float toGL_X(float x)
		{
			return 2 * ((S_x + S_w * x) / W_w) - 1;
		}

		float toGL_Y(float y)
		{
			return -1 * (2 * ((S_y + S_h * y) / W_h) - 1);
		}


		void main()
		{
			gl_Position = vec4(toGL_X(vin_pos[0]), toGL_Y(vin_pos[1]), 0.0f, 1.0f);
			vout_col = vin_col;
		}

		""", GL_VERTEX_SHADER)


	LINESET_FRAGMENT_SHADER = shaders.compileShader("""
		#version 460
		
		in vec4 vout_col;
		out vec4 fragColor;

		void main()
		{
			//fragColor = vec4(vout_col, 1.0);
			fragColor = vout_col;
		}
		""", GL_FRAGMENT_SHADER)



	LINESET_SHADER = shaders.compileProgram(LINESET_VERTEX_SHADER, LINESET_FRAGMENT_SHADER)
	###################################################################################
	global lset_S_w
	global lset_S_h
	global lset_S_x
	global lset_S_y
	global lset_W_w
	global lset_W_h

	lset_S_w = glGetUniformLocation(LINESET_SHADER, "S_w")
	lset_S_h = glGetUniformLocation(LINESET_SHADER, "S_h")
	lset_S_x = glGetUniformLocation(LINESET_SHADER, "S_x")
	lset_S_y = glGetUniformLocation(LINESET_SHADER, "S_y")
	lset_W_w = glGetUniformLocation(LINESET_SHADER, "W_w")
	lset_W_h = glGetUniformLocation(LINESET_SHADER, "W_h")
	###################################################################################



	###################################################################################
	##### SCREEN RENDER SHADER
	###################################################################################
	global SCREEN_VERTEX_SHADER
	global SCREEN_FRAGMENT_SHADER
	global SCREEN_SHADER
	###################################################################################
	SCREEN_VERTEX_SHADER = shaders.compileShader("""
		#version 330 core
		layout (location = 0) in vec2 aPos;
		layout (location = 1) in vec2 aTexCoords;

		out vec2 TexCoords;

		void main()
		{
			TexCoords = aTexCoords;
			gl_Position = vec4(aPos.x, aPos.y, 0.0, 1.0); 
		}
		""", GL_VERTEX_SHADER)



	SCREEN_FRAGMENT_SHADER = shaders.compileShader("""
		#version 330 core
		out vec4 FragColor;

		in vec2 TexCoords;

		uniform sampler2D screenTexture;

		void main()
		{
			vec3 col = texture(screenTexture, TexCoords).rgb;
			FragColor = vec4(col, 1.0);
		} 


		""", GL_FRAGMENT_SHADER)



	SCREEN_SHADER = shaders.compileProgram(SCREEN_VERTEX_SHADER, SCREEN_FRAGMENT_SHADER)
	###################################################################################
	global screen_tex_screenTexture

	screen_tex_screenTexture = glGetUniformLocation(SCREEN_SHADER, "screenTexture")
	###################################################################################

	


def SHOW_TRAIL_LINES():

	LW = max(1, screen.w / MAP_W)
	


	glUseProgram(TRAIL_SHADER)

	glUniform1f(trail_S_w, screen.SCALE * screen.DEFAULT_WIDTH / MAP_W)
	glUniform1f(trail_S_h, screen.SCALE * screen.DEFAULT_HEIGHT / MAP_H)
	glUniform1f(trail_S_x, screen.x)
	glUniform1f(trail_S_y, screen.y)
	glUniform1f(trail_W_w, WINDOW_WIDTH)
	glUniform1f(trail_W_h, WINDOW_HEIGHT)


	glUniform1f(trail_spd_min, MIN_SPD)
	glUniform1f(trail_spd_max, MAX_SPD)

	glUniform1f(trail_line_width, LW/WINDOW_WIDTH)


	glBindVertexArray(VAO1)
	glBindBuffer(GL_SHADER_STORAGE_BUFFER, VBO1)

	for i in range(7, -1, -1):

		if not OBJECTS[i].show_trails: continue


		pos = [x+0 for x in OBJECTS[i].prev_positions]
		c_len = OBJECTS[i].trail_cbuff_len + 1
		L = c_len*3

		if L == 0: continue

		pos.append(OBJECTS[i].x)
		pos.append(OBJECTS[i].y)
		pos.append(OBJECTS[i].speed)

		
		glBufferData(GL_SHADER_STORAGE_BUFFER, L*4, (c_float*L)(*pos), GL_STATIC_DRAW)



		N = c_len - 2

		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 0, VBO1)

		glDrawArrays(GL_TRIANGLES, 0, max(0, 6*(N-1)))

		


		#glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)




		#######################################################################################

	glUseProgram(0)

	#glFlush()		# enable if getting weird clipping!!

	'''
	for i in range(7, -1, -1):

		if not OBJECTS[i].show_trails: continue

		OBJECTS[i].prev_positions.pop()
		OBJECTS[i].prev_positions.pop()
		OBJECTS[i].prev_positions.pop()
	'''

	









DEG_2_RAD = math.pi / 180
RAD_2_DEG = 180 / math.pi












VECTOR_SCALE = 32
NUM_WIDTHS = 3
VEC_W = 2



CAM_POS = (0, 0)
C_MODE = 0



cam_scl_a = 8
cam_scl_b = 0

C_SCL = 8

CAM_WIDTH = 32 # idk why this works but it does
CAM_LINE_ALPHA = 0.5

A_VEL_SEGMENTS = 3









ls_numl = 0
ls_vdata = []
ls_cdata = []



def is_active_racer(racer_num):

	if racer_num > 7: return False

	# GP mode
	if gametype == 0: return True

	# Not GP-mode, so only racers 0 and 1 can possibly be active
	if racer_num > 1: return False

	# Match Race or Battle Mode
	if gametype == 2 or gametype == 6: return True

	# Time Trial [gametype == 4] (Need to check ghost)
	if C_MODE == 0: return True# both screens active (shouldn't happen in base game, but for mod support)
	elif C_MODE == 2: # top screen active only
		# racer 0 is player
		if racer_num == 0: return True

		# racer 1: check if should show ghost racer
		if BV.SHOW_GHOST and not BV.REPLAY_MODE: return True

		# racer 1: either ghost not enabled, or ghost enabled and in replay mode
		return False

	elif C_MODE == 4: # bottom screen active only
		# racer 1 is player
		if racer_num == 1: return True

		# racer 0: check if should show ghost racer
		if BV.SHOW_GHOST and not BV.REPLAY_MODE: return True

		# racer 0: either ghost not enabled, or ghost enabled and in replay mode
		return False


	return False



def racer_has_camera(racer_num):
	return (C_MODE == 0 and racer_num < 2) or (C_MODE == 2 and racer_num == 0) or (C_MODE == 4 and racer_num == 1)




def draw_line(v_a=(0, 0), v_b=(0,0), c_a=(0.0, 0.0, 0.0, 1.0), c_b=(0.0, 0.0, 0.0, 1.0)):
	global ls_vdata
	global ls_cdata
	global ls_numl


	#######################
	# Vertex 1
	#######################
	
	# Position
	ls_vdata.append(v_a[0])
	ls_vdata.append(v_a[1])

	# Color
	ls_cdata.append(c_a[0])
	ls_cdata.append(c_a[1])
	ls_cdata.append(c_a[2])

	# alpha channel
	try: ls_cdata.append(c_a[3])
	except IndexError: ls_cdata.append(1.0)

	#######################
	# Vertex 2
	#######################

	# Position
	ls_vdata.append(v_b[0])
	ls_vdata.append(v_b[1])

	# Color
	# Color
	ls_cdata.append(c_b[0])
	ls_cdata.append(c_b[1])
	ls_cdata.append(c_b[2])

	# alpha channel
	try: ls_cdata.append(c_b[3])
	except IndexError: ls_cdata.append(1.0)

	ls_numl += 1


def draw_lines(pnts, cols):

	L_p = len(pnts)
	L_c = len(cols)

	if L_p != L_c: raise IndexError("Mismatched sizes between points and color sets: pnts: " + str(L_p) + ", cols: " + str(L_c))

	for i in range(L_p - 1): 
		draw_line(
			v_a = pnts[i], 
			v_b = pnts[i+1], 
			c_a = cols[i], 
			c_b = cols[i+1]
		)




def DRAW_LINESET():
	global ls_vdata
	global ls_cdata
	global ls_numl

	glBindVertexArray(VAO1)
	
	glBindBuffer(GL_ARRAY_BUFFER, VBO1)
	#glBufferData(GL_ARRAY_BUFFER, ls_numl*(2*2)*4, (c_float*(ls_numl*(2*2)))(*ls_vdata), GL_STATIC_DRAW)
	glBufferData(GL_ARRAY_BUFFER, ls_numl*16, (c_float*(ls_numl*4))(*ls_vdata), GL_STATIC_DRAW)
	glVertexAttribPointer(glGetAttribLocation(LINESET_SHADER, 'vin_pos'), 2, GL_FLOAT, GL_FALSE, 0, None)
	glEnableVertexAttribArray(0)

	glBindBuffer(GL_ARRAY_BUFFER, VBO2)
	#glBufferData(GL_ARRAY_BUFFER, ls_numl*(4*2)*4, (c_float*(ls_numl*(4*2)))(*ls_cdata), GL_STATIC_DRAW)
	glBufferData(GL_ARRAY_BUFFER, ls_numl*32, (c_float*(ls_numl*8))(*ls_cdata), GL_STATIC_DRAW)
	glVertexAttribPointer(glGetAttribLocation(LINESET_SHADER, 'vin_col'), 4, GL_FLOAT, GL_FALSE, 0, None)
	glEnableVertexAttribArray(1)

	glDrawArrays(GL_LINES, 0, ls_numl*2) # The *2 here is necessary




def SHOW_WIDTH_1_VECTORS():
	global ls_vdata
	global ls_cdata
	global ls_numl

	LW = max(1, VEC_W * screen.w / MAP_W * (1 / NUM_WIDTHS))
	glLineWidth(LW)


	ls_numl = 0
	ls_vdata = []
	ls_cdata = []

	# show velocity data
	for i in range(7, -1, -1):

		if not is_active_racer(i): continue

		OBJ = OBJECTS[i]

		OBJ_x = OBJ.x
		OBJ_y = OBJ.y
		OBJ_vel = OBJ.vel
		OBJ_vx = OBJ_vel[0]/256
		OBJ_vy = OBJ_vel[1]/256
		OBJ_vz = OBJ_vel[2]#/256
		OBJ_spd = OBJ.speed/256
		OBJ_mspd = OBJ.max_speed / 256
		OBJ_acc = OBJ.accel/256
		OBJ_angle = OBJ.angle * DEG_2_RAD
		OBJ_v_angle = OBJ.v_angle * DEG_2_RAD
		OBJ_avel = OBJ.angle_vel * DEG_2_RAD

		OBJ_c_angle = OBJ.c_angle * DEG_2_RAD

		OBJ_tx = OBJ.dest[0]
		OBJ_ty = OBJ.dest[1]



		################################################
		'''
		draw_line(
			v_a = (
				CAM_POS[0] - 10, 
				CAM_POS[1]
			),
			v_b = (
				CAM_POS[0] + 10,
				CAM_POS[1]
			),
			c_a = (1.0, 1.0, 1.0, 1.0),
			c_b = (1.0, 1.0, 1.0, 1.0)
		)

		draw_line(
			v_a = (
				CAM_POS[0], 
				CAM_POS[1] - 10
			),
			v_b = (
				CAM_POS[0],
				CAM_POS[1] + 10
			),
			c_a = (1.0, 1.0, 1.0, 1.0),
			c_b = (1.0, 1.0, 1.0, 1.0)
		)
		'''
		################################################




		# Target coordinates
		################################################
		if BV.SHOW_TARGETS:
			t_alpha = 0.6
			t_size = 4
			# target line
			draw_line(
				v_a = (OBJ_x, OBJ_y),
				v_b = (OBJ_tx, OBJ_ty),
				c_a = (1.0, 1.0, 1.0, t_alpha),
				c_b = (1.0, 1.0, 1.0, t_alpha)
			)

			# target point
			'''
			vs = []
			cs = []
			num_segs = 12

			for j in range(num_segs+1):

				vs.append((
					(OBJ_tx + math.cos(j * math.pi * 2 / num_segs) * t_size),
					(OBJ_ty + math.sin(j * math.pi * 2 / num_segs) * t_size)
				))

				cs.append((1.0, 1.0, 1.0, t_alpha))

			draw_lines(vs, cs)
			'''
			'''
			draw_line(
				v_a = (OBJ_tx-t_size, OBJ_ty),
				v_b = (OBJ_tx+t_size, OBJ_ty),
				c_a = (1.0, 1.0, 1.0, t_alpha),
				c_b = (1.0, 1.0, 1.0, t_alpha)
			)

			draw_line(
				v_a = (OBJ_tx, OBJ_ty-t_size),
				v_b = (OBJ_tx, OBJ_ty+t_size),
				c_a = (1.0, 1.0, 1.0, t_alpha),
				c_b = (1.0, 1.0, 1.0, t_alpha)
			)
			'''
			
		################################################



		# Velocity components
		################################################
		if BV.SHOW_VEL_COMPONENTS:
			# X velocity
			draw_line(
				v_a = (OBJ_x, OBJ_y),
				v_b = (
					OBJ_x + OBJ_vx * VECTOR_SCALE,
					OBJ_y
				),
				c_a = (1.0, 1.0, 1.0, 1.0),
				c_b = (0.0, 1.0, 1.0, 1.0)
			)



			# Y velocity
			draw_line(
				v_a = (OBJ_x, OBJ_y),
				v_b = (
					OBJ_x,
					OBJ_y + OBJ_vy * VECTOR_SCALE
				),
				c_a = (1.0, 1.0, 1.0, 1.0),
				c_b = (0.0, 1.0, 1.0, 1.0)
			)

			
		################################################




		# Direction Normalized
		################################################
		if BV.SHOW_DIR_NORMALIZED:

			x_norm = - math.sin(OBJ_angle) #OBJ_mspd
			y_norm = - math.cos(OBJ_angle) #OBJ_mspd

			# Normalized direction
			draw_line(
				v_a = (OBJ_x, OBJ_y),
				v_b = (
					OBJ_x + x_norm * VECTOR_SCALE * 0.5,
					OBJ_y + y_norm * VECTOR_SCALE * 0.5
				),
				c_a = (1.0, 1.0, 1.0, 1.0),
				c_b = (0.0, 1.0, 1.0, 1.0)
			)

		################################################


		# Camera
		################################################
		if (BV.SHOW_CAMERA_ANGLE or BV.SHOW_CAM) and racer_has_camera(i):

			C = - math.sin(OBJ_c_angle)
			S = - math.cos(OBJ_c_angle)

			F_x = OBJ_x + C * VECTOR_SCALE
			F_y = OBJ_y + S * VECTOR_SCALE


			if BV.SHOW_CAMERA_ANGLE:
				# Actual direction
				draw_line(
					v_a = (OBJ_x, OBJ_y),
					v_b = (F_x, F_y),
					c_a = (0.9, 0.0, 1.0, 1.0),
					c_b = (0.9, 0.0, 1.0, 1.0)
				)




			C_W = CAM_WIDTH
			C_alpha = CAM_LINE_ALPHA

			if not BV.SHOW_CAM: 
				C_W = 0.5 * VECTOR_SCALE
				#C_alpha = 1.0

			R_x = OBJ_x  -  C * cam_scl_b * C_SCL  -  S * C_W
			R_y = OBJ_y  -  S * cam_scl_b * C_SCL  +  C * C_W

			L_x = OBJ_x  -  C * cam_scl_b * C_SCL  +  S * C_W
			L_y = OBJ_y  -  S * cam_scl_b * C_SCL  -  C * C_W


			
			# Ortho direction
			draw_line(
				v_a = (L_x, L_y),
				v_b = (R_x, R_y),
				c_a = (0.9, 0.0, 1.0, C_alpha),
				c_b = (0.9, 0.0, 1.0, C_alpha)
			)




			if BV.SHOW_CAM:
				CAM_DIST = 4

				C_x = OBJ_x - C * cam_scl_a * C_SCL
				C_y = OBJ_y - S * cam_scl_a * C_SCL

				
				# Camera direction
				draw_line(
					v_a = (OBJ_x, OBJ_y),
					v_b = (C_x, C_y),
					c_a = (0.9, 0.0, 1.0, CAM_LINE_ALPHA),
					c_b = (0.9, 0.0, 1.0, CAM_LINE_ALPHA)
				)


				
				# Cam_line A
				draw_line(
					v_a = (C_x, C_y),
					v_b = (
						C_x + (L_x - C_x) * CAM_DIST, 
						C_y + (L_y - C_y) * CAM_DIST
					),
					c_a = (1.0, 1.0, 0.0, CAM_LINE_ALPHA),
					c_b = (1.0, 1.0, 0.0, 0.0)
				)


				# Cam_line B
				draw_line(
					v_a = (C_x, C_y),
					v_b = (
						C_x + (R_x - C_x) * CAM_DIST, 
						C_y + (R_y - C_y) * CAM_DIST
					),
					c_a = (1.0, 1.0, 0.0, CAM_LINE_ALPHA),
					c_b = (1.0, 1.0, 0.0, 0.0)
				)









		################################################





		



		# Velocity Vector
		################################################
		if BV.SHOW_VEL_VECTOR:

			vx = - math.sin(OBJ_v_angle) * OBJ_spd
			vy = - math.cos(OBJ_v_angle) * OBJ_spd

			# velocity
			draw_line(
				v_a = (OBJ_x, OBJ_y),
				v_b = (
					OBJ_x + vx * VECTOR_SCALE, 
					OBJ_y + vy * VECTOR_SCALE
				),
				c_a = (1.0, 1.0, 1.0, 1.0),
				c_b = (0.0, 1.0, 0.2, 1.0)
			)
		################################################


		




		# Angular Velocity
		################################################
		if BV.SHOW_DIR_NORMALIZED and racer_has_camera(i):
			if OBJ_spd != 0:

				ang = OBJ_c_angle
				inc_ang = OBJ_avel / A_VEL_SEGMENTS

				if OBJ_avel < -math.pi:
					inc_ang = (OBJ_avel + math.pi*2) / A_VEL_SEGMENTS



				vs = []
				cs = []

				for j in range(A_VEL_SEGMENTS+1): # do first point, and then A_VEL_SEGMENTS new points

					x_norm = - math.sin(ang) #OBJ_mspd
					y_norm = - math.cos(ang) #OBJ_mspd

					ang += inc_ang

					vs.append((
						OBJ_x + x_norm * VECTOR_SCALE,
						OBJ_y + y_norm * VECTOR_SCALE
					))

					cs.append((1.0, 0.0, 1.0, 1.0))

				# return line
				draw_line(
					v_a = (
						(OBJ_x + vs[-1][0]) / 2, 
						(OBJ_y + vs[-1][1]) / 2
					),
					v_b = vs[-1],
					c_a = (1.0, 0.0, 1.0, 0.0),
					c_b = (1.0, 0.0, 1.0, 0.3)
				)


				draw_lines(vs, cs)




		################################################






	DRAW_LINESET()







def SHOW_WIDTH_2_VECTORS():
	global ls_vdata
	global ls_cdata
	global ls_numl

	LW = max(1, VEC_W * screen.w / MAP_W * (2 / NUM_WIDTHS))
	glLineWidth(LW)


	ls_numl = 0
	ls_vdata = []
	ls_cdata = []

	# show velocity data
	for i in range(7, -1, -1):

		if not is_active_racer(i): continue

		OBJ = OBJECTS[i]

		OBJ_x = OBJ.x
		OBJ_y = OBJ.y
		OBJ_vel = OBJ.vel
		OBJ_vx = OBJ_vel[0]/256
		OBJ_vy = OBJ_vel[1]/256
		OBJ_vz = OBJ_vel[2]#/256
		OBJ_spd = OBJ.speed / 256
		OBJ_mspd = OBJ.max_speed / 256
		OBJ_v_angle = OBJ.v_angle * DEG_2_RAD
		OBJ_angle = OBJ.angle * DEG_2_RAD


		



		



	DRAW_LINESET()




def SHOW_WIDTH_3_VECTORS():
	global ls_vdata
	global ls_cdata
	global ls_numl

	LW = max(1, VEC_W * screen.w / MAP_W * (3 / NUM_WIDTHS))
	glLineWidth(LW)


	ls_numl = 0
	ls_vdata = []
	ls_cdata = []

	# show velocity data
	for i in range(7, -1, -1):

		if not is_active_racer(i): continue

		OBJ = OBJECTS[i]

		OBJ_x = OBJ.x
		OBJ_y = OBJ.y
		OBJ_vel = OBJ.vel
		OBJ_vx = OBJ_vel[0]/256
		OBJ_vy = OBJ_vel[1]/256
		OBJ_vz = OBJ_vel[2]#/256
		OBJ_spd = OBJ.speed / 256
		OBJ_mspd = OBJ.max_speed / 256
		OBJ_v_angle = OBJ.v_angle * DEG_2_RAD
		OBJ_angle = OBJ.angle * DEG_2_RAD
		OBJ_acc = OBJ.accel / 256




		




		# Momentum Normalized
		################################################
		if BV.SHOW_VEL_NORMALIZED:
			
			if OBJ_spd != 0:

				x_norm = - math.sin(OBJ_v_angle) * OBJ_mspd
				y_norm = - math.cos(OBJ_v_angle) * OBJ_mspd


				# Normalized velocity
				'''
				ls_vdata.append(OBJ_x)
				ls_vdata.append(OBJ_y)
				#---
				ls_vdata.append(OBJ_x + x_norm * VECTOR_SCALE)
				ls_vdata.append(OBJ_y + y_norm * VECTOR_SCALE)


				# Colors
				ls_cdata.append(0.0)
				ls_cdata.append(0.0)
				ls_cdata.append(0.0)
				#---
				ls_cdata.append(0.0)
				ls_cdata.append(0.0)
				ls_cdata.append(0.0)

				ls_numl += 1
				'''

				draw_line(
					v_a = (OBJ_x, OBJ_y),
					v_b = (
						OBJ_x + x_norm * VECTOR_SCALE, 
						OBJ_y + y_norm * VECTOR_SCALE
					),
					c_a = (0.0, 0.0, 0.0, 1.0),
					c_b = (0.0, 0.0, 0.0, 1.0)
				)
		################################################



		# Acceleration
		################################################
		if BV.SHOW_ACCELERATION:
			
			if OBJ_acc != 0:

				C = - math.sin(OBJ_v_angle)
				S = - math.cos(OBJ_v_angle)

				#x_vel = C * OBJ_spd
				#y_vel = S * OBJ_spd

				x_acc = C * (OBJ_acc * 64)
				y_acc = S * (OBJ_acc * 64)


				# Normalized velocity
				
				if OBJ_acc < 0:
					# Colors
					COL_A = (0.4, 0.2, 0.2, 1.0)
					COL_B = (1.0, 0.5, 0.5, 1.0)
				else:
					# Colors
					COL_A = (0.2, 0.4, 0.2, 1.0)
					COL_B = (0.5, 1.0, 0.5, 1.0)


				draw_line(
					v_a = (OBJ_x, OBJ_y),
					v_b = (
						OBJ_x + x_acc * VECTOR_SCALE, 
						OBJ_y + y_acc * VECTOR_SCALE
					),
					c_a = COL_A,
					c_b = COL_B
				)

		################################################



		







	DRAW_LINESET()









def SHOW_EXTRA_VECTORS():
	glUseProgram(LINESET_SHADER)

	glUniform1f(lset_S_w, screen.SCALE * screen.DEFAULT_WIDTH / MAP_W)
	glUniform1f(lset_S_h, screen.SCALE * screen.DEFAULT_HEIGHT / MAP_H)
	glUniform1f(lset_S_x, screen.x)
	glUniform1f(lset_S_y, screen.y)
	glUniform1f(lset_W_w, WINDOW_WIDTH)
	glUniform1f(lset_W_h, WINDOW_HEIGHT)

	


	#SHOW_WIDTH_3_VECTORS()

	#SHOW_WIDTH_2_VECTORS()

	SHOW_WIDTH_1_VECTORS()





	glUseProgram(0)

	glLineWidth(1)








MAX_SPD = 0x100
MIN_SPD = 0xc0











def init_tk():
	# ============================ Tkinter setup stuff ================================

	global BV






	# setup window

	BV = BVmain.BV_Instance(WINDOW_SIZE=(WINDOW_WIDTH, WINDOW_HEIGHT), PYG_SIZE=(width, height))


	os.environ['SDL_WINDOWID'] = str(BV.embed.winfo_id())

	if platform.system() == "Windows":					# system()???
		os.environ['SDL_VIDEODRIVER'] = 'windib'

	BV.setup_window()



	# =================================================================================








def init_pygame():
	# ============================ Pygame setup stuff =================================
	global GL_CANVAS
	global screen
	global font

	pygame.init()

	pg_flags = DOUBLEBUF | OPENGL

	GL_CANVAS = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pg_flags)

	Assets.create_pygame_images()
	TrackHelper.set_render_quality(zone_scl=ZONE_SCL, flow_scl=FLOW_SCL)
	
	# these will get automatically called by set_render_quality since the scales for both will be changed
	#TrackHelper.gen_arrow_images()
	#TrackHelper.gen_cp_tiles()


	screen = KS.Screen((WINDOW_WIDTH, WINDOW_HEIGHT))

	font = None
	# =================================================================================


def init_gl():
	# ============================ OpenGL setup stuff =================================
	


	glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
	glDepthRange(0, 1)
	glMatrixMode(GL_PROJECTION)
	#gluPerspective(0, (WINDOW_WIDTH/WINDOW_HEIGHT), 0.1, 50.0)
	#view_mat = IndentityMat44()
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glShadeModel(GL_SMOOTH)
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glClearDepth(1.0)
	glDisable(GL_DEPTH_TEST)
	glDisable(GL_LIGHTING)
	glDepthFunc(GL_LEQUAL)
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)


	GEN_SHADERS()
	GENERATE_TEXTURES()
	GEN_VBO()
	GEN_FBO()






	glBindFramebuffer(GL_FRAMEBUFFER, FBO_0)

	# =================================================================================










# ==================================================================================================
#              MAIN
# ==================================================================================================

if platform.system() == "Windows":
	# set windows tray icon (if using windows of course :p)
	app_id = u'mrl314.booview.window.v20'
	ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

print("====================================================")
print("        Welcome to BooView (v" + PY_VERSION_NUMBER + ") by MrL314!        ")
print("====================================================")




WINDOW_SCALE = 1

FRAMES = 0

data = b''

BV = None

CONN_LUA_V = ""
CONN_NAME = ""

print("\n# Please connect socket via BizHawk's Lua Console. #\n")

while True:

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		
		conn, addr = s.accept()

		SOCKET_CONN = conn

		BYTES_AS_LIST = []


		with conn:

			_TIME = time.perf_counter()

			try:





				# =================================
				#    INIT
				# =================================

				#send_frame_signal()	# call "frame" once to set up

				# check if lua socket properly connected
				try: 
					wait_for_sync(initial_sync=True)
				except Exception as e:
					print("[INFO] Connection failed. This occasionally happens when\n       starting up for the first time. Try reconnecting!")

					try: CLOSE_CONN()
					except ConnectionResetError: pass
					except OSError: pass

					continue


				#_ = RECV_DATA() # dummy!



				BAD_LUA_CONN = False

				try: 
					CONN_LUA_V = match_lua_id(lua_version=LUA_VERSION_NUMBER) # tell Lua that it is connected to the python script (better safe than sorry)
				except ZeroDivisionError:
					BAD_LUA_CONN = True
				except Exception as e:
					raise e

				if BAD_LUA_CONN:
					print("[ERROR] Could not verify identity of connected socket.\n        Please ensure you are using version " + LUA_VERSION_NUMBER + " of the LuaSide.lua script\n")
					try: CLOSE_CONN()
					except ConnectionResetError: pass
					except OSError: pass

					break

				CONN_NAME = str(addr[0]) + " (" + str(CONN_LUA_V) + ")"

				print('[INFO] ID: ID_BVPY_' + str(PY_VERSION_NUMBER))
				print('[INFO] Connected to', CONN_NAME)

				send_frame_signal()	# call "frame" once to set up
				wait_for_sync()


				send_yield_signal()


				init_tk()
				init_pygame()
				init_gl()

				send_unyield_signal()
				

				map_ready = False
				map_changed = False
				map_loading = False
				
				prev_gamemode = 0x02
				prev_track_number = 0xff

				ghost_mode_byte = -2
				demo_byte = -2

				done = False

				

				# =================================






				# main loop

				while done == False:

					












					# =======================================    Button Display    ========================================

					
					for i in range(8):
						if BV.racers_to_follow["racer" + str(i)]:
							if not is_active_racer(i):
								BV.toggle_follow(i)


					if BV.TRAILS_TOGGLED:
						for i in range(8): OBJECTS[i].show_trails = BV.TRAIL_LINES  # maybe change later?

						BV.TRAILS_TOGGLED = False

					

					


					

					






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

					SPRITE_SCALE = BV.get_sprite_scale()

					

					#T = time.perf_counter()

					for event in pygame.event.get():
						if event.type == QUIT: 
							done = True
							BV.root.destroy()
							BV.root = None

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








					#T_0 = time.perf_counter() - T

					#print(100 * T_0 * 60)

					
					# ======================================================================================================

					





					try:
						
						CH_BYTES.set_bytes([])
						OBJ_BYTES.set_bytes([])
						ITEM_BYTES.set_bytes([])

						SOCKET_CONN.settimeout(1/120)
						try:
							data = RECV_DATA(block=False)
						except socket.timeout:
							data = "SOCKET_TIMEOUT"
							BYTES_AS_LIST = []
						SOCKET_CONN.settimeout(None)


						


								
						if not data:
							CLOSE_CONN()
							break


						

						if data == "close" or data == "close\n":
							break

						elif data[:7] == 'CH_DATA':

							data = data[7:]
							

							raw_bytes = data.split("\n")

							
							CH_BYTES.set_bytes(bytes.fromhex(raw_bytes[0]))

							OBJ_BYTES.set_bytes(bytes.fromhex(raw_bytes[1]))

							ITEM_BYTES.set_bytes(bytes.fromhex(raw_bytes[2]))

							# map update bytes
							MAP_UPDATE_BYTES = bytes.fromhex(raw_bytes[3])
							
							raw_bytes = raw_bytes[4:]

						elif data == "SOCKET_TIMEOUT":
							#print("[INFO] TIMEOUT")
							do_frame_update()
						else:
							pass





						if BV.in_file_dialogue:

							send_yield_signal()

							file_path = tk.filedialog.askopenfilename(filetypes=[("SRAM files", ".srm .sram")])

							_unpaused = True

							send_unyield_signal()
							

							if file_path != "": 
								
								SRM_DATA = []
								with open(file_path, "rb") as SRM_FILE:
									SRM_DATA = SRM_FILE.read()

								srm_send = ""
								for d in SRM_DATA:
									srm_send += " " + str(d)

								send_w_sram_signal(srm_send)

								print("[INFO] Uploaded data from ", file_path)


							BV.set_not_in_file_dialogue()

							do_frame_update()
							

							continue

							
						

						


						BYTES_AS_LIST = CH_BYTES.get_bytes()

						if BYTES_AS_LIST != []:
							
							
							ch_bytes = byte_buffer(BYTES_AS_LIST)
							obj_bytes = byte_buffer(OBJ_BYTES.get_bytes())
							item_bytes = byte_buffer(ITEM_BYTES.get_bytes())

							


							gamemode = next_byte(ch_bytes)

							C_MODE = next_byte(ch_bytes)

							p_ghost_mode_byte = ghost_mode_byte
							ghost_mode_byte = next_byte(ch_bytes)

							ghost_mode_2 = next_byte(ch_bytes)

							p_demo_byte = demo_byte
							demo_byte = next_byte(ch_bytes)


							if ghost_mode_byte == 0x02 and demo_byte == 0:
								if not (p_ghost_mode_byte == 0x02 and p_demo_byte == 0):
									BV.REPLAY_BUTTON.config(state="normal")

									if BV.REPLAY_MODE:
										BV.SHOW_GHOST = True
										BV.TRAIL_LINES = True
										SPRITE_SCALE = 2
										BV.set_tkvar('SPRITE_SCALE', "2")
										BV.SPRITE_SIZE_WIDGET.config(state='disabled')

										if C_MODE == 2:
											OBJECTS[0].show_trails = True
										elif C_MODE == 4:
											OBJECTS[1].show_trails = True

									else:
										pass

									BV.SHOW_GHOST = True
							else:
								if (p_ghost_mode_byte == 0x02 and p_demo_byte == 0):
									BV.SPRITE_SIZE_WIDGET.config(state='readonly')

									BV.SHOW_GHOST = False
									BV.REPLAY_MODE = False
									BV.REPLAY_BUTTON.config(relief=RAISED)
									BV.REPLAY_BUTTON.config(state="disabled")
									
							BV.SHOW_GHOST = ghost_mode_2

								





							# do not try to update stuff if not in a right gamemode
							if not (gamemode == 0x02 or gamemode == 0x0e):
								if prev_gamemode == 0x02 or prev_gamemode == 0x0e:
									for i in range(8):

										#BV.racers_to_follow["racer" + str(i)] = False
										#BV.P_FOLLOW[i] = -1

										BV.FOLLOW_BUTTONS[i].config(bg="#f0f0f0")
										BV.FOLLOW_BUTTONS[i].config(image=Assets.EMPTY_TK)
										BV.FOLLOW_BUTTONS[i].config(state="disabled")
										

									BV.REPLAY_BUTTON.config(state="disabled")
									BV.REPLAY_MODE = False
									BV.SHOW_GHOST = False

								
								do_frame_update()
								


								for m_button in CURR_FRAME_MOUSE:
									PREV_FRAME_MOUSE[m_button] = CURR_FRAME_MOUSE[m_button]

								for k_button in CURR_FRAME_KEYS:
									PREV_FRAME_KEYS[k_button] = CURR_FRAME_KEYS[k_button]

								## set up prev values
								prev_gamemode = gamemode
								prev_track_number = -1

								continue


							# In correct gamemode to display

							gametype = next_byte(ch_bytes)



							###### Control what map should be displayed 
							display_overlay = True
							


							current_track_number = next_byte(ch_bytes)

							current_theme_number = next_byte(ch_bytes)
							current_theme_object = next_byte(ch_bytes)



							if current_track_number != prev_track_number:

								send_reset_map_signal()

								
								RECV_DATA() # nonce

								send_yield_signal()

								map_loading = True

								setup_map_socket()


								for i in range(8):
									OBJECTS[i].reset_trail()

									#BV.racers_to_follow["racer" + str(i)] = False
									BV.P_FOLLOW[i] = -1
									#print("CLEARING BV.P_FOLLOW[" + str(i) + "] from track change")
									
									BV.FOLLOW_BUTTONS[i].config(bg="#f0f0f0")
									BV.FOLLOW_BUTTONS[i].config(image=Assets.EMPTY_TK)
									BV.FOLLOW_BUTTONS[i].config(state="disabled")

									map_changed = True

							else:

								
								

								byte_list = MAP_UPDATE_BYTES

								map_updates = []

								while len(byte_list) >= 3:

									offs = byte_list[0] + (byte_list[1] * 256)
									val = byte_list[2]

									map_updates.append((offs, val))

									byte_list = byte_list[3:]

								update_map_data(map_updates)
									
									






							
							




							
							
							if map_ready:

								FRAMES += 1

								
							


								###########################################################

								if map_changed:
									update_tilemap()
									update_zone_flow()
									map_changed = False

								if map_loading:
									map_loading = False
									send_unyield_signal()


								# render map
								renderTexture(TILEMAP_TEX, pos=(screen.x+screen.w/2, screen.y+screen.h/2), dim=(screen.w, screen.h), centered=True)


								if BV.show_zones: renderTexture(ZONEMAP_TEX, pos=(screen.x+screen.w/2, screen.y+screen.h/2), dim=(screen.w, screen.h), centered=True)

								if BV.show_flows: renderTexture(FLOWMAP_TEX, pos=(screen.x+screen.w/2, screen.y+screen.h/2), dim=(screen.w, screen.h), centered=True)
								
								
								###########################################################


								

						

								camera_angle = map_value(next_byte(ch_bytes), "degrees") + 90

								camx = next_word(ch_bytes) + 0x80
								camy = next_word(ch_bytes) + 0x66

								CAM_POS = (camx, camy)

								
								
								## DISPLAY OVERLAY DATA OVER TRACK
								if display_overlay:

									

									# Racer object data setting
									for i in range(8):


										########### PARSE RECIEVED DATA PER CHARACTER ##############

										OBJECTS[i].ch_num = next_byte(ch_bytes)

										X_coord = map_value(next_double(ch_bytes), "width")
										Y_coord = map_value(next_double(ch_bytes), "height")


										if is_active_racer(i):

											if OBJECTS[i].ch_num != BV.P_FOLLOW[i]:
												pfi = BV.P_FOLLOW[i]
												#print("SETTING UP FOLLOW BUTTON", i, "with character number", OBJECTS[i].ch_num, "BV.P_FOLLOW =", BV.P_FOLLOW[i], "BV.SHOW_GHOST =", BV.SHOW_GHOST)
												BV.P_FOLLOW[i] = OBJECTS[i].ch_num
												BV.FOLLOW_BUTTONS[i].config(image=Assets.CHARACTERS_TK[Objects.CHAR_NUM_TO_NAME(OBJECTS[i].ch_num)])
												BV.FOLLOW_BUTTONS[i].config(state="normal")

												if BV.racers_to_follow["racer" + str(i)] and pfi == -1:
													BV.FOLLOW_BUTTONS[i].config(bg="#c8c8c8")
											

										else:
											X_coord = -1000
											Y_coord = -1000
											#OBJECTS[i].reset_trail()
											OBJECTS[i].show_trails = False

											BV.racers_to_follow["racer" + str(i)] = False

											if BV.P_FOLLOW[i] != -1:
												BV.P_FOLLOW[i] = -1
												#print("DISABLING FOLLOW BUTTON", i)
												BV.FOLLOW_BUTTONS[i].config(bg="#f0f0f0")
												BV.FOLLOW_BUTTONS[i].config(image=Assets.EMPTY_TK)
												BV.FOLLOW_BUTTONS[i].config(state="disabled")


										

										OBJECTS[i].x = X_coord
										OBJECTS[i].y = Y_coord
										OBJECTS[i].z = next_double(ch_bytes)*256 # TO-DO MAYBE REMOVE THIS 256?

										OBJECTS[i].vel = (map_value(next_word_signed(ch_bytes)/4, "width"), 
											              map_value(next_word_signed(ch_bytes)/4, "height"),
											              map_value(next_word_signed(ch_bytes)/4, "height"))

										OBJECTS[i].speed = map_value(next_word_signed(ch_bytes)/4, "width")

										OBJECTS[i].max_speed = map_value(next_word_signed(ch_bytes)/4, "width")

										OBJECTS[i].accel = map_value(next_word_signed(ch_bytes)/4, "width")


										OBJECTS[i].angle = map_value(next_word(ch_bytes)/256, "degrees")

										OBJECTS[i].v_angle = map_value(next_word(ch_bytes)/256, "degrees")

										OBJECTS[i].c_angle = map_value(next_word(ch_bytes)/256, "degrees")

										OBJECTS[i].angle_vel = map_value(next_word(ch_bytes)/256, "degrees")

										OBJECTS[i].dest = (map_value(next_word(ch_bytes), "width"),
											               map_value(next_word(ch_bytes), "height"))

										

									#print("Racer Data Time:", 100 * (time.perf_counter() - T) * 60)

									#T = time.perf_counter()

									#Obstacle object data
									for i in range(8):

										#obj_addr = next_word(obj_bytes)
										OBJECTS[num_racers + i].address = next_word(obj_bytes)

										OBJECTS[num_racers + i].x = map_value(next_double(obj_bytes), "width")
										OBJECTS[num_racers + i].y = map_value(next_double(obj_bytes), "height")
										OBJECTS[num_racers + i].z = next_byte(obj_bytes)/256 + next_word(obj_bytes) # TO-DO MAYBE REMOVE THIS 256?
										next_byte(obj_bytes) # waste because there's a bug with MONTY?????????

										#if OBJECTS[num_racers + i].z > 0x1000: print(hex(int(OBJECTS[num_racers + i].z * 256)))


										if gametype != 6:
											#OBJECTS[num_racers + i].ch_num = (current_track_number * 4) + (ANIM_TIMER // ANIM_TIMER_SWAP) # dummy
											#print(((current_theme_object//2) * 4))
											OBJECTS[num_racers + i].ch_num = ((current_theme_object//2) * 4) + (ANIM_TIMER // ANIM_TIMER_SWAP) # dummy

										else:
											#OBJECTS[num_racers + i].ch_num = (current_track_number * 4) + (i // 3)
											OBJECTS[num_racers + i].ch_num = 28 + (i // 3)


											#print("Object", i, ": ", format(obj_addr, "04x"))

									#print("Obstacle Data Time:", 100 * (time.perf_counter() - T) * 60)

									#T = time.perf_counter()

									
									# Item object data
									for i in range(8):

										if (gametype == 0 and i < 2) or (gametype == 2) or (gametype == 6 and i < 6):

											########### PARSE RECIEVED DATA PER ITEM ##############

											OBJECTS[num_racers + num_obstacles + i].address = next_word(item_bytes)

											alive = next_byte(item_bytes)

											if alive < 0x80:
												OBJECTS[num_racers + num_obstacles + i].is_alive = False
											else:
												OBJECTS[num_racers + num_obstacles + i].is_alive = True

											ch_num_1 = next_byte(item_bytes)
											ch_num_2 = next_byte(item_bytes)
											
											OBJECTS[num_racers + num_obstacles + i].ch_num = (ch_num_2 * 8) + ch_num_1

											

											
											OBJECTS[num_racers + num_obstacles + i].x = map_value(next_double(item_bytes), "width")
											OBJECTS[num_racers + num_obstacles + i].y = map_value(next_double(item_bytes), "height")
											OBJECTS[num_racers + num_obstacles + i].z = next_double(item_bytes)*256 # TO-DO MAYBE REMOVE THIS 256?
									
									

									#print("Item Data Time:", 100 * (time.perf_counter() - T) * 60)
									#UPDATING
									#T1 = time.perf_counter() - T0

									#print("TOTAL OBJECT TIME:", 100 * T1 * 60)


									#==============================================================================================================
									#
									#    MAIN UPDATING ROUTINE
									#
									#==============================================================================================================

									
									


									if True:
										m_x, m_y = pygame.mouse.get_pos()
										mouse = (m_x, m_y)
										m_x = disp2map_X(m_x)
										m_y = disp2map_Y(m_y)
										

										mouse_rel = pygame.mouse.get_rel()

										







									if MOUSE_NEW["right"]:
										
										for i in range(len(OBJECTS)):

											OBJ = OBJECTS[i]

											O_x = OBJ.x
											O_y = OBJ.y

											

											if abs(O_x - m_x) < 5 * SPRITE_SCALE:
												if abs(O_y - m_y) < 5 * SPRITE_SCALE:
													grabbed = i
													m_off = (O_x - m_x, O_y - m_y)
													break




								
									if CURR_FRAME_MOUSE["right"]:
										
										if grabbed != -1:
											

											X_COORD = int((m_x + m_off[0]))
											Y_COORD = int((m_y + m_off[1] + 4))

										

											OBJECTS[grabbed].x = X_COORD
											OBJECTS[grabbed].y = Y_COORD

											ADDR = OBJECTS[grabbed].address

										
											if F == 1:
												F = 0
												
												
												
												part1 = "W_BYTES addr" + " " + str(ADDR + 0x18) + " " + "bytes" + " " + str(X_COORD & 0xff) + " " + str((X_COORD>>8 & 0xff)) + " 00 00 " + str(Y_COORD & 0xff) + " " + str((Y_COORD>>8 & 0xff)) + " 00 00 05 " + "\n"
												
												send_raw_signal(part1)

											F += 1

									else:
										if grabbed != -1:
											ADDR = OBJECTS[grabbed].address
											ground_instr = "W_BYTES addr" + " " + str(ADDR + 0x1e) + " " + "bytes" + " " + "00 00 00 00" + "\n"

											send_raw_signal(ground_instr)

										grabbed = -1
												







									














									


									if BV.REPLAY_MODE and gametype == 4 and demo_byte == 0:

										
										send_ghost_signal()

										if C_MODE == 2:
											# top screen
											p_f = BV.racers_to_follow["racer0"]
											BV.racers_to_follow["racer0"] = True
											if p_f == False: BV.FOLLOW_BUTTONS[0].config(bg="#c8c8c8")

										elif C_MODE == 4:
											# bottom screen
											p_f = BV.racers_to_follow["racer1"]
											BV.racers_to_follow["racer1"] = True
											if p_f == False: BV.FOLLOW_BUTTONS[1].config(bg="#c8c8c8")

									else:
										if BV.GHOST_TURN_OFF:
											send_ghost_off_signal()
											BV.GHOST_TURN_OFF = False



									FOLLOWING = []

									for racer in BV.racers_to_follow:
										if BV.racers_to_follow[racer] == True:
											FOLLOWING.append(int(racer[-1])) # cheap but dirty way to add the racer number in
									




									


									

																
									if CURR_FRAME_MOUSE["scroll_up"]:
										screen.zoom(mouse, screen.SCALE * 1.1)
									elif CURR_FRAME_MOUSE["scroll_down"]:
										screen.zoom(mouse, screen.SCALE * 0.9)
									

									
								


									
									if CURR_FRAME_MOUSE["left"]:
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


										screen.center_x = CENTER_X * screen.DEFAULT_WIDTH/MAP_W
										screen.center_y = CENTER_Y * screen.DEFAULT_HEIGHT/MAP_H







									
									


									#==============================================================================================================


									#DISPLAY


									if BV.TRAIL_LINES == False:
										NUM_TRAILS = 0
									elif gametype == 4:
										NUM_TRAILS = MAX_TRAILS_CONFIG
									else:
										NUM_TRAILS = MAX_TRAILS_CONFIG/16


									if FRAME_NUMBER > FRAME_SKIP:

										#T0 = time.perf_counter()

										#print(screen.SCALE, screen.w, screen.DEFAULT_WIDTH)
										
										FRAME_NUMBER = 0

										#CANVAS.blit(BG, (0, 0))
										
										####CANVAS.blit(screen.canvas, (0, 0))   #--- come back to this later!

										#T0 = time.perf_counter()
										# trails
										#l_width = screen.w / MAP_W

										if BV.TRAIL_LINES:
											SHOW_TRAIL_LINES()

											#T1 = time.perf_counter() - T0

											#print("Line Time:", 100 * T1 * 60)
										


										#glFinish()
										#glFlush()

										#glColor3f(1.0, 1.0, 1.0)

										#T0 = time.perf_counter()

										TRAIL_AMT = NUM_TRAILS
										if BV.REPLAY_MODE: TRAIL_AMT = TRAIL_AMT // 2

										# racers
										for i in range(7, -1, -1):
											OBJ = OBJECTS[i]
											if (gametype == 0) or (gametype == 2 and i < 2) or (gametype == 4 and i < 2) or (gametype == 6 and i < 2):
												#print(i)
												OBJ.scl = math.floor(screen.SCALE * screen.DEFAULT_WIDTH/MAP_W * width//128 * SQRT_2 * SPRITE_SCALE / 1)
												OBJ.disp_x = map2disp_X(OBJ.x)
												OBJ.disp_y = map2disp_Y(OBJ.y)
												if BV.REPLAY_MODE and i == 1 and gametype == 4:
													#OBJ.display(screen, trails=False)
													pass
												else:
													if (gametype == 4 and i == 1):
														GHOST_FLASH_TIMER += 1
														if GHOST_FLASH_TIMER == 2:
															GHOST_FLASH_TIMER = 0

														t = TRAIL_AMT
														if BV.REPLAY_MODE: t = 0

														if GHOST_FLASH_TIMER % 2 == 0:
															OBJ.display(d_method=renderObject)
															OBJ.update_trails(trails=t, log_freq=TRAIL_FREQ_CONFIG)
															#pass
														else:
															OBJ.display(ghost=True, d_method=renderObject)
															OBJ.update_trails(trails=t, log_freq=TRAIL_FREQ_CONFIG)
														
													else:
														OBJ.display(d_method=renderObject)
														OBJ.update_trails(trails=TRAIL_AMT, log_freq=TRAIL_FREQ_CONFIG)

										# obstacles
										for i in range(7, -1, -1):
											j = num_racers + i
											OBJ = OBJECTS[j]
											OBJ.scl = max(0, math.floor(screen.SCALE * screen.DEFAULT_WIDTH/MAP_W * width//128 * SPRITE_SCALE / 1))
											OBJ.disp_x = map2disp_X(OBJ.x)
											OBJ.disp_y = map2disp_Y(OBJ.y)
											OBJ.display(d_method=renderObject)

										#items
										for i in range(7, -1, -1):
											j = num_racers + num_obstacles + i
											OBJ = OBJECTS[j]
											if (gametype == 0 and i < 2) or (gametype == 2) or (gametype == 6 and i < 6):
												if OBJ.is_alive:
													OBJ.scl = math.floor(screen.SCALE * screen.DEFAULT_WIDTH/MAP_W * width//256 * SPRITE_SCALE / 1)
													OBJ.disp_x = map2disp_X(OBJ.x)
													OBJ.disp_y = map2disp_Y(OBJ.y)
													OBJ.display(d_method=renderObject)






										if BV.REPLAY_MODE:
											if not BV.P_REPLAY_MODE:
												if C_MODE == 2:
													OBJECTS[0].show_trails = True
													OBJECTS[0].copy_trail(OBJECTS[1])
												elif C_MODE == 4:
													OBJECTS[1].show_trails = True
													OBJECTS[1].copy_trail(OBJECTS[0])
										else:
											if BV.P_REPLAY_MODE:
												if C_MODE == 2:
													OBJECTS[1].copy_trail(OBJECTS[0])
												elif C_MODE == 4:
													OBJECTS[0].copy_trail(OBJECTS[1])

										BV.P_REPLAY_MODE = BV.REPLAY_MODE



										#############################################################
										#  Direction lines for racers
										#############################################################

										if True:	# later change to "if SHOW_<dir data>:"
											SHOW_EXTRA_VECTORS()
										





										'''

										if SHOW_DEBUG:

											DEBUG_LIST = [
												"BV.REPLAY_MODE: " + str(BV.REPLAY_MODE),
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



									#glPopMatrix()
								



							else:
								#print("[INFO] MAP NOT YET READY")
								pass
							
							


							do_frame_update()
							
							

							




							# SET UP "PREV" VALUES

							for m_button in CURR_FRAME_MOUSE:
								PREV_FRAME_MOUSE[m_button] = CURR_FRAME_MOUSE[m_button]

							for k_button in CURR_FRAME_KEYS:
								PREV_FRAME_KEYS[k_button] = CURR_FRAME_KEYS[k_button]



							## set up prev values
							prev_gamemode = gamemode
							prev_track_number = current_track_number
					except ZeroDivisionError:

						do_frame_update()
						
					except Exception as e:
						#traceback.print_exc()
						#print(e)

						#print(BYTES_AS_LIST)
						#conn.send(b"close\n")
						#conn.close()
						CLOSE_CONN()
						raise
						

					

			except TclError as e:
				#traceback.print_exc()
				#print(e)
				pass
			except Exception as e:
				traceback.print_exc()
				print(e)

				

			pygame.quit()

			if BV.root != None:
				try:
					BV.root.destroy()
					BV.root = None
				except Exception:
					pass

			print("[INFO] Disconnected from", CONN_NAME, end="")
			printed_reason = False

			if data == "close" or data == "close\n":
				if len(data) > 6:
					print("\n       Reason: ", data[6:])
					printed_reason = True


			if not printed_reason: print("\n       Reason: Server Script Forcibly Stopped")



			try: CLOSE_CONN()
			except ConnectionResetError: pass
			except OSError: pass

	break


	
		