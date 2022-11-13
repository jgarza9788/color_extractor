
import numpy as np
from PIL import Image
import numpy as np
# import cv2

def downres(imagefile,scaleby=8):

    im = Image.open(imagefile)
    im = np.array(im)

    original_width = im.shape[1]
    original_height = im.shape[0]

    min_wh = min([original_width,original_height])

    if min_wh < 500:
        return imagefile

    width = original_width // scaleby
    height = original_height // scaleby

    print(im.shape)

    resized_image = np.zeros(shape=(height, width, im.shape[2]), dtype=np.uint8)

    scale = scaleby

    for i in range(0, original_height, scale):
        for j in range(0, original_width, scale):
            try:
                resized_image[ i//scale , j//scale] = np.mean(im[i:i + scale, j:j+scale], axis=(0, 1))
            except Exception as e:
                # print(str(e))
                pass

    # save file
    im = Image.fromarray(resized_image)
    fn = imagefile.split('.')
    fn = '.'.join(fn[:-1]) + '_small.' + fn[-1]
    im.save(fn)

    return fn



if __name__ == '__main__':

    # this is just a test
    downres(r"C:\Users\JGarza\GitHub\Python_Pro_Bootcamp\Sections\Section91_color_palette_gen\static\imgs\5a4f053d3cac434ada0c1cfda611629a.jpg")
