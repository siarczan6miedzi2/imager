import numpy as np
from PIL import Image
from time import time
import math

# a*a is about 1.5 times faster than a**2
# so it's going to be used,
# at least for O(n^2) algorhithms

WIDTH = 1000
HEIGHT = 2500

def ellipse(cx, cy, Rx, Ry, color, fade=0, fxA=0, fyA=0, fxB=WIDTH-1, fyB=HEIGHT-1):
	if fade > 100: return # throw error
	xLowest = Rx*(100-fade)//100
	xHighest = Rx*(100+fade)//100
	yLowest = Ry*(100-fade)//100
	yHighest = Ry*(100+fade)//100
	RHighest = (1+1.0*fade/100)
	RLowest = (1-1.0*fade/100)
	
	for x in range(cx-xHighest, cx+xHighest):
		for y in range(cy-yHighest, cy+yHighest):
			if (x >= fxA and x <= fxB and y >= fyA and y <= fyB): # in frame
				RCurrent = (1.0*(x-cx)*(x-cx)/(Rx*Rx)) + (1.0*(y-cy)*(y-cy)/(Ry*Ry)) # square of the radius
				if (RCurrent < RLowest*RLowest): data[y][x] = color # colored inner Ellipse
				elif (RCurrent > RHighest*RHighest): pass # no ellipse
				else: # shaded outer ellipse-ring-oid
					if (fade > 0): # only needed if any fade
						weight = (1.0*(RHighest-math.sqrt(RCurrent))/(RHighest-RLowest))**2 # weight squared looks nicer
						for i in range(0, 3):
							data[y][x][i] = int(1.0*data[y][x][i]*(1-weight)) + int(1.0*color[i]*weight)

def circle(cx, cy, R, color, fade=0, fxA=0, fyA=0, fxB=WIDTH-1, fyB=HEIGHT-1):
	ellipse(cx, cy, R, R, color, fade, fxA, fyA, fxB, fyB)

# def circle(cx, cy, R, color, fade=0, fxA=0, fyA=0, fxB=WIDTH-1, fyB=HEIGHT-1):
#	if fade > 100: return # throw error
#	if fade == 0: # faster version if no fade needed
#		for x in range(cx-R, cx+R):
#			for y in range(cy-R, cy+R):
#				if (x >= fxA and x <= fxB and y >= fyA and y <= fyB): # in frame
#					if ((x-cx)*(x-cx) + (y-cy)*(y-cy) <= R*R):
#						data[y][x] = color
#	else:
#		lowest = R*(100-fade)//100
#		highest = R*(100+fade)//100
#		for x in range(cx-highest, cx+highest):
#			for y in range(cy-highest, cy+highest):
#				if (x >= fxA and x <= fxB and y >= fyA and y <= fyB): # in frame
#					RCurrent = (x-cx)*(x-cx) + (y-cy)*(y-cy)
#					if (RCurrent < lowest*lowest): # colored "inner" circle
#						data[y][x] = color
#					elif (RCurrent > highest*highest): pass # no circle
#					else: # shaded "outer" ring
#						weight = (1.0*(highest-math.sqrt(RCurrent))/(highest-lowest))**2 # weight squared looks nicer
#						for i in range(0, 3):
#							data[y][x][i] = int(1.0*data[y][x][i]*(1-weight)) + int(1.0*color[i]*weight)
					
