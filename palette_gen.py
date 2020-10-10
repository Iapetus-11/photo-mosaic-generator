from multiprocessing import Pool
import base64
import json
import cv2
import os

def pal_from_image(image_file, dest_dims, verbose):
    if verbose:
        print(f'Processing: {image_file}')

    img = cv2.imread(image_file, cv2.IMREAD_UNCHANGED)

    if img is None:
        return

    if img.shape[1] != dest_dims[1] or img.shape[0] != dest_dims[0]:
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

    return (
        [[int(avg/128) for avg in avgs], image_file],
        [[int(avg/64) for avg in avgs], image_file],
        [[int(avg/32) for avg in avgs], image_file],
        {image_file: b}
    )

class Palette:
    def __init__(self, *, resolution: int = 16, source_dir: str = '.', verbose: bool = False):
        self.source_dir = source_dir
        self.dest_dims = (resolution, resolution)
        self.data = None
        self.verbose = verbose

    def process(self):
        if self.verbose: print('Processing images...')

        image_files = (*filter((lambda file: (file.endswith('.png') or file.endswith('.jpg'))), next(os.walk(self.source_dir))[2]),)

        with Pool(8) as pool:
            raw_p = (*filter((lambda e: bool(e)), pool.map(pal_from_image, image_files)),)

        map_bi = []
        map_quad = []
        map_oct = []
        palette = {}

        for res in raw_p:
            map_bi.append(res[0])
            map_quad.append(res[1])
            map_oct.append(res[2])
            palette.update(res[3])

        self.data = {
            'dims': desired_dims,
            'bi': map_bi,
            'quad': map_quad,
            'oct': map_oct,
            'palette': palette
        }

        if self.verbose: print('Done!')
