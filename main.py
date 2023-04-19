from image_generation import *
from lossless_compressions import *
from lossly_compressions import *

image = random_color_img(512)
gif_compression = GIF_compress(image)
# print(len(np.array2string(gif_compression)))

huffman_compression = Huffman(np.array2string(gif_compression))
huffman_encode = huffman_compression.encode()
# print(huffman_encode)

deflate_compression = Deflate(np.array2string(gif_compression))
deflate_encode = deflate_compression.encode()
# print(deflate_encode)

rle_compression = RLE(np.array2string(gif_compression))
rle_encode = rle_compression.encode()
print(type(rle_encode))
print(rle_encode)

lzm_compression = LZM()
lzm_encode = lzm_compression.encode(np.array2string(gif_compression))
# print(lzm_encode)

aec_compression = AEC(np.array2string(gif_compression))
aec_encode = aec_compression.encode()
# print(type(aec_encode))
# print(aec_encode)
