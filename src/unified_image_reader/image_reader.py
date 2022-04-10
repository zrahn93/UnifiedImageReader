"""
    Image Reader

    1) Give it a filepath for a supported image format, and optionally an adapter to operate on the image file
    2) If an adapter is not provided as an argument, one will be created from a mapping of formats to adapters
    3) Include utility methods for validation and extraction of region parameters
    4) Include functionality for getting image regions using the reading behavior of an adapter
"""

import os
from typing import Iterable, Union
import numpy as np

from unified_image_reader.adapters import Adapter, SlideIO, VIPS

FORMAT_ADAPTER_MAP = {
    "tif": VIPS,
    "tiff": VIPS,
    "svs": SlideIO
}


class UnsupportedFormatException(Exception):
    pass


class InvalidCoordinatesException(Exception):
    pass


class InvalidDimensionsException(Exception):
    pass


class ImageReader():
    """
    ImageReader _summary_

    :raises UnsupportedFormatException: _description_
    :raises TypeError: _description_
    :raises an: _description_
    :raises IndexError: _description_
    :raises InvalidCoordinatesException: _description_
    :raises InvalidDimensionsException: _description_
    :return: _description_
    :rtype: _type_
    """    

    """ Interface for adapters which specify reading behavior """

    def __init__(self, filepath: str, adapter: Union[Adapter, None] = None):
        """
        __init__ _summary_

        :param filepath: _description_
        :type filepath: str
        :param adapter: _description_, defaults to None
        :type adapter: Union[Adapter, None], optional
        :raises UnsupportedFormatException: _description_
        """        
        """
        Initialize ImageReader object

        Parameters:
            filepath (str): Filepath to image file to be opened
            adapter(Adapter | None): Object which specifies reading behavior (optional)

        """
        self.filepath = filepath
        # initialize the adapter
        self.adapter = None
        if adapter is None:  # choose based on file format
            image_format = self.filepath.split('.')[-1]
            adapter = FORMAT_ADAPTER_MAP.get(image_format)
            if adapter is None:
                raise UnsupportedFormatException(image_format)
        self.adapter = adapter(filepath)

    def get_region(self, region_identifier: Union[int, Iterable], region_dims: Iterable):

        """
         _summary_

        :raises TypeError: _description_
        :return: _description_
        :rtype: _type_
        """        
        """
        Get a rectangular region from an image using an adapter's implementation after validating and extracting region data

        Parameters:
            region_identifier(int | Tuple[int]): An (x,y) coordinate tuple or an indexed region based on region dimensions
            region_dims(Tuple[int]): An (x,y) coordinate tuple representing the region dimensions

        Returns:
            np.ndarray: A numpy array representative of the rectangular region from the image
        """
        # Make sure that region_coordinates is a tuple of length 2
        region_coordinates = None
        if isinstance(region_identifier, int):
            region_coordinates = self.region_index_to_coordinates(
                region_identifier, region_dims)
        elif isinstance(region_identifier, Iterable):
            assert (len(region_identifier) == 2)
            region_coordinates = region_identifier
        else:
            raise TypeError(
                f"region_identifier should be either int or Iterable but is {type(region_identifier)=}, {region_identifier=}")
        # make sure that the region is in bounds
        self.validate_region(region_coordinates, region_dims)
        # call the implementation
        return self._get_region(region_coordinates, region_dims)

    def _get_region(self, region_coordinates, region_dims) -> np.ndarray:
        """
        _get_region _summary_

        :param region_coordinates: _description_
        :type region_coordinates: _type_
        :param region_dims: _description_
        :type region_dims: _type_
        :return: _description_
        :rtype: np.ndarray
        """        
        """
        Call an adapter's implementation to get a rectangular image region

        Parameters:
            region_coordinates(Tuple[int]): An (x,y) coordinate tuple representing the top-left pixel of the region
            region_dims(Tuple[int]): A tuple representing the width and height dimensions of the region

        Returns:
            np.ndarray: A numpy array representative of the rectangular region from the image
        """
        return self.adapter.get_region(region_coordinates, region_dims)

    def number_of_regions(self, region_dims: Iterable):
        """
        number_of_regions _summary_

        :param region_dims: _description_
        :type region_dims: Iterable
        :return: _description_
        :rtype: _type_
        """        
        """
        Calculates the number of regions in the image based on the dimensions of each region

        Parameters:
            region_dims(Tuple[int]): A tuple representing the width and height dimensions of the region

        Returns:
            int: The number of regions
        """
        width, height = region_dims
        return (self.width // width) * (self.height // height)

    def validate_region(self, region_coordinates: Iterable, region_dims: Iterable) -> None:
        """
        validate_region _summary_

        :param region_coordinates: _description_
        :type region_coordinates: Iterable
        :param region_dims: _description_
        :type region_dims: Iterable
        :raises an: _description_
        :raises IndexError: _description_
        :raises InvalidCoordinatesException: _description_
        :raises InvalidDimensionsException: _description_
        """        
        """
        Checks that a region is within the bounds of the image

        Parameters:
             region_coordinates(Tuple[int]): An (x,y) coordinate tuple representing
                                             the top-left pixel of the region
             region_dims(Tuple[int]): A tuple representing the width and height dimensions
                                      of the region
        """
        def not_valid():
            """
            not_valid _summary_

            :raises an: _description_
            :raises IndexError: _description_
            """            
            """ Wrapper function to raise an error on invalid coordinates or dimensions"""
            raise IndexError(region_coordinates, region_dims, self.dims)
        # first ensure coordinates are in bounds
        if not (len(region_coordinates) == 2):
            raise InvalidCoordinatesException(region_coordinates)
        left, top = region_coordinates
        if not (0 <= left < self.width):
            not_valid()
        if not (0 <= top < self.height):
            not_valid()
        # then check dimensions with coordinates
        if not (len(region_dims) == 2):
            raise InvalidDimensionsException(region_dims)
        region_width, region_height = region_dims
        if not (0 < region_width and left+region_width <= self.width):
            not_valid()
        if not (0 < region_height and top+region_height <= self.height):
            not_valid()

    def region_index_to_coordinates(self, region_index: int, region_dims: Iterable):
        """
        region_index_to_coordinates _summary_

        :param region_index: _description_
        :type region_index: int
        :param region_dims: _description_
        :type region_dims: Iterable
        :return: _description_
        :rtype: _type_
        """        
        """
        Converts the index of a region to coordinates of the top-left pixel of the region

        Parameters:
            region_index(int): The nth region of the image (where n >= 0) based on region dimensions
            region_dims(Tuple[int]): A tuple representing the width and height dimensions of the region

        Returns:
            Tuple(int): An (x,y) coordinate tuple representing the top-left pixel of the region
        """
        region_width, region_height = region_dims
        width_regions = self.width // region_width
        left = (region_index % width_regions) * region_width
        top = (region_index // width_regions) * region_height
        return (left, top)

    @property
    def width(self):
        """
        width _summary_

        :return: _description_
        :rtype: _type_
        """        
        return self.adapter.get_width()

    @property
    def height(self):
        """
        height _summary_

        :return: _description_
        :rtype: _type_
        """        
        return self.adapter.get_height()

    @property
    def dims(self):
        """
        dims _summary_

        :return: _description_
        :rtype: _type_
        """        
        return self.width, self.height
