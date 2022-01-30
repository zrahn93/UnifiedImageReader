
"""
    Example:

        img = Image("test.tiff")
        region = img.get_region(0) # gives the top-left 512x512 region of the image
"""

import numpy as np

from ImageReader import ImageReader

DEFAULT_REGION_DIMS = (512,512)

class Image(object):

    def __init__(self, filepath, format=None):
        self.filepath = filepath
        if format is None:
            self.format = filepath.split('.')[-1]
        elif '.' in format:
            self.format = format.split('.')[-1]
        else:
            self.format = format
        self.reader = ImageReader.get_reader(self.filepath, self.format)

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
