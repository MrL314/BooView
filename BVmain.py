


import tkinter as tk
from tkinter import *
from tkinter import filedialog


import threading


import os, sys, platform

import Assets

import time



PRESSED_RELIEF = SUNKEN


class BV_Instance():

	def __init__(self, WINDOW_SIZE=(0, 0), PYG_SIZE=(0, 0)):

		self.root = tk.Tk()

		self.WINDOW_WIDTH, self.WINDOW_HEIGHT = WINDOW_SIZE

		self.embed = tk.Frame(self.root, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT)
		self.embed.grid(columnspan = (PYG_SIZE[0]), rowspan = PYG_SIZE[1])   # check and fix?
		self.embed.pack(side=LEFT)




		# Set up all "global" variables
		self.setup_variables()



		





	def setup_window(self):


		self.root.title("BooView")
		self.root.iconphoto(False, PhotoImage(file='assets/icon.png'))
		self.root.resizable(False, False)
		self.root.lift()
		self.root.attributes("-topmost", True)
		self.root.attributes("-topmost", False)


		# frame management

		SIDE_FRAME_WIDTH = 100
		button_width = 50
		button_height = 50

		Assets.create_tk_images()

		

		SIDE_FRAME = tk.Frame(self.root, width=SIDE_FRAME_WIDTH, height=self.WINDOW_HEIGHT)



		self.REPLAY_BUTTON = tk.Button(SIDE_FRAME, text="Replay Ghost", command=self.toggle_REPLAY_MODE)

		self.REPLAY_BUTTON.config(state="disabled")




		CBOX_FRAME = tk.Frame(SIDE_FRAME, width=SIDE_FRAME_WIDTH)

		TRAIL_CBOX_VAR = tk.BooleanVar()
		self.TRAIL_CBOX  = tk.Checkbutton(CBOX_FRAME, text="Show Trails", variable=TRAIL_CBOX_VAR, onvalue=True, offvalue=False, command=self.set_trail_var)

		ZONE_CBOX_VAR = tk.BooleanVar()
		self.ZONE_CBOX   = tk.Checkbutton(CBOX_FRAME, text="Show Zones", variable=ZONE_CBOX_VAR, onvalue=True, offvalue=False, command=self.set_zone_var)
		
		FLOW_CBOX_VAR = tk.BooleanVar()
		self.FLOW_CBOX   = tk.Checkbutton(CBOX_FRAME, text="Show Flowmap", variable=FLOW_CBOX_VAR, onvalue=True, offvalue=False, command=self.set_flow_var)

		CAM_CBOX_VAR = tk.BooleanVar()
		self.CAM_CBOX = tk.Checkbutton(CBOX_FRAME, text="Show Cameras", variable=CAM_CBOX_VAR, onvalue=True, offvalue=False, command=self.set_cam_var)

		VEC_CBOX_VAR = tk.BooleanVar()
		self.VEC_CBOX = tk.Checkbutton(CBOX_FRAME, text="Show Vectors", variable=VEC_CBOX_VAR, onvalue=True, offvalue=False, command=self.set_vec_var)

		TGT_CBOX_VAR = tk.BooleanVar()
		self.TGT_CBOX = tk.Checkbutton(CBOX_FRAME, text="Show Targets", variable=TGT_CBOX_VAR, onvalue=True, offvalue=False, command=self.set_tgt_var)





		FOLLOW_FRAME = tk.LabelFrame(SIDE_FRAME, relief=GROOVE, text="FOLLOW RACER")

		FOLLOW_1_BUTTON = tk.Button(FOLLOW_FRAME, image=Assets.EMPTY_TK, command=self.toggle_follow_1, width=button_width, height=button_height, relief=FLAT)
		FOLLOW_2_BUTTON = tk.Button(FOLLOW_FRAME, image=Assets.EMPTY_TK, command=self.toggle_follow_2, width=button_width, height=button_height, relief=FLAT)
		FOLLOW_3_BUTTON = tk.Button(FOLLOW_FRAME, image=Assets.EMPTY_TK, command=self.toggle_follow_3, width=button_width, height=button_height, relief=FLAT)
		FOLLOW_4_BUTTON = tk.Button(FOLLOW_FRAME, image=Assets.EMPTY_TK, command=self.toggle_follow_4, width=button_width, height=button_height, relief=FLAT)
		FOLLOW_5_BUTTON = tk.Button(FOLLOW_FRAME, image=Assets.EMPTY_TK, command=self.toggle_follow_5, width=button_width, height=button_height, relief=FLAT)
		FOLLOW_6_BUTTON = tk.Button(FOLLOW_FRAME, image=Assets.EMPTY_TK, command=self.toggle_follow_6, width=button_width, height=button_height, relief=FLAT)
		FOLLOW_7_BUTTON = tk.Button(FOLLOW_FRAME, image=Assets.EMPTY_TK, command=self.toggle_follow_7, width=button_width, height=button_height, relief=FLAT)
		FOLLOW_8_BUTTON = tk.Button(FOLLOW_FRAME, image=Assets.EMPTY_TK, command=self.toggle_follow_8, width=button_width, height=button_height, relief=FLAT)

		self.FOLLOW_BUTTONS = [FOLLOW_1_BUTTON, FOLLOW_2_BUTTON, FOLLOW_3_BUTTON, FOLLOW_4_BUTTON, FOLLOW_5_BUTTON, FOLLOW_6_BUTTON, FOLLOW_7_BUTTON, FOLLOW_8_BUTTON]

		
		SPRITE_SIZE_FRAME = tk.LabelFrame(SIDE_FRAME, relief=GROOVE, text="SPRITE SCALE")

		SPRITE_SCALE_VAR = StringVar()

		self.SPRITE_SIZE_WIDGET = tk.Spinbox(SPRITE_SIZE_FRAME, increment=1, from_=1, to=4, state='readonly', width=4 , justify=RIGHT, textvariable=SPRITE_SCALE_VAR)
		self.SPRITE_SIZE_WIDGET.pack(side=TOP, fill=X)


		self.SRAM_UPLOAD_BUTTON = tk.Button(SIDE_FRAME, text="Upload SRAM Data", command=self.set_in_file_dialogue)




		self.TK_VARS = {
			"CAM_CBOX": CAM_CBOX_VAR,
			"VEC_CBOX": VEC_CBOX_VAR,
			"SPRITE_SCALE": SPRITE_SCALE_VAR,
			"TRAIL_CBOX": TRAIL_CBOX_VAR,
			"ZONE_CBOX": ZONE_CBOX_VAR,
			"FLOW_CBOX": FLOW_CBOX_VAR,
			"TGT_CBOX": TGT_CBOX_VAR,

		}



		self.set_tkvar("SPRITE_SCALE", "2")



		SIDE_TABLE = [
			[(self.REPLAY_BUTTON, 2)],
			[(CBOX_FRAME, 2)],
			[(FOLLOW_FRAME, 2)],
			[(SPRITE_SIZE_FRAME, 2)],
			[(self.SRAM_UPLOAD_BUTTON, 2)]
			]


		CBOX_TABLE = [
			[self.TRAIL_CBOX],
			[self.ZONE_CBOX],
			[self.FLOW_CBOX],
			[self.CAM_CBOX],
			[self.VEC_CBOX],
			[self.TGT_CBOX],
		]

		
		FOLLOW_TABLE = [
			[self.FOLLOW_BUTTONS[0], self.FOLLOW_BUTTONS[1]],
			[self.FOLLOW_BUTTONS[2], self.FOLLOW_BUTTONS[3]],
			[self.FOLLOW_BUTTONS[4], self.FOLLOW_BUTTONS[5]],
			[self.FOLLOW_BUTTONS[6], self.FOLLOW_BUTTONS[7]],
		]


		self.pack_group(FOLLOW_TABLE)
		
		self.pack_group(CBOX_TABLE, sticky="NW")


		self.pack_group(SIDE_TABLE)


		SIDE_FRAME.pack(side=LEFT)
		self.root.update()


	def pack_group(self, g, sticky="NEWS"):
		row = 0
		for el_row in g:
			col = 0
			for b in el_row:
				if type(b) == type(tuple()):
					b[0].grid(column = col, row = row, columnspan=b[1], sticky=sticky)
				else:
					b.grid(column = col, row = row, sticky=sticky)

				col += 1

			row += 1





	def setup_variables(self):
		self.racers_to_follow = {
			"racer0": False,
			"racer1": False,
			"racer2": False,
			"racer3": False,
			"racer4": False,
			"racer5": False,
			"racer6": False,
			"racer7": False
		}
		

		self.REPLAY_MODE = False
		self.P_REPLAY_MODE = False
		self.SHOW_GHOST = False
		self.GHOST_TURN_OFF = False
		self.TRAIL_LINES = False

		self.TRAILS_TOGGLED = False

		self.P_FOLLOW = [-1]*8

		self.show_zones = False
		self.show_flows = False



		self.SHOW_DIR_NORMALIZED = False
		self.SHOW_CAMERA_ANGLE = False
		self.SHOW_CAM = False
		self.SHOW_VEL_VECTOR = False
		self.SHOW_TARGETS = False
		

		self.SHOW_VEL_COMPONENTS = False
		self.SHOW_VEL_NORMALIZED = False
		self.SHOW_ACCELERATION = False

		self.in_file_dialogue = False



	def get_sprite_scale(self):
		return int(self.get_tkvar('SPRITE_SCALE'))





	def toggle_REPLAY_MODE(self):

		R = not self.REPLAY_MODE

		if R: 
			self.REPLAY_BUTTON.config(relief=PRESSED_RELIEF)
			self.TRAIL_CBOX.deselect()
			self.TRAIL_CBOX.invoke()
			#self.TRAIL_LINES = True
			self.SPRITE_SIZE_WIDGET.config(state='disabled')
		else:
			self.REPLAY_BUTTON.config(relief=RAISED)
			self.SPRITE_SIZE_WIDGET.config(state='readonly')
			self.GHOST_TURN_OFF = True

		self.REPLAY_MODE = R


			


	def toggle_follow_1(self): self.toggle_follow(0)
	def toggle_follow_2(self): self.toggle_follow(1)
	def toggle_follow_3(self): self.toggle_follow(2)
	def toggle_follow_4(self): self.toggle_follow(3)
	def toggle_follow_5(self): self.toggle_follow(4)
	def toggle_follow_6(self): self.toggle_follow(5)
	def toggle_follow_7(self): self.toggle_follow(6)
	def toggle_follow_8(self): self.toggle_follow(7)
	def toggle_follow(self, n):
		r_nm = "racer" + str(n)

		self.racers_to_follow[r_nm] = not self.racers_to_follow[r_nm]

		if self.racers_to_follow[r_nm]: 
			self.FOLLOW_BUTTONS[n].config(bg="#c8c8c8")
		else: 
			self.FOLLOW_BUTTONS[n].config(bg="#f0f0f0")



	def set_in_file_dialogue(self):
		self.in_file_dialogue = True

	def set_not_in_file_dialogue(self):
		self.in_file_dialogue = False



	def get_tkvar(self, v):
		return self.TK_VARS[v].get()

	def set_tkvar(self, v, val):
		self.TK_VARS[v].set(val)


	def set_trail_var(self):

		if not self.REPLAY_MODE:

			self.TRAIL_LINES = self.get_tkvar('TRAIL_CBOX')

			#if self.TRAIL_LINES: self.TRAIL_BUTTON.config(relief=PRESSED_RELIEF)
			#else:                self.TRAIL_BUTTON.config(relief=RAISED)

			self.TRAILS_TOGGLED = True

	def set_zone_var(self):
		self.show_zones = self.get_tkvar('ZONE_CBOX')

		#if self.show_zones: self.CP_BUTTON.config(relief=PRESSED_RELIEF)
		#else:               self.CP_BUTTON.config(relief=RAISED)

	def set_flow_var(self):
		self.show_flows = self.get_tkvar('FLOW_CBOX')

		#if self.show_flows: self.FLOW_BUTTON.config(relief=PRESSED_RELIEF)
		#else:               self.FLOW_BUTTON.config(relief=RAISED)


	def set_cam_var(self):
		self.SHOW_CAM = self.get_tkvar('CAM_CBOX')


	def set_vec_var(self):
		self.SHOW_DIR_NORMALIZED = self.SHOW_CAMERA_ANGLE = self.SHOW_VEL_VECTOR = self.get_tkvar('VEC_CBOX')


	def set_tgt_var(self):
		self.SHOW_TARGETS = self.get_tkvar('TGT_CBOX')




