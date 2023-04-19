import matplotlib.pyplot as plt

from image_generation import *
from lossless_compressions import *
from lossly_compressions import *

# image = random_color_img(512)
# gif_compression = GIF_compress(image)
# print(len(np.array2string(gif_compression)))
#
# huffman_compression = Huffman(np.array2string(gif_compression))
# huffman_encode = huffman_compression.encode()
# # print(huffman_encode)
#
# deflate_compression = Deflate(np.array2string(gif_compression))
# deflate_encode = deflate_compression.encode()
# # print(deflate_encode)
#
# rle_compression = RLE(np.array2string(gif_compression))
# rle_encode = rle_compression.encode()
# print(type(rle_encode))
# print(rle_encode)
#
# lzm_compression = LZM()
# lzm_encode = lzm_compression.encode(np.array2string(gif_compression))
# # print(lzm_encode)
#
# aec_compression = AEC(np.array2string(gif_compression))
# aec_encode = aec_compression.encode()


# print(type(aec_encode))
# print(aec_encode)

def np_to_string(array):

    return ''.join(str(s) for s in array.ravel())


def display_result(image, id):
    # im = np.array2string(image, formatter={'int':lambda x: hex(x)}, precision=0)
    im = np_to_string(image)
    print(len(im))
    # print(np.asarray(image).shape)

    huffman_compression = Huffman(im)
    huffman_encode = huffman_compression.encode()

    deflate_compression = Deflate(im)
    deflate_encode = deflate_compression.encode()

    rle_compression = RLE(im)
    rle_encode = rle_compression.encode()

    lzm_compression = LZM()
    lzm_encode = lzm_compression.encode(im)

    aec_compression = AEC(im)
    aec_encode = aec_compression.encode()

    fig, (ax1, ax2) = plt.subplots(1, 2, )
    ax1.imshow(image)
    ax2.bar(['org','Huf', 'Def', 'RLE', 'LZM', 'AEC'],
            [len(bytes(im, 'utf-8')),len(huffman_encode), len(deflate_encode), len(rle_encode), len(lzm_encode), len(aec_encode)/8])
    name = './plots/image' + str(id) + '.png'
    plt.savefig(name)
    plt.show()



for i in range(1, 11):
    image = random_color_img(i*16)
    gif_compression = GIF_compress(image)
    jpeg_compression = JPEG_compress(image)

    display_result(gif_compression, 'random_color_image_gif' + str(i*16))
    display_result(jpeg_compression, 'random_color_image_jpeg' + str(i*16))

    image = random_repeat_img(i * 16, 4)
    gif_compression = GIF_compress(image)
    jpeg_compression = JPEG_compress(image)

    display_result(gif_compression, 'random_repeat_image_gif' + str(i*16))
    display_result(jpeg_compression, 'random_repeat_image_jpeg' + str(i*16))

    image = random_grey_img(i * 16)
    gif_compression = GIF_compress(image)
    jpeg_compression = JPEG_compress(image)

    display_result(gif_compression, 'random_grey_image_gif' + str(i*16))
    display_result(jpeg_compression, 'random_grey_image_jpeg' + str(i*16))
