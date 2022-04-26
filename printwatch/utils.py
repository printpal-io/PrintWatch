import PIL.Image as Image
from PIL import ImageDraw
from math import sqrt, ceil
import os


class ROI():
    def _get_cropped_area(image, coords : tuple):
        #image must be an Image object
        return image.crop(coords)

    def get_cropped_areas(image, regions : list):
        return [_get_cropped_area(image, region) for region in regions]

    def preview_slices(image, regions):
        base_image = ImageDraw.Draw(image)

        slices = get_cropped_areas(image, regions)
        for ele in slices:
            idx = slices.index(ele)

            base_image.rectangle([(regions[idx][0], regions[idx][1]), (regions[idx][2], regions[idx][3])], fill = None, outline = 'red', width = int(ceil(0.002 * sqrt(image.size[0] * image.size[1]))))
            ele.show()
        image.show()
