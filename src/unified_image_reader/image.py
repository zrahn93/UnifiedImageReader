
"""
    Example:

        img = Image("test.tiff")
        region = img.get_region(0) # gives the top-left 512x512 region of the image
"""

import contextlib

import numpy as np

from .config import DEFAULT_REGION_DIMS
from .image_reader import ImageReader

class Image(contextlib.AbstractContextManager):

    def __init__(self, filepath, reader=None):
        self.filepath = filepath
        self.reader = reader or ImageReader(filepath)
        self._iter = None

    def get_region(self, region_identifier, region_dims=DEFAULT_REGION_DIMS) -> np.ndarray:
        return self.reader.get_region(region_identifier, region_dims)

    def number_of_regions(self, region_dims=DEFAULT_REGION_DIMS) -> int:
        return self.reader.number_of_regions(region_dims)

    @property
    def width(self):
        return self.reader.width

    @property
    def height(self):
        return self.reader.height

    @property
    def dims(self):
        return self.width, self.height

    def __iter__(self):
        if self._iter is not None:
            raise Exception(type(self._iter), self._iter)
        else:
            self._iter = 0
        return self
    
    def __next__(self):
        if self._iter >= self.number_of_regions():
            raise StopIteration
        else:
            region = self.get_region(self._iter)
            self._iter += 1
            return region
