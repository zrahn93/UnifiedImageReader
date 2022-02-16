
"""
    Example:

        img = Image("test.tiff")
        region = img.get_region(0) # gives the top-left 512x512 region of the image
"""

import numpy as np

from .image_reader import ImageReader

DEFAULT_REGION_DIMS = (512, 512)


class Image(object):

    def __init__(self, filepath, reader=None):
        self.filepath = filepath
        self.reader = reader or ImageReader(filepath)

    def get_region(self, region_identifier, region_dims=DEFAULT_REGION_DIMS) -> np.ndarray:
        return self.reader.get_region(region_identifier, region_dims)

    def number_of_regions(self, region_dims=DEFAULT_REGION_DIMS) -> int:
        return self.reader.number_of_regions(region_dims)

    @property
    def width(self):
        return self.reader.get_width()

    @property
    def height(self):
        return self.reader.get_height()

    def get_dimensions(self):
        return self.width, self.height
