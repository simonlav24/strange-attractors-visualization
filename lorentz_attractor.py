import pygame
import math
from random import randint, uniform
import engine3d
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 12)

win_width = 800
win_height = 500
win = pygame.display.set_mode((win_width,win_height))
engine3d.world_position_start(0,200) #lorentz: (0,200)
sigma = 10
rho = 28
beta = 2.6
alpha = 1.4

dt = 0.005


class Point:
	_reg = []
	def __init__(self,x,y,z,color):
		self._reg.append(self)
		self.pos = (x,y,z)
		self.ipos = (x,y,z)
		self.color = color
		
	def step(self):
		x, y, z = self.pos[0], self.pos[1], self.pos[2]
		#lorentz:
		velx = sigma * (y - x)
		vely = x * (rho - z) - y
		velz = x * y - beta * z
		
		#halvorsen:
		# velx = - alpha * x -4 * y - 4 * z - y**2 
		# vely = - alpha * y -4 * z - 4 * x - z**2
		# velz = - alpha * z -4 * x - 4 * y - x**2
		
		velx *= dt
		vely *= dt
		velz *= dt
		
		self.pos = (self.pos[0] + velx, self.pos[1] + vely, self.pos[2] + velz)
		#distance limitter
		#if math.fabs(self.pos[0]) > 1000 or math.fabs(self.pos[1]) > 1000 or math.fabs(self.pos[2]) > 1000:
		#	self._reg.remove(self)
		#	del self
	def draw(self):
		engine3d.draw_point(self.pos, self.color, True)

def dist2view(point):
	return math.sqrt((point.pos[0] - engine3d.cam_vec[0])**2 + (point.pos[1] - engine3d.cam_vec[1])**2 + (point.pos[2] - engine3d.cam_vec[2])**2)

for i in range(600):
	Point(uniform(-1,1),uniform(-1,1),uniform(-1,1), engine3d.hsv2rgb(randint(0,100),100,100) )

def print_stats():
	toprint = "sigma: " + str(sigma) + "\nrho: " + str(rho) + "\nbeta: " + str(beta)
	textsurface = myfont.render( "sigma: " + "{:.3f}".format(sigma) , False, (255, 255, 255))
	win.blit(textsurface,(0,0))
	textsurface = myfont.render( "rho: " + "{:.3f}".format(rho) , False, (255, 255, 255))
	win.blit(textsurface,(0,15))
	textsurface = myfont.render( "beta: " + "{:.3f}".format(beta) , False, (255, 255, 255))
	win.blit(textsurface,(0,30))
values = [0,0,0]
def mouse_check():
	mouse_pos = pygame.mouse.get_pos()
	if mouse_pos[1] > 0 and mouse_pos[1] < 15:
		values[0] = 1
	else:
		values[0] = 0
	if mouse_pos[1] > 15 and mouse_pos[1] < 30:
		values[1] = 1
	else:
		values[1] = 0
	if mouse_pos[1] > 30 and mouse_pos[1] < 45:
		values[2] = 1
	else:
		values[2] = 0
dict = {0:sigma, 1:rho, 2:beta}
	

################################################################################ Main Loop
win.fill((0,0,0))
run = True

while run:
	pygame.time.delay(1)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		engine3d.mouse_event_check(event)
		#mouse wheels:
		if event.type == pygame.MOUSEBUTTONDOWN and 1 in values:
			if event.button == 4:
				if values[0] == 1:
					sigma += 0.1
				if values[1] == 1:
					rho += 0.1
				if values[2] == 1:
					beta += 0.1
			elif event.button == 5:
				if values[0] == 1:
					sigma -= 0.1
				if values[1] == 1:
					rho -= 0.1
				if values[2] == 1:
					beta -= 0.1
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		run = False

	#change values:
	if keys[pygame.K_1]:
		sigma = float(input("Enter the sigma value:"))
	if keys[pygame.K_2]:
		rho = float(input("Enter the rho value:"))
	if keys[pygame.K_3]:
		beta = float(input("Enter the beta value:"))
	if keys[pygame.K_r]:
		sigma = 10
		rho = 28
		beta = 2.6
	if keys[pygame.K_t]:
		for p in Point._reg:
			p.pos = p.ipos
			p.list = []
	#steps
	win.fill((0,0,0))
	engine3d.mouse_hold_check()
	engine3d.update_vecs()
	engine3d.draw_axis()
	
	Point._reg.sort(key = dist2view, reverse = True)
	for p in Point._reg:
		p.step()
		p.draw()
	
	print_stats()
	mouse_check()
	#update game
	pygame.display.update() 

pygame.quit()