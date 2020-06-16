import random
import turtle
import time


wn = turtle.Screen()
wn.title("chaos")
wn.bgcolor("white")
wn.setup(width = 800, height = 600)
wn.tracer(0)

size = 1

current_point = [0,0]

point = turtle.Turtle()
point.penup()
point.color("red")

def mat1(point_to,a,b,c,d,f):
	global size
	a*=size
	b*=size
	c*=size
	d*=size
	f*=size
	point_to[0] = (a*point_to[0] + b*point_to[1])
	point_to[1] = (c*point_to[0] + d*point_to[1] +f)

point_jump = [current_point[0],current_point[1]]

time1 = time.time()
random.seed((time1	- int(time1))*1000)

def game(point_j):
	rand = random.randint(1,100)
	
	if rand == 1:
		#print(1)
		mat1(point_j,0,0,0,0.25,0)
	elif rand >=  2 and rand <= 86:
		#print(2)
		mat1(point_j,0.85,0.04,-0.04,0.85,1.60)
	elif rand >= 87 and rand <= 93:
		#print(3)
		mat1(point_j,0.20,-0.26,0.23,0.22,1.60)
	elif rand >= 94 and rand <= 100:
		#print(4)
		mat1(point_j,-0.15,0.28,0.26,0.24,0.44)
		
	point.setposition(point_j[0]*100-50,point_j[1]*50-250)
	point.dot()
	
	
	

#main loop
while True:
	wn.update()
	game(point_jump)