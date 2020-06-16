from math import fabs
#import random
import pygame
pygame.init()

win_width = 800
win_height = 500
win = pygame.display.set_mode((win_width,win_height))

scale = 200
def transform(pos):
	x = pos[0]*scale
	y = pos[1]*scale
	x += win_width / 2
	y += win_height / 2
	x = int(x)
	y = int(y)
	return (x,y)
	
def sign(x):
	if x < 0:
		return -1
	elif x > 0:
		return 1
	return 0

################################################################################ Setup:

a = 0.5
b = 1.1

def x_next(pn):
	if fabs(pn[0]) < 0.5:
		return (2-a) * pn[0] - b * pn[1]
	else:
		return a * pn[0] - b * pn[1] + (1-a)* sign(pn[0])
def y_next(pn):
	if fabs(pn[0]) < 0.5:
		return -b * pn[0] + a * pn[1]
	else:
		return b * pn[0] + a * pn[1] - b * sign(pn[0])
	
def make_serie(start_pos, count):
	serie = []
	serie.append(start_pos)
	current_pos = start_pos
	for i in range(count):
		x_n = x_next(current_pos)
		y_n = y_next(current_pos)
		serie.append((x_n, y_n))
		current_pos = (x_n, y_n)
	return serie
		

b = 0


################################################################################ Main Loop:
run = True
while run:
	pygame.time.delay(100)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		run = False

	#background:
	win.fill((255,255,255))
	
	#step:
	
	serie = make_serie((1,1), 10000)
	b += 0.001
	
	
	#draw:
	for i in serie:
		#pygame.draw.circle(win, (0,0,0), transform((i[0],i[1])), 2)
		win.fill((0,0,0), (transform(i), (2, 2)))
	
	
	pygame.display.update()
pygame.quit()














