import pygame
from pygame.gfxdraw import *
from pygame.locals import *



class Screen(pygame.Surface):
	def __init__(self, size, x=0, y=0):
		super().__init__(size)
		self._x = x
		self._y = y
		self._DEFAULT_X = x
		self._DEFAULT_Y = y
		self._w = size[0]
		self._h = size[1]
		self._DEFAULT_WIDTH = size[0]
		self._DEFAULT_HEIGHT = size[1]
		self._canvas = pygame.Surface(size)
		self._canvas.fill((0, 0, 0))
		self._screen = pygame.Surface(size)

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
	def w(self):
		return self._w
	@w.setter
	def w(self, _w):
		self._w = _w
	
	@property
	def h(self):
		return self._h
	@h.setter
	def h(self, _h):
		self._h = _h

	@property
	def DEFAULT_X(self):
		return self._DEFAULT_X
	@property
	def DEFAULT_Y(self):
		return self._DEFAULT_Y
	@property
	def DEFAULT_WIDTH(self):
		return self._DEFAULT_WIDTH
	@property
	def DEFAULT_HEIGHT(self):
		return self._DEFAULT_HEIGHT


	@property
	def SCALE(self):
		return (self.w / self.DEFAULT_WIDTH) / 2

	@property
	def INV_SCALE(self):
		return (self.DEFAULT_WIDTH / self.w) * 2
	



	@property
	def canvas(self):
		if self.w < self.DEFAULT_WIDTH:
			self.w = self.DEFAULT_WIDTH
			self.h = self.DEFAULT_HEIGHT

		if self.x > self.DEFAULT_X:
			self.x = self.DEFAULT_X
		if self.y > self.DEFAULT_Y:
			self.y = self.DEFAULT_Y
		if self.x + self.w < self.DEFAULT_X + self.DEFAULT_WIDTH:
			self.x = self.DEFAULT_X + self.DEFAULT_WIDTH - self.w
		if self.y + self.h < self.DEFAULT_Y + self.DEFAULT_HEIGHT:
			self.y = self.DEFAULT_Y + self.DEFAULT_HEIGHT - self.h
		
		cv = pygame.Surface(( ((self.DEFAULT_WIDTH*self.INV_SCALE/2)//1 + 1) * 1, ((self.DEFAULT_HEIGHT*self.INV_SCALE/2)//1 + 1) * 1))

		#cv.blit(self._screen, (self.x*self.INV_SCALE, self.y*self.INV_SCALE), area=cv.get_rect().move(self.x * self.INV_SCALE * -1, self.y * self.INV_SCALE * -1))
		#cv.blit(self._screen, (0, 0), area=cv.get_rect().move(self.x * self.INV_SCALE * -1, self.y * self.INV_SCALE * -1))

		cv.blit(self._screen, (self.x*self.INV_SCALE/2, self.y*self.INV_SCALE/2))

		#cv.blit(self._screen, (self.x*self.INV_SCALE, self.y*self.INV_SCALE), area=cv.get_rect())

		cv = pygame.transform.smoothscale(cv, (self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT))
		
		return cv
	


	@property
	def center_x(self):
		return self.INV_SCALE*(-self.x + self.DEFAULT_WIDTH/2)
	@center_x.setter
	def center_x(self, _x):
		self.x = -(_x*self.SCALE) + (self.DEFAULT_WIDTH/2)

	@property
	def center_y(self):
		return self.INV_SCALE*(-self.y + self.DEFAULT_HEIGHT/2)
	@center_y.setter
	def center_y(self, _y):
		self.y = -(_y*self.SCALE) + (self.DEFAULT_HEIGHT/2)

	

	def zoom(self, pos, zoom_ratio):

		if self.w * zoom_ratio > self.DEFAULT_WIDTH * 8:
			zoom_ratio = (self.INV_SCALE/2) * 8

		self.w = self.w * zoom_ratio
		self.h = self.h * zoom_ratio
		x,y = pos

		self.x = zoom_ratio*(self.x - x) + x
		self.y = zoom_ratio*(self.y - y) + y


	def blit(self, surface, position, area=None, special_flags=0):
		self._screen.blit(surface, position, area=area, special_flags=special_flags)
