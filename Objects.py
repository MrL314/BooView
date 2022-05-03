
import pygame
from pygame.gfxdraw import *
from pygame.locals import *

from collections import deque

import math


import Assets





global CHARACTER_NAMES

SQRT_2 = 2 ** 0.5


CHARACTER_NAMES = ("mario", "luigi", "bowser", "peach", "dk", "koopa", "toad", "yoshi")

def CHAR_NUM_TO_NAME(n):
	if n < 0x10:
		if n%2==0:
			return CHARACTER_NAMES[n//2]
		else:
			raise IndexError("Invalid Character Number: " + str(n))
	else:
		# fix up later to include the items
		return "arrow"


#ITEM_NAMES = ("banana", "gshell", "rshell", "killer", "ai1", "ai2", "banana2", "gshell2")
#ITEM_NAMES = ("mario_arrow", "luigi_arrow", "bowser_arrow", "peach_arrow", "dk_jr_arrow", "koopa_arrow", "toad_arrow", "yoshi_arrow") # ONLY FOR TESTING
ITEM_NAMES = ("banana", "g_shell", "r_shell", "killer", "p_mush", "p_mush", "banana", "g_shell",
	"banana", "g_shell", "r_shell", "killer", "p_mush", "p_mush", "banana", "g_shell",
	"banana", "g_shell", "r_shell", "killer", "fireball", "fireball", "banana", "g_shell",
	"banana", "g_shell", "r_shell", "killer", "p_mush", "p_mush", "banana", "g_shell",
	"banana", "g_shell", "r_shell", "killer", "banana", "banana", "banana", "g_shell",
	"banana", "g_shell", "r_shell", "killer", "g_shell", "g_shell", "banana", "g_shell",
	"banana", "g_shell", "r_shell", "killer", "p_mush", "p_mush", "banana", "g_shell",
	"banana", "g_shell", "r_shell", "killer", "egg", "egg", "banana", "g_shell"
	) # ONLY FOR TESTING



def ITEM_NUM_TO_NAME(n):
	try:
		name = ITEM_NAMES[n//2]
		return name
	except:
		raise IndexError("Invalid Character Number: " + str(n))
	


'''
OBSTACLE_NAMES = ("pipe_g", "pipe_g", "pipe_g", "pipe_g", 
	"pole", "pole", "pole", "pole", 
	"mole", "mole", "mole", "mole", 
	"thwomp", "thwomp", "thwomp", "thwomp", 
	"pipe_g", "pipe_g", "pipe_g", "pipe_g", 
	"thwomp_2_A", "thwomp_2_B", "thwomp_2_A", "thwomp_2_B",
	"cheep", "cheep", "cheep", "cheep", 
	"pipe_g", "pipe_g", "pipe_g", "pipe_g", 
	"pole", "pole", "pole", "pole", 
	"thwomp", "thwomp", "thwomp", "thwomp", 
	"plant_A", "plant_A", "plant_B", "plant_B", 
	"mole", "mole", "mole", "mole", 
	"pipe_g", "pipe_g", "pipe_g", "pipe_g", 
	"cheep", "cheep", "cheep", "cheep", 
	"pipe_g", "pipe_g", "pipe_g", "pipe_g", 
	"pipe_g", "pipe_g", "pipe_g", "pipe_g", 
	"pole", "pole", "pole", "pole", 
	"thwomp", "thwomp", "thwomp", "thwomp", 
	"plant_A", "plant_A", "plant_B", "plant_B", 
	"pipe_o", "pipe_o", "pipe_o", "pipe_o", 
	"balloon_b", "balloon_r", "balloon_b", "balloon_r", 
	"balloon_b", "balloon_r", "balloon_b", "balloon_r",
	"balloon_b", "balloon_r", "balloon_b", "balloon_r",
	"balloon_b", "balloon_r", "balloon_b", "balloon_r",)
'''

OBSTACLE_NAMES = ("pole", "pole", "pole", "pole", 
	"pipe_g", "pipe_g", "pipe_g", "pipe_g", 
	"mole", "mole", "mole", "mole", 
	"plant_A", "plant_A", "plant_B", "plant_B", 
	"pipe_g", "pipe_g", "pipe_g", "pipe_g", #VL pipes
	"cheep", "cheep", "cheep", "cheep", 
	"thwomp", "thwomp", "thwomp", "thwomp", 
	"balloon_b", "balloon_r", "balloon_b", "balloon_r",)




def OBSTACLE_NUM_TO_NAME(n):
	try:
		o = OBSTACLE_NAMES[n]
		#print(o)
		return o
	except:
		return "pipe_g"


#=========================================================================================================================
#
#         Base Object Class
#
#=========================================================================================================================


class Game_Object(object):

	def __init__(self, x=-100, y=-100, angle=0, img="", surface=None, OBJ_ID="", img_scale=1, address=0):
		self.x = x
		self.y = y
		self.z = 0
		#self.disp_x = x
		#self.disp_y = y
		self.angle = angle
		self.img = img
		self.surface = surface
		self.scl = img_scale
		self.ID = OBJ_ID
		self.address = address
		self.win_scl = 1
		#self.tex = img

	@property
	def x(self):
		return self._x
	@x.setter
	def x(self, _x):
		self._x = _x
	
	@property
	def y(self):
		return self._y
	@y.setter
	def y(self, _y):
		self._y = _y

	@property
	def z(self):
		return self._z
	@z.setter
	def z(self, _z):
		self._z = _z

	@property
	def disp_x(self):
		return self._disp_x
	@disp_x.setter
	def disp_x(self, _disp_x):
		self._disp_x = _disp_x
	
	@property
	def disp_y(self):
		return self._disp_y
	@disp_y.setter
	def disp_y(self, _disp_y):
		self._disp_y = _disp_y

	@property
	def OBJ_ID(self):
		return self._OBJ_ID
	@OBJ_ID.setter
	def OBJ_ID(self, _OBJ_ID):
		self._OBJ_ID = _OBJ_ID


	@property
	def img(self):
		return self._img
	@img.setter
	def img(self, _img):
		_t = _img

		obj_name = ""
		if type(_img) == type(""):
			obj_name = _img
		else:
			pass

		if obj_name != "":
			_img = Assets.GET_IMAGE(obj_name)
		
		self._img = _img

		self.tex = _t



	@property
	def tex(self):
		return self._tex
	@tex.setter
	def tex(self, _tex):
		obj_name = ""
		if type(_tex) == type(""):
			obj_name = _tex
		else:
			pass

		if obj_name != "":
			_tex = Assets.GET_TEXTURE(obj_name)

		#print("Setting tex to", _tex)
		
		self._tex = _tex

	@property
	def scl(self):
		return self._scl
	@scl.setter
	def scl(self, _scl):
		self._scl = _scl


	@property
	def win_scl(self):
		return self._win_scl
	@win_scl.setter
	def win_scl(self, _win_scl):
		self._win_scl = _win_scl


	@property
	def angle(self):
		return self._angle
	@angle.setter
	def angle(self, _angle):
		self._angle = _angle


	@property
	def surface(self):
		return self._surface
	@surface.setter
	def surface(self, _surface):
		self._surface = _surface


	@property
	def address(self):
		return self._address
	@address.setter
	def address(self, _address):
		self._address = _address
	


	

	def display_on(self, surface=None):
		main_surface = self.surface

		if surface == None:
			surface = self.surface

		self.surface = surface
		self.display()
		self.surface = main_surface


	def display(self, d_method=None):
		
		z_scl = self.z
		if z_scl > 0x8000:
			z_scl -= 0x10000
		z_scl /= 0x2000
		z_scl += 1

		#if z_scl > 10: print(self.z)
		if d_method == None:
			"""

			#IMG = pygame.transform.smoothscale(self.img, (self.scl, self.scl))
			#IMG = pygame.transform.scale(self.img, (math.floor(self.scl * z_scl / self.win_scl), math.floor(self.scl * z_scl / self.win_scl)))
			IMG = pygame.transform.scale(self.img, (math.floor(self.scl * z_scl), math.floor(self.scl * z_scl)))
			#IMG = pygame.transform.smoothscale(self.img, (self.img.get_width()*self.scl, self.img.get_height()*self.scl))
			#IMG = pygame.transform.scale(self.img, (self.img.get_width()*self.scl, self.img.get_height()*self.scl))
			IMG = Assets.rot_image(IMG, self.angle)
			
			'''
			self.surface.blit(IMG, (
				math.floor( (self.disp_x-(IMG.get_width()  ))//self.win_scl), 
				math.floor( (self.disp_y-(IMG.get_height() ))//self.win_scl)
			))
			'''
			self.surface.blit(IMG, (
				math.floor( ((self.disp_x)-(IMG.get_width() / 2 ))), 
				math.floor( ((self.disp_y)-(IMG.get_height()/ 2 )))
			))
			"""

		else:

			d_method(
				self.tex, 
				pos=(
					self.disp_x, 
					self.disp_y
				), 
				dim=(
					self.scl * z_scl, 
					self.scl * z_scl
				), 
				rot=(
					0, 
					0, 
					self.angle
				),
				centered=True
			)







#=========================================================================================================================
#
#         RACER CLASS
#
#=========================================================================================================================


class Racer(Game_Object):

	def __init__(self, x=-100, y=-100, angle=0, obj_name="", surface=None, OBJ_ID="", display_dest=False, img_scale=1, address=0):
		super().__init__(x, y, angle, obj_name, surface, OBJ_ID, img_scale=img_scale, address=address)

		self.vel = (0, 0, 0)
		self.speed = 0
		self.max_speed = 0
		self.accel = 0
		self.v_angle = 0
		self.c_angle = 0
		self.angle_vel = 0
		self.dest = (x, y)
		self.display_dest = display_dest
		self.ch_num = -1
		self.buttons = 0

		'''
		self.prev_positions = deque()
		self.p_pos_counter = deque()
		self.trail_cbuff_len = 0
		self.trail_disp_len = 0
		self.avg_speed = 0
		'''

		self.reset_trail()

		self.log = 0

		self.max_trails = 0
		self._show_trails = self.show_trails = False

	@property
	def vel(self):
		return self._vel
	@vel.setter
	def vel(self, _vel):
		self._vel = _vel


	@property
	def speed(self):
		return self._speed
	@speed.setter
	def speed(self, _speed):
		self._speed = _speed

	@property
	def max_speed(self):
		return self._max_speed
	@max_speed.setter
	def max_speed(self, _max_speed):
		self._max_speed = _max_speed


	@property
	def accel(self):
		return self._accel
	@accel.setter
	def accel(self, _accel):
		self._accel = _accel


	@property
	def v_angle(self):
		return self._v_angle
	@v_angle.setter
	def v_angle(self, _v_angle):
		self._v_angle = _v_angle


	@property
	def c_angle(self):
		return self._c_angle
	@c_angle.setter
	def c_angle(self, _c_angle):
		self._c_angle = _c_angle


	@property
	def angle_vel(self):
		return self._angle_vel
	@angle_vel.setter
	def angle_vel(self, _angle_vel):
		self._angle_vel = _angle_vel


	@property
	def ch_num(self):
		return self._ch_num
	@ch_num.setter
	def ch_num(self, _ch_num):
		try:
			self.ch_num
		except:
			self._ch_num = -1

		if self.ch_num != _ch_num:
			self.img = CHAR_NUM_TO_NAME(_ch_num)

		self._ch_num = _ch_num

	


	@property
	def dest(self):
		return self._dest
	@dest.setter
	def dest(self, _dest):
		self._dest = _dest


	@property
	def buttons(self):
		return self._buttons
	@buttons.setter
	def buttons(self, _buttons):
		self._buttons = _buttons


	@property
	def max_trails(self):
		return self._max_trails
	@max_trails.setter
	def max_trails(self, _max_trails):
		self._max_trails = _max_trails

	@property
	def show_trails(self):
		return self._show_trails
	@show_trails.setter
	def show_trails(self, _show_trails):
		if _show_trails != self._show_trails: self.reset_trail()

		self._show_trails = _show_trails

	
	
	

	def reset_trail(self):
		self.prev_positions = deque()
		self.p_pos_counter = deque()
		self.trail_cbuff_len = 0
		self.trail_len = 0
		self.avg_speed = 0

		self.prev_x = None
		self.prev_y = None
		#self.last_s = None


	def copy_trail(self, other):
		self.trail_cbuff_len = other.trail_cbuff_len + 0
		self.trail_len = other.trail_len + 0
		self.avg_speed = other.avg_speed + 0
		self.log = other.log + 0

		if other.prev_x == None:
			self.prev_x = None
		else:
			self.prev_x = other.prev_x + 0
		
		if other.prev_y == None:
			self.prev_y = None
		else:
			self.prev_y = other.prev_y + 0



		self.prev_positions = deque()
		self.p_pos_counter = deque()

		for i in range(len(other.prev_positions)):
			self.prev_positions.append(0 + other.prev_positions[i])

		for i in range(len(other.p_pos_counter)):
			self.p_pos_counter.append(0 + other.p_pos_counter[i])
		'''
		self.prev_positions = other.prev_positions
		self.p_pos_counter = other.p_pos_counter
		'''


	def display_on(self, surface=None):
		main_surface = self.surface

		if surface == None:
			surface = self.surface

		self.surface = surface
		self.display()
		self.surface = main_surface


	def map_pos(self, pos, SCREEN):
		return (pos[0]*SCREEN.SCALE + SCREEN.x, pos[1]*SCREEN.SCALE + SCREEN.y)

	def update_trails(self, trails=0, log_freq=6):
		p_show = self.show_trails

		if trails > 1: self.show_trails = True
		else: self.show_trails = False





		if self.show_trails:
			self.max_trails = trails

			self.avg_speed += self.speed


			if self.log == log_freq-1:

				
				### OLD VERSION
				######################################################################
				"""

				#if coord_fnc == None: coord_fnc = iden
				#if speed_fnc == None: speed_fnc = iden

				# add new position for trail

				next_pos = (self.x, self.y)
				next_spd = self.avg_speed/log_freq


				

				if self.trail_cbuff_len != 0:
					self.prev_positions.popleft()
					self.prev_positions.popleft()
					self.prev_positions.popleft()

				self.trail_cbuff_len += 1




				#self.prev_positions.appendleft(0)	# dummy data
				self.prev_positions.appendleft(next_spd)
				self.prev_positions.appendleft(next_pos[1])
				self.prev_positions.appendleft(next_pos[0])

				self.prev_positions.appendleft(next_spd)
				self.prev_positions.appendleft(next_pos[1])
				self.prev_positions.appendleft(next_pos[0])
				
				



				while self.trail_cbuff_len > self.max_trails: 

					self.prev_positions.pop()
					self.prev_positions.pop()
					self.prev_positions.pop()

					#self.prev_positions.pop()	# dummy


					self.trail_cbuff_len -= 1
				"""
				##############################################################################


				### NEW VERSION
				######################################################################

				# add new position for trail
				
				#next_pos = (self.x, self.y)
				new_x = self.x
				new_y = self.y
				new_s = self.avg_speed/log_freq

				new_pt = True

				if self.prev_x != None:
					if self.trail_cbuff_len != 0:
						if self.prev_x == new_x and self.prev_y == new_y:
							new_pt = False




				self.prev_x = new_x
				self.prev_y = new_y

				self.trail_len += 1



				if new_pt:

					# append number of frames this position is held
					self.p_pos_counter.append(1)

					'''
					# if there is a duplicate entry point, remove it from the queue
					if self.trail_cbuff_len > 0:
						self.prev_positions.pop()
						self.prev_positions.pop()
						self.prev_positions.pop()
					'''

					# append new point
					self.prev_positions.append(new_x)
					self.prev_positions.append(new_y)
					self.prev_positions.append(new_s)

					'''
					# append copy of new point so display looks correct (maybe change later?)
					self.prev_positions.append(new_x)
					self.prev_positions.append(new_y)
					self.prev_positions.append(new_s)
					'''

					# increment length of buffer
					self.trail_cbuff_len += 1


				else:
					# increment number of frames last position is repeated
					self.p_pos_counter[-1] += 1




				while self.trail_len >= self.max_trails:

					end_cnt = self.p_pos_counter[0] - 1

					if end_cnt == 0:
						# remove end point from position list
						self.prev_positions.popleft()
						self.prev_positions.popleft()
						self.prev_positions.popleft()

						# remove end count from count list
						self.p_pos_counter.popleft()

						# decrease buffer count
						self.trail_cbuff_len -= 1
					else:
						# decrement count of end
						self.p_pos_counter[0] = end_cnt

					self.trail_len -= 1


				######################################################################
			
			self.log += 1
			if self.log == log_freq:
				self.log = 0
				self.avg_speed = 0

		else:
			if p_show: self.reset_trail()


	def display(self, ghost=False, d_method=None):

		if not ghost:
			super().display(d_method=d_method)



def iden(x): return x




#=========================================================================================================================
#
#         ITEM CLASS
#
#=========================================================================================================================






class Item(Game_Object):
	def __init__(self, x=-100, y=-100, angle=0, obj_name="", surface=None, OBJ_ID="", img_scale=1, address=0):
		super().__init__(x, y, angle, obj_name, surface, OBJ_ID, img_scale, address)

		self.vel = (0, 0)
		self.dest = (x, y)
		self.ch_num = -1
		self.is_alive = False
		


	@property
	def speed(self):
		return (self.vel[0]**2 + self.vel[1]**2)**0.5

	@property
	def vel(self):
		return self._vel
	@vel.setter
	def vel(self, _vel):
		self._vel = _vel


	@property
	def ch_num(self):
		return self._ch_num
	@ch_num.setter
	def ch_num(self, _ch_num):
		try:
			self.ch_num
		except:
			self._ch_num = -1

		if self.ch_num != _ch_num:
			self.img = ITEM_NUM_TO_NAME(_ch_num)

		self._ch_num = _ch_num

	@property
	def is_alive(self):
		return self._is_alive
	@is_alive.setter
	def is_alive(self, _is_alive):
		self._is_alive = _is_alive

	




	def display_on(self, surface=None):
		main_surface = self.surface

		if surface == None:
			surface = self.surface

		self.surface = surface
		self.display()
		self.surface = main_surface


	def display(self, d_method=None):
		super().display(d_method=d_method)




#=========================================================================================================================
#
#         OBSTACLE CLASS
#
#=========================================================================================================================





class Obstacle(Game_Object):
	def __init__(self, x=-100, y=-100, angle=0, obj_name="", surface=None, OBJ_ID="", img_scale=1, address=0):
		super().__init__(x, y, angle, obj_name, surface, OBJ_ID, img_scale, address)

		self.vel = (0, 0)
		self.dest = (x, y)
		self.ch_num = -1
		


	@property
	def speed(self):
		return (self.vel[0]**2 + self.vel[1]**2)**0.5

	@property
	def vel(self):
		return self._vel
	@vel.setter
	def vel(self, _vel):
		self._vel = _vel


	@property
	def ch_num(self):
		return self._ch_num
	@ch_num.setter
	def ch_num(self, _ch_num):
		try:
			self.ch_num
		except:
			self._ch_num = -1

		if self.ch_num != _ch_num:
			#self.img = "pipe"
			self.img = OBSTACLE_NUM_TO_NAME(_ch_num)

		self._ch_num = _ch_num

	




	def display_on(self, surface=None):
		main_surface = self.surface

		if surface == None:
			surface = self.surface

		self.surface = surface
		self.display()
		self.surface = main_surface


	def display(self, d_method=None):
		super().display(d_method=d_method)
