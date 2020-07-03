import imager as img

# test of circles with varoius parametres

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