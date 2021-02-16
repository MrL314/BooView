import pygame
from pygame.gfxdraw import *
from pygame.locals import *

from tkinter import *

from PIL import Image
from PIL import ImageTk

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


global MARIO_TK
global LUIGI_TK
global BOWSER_TK
global PEACH_TK
global DK_JR_TK
global KOOPA_TK
global TOAD_TK
global YOSHI_TK
global EMPTY_TK


MARIO_IMAGE  = pygame.image.load('assets/mario.png')
LUIGI_IMAGE  = pygame.image.load('assets/luigi.png')
BOWSER_IMAGE = pygame.image.load('assets/bowser.png')
PEACH_IMAGE  = pygame.image.load('assets/peach.png')
DK_JR_IMAGE  = pygame.image.load('assets/dk_jr.png')
KOOPA_IMAGE  = pygame.image.load('assets/koopa.png')
TOAD_IMAGE   = pygame.image.load('assets/toad.png')
YOSHI_IMAGE  = pygame.image.load('assets/yoshi.png')
ARROW_IMAGE  = pygame.image.load('assets/arrow.png')



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
	EMPTY_TK  = ImageTk.PhotoImage(Image.open('assets/empty.png').resize((button_width, button_height), Image.ANTIALIAS))

	CHARACTERS_TK = (MARIO_TK, LUIGI_TK, BOWSER_TK, PEACH_TK, DK_JR_TK, KOOPA_TK, TOAD_TK, YOSHI_TK)



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


CHARACTERS_TK = (MARIO_TK, LUIGI_TK, BOWSER_TK, PEACH_TK, DK_JR_TK, KOOPA_TK, TOAD_TK, YOSHI_TK)

G_SHELL_IMAGE  = pygame.image.load('assets/g_shell.png')
R_SHELL_IMAGE  = pygame.image.load('assets/r_shell.png')
BANANA_IMAGE   = pygame.image.load('assets/banana.png')
FIREBALL_IMAGE = pygame.image.load('assets/fireball.png')
P_MUSH_IMAGE   = pygame.image.load('assets/p_mush.png')
EGG_IMAGE      = pygame.image.load('assets/egg.png')

KILLER_IMAGE  = pygame.image.load('assets/killer.png')



PIPE_G_IMAGE    = pygame.image.load('assets/pipe_g.png')
PIPE_O_IMAGE    = pygame.image.load('assets/pipe_o.png')

THWOMP_IMAGE      = pygame.image.load('assets/thwomp.png')
THWOMP_2_A_IMAGE  = pygame.image.load('assets/thwomp_2_A.png')
THWOMP_2_B_IMAGE  = pygame.image.load('assets/thwomp_2_B.png')

CHEEP_IMAGE     = pygame.image.load('assets/cheep.png')
MOLE_IMAGE      = pygame.image.load('assets/mole.png')
POLE_IMAGE      = pygame.image.load('assets/pole.png')

PLANT_A_IMAGE      = pygame.image.load('assets/plant_A.png')
PLANT_B_IMAGE      = pygame.image.load('assets/plant_B.png')

BALLOON_B_IMAGE   = pygame.image.load('assets/balloon_b.png')
BALLOON_R_IMAGE   = pygame.image.load('assets/balloon_r.png')





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



def GET_IMAGE(obj_name):
	if obj_name.lower() in OBJECT_IMAGES:
		img = OBJECT_IMAGES[obj_name.lower()].copy()
	else:
		img = ARROW_IMAGE.copy()
	
	return img



def rot_image(image, angle):
	orig_rect = image.get_rect()
	rot_image = pygame.transform.rotate(image, angle)
	rot_rect = orig_rect.copy()
	rot_rect.center = rot_image.get_rect().center
	rot_image = rot_image.subsurface(rot_rect).copy()
	return rot_image