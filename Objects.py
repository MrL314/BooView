
import pygame
from pygame.gfxdraw import *
from pygame.locals import *

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
			raise IndexError("Invalid Character Number")
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
		obj_name = ""
		if type(_img) == type(""):
			obj_name = _img
		else:
			pass

		if obj_name != "":
			_img = Assets.GET_IMAGE(obj_name)
		
		self._img = _img

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


	def display(self):
		
		z_scl = self.z
		if z_scl > 0x8000:
			z_scl -= 0x10000
		z_scl /= 0x2000
		z_scl += 1
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







#=========================================================================================================================
#
#         RACER CLASS
#
#=========================================================================================================================


class Racer(Game_Object):

	def __init__(self, x=-100, y=-100, angle=0, obj_name="", surface=None, OBJ_ID="", display_dest=False, img_scale=1, address=0):
		super().__init__(x, y, angle, obj_name, surface, OBJ_ID, img_scale=img_scale, address=address)

		self.vel = (0, 0)
		self.dest = (x, y)
		self.display_dest = display_dest
		self.ch_num = -1
		self.buttons = 0

		self.prev_positions = []
		
		self.log = 0

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
	

	def clear_trail(self):
		self.prev_positions = []


	def display_on(self, surface=None):
		main_surface = self.surface

		if surface == None:
			surface = self.surface

		self.surface = surface
		self.display()
		self.surface = main_surface

	def reset_trail(self):
		self.prev_positions = []

	def display(self, SCREEN=None, trails=0, ghost=False):

		if self.log == 0:
			
			self.prev_positions = ([(self.x, self.y)] + self.prev_positions)[:trails]   # for TT ghost mode
			#self.prev_positions = ([(self.x, self.y)] + self.prev_positions)[:20]

		self.log += 1
		if self.log == 3:
			self.log = 0
		if SCREEN != None:
		

			'''
			for i in range(len(self.prev_positions) - 1):
				x_0 = self.prev_positions[i][0]
				y_0 = self.prev_positions[i][1]
				x_1 = self.prev_positions[i+1][0]
				y_1 = self.prev_positions[i+1][1]
			'''

			disp_prev_positions = [(x*SCREEN.SCALE + SCREEN.x, y*SCREEN.SCALE + SCREEN.y) for x,y in self.prev_positions]

			if len(self.prev_positions) > 2:
				#pygame.draw.lines(self.surface, (0, 0, 255), False, disp_prev_positions, 4)
				pygame.draw.aalines(self.surface, (0, 255, 0), False, disp_prev_positions)
				#pygame.draw.aalines(self.surface, (0, 255, 0), False, [(x+1, y  ) for x,y in disp_prev_positions])
				#pygame.draw.aalines(self.surface, (0, 255, 0), False, [(x  , y+1) for x,y in disp_prev_positions])
				#pygame.draw.aalines(self.surface, (0, 255, 0), False, [(x-1, y  ) for x,y in disp_prev_positions])
				#pygame.draw.aalines(self.surface, (0, 255, 0), False, [(x  , y-1) for x,y in disp_prev_positions])



		if not ghost:
			super().display()

		if self.display_dest == True:
			pygame.draw.circle(self.surface, (255, 255, 255), (math.floor(self.dest[0]), math.floor(self.dest[1])), math.floor(3*width/600))






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


	def display(self):
		super().display()




#=========================================================================================================================
#
#         ITEM CLASS
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


	def display(self):
		super().display()
