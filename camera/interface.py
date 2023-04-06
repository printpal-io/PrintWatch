from amcrest import AmcrestCamera
import PIL.Image as Image
from io import BytesIO
from typing import List, Union



class Camera:

    def __init__(
            self,
            ip_address : str = '192.168.1.10',
            port : int = 80,
            username : str = 'admin',
            password : str = 'admin'
        ):
        self.camera = AmcrestCamera(
                        ip_address,
                        port,
                        username,
                        password
                        ).camera

        self.byte_frame = None
        self.pil_image = None

    def _snap_internal(self):
        self.byte_frame = self.camera.snapshot(stream=False)

    def snap(self):
        self._snap_internal()
        self.pil_image = Image.open(BytesIO(self.byte_frame))

    def _crop(
            self,
            image : Image = None,
            region : tuple = ()
        ) -> Image:
        if len(region) < 4:
            return None

        if image is None:
            if self.pil_image is not None:
                return self.pil_image.crop(region)
            else:
                return None
        else:
            return image.crop(region)

    def crop_all(
            self,
            regions : List[tuple],
            image : Image = None
        )-> List:
        # Do not support custom images for now
        if image is not None:
            return False

        # Return full size image if regions don't exist,
        # if image doesn't exist, return False
        if len(regions) < 1 or len(regions[0]) < 4:
            if self.pil_image is not None:
                return self.pil_image
            return False

        subregions = []
        for region in regions:
            subregions.append(self._crop(region=region))

        return subregions


if __name__ == '__main__':
    cam = Camera(
            ip_address='192.168.1.108',
            port=80,
            username='admin',
            password='Favoritemovie1'
        )
    cam.snap()
    vals = cam.crop_all(
            [
                (0, 0, 640, 640),
                (640, 640, 1280, 1280)
            ]
        )
    cam.pil_image.show()
    vals[0].show()
    vals[1].show()
