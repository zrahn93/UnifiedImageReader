
import os
from typing import Iterable, Union
import numpy as np

from unified_image_reader.adapters import Adapter, SlideIO, VIPS

FORMAT_ADAPTER_MAP = {
    "tif": VIPS,
    "tiff": VIPS,
    "svs": SlideIO
}

class UnsupportedFormatException(Exception): pass
class InvalidCoordinatesException(Exception): pass
class InvalidDimensionsException(Exception): pass

class ImageReader():

    def __init__(self, filepath: str, adapter: Union[Adapter, None] = None):
        # process filepath
        assert os.path.isfile(filepath), f"filepath is not a file --> {filepath}"
        self.filepath = filepath
        # initialize the adapter
        self.adapter = None
        if adapter is None: # choose based on file format
            format = self.filepath.split('.')[-1]
            adapter = FORMAT_ADAPTER_MAP.get(format)
            if adapter is None:
                raise UnsupportedFormatException(format)
        self.adapter = adapter()
    
    def get_region(self, region_identifier: Union[int, Iterable], region_dims: Iterable):
        # Make sure that region_coordinates is a tuple of length 2
        region_coordinates = None
        if isinstance(region_identifier, int):
            region_coordinates = self.region_index_to_coordinates(region_identifier, region_dims)
        elif isinstance(region_identifier, Iterable):
            assert (len(region_identifier) == 2)
            region_coordinates = region_identifier
        # make sure that the region is in bounds
        self.validate_region(region_coordinates, region_dims)
        # call the implementation
        return self._get_region(self, region_identifier, region_dims)

    def _get_region(self, region_coordinates, region_dims) -> np.ndarray: 
        return self.adapter.get_region(region_coordinates, region_dims)

    def number_of_regions(self, region_dims: Iterable):
        width, height = region_dims
        return (self.width // width) * (self.height // height)

    def validate_region(self, region_coordinates: Iterable, region_dims: Iterable) -> None:
        # first ensure coordinates are in bounds
        if not (len(region_coordinates) == 2): raise InvalidCoordinatesException(region_coordinates)
        x, y = region_coordinates
        if not (0 <= x < self.width): raise IndexError(x, self.width)
        if not (0 <= y < self.height): raise IndexError(y, self.height)
        # then check dimensions with coordinates
        if not (len(region_dims) == 2): raise InvalidDimensionsException(region_dims)
        width, height = region_dims
        if not (0 < width and x+width < self.width): raise IndexError(x, width, self.width)
        if not (0 < height and y+height < self.height): raise IndexError(y, height, self.height)

    def region_index_to_coordinates(self, region_index: int, region_dims: Iterable):
        width, height = region_dims
        width_regions = self.width // width
        top = (region_index // width_regions) * height
        left = (region_index % width_regions) * width
        return (top, left)

    @property
    def width(self):
        return self.adapter.get_width()

    @property
    def height(self):
        return self.adapter.get_height()
    
    @property
    def dims(self):
        return self.width, self.height
