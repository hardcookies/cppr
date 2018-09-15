#!/usr/bin/env python

import os
import random

import cv2
import numpy

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

FONT_DIR = "./fonts"
FONT_HEIGHT = 32  # Pixel size to which the chars are resized

CHARS = "京津晋冀蒙辽吉黑沪苏浙皖闽赣鲁豫鄂湘粤桂琼渝川贵云藏陕甘青宁新"

def make_char_ims(font_path, output_height):
    font_size = output_height * 4

    # 加载字体并创建一个字体对象
    font = ImageFont.truetype(font_path, font_size)

    height = max(font.getsize(c)[1] for c in CHARS)

    for c in CHARS:
        width = font.getsize(c)[0]
        im = Image.new("P", (width, height), 0)

        draw = ImageDraw.Draw(im)
        draw.text((0, 0), c, 255, font=font)
        scale = float(output_height) / height
        im = im.resize((int(width * scale), output_height))
        yield c, numpy.array(im).astype(numpy.float32) / 255.

def load_fonts(folder_path):
    font_char_ims = {}
    fonts = [f for f in os.listdir(folder_path) if f.endswith('tf')]
    for font in fonts:
        font_char_ims[font] = dict(make_char_ims(os.path.join(folder_path,
                                                              font),
                                                 FONT_HEIGHT))
    return fonts, font_char_ims


fonts, font_char_ims = load_fonts(FONT_DIR)

a_char_im = font_char_ims[random.choice(fonts)][random.choice(CHARS)]
im = Image.fromarray(a_char_im * 255)
im.show()