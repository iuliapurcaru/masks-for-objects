from PIL import Image

fp = open("image-compressed-2.txt")
for i, line in enumerate(fp):
    if i == 1:
        line = fp.readline()
        break
fp.close()

array = line.split()
array = list(map(float, array))

x_center = array[1] * 100
y_center = array[2] * 100
width = array[3] * 100
height = array[4] * 100

left = x_center - width/2 - height/2
top = y_center - width/2 - height/2
right = x_center + width/2 + height/2
bottom = y_center + width/2 + height/2

left = 54
top = 150
right = 180
bottom = 430

img = Image.open(r"imagini/image-2.jpeg")
img_res = img.crop((left, top, right, bottom))
img_res.show()