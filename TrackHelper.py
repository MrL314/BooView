
import pygame
from pygame.gfxdraw import *
from pygame.locals import *


import random

import Assets

def word_to_RGB(w):
	r = ((w       ) % 32) * 8
	g = ((w   / 32) % 32) * 8
	b = ((w / 1024) % 32) * 8

	r = (r + (r / 32)) // 1
	g = (g + (g / 32)) // 1
	b = (b + (b / 32)) // 1

	if r > 255: r = 255
	if g > 255: g = 255
	if b > 255: b = 255

	return (r, g, b)




def generate_palette(p_data):
	pal_vals = []

	i = 0
	val = 0
	while i < len(p_data):
		if i % 2 == 0:
			val = p_data[i]
		else:
			val += p_data[i] * 256

			pal_vals.append(word_to_RGB(val))

		i += 1

	#pal = [pal_vals[i*8: (i+1)*8] for i in range(len(pal_vals)//8)]

	return pal_vals




def pixels_to_bytes(p):
	p_b = []

	for r,g,b in p:
		p_b.append(int(r))
		p_b.append(int(g))
		p_b.append(int(b))

	return bytes(p_b)

def pixels_to_bytes_alpha(p, alpha):
	p_b = []

	for r,g,b in p:
		p_b.append(int(r))
		p_b.append(int(g))
		p_b.append(int(b))
		p_b.append(int(alpha))

	return bytes(p_b)



def bytes_to_tile_buffer(tile_bytes, pal):

	tile = []

	for b in tile_bytes:
		tile.append(pal[b])

	return pixels_to_bytes(tile)





