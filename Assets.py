import pygame, numpy
from pygame.gfxdraw import *
from pygame.locals import *

from tkinter import *

from PIL import Image
from PIL import ImageTk

import OpenGL

from OpenGL.GL import *
from OpenGL.GLU import *

#=========================================================================================================================
#
#         IMAGES
#
#=========================================================================================================================

#global TOOL_ICON
#TOOL_ICON = pygame.image.load('assets/icon.png')


'''
MARIO_IMAGE  = pygame.transform.smoothscale(pygame.image.load('assets/mario.png') , (width//64, height//64))
LUIGI_IMAGE  = pygame.transform.smoothscale(pygame.image.load('assets/luigi.png') , (width//64, height//64))
BOWSER_IMAGE = pygame.transform.smoothscale(pygame.image.load('assets/bowser.png'), (width//64, height//64))
PEACH_IMAGE  = pygame.transform.smoothscale(pygame.image.load('assets/peach.png') , (width//64, height//64))
DK_JR_IMAGE  = pygame.transform.smoothscale(pygame.image.load('assets/dk_jr.png') , (width//64, height//64))
KOOPA_IMAGE  = pygame.transform.smoothscale(pygame.image.load('assets/koopa.png') , (width//64, height//64))
TOAD_IMAGE   = pygame.transform.smoothscale(pygame.image.load('assets/toad.png')  , (width//64, height//64))
YOSHI_IMAGE  = pygame.transform.smoothscale(pygame.image.load('assets/yoshi.png') , (width//64, height//64))
ARROW_IMAGE  = pygame.transform.smoothscale(pygame.image.load('assets/arrow.png') , (width//64, height//64))
'''

global MARIO_IMAGE
global LUIGI_IMAGE
global BOWSER_IMAGE
global PEACH_IMAGE
global DK_JR_IMAGE
global KOOPA_IMAGE
global TOAD_IMAGE
global YOSHI_IMAGE
global ARROW_IMAGE

global OBJECT_IMAGES
global OBJECT_TEXTURES

global MARIO_TK
global LUIGI_TK
global BOWSER_TK
global PEACH_TK
global DK_JR_TK
global KOOPA_TK
global TOAD_TK
global YOSHI_TK
global ARROW_TK
global EMPTY_TK



global GL_CNV_ID



OBJECT_IMAGES = {}

MARIO_IMAGE  = None
LUIGI_IMAGE  = None
BOWSER_IMAGE = None
PEACH_IMAGE  = None
DK_JR_IMAGE  = None
KOOPA_IMAGE  = None
TOAD_IMAGE   = None
YOSHI_IMAGE  = None
ARROW_IMAGE  = None



global CHARACTERS_TK



def create_tk_images():
	global MARIO_TK
	global LUIGI_TK
	global BOWSER_TK
	global PEACH_TK
	global DK_JR_TK
	global KOOPA_TK
	global TOAD_TK
	global YOSHI_TK
	global ARROW_TK
	global EMPTY_TK

	global CHARACTERS_TK

	button_width = 50
	button_height = 50

	MARIO_TK  = ImageTk.PhotoImage(Image.open('assets/mario.png').resize((button_width, button_height), Image.ANTIALIAS))
	LUIGI_TK  = ImageTk.PhotoImage(Image.open('assets/luigi.png').resize((button_width, button_height), Image.ANTIALIAS))
	BOWSER_TK = ImageTk.PhotoImage(Image.open('assets/bowser.png').resize((button_width, button_height), Image.ANTIALIAS))
	PEACH_TK  = ImageTk.PhotoImage(Image.open('assets/peach.png').resize((button_width, button_height), Image.ANTIALIAS))
	DK_JR_TK  = ImageTk.PhotoImage(Image.open('assets/dk_jr.png').resize((button_width, button_height), Image.ANTIALIAS))
	KOOPA_TK  = ImageTk.PhotoImage(Image.open('assets/koopa.png').resize((button_width, button_height), Image.ANTIALIAS))
	TOAD_TK   = ImageTk.PhotoImage(Image.open('assets/toad.png').resize((button_width, button_height), Image.ANTIALIAS))
	YOSHI_TK  = ImageTk.PhotoImage(Image.open('assets/yoshi.png').resize((button_width, button_height), Image.ANTIALIAS))
	ARROW_TK  = ImageTk.PhotoImage(Image.open('assets/arrow.png').resize((button_width, button_height), Image.ANTIALIAS))
	EMPTY_TK  = ImageTk.PhotoImage(Image.open('assets/empty.png').resize((button_width, button_height), Image.ANTIALIAS))

	CHARACTERS_TK = {
		"mario": MARIO_TK,
		"luigi": LUIGI_TK,
		"bowser": BOWSER_TK,
		"peach": PEACH_TK,
		"dk": DK_JR_TK, 
		"koopa": KOOPA_TK, 
		"toad": TOAD_TK, 
		"yoshi": YOSHI_TK, 
		"arrow": ARROW_TK,
		"empty": EMPTY_TK
	}



