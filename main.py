from PIL import Image


def crop_image(index):
    with open("resurse/image-" + str(index) + ".txt") as fp:
        for i, line in enumerate(fp):
            array = line.split()
            if array[0] == '72':
                break

    array = list(map(float, array))
    class_, x_center, y_center, width, height = array

    img = Image.open("resurse/image-" + str(index) + ".jpeg")
    img_height, img_width = img.size
    left = (x_center - width/2) * img_width
    top = (y_center - height/2) * img_height
    right = (x_center + width/2) * img_width
    bottom = (y_center + height/2) * img_height

    img = img.crop((left, top, right, bottom))
    img.save("resurse/image-crop-" + str(index) + ".jpeg")


crop_image(2)
