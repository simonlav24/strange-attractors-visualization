import math
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

################################################################################ Setup:

a = 0.3
d = 0

def x_next(pn):
	return a * pn[0] + (1-a) * (1-d*(pn[1]**2))
def y_next(pn):
	return pn[0]
	
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
		
#serie = make_serie((1,1), 10000)

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
	if d < 2.24:
		d += 0.01
	
	
	#draw:
	for i in serie:
		#pygame.draw.circle(win, (0,0,0), transform((i[0],i[1])), 2)
		win.fill((0,0,0), (transform(i), (2, 2)))
	
	
	pygame.display.update()
pygame.quit()