MARIO_TK  = None
LUIGI_TK  = None
BOWSER_TK = None
PEACH_TK  = None
DK_JR_TK  = None
KOOPA_TK  = None
TOAD_TK   = None
YOSHI_TK  = None
EMPTY_TK  = None
ICON_TK   = None


CHARACTERS_TK = {
	"mario": MARIO_TK,
	"luigi": LUIGI_TK,
	"bowser": BOWSER_TK,
	"peach": PEACH_TK,
	"dk": DK_JR_TK, 
	"koopa": KOOPA_TK, 
	"toad": TOAD_TK, 
	"yoshi": YOSHI_TK, 
	"arrow": EMPTY_TK,
	"empty": EMPTY_TK
}


def create_pygame_images():

	global MARIO_IMAGE
	global LUIGI_IMAGE
	global BOWSER_IMAGE
	global PEACH_IMAGE
	global DK_JR_IMAGE
	global KOOPA_IMAGE
	global TOAD_IMAGE
	global YOSHI_IMAGE
	global ARROW_IMAGE


	MARIO_IMAGE  = pygame.image.load('assets/mario.png').convert_alpha()
	LUIGI_IMAGE  = pygame.image.load('assets/luigi.png').convert_alpha()
	BOWSER_IMAGE = pygame.image.load('assets/bowser.png').convert_alpha()
	PEACH_IMAGE  = pygame.image.load('assets/peach.png').convert_alpha()
	DK_JR_IMAGE  = pygame.image.load('assets/dk_jr.png').convert_alpha()
	KOOPA_IMAGE  = pygame.image.load('assets/koopa.png').convert_alpha()
	TOAD_IMAGE   = pygame.image.load('assets/toad.png').convert_alpha()
	YOSHI_IMAGE  = pygame.image.load('assets/yoshi.png').convert_alpha()
	ARROW_IMAGE  = pygame.image.load('assets/arrow.png').convert_alpha()

	# --------------

	G_SHELL_IMAGE  = pygame.image.load('assets/g_shell.png').convert_alpha()
	R_SHELL_IMAGE  = pygame.image.load('assets/r_shell.png').convert_alpha()
	BANANA_IMAGE   = pygame.image.load('assets/banana.png').convert_alpha()
	FIREBALL_IMAGE = pygame.image.load('assets/fireball.png').convert_alpha()
	P_MUSH_IMAGE   = pygame.image.load('assets/p_mush.png').convert_alpha()
	EGG_IMAGE      = pygame.image.load('assets/egg.png').convert_alpha()

	KILLER_IMAGE  = pygame.image.load('assets/killer.png').convert_alpha()



	PIPE_G_IMAGE    = pygame.image.load('assets/pipe_g.png').convert_alpha()
	PIPE_O_IMAGE    = pygame.image.load('assets/pipe_o.png').convert_alpha()

	THWOMP_IMAGE      = pygame.image.load('assets/thwomp.png').convert_alpha()
	THWOMP_2_A_IMAGE  = pygame.image.load('assets/thwomp_2_A.png').convert_alpha()
	THWOMP_2_B_IMAGE  = pygame.image.load('assets/thwomp_2_B.png').convert_alpha()

	CHEEP_IMAGE     = pygame.image.load('assets/cheep.png').convert_alpha()
	MOLE_IMAGE      = pygame.image.load('assets/mole.png').convert_alpha()
	POLE_IMAGE      = pygame.image.load('assets/pole.png').convert_alpha()

	PLANT_A_IMAGE      = pygame.image.load('assets/plant_A.png').convert_alpha()
	PLANT_B_IMAGE      = pygame.image.load('assets/plant_B.png').convert_alpha()

	BALLOON_B_IMAGE   = pygame.image.load('assets/balloon_b.png').convert_alpha()
	BALLOON_R_IMAGE   = pygame.image.load('assets/balloon_r.png').convert_alpha()

	global OBJECT_IMAGES

	OBJECT_IMAGES = {
		"mario": MARIO_IMAGE,
		"luigi": LUIGI_IMAGE,
		"bowser": BOWSER_IMAGE,
		"peach": PEACH_IMAGE,
		"dk": DK_JR_IMAGE,
		"koopa": KOOPA_IMAGE,
		"toad": TOAD_IMAGE,
		"yoshi": YOSHI_IMAGE,
		"arrow": ARROW_IMAGE,
		"g_shell": G_SHELL_IMAGE,
		"r_shell": R_SHELL_IMAGE,
		"banana": BANANA_IMAGE,
		"fireball": FIREBALL_IMAGE,
		"p_mush": P_MUSH_IMAGE,
		"egg": EGG_IMAGE,
		"killer": KILLER_IMAGE,
		"pipe_g": PIPE_G_IMAGE,
		"pipe_o": PIPE_O_IMAGE,
		"thwomp": THWOMP_IMAGE,
		"thwomp_2_a": THWOMP_2_A_IMAGE,
		"thwomp_2_b": THWOMP_2_B_IMAGE,
		"cheep": CHEEP_IMAGE,
		"mole": MOLE_IMAGE,
		"pole": POLE_IMAGE,
		"plant_a": PLANT_A_IMAGE,
		"plant_b": PLANT_B_IMAGE,
		"balloon_b": BALLOON_B_IMAGE,
		"balloon_r": BALLOON_R_IMAGE
	}




