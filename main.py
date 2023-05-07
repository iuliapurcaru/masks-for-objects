import numpy as np
from PIL import Image
import cv2

# cropping the object

def crop_image(index):
    with open("resources/text_files/image-" + str(index) + ".txt") as fp:
        for i, line in enumerate(fp):
            array = line.split()
            if array[0] == '72':
                break

    array = list(map(float, array))
    class_, x_center, y_center, width, height = array

    img = Image.open("resources/generated_images/image-" + str(index) + ".jpeg")
    img_height, img_width = img.size
    left = (x_center - width/2) * img_width
    top = (y_center - height/2) * img_height
    right = (x_center + width/2) * img_width
    bottom = (y_center + height/2) * img_height

    img = img.crop((left, top, right, bottom))
    img.save("resources/crops/crop-" + str(index) + ".jpeg")


# creating the mask based on the color

def create_mask(index):
    img = cv2.imread("resources/crops/crop-" + str(index) + ".jpeg")
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_color = np.array([100, 40, 40])
    upper_color = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_color, upper_color)

    result = cv2.bitwise_and(img, img, mask=mask)
    cv2.imwrite("resources/masks/mask-" + str(index) + ".jpeg", result)


# converting mask to YUV

def convert_yuv(index):
    img = cv2.imread("resources/crops/crop-" + str(index) + ".jpeg")

    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    cv2.imwrite("resources/crops_YUV/crop-yuv-" + str(index) + ".jpeg", img_yuv)

    y, u, v = cv2.split(img_yuv)
    lut_u = np.array([[[i, 255-i, 0] for i in range(256)]], dtype=np.uint8)
    lut_v = np.array([[[0, 255-i, i] for i in range(256)]], dtype=np.uint8)
    y = cv2.cvtColor(y, cv2.COLOR_GRAY2BGR)
    u = cv2.cvtColor(u, cv2.COLOR_GRAY2BGR)
    v = cv2.cvtColor(v, cv2.COLOR_GRAY2BGR)

    u_mapped = cv2.LUT(u, lut_u)
    v_mapped = cv2.LUT(v, lut_v)

    result = np.vstack([img, y, u_mapped, v_mapped])

    cv2.imwrite("resources/crops_YUV/crop-yuv-channels-" + str(index) + ".jpeg", result)


# making transparent mask

def transparent_mask(index):
    img = cv2.imread("resources/masks/mask-" + str(index) + ".jpeg")

    img_transparent = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, alpha = cv2.threshold(img_transparent, 2, 255, cv2.THRESH_BINARY)

    b, g, r = cv2.split(img)
    rgba = [b, g, r, alpha]
    img_transparent = cv2.merge(rgba, 4)

    cv2.imwrite("resources/masks/mask-" + str(index) + ".png", img_transparent)


for i in range(3):  # works for images 0, 1 and 2
    crop_image(i)
    create_mask(i)
    convert_yuv(i)
    transparent_mask(i)