def get_tile_imgs(t_data, p_data):

	pal = generate_palette(p_data)

	TILES = [bytes_to_tile_buffer(t_data[n * 64:(n + 1) * 64], pal) for n in range(len(t_data)//64)]

	return [pygame.image.frombuffer(TILE, (8, 8), "RGB") for TILE in TILES]




def get_tilemap_from_data(m_data, t_data, p_data):

	MAP = pygame.Surface((1024, 1024))

	TILE_IMGS = get_tile_imgs(t_data, p_data)

	for y in range(128):
		for x in range(128):
			MAP.blit(TILE_IMGS[m_data[y * 128 + x]], (x * 8, y * 8))

	return (MAP, TILE_IMGS)
















def fix_diff_surround(diff_map):

	new_diff_map = [[False for x in range(3)] for y in range(3)]
	

	TOP = 0		# define top row
	MID = 1		# define mid (both row and column)
	BOT = 2		# define bottom row

	LEF = 0		# define left column
	RHT = 2		# define right column


	# checking order
	#
	# 1 . . . 2
	# .       .
	# .       .
	# .       .
	# 3 . . . 4

	# set corners
	if diff_map[TOP][LEF] == True: new_diff_map[TOP][LEF] = True	# check 1
	if diff_map[TOP][RHT] == True: new_diff_map[TOP][RHT] = True	# check 2
	if diff_map[BOT][LEF] == True: new_diff_map[BOT][LEF] = True	# check 3
	if diff_map[BOT][RHT] == True: new_diff_map[BOT][RHT] = True	# check 4





	# checking order
	#
	# . 5 5 5 .
	# 6       7
	# 6       7
	# 6       7
	# . 8 8 8 .


	# top band
	# if top enabled, set top corners as well
	# x - - - x
	# .       .
	# .       .
	# .       .
	# . . . . .
	if diff_map[TOP][MID]:
		new_diff_map[TOP][LEF] = True
		new_diff_map[TOP][MID] = True
		new_diff_map[TOP][RHT] = True


	# left band
	# if left enabled, set left corners as well
	# x . . . .
	# |       .
	# |       .
	# |       .
	# x . . . .
	if diff_map[MID][LEF]:
		new_diff_map[TOP][LEF] = True
		new_diff_map[MID][LEF] = True
		new_diff_map[BOT][LEF] = True


	# right band
	# if right enabled, set right corners as well
	# . . . . x
	# .       |
	# .       |
	# .       |
	# . . . . x
	if diff_map[MID][RHT]:
		new_diff_map[TOP][RHT] = True
		new_diff_map[MID][RHT] = True
		new_diff_map[BOT][RHT] = True


	# bottom band
	# if bottom enabled, set bottom corners as well
	# . . . . .
	# .       .
	# .       .
	# .       .
	# x - - - x
	if diff_map[BOT][MID]:
		new_diff_map[BOT][LEF] = True
		new_diff_map[BOT][MID] = True
		new_diff_map[BOT][RHT] = True


	return new_diff_map
	






def make_base_cp_tile(c_dict):
	return pygame.image.frombuffer(pixels_to_bytes_alpha([c_dict["base"]]*256, 100), (16, 16), "RGBA")


CP_COLS = {
	"red": {"base": (255, 100, 100), "border": (255, 50, 50)},
	"orange": {"base": (255, 200, 100), "border": (255, 100, 0)},
	"green": {"base": (100, 255, 100), "border": (0, 255, 0)},
	"yellow": {"base": (255, 255, 100), "border": (230, 230, 0)}
}

cp_colors = (
	CP_COLS["red"],
	CP_COLS["orange"],
	CP_COLS["green"],
	CP_COLS["yellow"]
)

'''
red_tile    = pygame.image.frombuffer(pixels_to_bytes_alpha([(255, 100, 100)]*256, 100), (16, 16), "RGBA")
orange_tile = pygame.image.frombuffer(pixels_to_bytes_alpha([(255, 200, 100)]*256, 100), (16, 16), "RGBA")
green_tile  = pygame.image.frombuffer(pixels_to_bytes_alpha([(100, 255, 100)]*256, 100), (16, 16), "RGBA")
yellow_tile = pygame.image.frombuffer(pixels_to_bytes_alpha([(255, 255, 100)]*256, 100), (16, 16), "RGBA")
'''

red_tile = make_base_cp_tile(CP_COLS["red"])
orange_tile = make_base_cp_tile(CP_COLS["orange"])
green_tile = make_base_cp_tile(CP_COLS["green"])
yellow_tile = make_base_cp_tile(CP_COLS["yellow"])

cp_tiles = (red_tile, orange_tile, green_tile, yellow_tile)



def get_cp_tile(cp_num, diff_map):


	BORDER_WIDTH = 3


	cp_col = cp_num % 4							# which color to use based on the cp number
	border_map = fix_diff_surround(diff_map)	# adjusted border map to fix corner overwriting


	TOP = 0		# define top row
	MID = 1		# define mid (both row and column)
	BOT = 2		# define bottom row

	LEF = 0		# define left column
	RHT = 2		# define right column


	base_tile = cp_tiles[cp_col]	# base cp tile (pre-rendered to save minimal time)
	CP_COLOR = cp_colors[cp_col]	# color dict based on cp number


	BASE_COLOR = (
		CP_COLOR["base"][0],	# red channel
		CP_COLOR["base"][1],	# green channel
		CP_COLOR["base"][2],	# blue channel
		100						# alpha channel
	)


	BORDER_COLOR = (
		CP_COLOR["border"][0],	# red channel
		CP_COLOR["border"][1],	# green channel
		CP_COLOR["border"][2],	# blue channel
		150						# alpha channel
	)


	img_buff = list(pygame.image.tostring(base_tile, "RGBA"))
	pix = []


	# convert buffer to pixel 4-tuples
	for i in range(len(img_buff) // 4):
		pixel = (
			img_buff[i*4 + 0],	# red channel
			img_buff[i*4 + 1],	# green channel
			img_buff[i*4 + 2],	# blue channel
			img_buff[i*4 + 3]	# alpha channel
		)
		pix.append(pixel)



	##### process border pixels here

	# corners are a NxN square of border pixels

	# top left corner
	if border_map[TOP][LEF] == True:
		for i in range(BORDER_WIDTH):
			for j in range(BORDER_WIDTH):
				x = j
				y = i
				pix[y * 16 + x] = BORDER_COLOR


	# top right corner
	if border_map[TOP][RHT] == True:
		for i in range(BORDER_WIDTH):
			for j in range(BORDER_WIDTH):
				x = 15-j
				y = i
				pix[y * 16 + x] = BORDER_COLOR


	# bottom left corner
	if border_map[BOT][LEF] == True:
		for i in range(BORDER_WIDTH):
			for j in range(BORDER_WIDTH):
				x = j
				y = 15-i
				pix[y * 16 + x] = BORDER_COLOR


	# bottom right corner
	if border_map[BOT][RHT] == True:
		for i in range(BORDER_WIDTH):
			for j in range(BORDER_WIDTH):
				x = 15-j
				y = 15-i
				pix[y * 16 + x] = BORDER_COLOR



	# side-bands are N pixels wide, and 16-(N*2) pixels long 
	#    (N pixels on each border dont need to be rendered again)

	# top band
	if border_map[TOP][MID] == True:
		for i in range(BORDER_WIDTH):
			for j in range(16 - (BORDER_WIDTH * 2)):
				x = BORDER_WIDTH + j
				y = i
				pix[y * 16 + x] = BORDER_COLOR

	# bottom band
	if border_map[BOT][MID] == True:
		for i in range(BORDER_WIDTH):
			for j in range(16 - (BORDER_WIDTH * 2)):
				x = BORDER_WIDTH + j
				y = 15-i
				pix[y * 16 + x] = BORDER_COLOR

	# left band
	if border_map[MID][LEF] == True:
		for i in range(16 - (BORDER_WIDTH * 2)):
			for j in range(BORDER_WIDTH):
				x = j
				y = BORDER_WIDTH + i
				pix[y * 16 + x] = BORDER_COLOR

	# right band
	if border_map[MID][RHT] == True:
		for i in range(16 - (BORDER_WIDTH * 2)):
			for j in range(BORDER_WIDTH):
				x = 15-j
				y = BORDER_WIDTH + i
				pix[y * 16 + x] = BORDER_COLOR






	# convert pixel buffer back to image
	out_buff = []

	for p in pix:
		out_buff.append(p[0])	# red channel
		out_buff.append(p[1])	# green channel
		out_buff.append(p[2])	# blue channel
		out_buff.append(p[3])	# alpha channel


	return pygame.image.frombuffer(bytes(out_buff), (16, 16), "RGBA")















def get_cpmap_flowmap_from_data(cp_data, flow_data):
	"""Generate the images for the overlay for the cp and flow maps"""

	CP_MAP   = pygame.Surface((1024, 1024), SRCALPHA)	#  cp  map base surface, SRCALPHA to set as alpha enabled
	FLOW_MAP = pygame.Surface((1024, 1024), SRCALPHA)	# flow map base surface, SRCALPHA to set as alpha enabled



	# pad the borders of the cp map in order to handle literal edge cases later
	cp_padded = [[-1 for x in range(64+2)] for y in range(64+2)]

	for y in range(64):
		for x in range(64):
			cp_padded[y+1][x+1] = cp_data[y * 64 + x]





	# checkpoint and flow maps are a 64x64 table
	for y in range(64):
		for x in range(64):
			
			
			_y = y+1	# padded map coords
			_x = x+1	# padded map coords

			cp_num = cp_padded[_y][_x]	# checkpoint tile number
			

			if cp_num == 0x7f: continue	# skip render if cp=0x7f (null cp) 



			######## make flow map tile

			flow_angle = -(360 * flow_data[y * 64 + x] / 255)
			arr_img = pygame.transform.smoothscale(
												Assets.rot_image(Assets.ARROW_IMAGE, flow_angle),	# rotated arrow image
												(16, 16))											# resize to a 16x16 image
											
			# blit flow arrow onto map
			FLOW_MAP.blit(
				arr_img, 			# rotated arrow image
				(x * 16, y * 16))	# convert tile xy to coordinate xy
			




			######## make cp map tile

			diff_map = [[False for j in range(3)] for i in range(3)]

			# check the 3x3 area around current cp, to make the border for the tile
			for y_off in range(3):
				for x_off in range(3):
					other_cp = cp_padded[_y + y_off - 1][_x + x_off - 1]	# change coordinates to the padded cp map coords

					if cp_num != other_cp:	diff_map[y_off][x_off] = True	# set proper "different checkpoint" index


			cp_img = pygame.transform.smoothscale(
											get_cp_tile(cp_num, diff_map),	# get the cp tile, with borders
											(16, 16))						# resize to a 16x16 block
										
			CP_MAP.blit(
				cp_img, 			# resized bordered cp tile
				(x * 16, y * 16))	# convert tile xy to coordinate xy
			






	CP_IMAGE = CP_MAP.copy() # pygame.image.frombuffer(CP_TILES, )
	FLOW_IMAGE = FLOW_MAP.copy() #
	return (CP_IMAGE, FLOW_IMAGE)







