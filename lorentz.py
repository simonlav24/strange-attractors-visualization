import pygame
import math

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 12)

win_width = 800
win_height = 500
scale_factor = 10
win = pygame.display.set_mode((win_width,win_height))

sigma = 10
rho = 28
beta = 2.6

a = 0.2
b = 0.2
c = 5.7 

alpha = 1.4

#for lorentz 0.01
dt = 0.005
zoom = 3
angle = 0
pos_x = win_width/2
pos_y = win_height/2 + 100
trace_size = -1

def param(x,y,z):
	x*=zoom
	y*=zoom
	z*=zoom
	return ((x+y)*math.cos(angle) + (x-y)*math.sin(angle) + pos_x,\
	-((x*math.cos(angle) - y*math.sin(angle))*math.tan((5*math.pi)/6) + \
	(x*math.sin(angle) + y*math.cos(angle))*math.tan(math.pi/6) + (2/math.sqrt(3))*z) + pos_y) 

class Point:
	_reg = []
	def __init__(self,x,y,z,color):
		self._reg.append(self)
		self.pos = (x,y,z)
		self.ipos = (x,y,z)
		#self.vel = (x,y,z)
		self.list = [self.pos]
		self.color = color
		
	def step(self):
		x, y, z = self.pos[0], self.pos[1], self.pos[2]
		#lorentz:
		#velx = sigma * (self.pos[1] - self.pos[0])
		#vely = self.pos[0] * (rho - self.pos[2]) - self.pos[1]
		#velz = self.pos[0] * self.pos[1] - beta * self.pos[2]
		
		#rossler:
		#velx = - self.pos[1] - self.pos[2]
		#vely = self.pos[0] + a * self.pos[1]
		#velz = b + self.pos[2] * (self.pos[0] - c)
		
		#halvorsen:
		velx = - alpha * x -4 * y - 4 * z - y**2 
		vely = - alpha * y -4 * z - 4 * x - z**2
		velz = - alpha * z -4 * x - 4 * y - x**2
		# print((velx,vely,velz))
		
		velx *= dt
		vely *= dt
		velz *= dt
		
		self.pos = (self.pos[0] + velx, self.pos[1] + vely, self.pos[2] + velz)
		
		self.list.append(self.pos)
		if trace_size != -1:
			if len(self.list) >= trace_size:
				self.list.pop(0)
	def draw(self):
		#for i in self.list:
			#draw_point(i)
		draw_path(self.list, self.color)
		
		
def draw_point(pos):
	pos_param = (int(param(pos[0], pos[1], pos[2])[0]), int(param(pos[0], pos[1], pos[2])[1]))
	pygame.draw.circle(win, (255,0,0), pos_param , 1)
def draw_path(list, color):
	if len(list) == 1:
		list.append(list[0])
	if len(list) == 0:
		return
	lines_list = []
	for pos in list:
		pos_param = (int(param(pos[0], pos[1], pos[2])[0]), int(param(pos[0], pos[1], pos[2])[1]))
		lines_list.append(pos_param)
	pygame.draw.lines(win, color, False, lines_list)
def draw_axis():
	draw_path([(0,0,0), (5,0,0)], (255,0,0))
	draw_path([(0,0,0), (0,5,0)], (0,255,0))
	draw_path([(0,0,0), (0,0,5)], (0,0,255))
	

Point(0.1,0,0, (255,0,0))
#Point(1,1,1, (0,0,255))

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
	if keys[pygame.K_a]:
		pos_x -= 1
	if keys[pygame.K_d]:
		pos_x += 1
	if keys[pygame.K_UP]:
		zoom += 0.1
	if keys[pygame.K_DOWN]:
		if zoom > 0:
			zoom -= 0.1
	if keys[pygame.K_RIGHT]:
		angle += 0.01
	if keys[pygame.K_LEFT]:
		angle -= 0.01
	if keys[pygame.K_w]:
		pos_y -= 1
	if keys[pygame.K_s]:
		pos_y += 1
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
		for p in Point._reg:
			p.pos = p.ipos
			p.list = []
	#steps
	
	win.fill((0,0,0))
	draw_axis()
	for p in Point._reg:
		p.step()
		p.draw()
	
	print_stats()
	mouse_check()
	#update game
	pygame.display.update() 

pygame.quit()