import imager as img
from random import randint as rand

# circles with varoius parametres

imager = img.Imager(1000, 1000)

for i in range(5):
	for j in range(5):
		x = i*200+100
		y = j*200+100
		R = (i+1)*10
		f = j*25
		colR = i*50
		colG = 0
		colB = j*50
		imager.circle(x, y, R, [colR, colG, colB], fade=f)

imager.save("circles.png")

# eye-on-a-peacock's-tail pattern made out of circles

imager = img.Imager(1000, 1000)

for R in range(400, 0, -40):
	imager.circle(R, 499, R, [rand(0, 255), rand(0, 255), rand(0, 255)])

imager.save("peacock.png")
