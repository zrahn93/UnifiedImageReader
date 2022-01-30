import pyvips
import math
import numpy as np

FORMAT_TO_DTYPE = {
    'uchar': np.uint8,
    'char': np.int8,
    'ushort': np.uint16,
    'short': np.int16,
    'uint': np.uint32,
    'int': np.int32,
    'float': np.float32,
    'double': np.float64,
    'complex': np.complex64,
    'dpcomplex': np.complex128,
}
class RegionOutOfBoundsException(Exception):
    
    def __init__(self, region_identifier): super().__init__(region_identifier)

class TiffAdapter:
    
    def __init__(self, filepath: str):
        
        self._image = pyvips.Image.new_from_file(filepath)
        self._width = self._image.width
        self._height = self._image.height
    
    def get_image(self):
        
        return self._image
    
    def get_region(self, region_identifier, region_dims):
        
        if region_identifier >= self.number_of_regions(region_dims):
            raise RegionOutOfBoundsException(region_identifier)
        
        top = 0
        left = 0
        if self._height <= (region_identifier * region_dims[1]):
            left = ((region_identifier * region_dims[1]) // self._height) * region_dims[0]
            top = min(region_identifier * region_dims[1] % self._height, region_identifier * region_dims[1])
        else:
            top = region_identifier * region_dims[1]
        
        if (top + region_dims[1]) > self._height:
            height = self._height - top
        else:
            height = region_dims[1]
        
        if (left + region_dims[0] ) > self._width:
            width = self._width - left
        else:
            width = region_dims[0]
        
        output_img = self._image.crop(left, top, width, height)
        np_output = np.ndarray(buffer=output_img.write_to_memory(), dtype=FORMAT_TO_DTYPE[output_img.format], shape=[output_img.height, output_img.width, output_img.bands])
        return np_output

    def number_of_regions(self, region_dims):
        #Example: 512x512 region dimensions for a 1024x1024 image results in 4 512x512 regions
        return math.ceil((self._width * self._height) / (region_dims[0] * region_dims[1]))