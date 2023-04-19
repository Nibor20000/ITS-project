import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import scipy  # pip install scipy


np.random.seed(42069)

sizes = [50, 100, 500]


def white_img(size):
    img = np.zeros([size, size, 3], dtype=np.uint8)
    img[:] = 255
    return img


def random_color_img(size):
    img = np.random.rand(size, size, 3) * 255
    img = Image.fromarray(img.astype('uint8')).convert('RGBA')
    return img


def random_grey_img(size):
    img = np.random.rand(size, size) * 255
    img = Image.fromarray(img.astype('uint8')).convert('RGBA')
    return img


def random_repeat_img(size, block):
    img_small = np.random.rand(int(size / block), int(size / block), 3) * 255
    img = np.repeat(np.repeat(img_small, block, axis=0), block, axis=1)
    img = Image.fromarray(img.astype('uint8')).convert('RGBA')
    return img


# fig, axs = plt.subplots(5, len(sizes), figsize=(30, 30))

# for count, size in enumerate(sizes):
#     axs[0, count].imshow(white_img(size))
#     axs[1, count].imshow(random_color_img(size))
#     axs[2, count].imshow(random_grey_img(size))
#     axs[3, count].imshow(random_repeat_img(size, 2))
#     axs[4, count].imshow(random_repeat_img(size, 4))
#
# plt.show()