def gradient(xa, ya, xb, yb, color, direction, fxA=0, fyA=0, fxB=WIDTH-1, fyB=HEIGHT-1):
	if direction == 'down':
		for y in range(ya, yb+1):
			weight = (1.0*(yb+1-y)/(yb+1-ya))**2
			for x in range(xa, xb+1):
				if (x >= fxA and x <= fxB and y >= fyA and y <= fyB): # in frame
					for i in range(0, 3):
						data[y][x][i] = int(1.0*data[y][x][i]*(1-weight)) + int(1.0*color[i]*weight)
	elif direction == 'up':
		for y in range(ya, yb+1):
			weight = (1.0*(ya-y)/(ya-yb+1))**2
			for x in range(xa, xb+1):
				if (x >= fxA and x <= fxB and y >= fyA and y <= fyB): # in frame
					for i in range(0, 3):
						data[y][x][i] = int(1.0*data[y][x][i]*(1-weight)) + int(1.0*color[i]*weight)
	elif direction == 'right':
		for x in range(xa, xb+1):
			weight = (1.0*(xb+1-x)/(xb+1-xa))**2
			for y in range(ya, yb+1):
				if (x >= fxA and x <= fxB and y >= fyA and y <= fyB): # in frame
					for i in range(0, 3):
						data[y][x][i] = int(1.0*data[y][x][i]*(1-weight)) + int(1.0*color[i]*weight)
	elif direction == 'left':
		for x in range(xa, xb+1):
			weight = (1.0*(xa-x)/(xa-xb+1))**2
			for y in range(ya, yb+1):
				if (x >= fxA and x <= fxB and y >= fyA and y <= fyB): # in frame
					for i in range(0, 3):
						data[y][x][i] = int(1.0*data[y][x][i]*(1-weight)) + int(1.0*color[i]*weight)
						
def rectangle(xa, ya, xb, yb, color, fade=0, fxA=0, fyA=0, fxB=WIDTH-1, fyB=HEIGHT-1):
	if fade > 100: return # throw error
	if fade == 0: # faster version if no fade needed
		for x in range(xa, xb):
			for y in range(ya, yb):
				if (x >= fxA and x <= fxB and y >= fyA and y <= fyB): # in frame
					data[y][x] = color
	if fade == 100: # reduction to ellipse
		ellipse((xb+xa)//2, (yb+ya)//2, (xb-xa)//2, (yb-ya)//2, color, 100, fxA, fyA, fxB, fyB)
	else:
		# calculate the borders of inner full rectangle and outer shaded region
		xaInner = int(xa+(xb-xa)*fade/200) # 100 to convert fade, 2 for 2 sides
		xaOuter = int(xa-(xb-xa)*fade/200)
		yaInner = int(ya+(yb-ya)*fade/200)
		yaOuter = int(ya-(yb-ya)*fade/200)
		xbInner = int(xb-(xb-xa)*fade/200)
		xbOuter = int(xb+(xb-xa)*fade/200)
		ybInner = int(yb-(yb-ya)*fade/200)
		ybOuter = int(yb+(yb-ya)*fade/200)
		# inner full rectangle
		for x in range(xaInner, xbInner):
			for y in range(yaInner, ybInner):
				if (x >= fxA and x <= fxB and y >= fyA and y <= fyB): # in frame
					data[y][x] = color
		# outer shaded quarter-ellipses
		ellipse(xaInner, yaInner, (xaInner-xaOuter)//2, (yaInner-yaOuter)//2, color, fade=100, fxB=xaInner, fyB=yaInner)
		ellipse(xbInner, yaInner, (xaInner-xaOuter)//2, (yaInner-yaOuter)//2, color, fade=100, fxA=xbInner, fyB=yaInner)
		ellipse(xaInner, ybInner, (xaInner-xaOuter)//2, (yaInner-yaOuter)//2, color, fade=100, fxB=xaInner, fyA=ybInner)
		ellipse(xbInner, ybInner, (xaInner-xaOuter)//2, (yaInner-yaOuter)//2, color, fade=100, fxA=xbInner, fyA=ybInner)
		# outer gradients
		gradient(xaInner+1, yaOuter, xbInner-1, yaInner, color, 'up')
		gradient(xbInner, yaInner+1, xbOuter, ybInner-1, color, 'right')
		gradient(xaInner+1, ybInner, xbInner-1, ybOuter, color, 'down')
		gradient(xaOuter, yaInner+1, xaInner, ybInner-1, color, 'left')

def rectangleCentered(x, y, w, h, color, fade=0):
	rectangle(int(x-w/2), int(y-h/2), int(x+w/2), int(y+h/2), color, fade)

def main():

	# the image vector; white background
	data = np.full((HEIGHT, WIDTH, 3), 255, dtype=np.uint8)

	start = time()
	
	img = Image.fromarray(data)
	img.save('tt.png')
		
	print(time()-start)
	
if __name__ == "__main__": main()

