from dahuffman import HuffmanCodec  # pip install dahuffman
import numpy as np
import rle  # pip install python-rle

import deflate  # pip install deflate

from arithmetic_compressor import AECompressor  # pip install arithmetic_compressor
from arithmetic_compressor.models import StaticModel
from arithmetic_compressor.models import PPMModel

from math import floor, ceil
from typing import AnyStr

ASCII_TO_INT: dict = {i.to_bytes(1, 'big'): i for i in range(256)}
INT_TO_ASCII: dict = {i: b for b, i in ASCII_TO_INT.items()}

original_string = "hello world"


class Huffman:
    def __init__(self, data):
        self.codec = HuffmanCodec.from_data(data)
        self.data = data

    def encode(self):
        return self.codec.encode(self.data)

    def decode(self, data):
        return self.codec.decode(data)


# test = Huffman(original_string)
# test_encode = test.encode()
# print(test.decode(test_encode))


class RLE:
    def __init__(self, data):
        self.data = data
        self.rle = rle

    def encode(self):

        # return ''.join(str(s) for s in (''.join(str(s) for s in self.rle.encode(self.data))))
        return bytes(''.join(np.asarray(self.rle.encode(self.data))[0]), 'utf-8')

    def decode(self, data):
        return ''.join(self.rle.decode(data[0], data[1]))


# test = RLE(original_string)
# test_encode = test.encode()
# print(test.decode(test_encode))


class Deflate:
    def __init__(self, data):
        self.level = 6
        self.data = data

    def encode(self,):
        # return self.rle.encode(self.data)
        return deflate.gzip_compress(bytes(self.data, 'utf-8'), self.level)

    def decode(self, data):
        return deflate.gzip_decompress(data).decode("utf-8")

#
# test = Deflate(original_string)
# test_encode = test.encode()
# print(test.decode(test_encode))


class LZM:
    def encode(self, data: AnyStr) -> bytes:
        if isinstance(data, str):
            data = data.encode()
        keys: dict = ASCII_TO_INT.copy()
        n_keys: int = 256
        compressed: list = []
        start: int = 0
        n_data: int = len(data) + 1
        while True:
            if n_keys >= 512:
                keys = ASCII_TO_INT.copy()
                n_keys = 256
            for i in range(1, n_data - start):
                w: bytes = data[start:start + i]
                if w not in keys:
                    compressed.append(keys[w[:-1]])
                    keys[w] = n_keys
                    start += i - 1
                    n_keys += 1
                    break
            else:
                compressed.append(keys[w])
                break
        bits: str = ''.join([bin(i)[2:].zfill(9) for i in compressed])
        return int(bits, 2).to_bytes(ceil(len(bits) / 8), 'big')

    def decode(self, data: AnyStr) -> bytes:
        if isinstance(data, str):
            data = data.encode()
        keys: dict = INT_TO_ASCII.copy()
        bits: str = bin(int.from_bytes(data, 'big'))[2:].zfill(len(data) * 8)
        n_extended_bytes: int = floor(len(bits) / 9)
        bits: str = bits[-n_extended_bytes * 9:]
        data_list: list = [int(bits[i * 9:(i + 1) * 9], 2)
                           for i in range(n_extended_bytes)]
        previous: bytes = keys[data_list[0]]
        uncompressed: list = [previous]
        n_keys: int = 256
        for i in data_list[1:]:
            if n_keys >= 512:
                keys = INT_TO_ASCII.copy()
                n_keys = 256
            try:
                current: bytes = keys[i]
            except KeyError:
                current = previous + previous[:1]
            uncompressed.append(current)
            keys[n_keys] = previous + current[:1]
            previous = current
            n_keys += 1
        return b''.join(uncompressed).decode("utf-8")


# test = LZM()
# test_encode = test.encode(original_string)
# print(test.decode(test_encode))


class AEC:
    def __init__(self, data):
        self.N = len(data)
        self.model = PPMModel(list(set(data)), k=len(list(set(data))))
        self.coder = AECompressor(self.model)
        self.data = data

    def encode(self):
        bits = self.coder.compress(self.data)
        string = "".join(str(b) for b in bits)
        return bytes(string, 'utf-8')

    def decode(self, data):
        return ''.join(self.coder.decompress((data), self.N))


# test = AEC(original_string)
# test_encode = test.encode()
# print(test.decode(test_encode))
