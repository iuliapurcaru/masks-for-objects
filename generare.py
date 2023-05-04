import keras_cv
from PIL import Image

# saving images as jpeg for lossy compression
def save_images(images):
    for i in range(len(images)):
        img = Image.fromarray(images[i])
        img.save("resources/image-" + str(i) + ".jpeg")

# lossy compression
def compress_images(images):
    for i in range(len(images)):
        img = Image.open("image-" + str(i) + ".jpeg")
        img.save("resources/image-file-compressed-" + str(i) + ".jpeg", optimize=True, quality=10)
    return


# generating AI images using keras_cv
model = keras_cv.models.StableDiffusion(img_width=512, img_height=512)
images = model.text_to_image("an image of a realistic indigo refrigerator in a kitchen with white furniture", batch_size=3)

save_images(images)
compress_images(images)
