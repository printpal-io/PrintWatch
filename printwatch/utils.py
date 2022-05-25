import PIL.Image as Image
from PIL import ImageDraw
from math import sqrt, ceil
import os
import base64
import io

class FileSupportedException(Exception):
    def __init__(self):
        self.message = 'Filetype not supported for image loading'

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


class ImageFileLoader():
    def __init__(self):
        self.queue = []

    def load_file(self, filename):
        self.queue.append([filename, self._file_loader(filename)])

    def _get(self, idx=0):
        try:
            element = self.queue[idx]
            self.queue.pop(idx)
            return element
        except IndexError:
            return []


    def _file_loader(self, fn):
        try:
            im = Image.open(os.path.join(os.getcwd(), fn))
            if fn.endswith('.png'):
                im = im.convert('RGB')
            img_byte_arr = io.BytesIO()
            im.save(img_byte_arr, format='png')
            image_bytes = img_byte_arr.getvalue()
        except:
            raise FileSupportedException()

        return image_bytes
