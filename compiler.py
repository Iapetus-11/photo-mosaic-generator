import numpy as np
import random
import base64
import json
import cv2

def im_from_64(b):
    return cv2.imdecode(np.frombuffer(base64.b64decode(b), np.uint8), cv2.IMREAD_COLOR)

def draw_image(canvas, img, x, y):
    for i, row in enumerate(img):
        for j, pix in enumerate(row):
            canvas[i+y][j+x] = pix

with open('map.json', 'r') as data:
    data = json.load(data)

palette_bi = dict([(tuple(entry[0]), entry[1]) for entry in data['bi']])
palette_quad = dict([(tuple(entry[0]), entry[1]) for entry in data['quad']])
palette_oct = dict([(tuple(entry[0]), entry[1]) for entry in data['oct']])

palette_map = {k: im_from_64(v) for k, v in data['palette'].items()}

source = cv2.imread('../../Downloads/rick.png')
#source = cv2.imread('../thanos_grin.png')
source = cv2.resize(source, (int(int(source.shape[1]/data['dims'][1])*4), int(int(source.shape[0]/data['dims'][0])*4)))
source = cv2.blur(source, (2, 2))

#cv2.imshow('image', source)
#cv2.waitKey(0)

xi = data['dims'][1]
yi = data['dims'][1]

img = np.zeros((source.shape[0]*data['dims'][0], source.shape[1]*data['dims'][1], 3), np.uint8)

y = 0
for row in source:
    x = 0
    for pix in row: # bgr
        pal_key = palette_oct.get((int(pix[2]/32), int(pix[1]/32), int(pix[0]/32)))

        if pal_key is None:
            pal_key = palette_quad.get((int(pix[2]/64), int(pix[1]/64), int(pix[0]/64)))

        if pal_key is None:
            pal_key = palette_bi.get((int(pix[2]/128), int(pix[1]/128), int(pix[0]/128)))

        if pal_key is None:
            print(f'No match for pixel ({pix[2]}, {pix[1]}, {pix[0]}) found, using random.')
            pal_key = palette_oct[random.choice([*palette_oct.keys()])]

        draw_image(img, palette_map[pal_key], x, y)

        x += xi
    y += yi

cv2.imshow('image', cv2.resize(img, (int(img.shape[1]/1), int(img.shape[0]/1))))
cv2.waitKey(0)
