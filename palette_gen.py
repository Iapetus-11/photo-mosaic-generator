from multiprocessing import Pool
import base64
import json
import cv2
import os

desired_dims = (16, 16)  # h, w

def process(image_file):
    print(f'Processing: {image_file}')

    img = cv2.imread(image_file, cv2.IMREAD_UNCHANGED)

    if img is None:
        return

    if img.shape[1] != desired_dims[1] or img.shape[0] != desired_dims[0]:
        img = cv2.resize(img, desired_dims)

    p_count = 0
    avgs = [0, 0, 0]  # bgr

    for row in img:
        for pixel in row:
            if len(pixel) > 3 and pixel[3] < 255:
                return

            avgs[0] += pixel[0]
            avgs[1] += pixel[1]
            avgs[2] += pixel[2]

            p_count += 1

    avgs[0] /= p_count
    avgs[1] /= p_count
    avgs[2] /= p_count

    avgs.reverse()  # turn into rgb

    b = base64.b64encode(cv2.imencode('.png', img)[1]).decode('utf-8')

    return [[int(avg/128) for avg in avgs], image_file], [[int(avg/64) for avg in avgs], image_file], [[int(avg/32) for avg in avgs], image_file], {image_file: b}

def main():
    print('Processing images...')

    image_files = (*filter((lambda file: (file.endswith('.png') or file.endswith('.jpg'))), next(os.walk('.'))[2]),)

    with Pool(8) as pool:
        raw_p = (*filter((lambda e: bool(e)), pool.map(process, image_files)),)

    map_bi = []
    map_quad = []
    map_oct = []
    palette = {}

    for res in raw_p:
        map_bi.append(res[0])
        map_quad.append(res[1])
        map_oct.append(res[2])
        palette.update(res[3])

    out = {
        'dims': desired_dims,
        'bi': map_bi,
        'quad': map_quad,
        'oct': map_oct,
        'palette': palette
    }

    print(f'Dumping images ({len(raw_p)} total)...')

    with open('map.json', 'w+') as out_f:
        out_f.write(json.dumps(out))

    print('Done!')

if __name__ == '__main__':
    main()