def create_GL_textures():
	global OBJECT_TEXTURES
	global GL_CNV_ID

	GL_CNV_ID = glGenTextures(1)

	OBJECT_TEXTURES = {}

	for img in OBJECT_IMAGES:
		OBJECT_TEXTURES[img] = surfToNewGLTex(GET_IMAGE(img))




def surfToNewGLTex(surf):
	new_tex = glGenTextures(1)
	return surfToGLTex(surf, ID=new_tex)


def surfToGLTex(surf, ID=None):
	global GL_CNV_ID

	rgb_S = pygame.image.tostring(surf, 'RGBA')

	if ID == None: glBindTexture(GL_TEXTURE_2D, GL_CNV_ID)
	else: glBindTexture(GL_TEXTURE_2D, ID)

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
	s_rect = surf.get_rect()
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, s_rect.width, s_rect.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, rgb_S)
	glGenerateMipmap(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, 0)

	if ID == None: return GL_CNV_ID
	else: return ID





def buffToGLTex(buff, size, ID=None, ALPHA=True):
	global GL_CNV_ID

	if ID == None: ID = GL_CNV_ID

	glBindTexture(GL_TEXTURE_2D, ID)

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

	if ALPHA: glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, size[0], size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, buff)
	else: glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size[0], size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, buff)

	glGenerateMipmap(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, 0)

	return ID






def IndentityMat44(): return numpy.matrix(numpy.identity(4), copy=False, dtype='float32')







def GET_IMAGE(obj_name):
	global OBJECT_IMAGES

	if obj_name.lower() in OBJECT_IMAGES:
		img = OBJECT_IMAGES[obj_name.lower()].copy()
	else:
		img = ARROW_IMAGE.copy()
	
	return img


def GET_TEXTURE(obj_name):
	global OBJECT_TEXTURES

	if obj_name.lower() in OBJECT_TEXTURES:
		img = OBJECT_TEXTURES[obj_name.lower()]
	else:
		img = OBJECT_TEXTURES['arrow']
	
	return img


def rot_image(image, angle):
	orig_rect = image.get_rect()
	rot_image = pygame.transform.rotate(image, angle)
	rot_rect = orig_rect.copy()
	rot_rect.center = rot_image.get_rect().center
	rot_image = rot_image.subsurface(rot_rect).copy()
	return rot_image