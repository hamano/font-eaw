#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

# 画像のサイズ
font_size = 64
width, height = font_size * 16, font_size * 18

COLOR_WHITE=(0xFF, 0xFF, 0xFF)
COLOR_BLACK=(0, 0, 0)
image = Image.new('RGB', (width, height), color=COLOR_WHITE)

draw = ImageDraw.Draw(image)

font_path = "build/EAW-CONSOLE-Regular.ttf"
#font_path = "build/EAW-CONSOLE-Bold.ttf"
font = ImageFont.truetype(font_path, font_size)

x, y = 0, 0

with open('sample/sample.txt', 'r') as f:
    for line in f:
        print(line.rstrip())
        draw.text((x, y), line, font=font, fill=COLOR_BLACK)
        y += font_size

image.save("sample/sample.png")

image.show()
