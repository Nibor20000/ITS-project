import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import scipy  # pip install scipy

def GIF_compress(img):
    img_array = np.asarray(img)
    # print(type(img_array))
    compressed = np.floor_divide(img_array, 32) * 32
    # print(compressed)
    return compressed


# image = random_repeat_img(10, 2)
# plt.imshow(image)
# plt.show()
# print(type(image))
# plt.imshow(GIF_compress(image))
# plt.show()
def dct2(a):
    return scipy.fftpack.dct(scipy.fftpack.dct(a, axis=0, norm='ortho'), axis=1, norm='ortho')


def idct2(a):
    return scipy.fftpack.idct(scipy.fftpack.idct(a, axis=0, norm='ortho'), axis=1, norm='ortho')


def JPEG_compress(img):  # https://pi.math.cornell.edu/~web6140/TopTenAlgorithms/JPEG.html
    # Convert to YCbCr instead of RGB
    img_YCbCr = img.convert('YCbCr')
    # Convert to np array, so we can use it
    img_array = np.array(img_YCbCr, dtype=np.uint8)

    # Downsampling
    img_array[:,  2] = np.floor_divide(img_array[:,  2], 2) *2
    img_array[:,  3] = np.floor_divide(img_array[:,  3], 2) *2
    # DCT compression
    imsize = img_array.shape
    dct = np.zeros(imsize)
    # Do 8x8 DCT on image (in-place)
    for i in np.r_[:imsize[0]:8]:
        for j in np.r_[:imsize[1]:8]:
            dct[i:(i + 8), j:(j + 8)] = dct2(img_array[i:(i + 8), j:(j + 8)])
    thresh = 0.012
    dct_thresh = dct * (abs(dct) > (thresh * np.max(dct)))
    im_dct = np.zeros(imsize)

    # Reapply the DCT to the image
    for i in np.r_[:imsize[0]:8]:
        for j in np.r_[:imsize[1]:8]:
            im_dct[i:(i + 8), j:(j + 8)] = idct2(dct_thresh[i:(i + 8), j:(j + 8)])
    compressed = np.floor(im_dct).astype(int)

    return compressed


# img = random_color_img(16)
# plt.imshow(JPEG_compress(img))
# plt.show()