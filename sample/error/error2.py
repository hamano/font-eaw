#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

# 画像のサイズ
font_size = 64
width, height = font_size * 4, font_size

COLOR_WHITE=(0xFF, 0xFF, 0xFF)
COLOR_BLACK=(0, 0, 0)
image = Image.new('RGB', (width, height), color=COLOR_WHITE)

draw = ImageDraw.Draw(image)

font_path = "build/EAW-CONSOLE-Regular.ttf"
font = ImageFont.truetype(font_path, font_size)

draw.text((0, 0), '※', font=font, fill=COLOR_BLACK)
draw.text((font_size * 1, 0), '※', font=font, fill=COLOR_BLACK)
draw.text((font_size * 2, 0), '', font=font, fill=COLOR_BLACK)
draw.text((font_size * 3, 0), '', font=font, fill=COLOR_BLACK)
image = image.resize((int(width / 2), height))

image = image.quantize(8)
image.save("sample/error/error2.png")
image.show()
