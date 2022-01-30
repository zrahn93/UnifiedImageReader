
import numpy as np
import pyvips

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
    'dpcomplex': np.complex128
}

class RegionOutOfBoundsException(Exception):
    def __init__(self, region_identifier): super().__init__(region_identifier)

class VIPSAdapter:
    
    def __init__(self, filepath: str):

        if filepath.endswith(".svs"):
            raise NotImplementedError("svs images aren't really supported right now because of shenanigans - see this link for help: https://github.com/libvips/libvips/issues/2365")

        self._image = pyvips.Image.new_from_file(filepath)
        self._width = self._image.width
        self._height = self._image.height
    
    def get_image(self): return self._image
    
    def get_width(self): return self._width

    def get_height(self): return self._height

    def get_region(self, region_identifier, region_dims):
        
        if region_identifier >= self.number_of_regions(region_dims):
            raise RegionOutOfBoundsException(region_identifier)

        left, top = (-1, -1)
        width, height = region_dims

        if isinstance(region_identifier, int):

            width_regions = self._width // width
            top = (region_identifier // width_regions) * height
            left = (region_identifier % width_regions) * width
            print(width, height, width_regions, top, left)

        elif isinstance(region_identifier, tuple):

            if len(region_identifier) != 2:
                raise ValueError(f"{len(region_identifier) = }")
            raise NotImplementedError()

        output_img = self._image.crop(left, top, width, height)
        np_output = np.ndarray(buffer=output_img.write_to_memory(), dtype=FORMAT_TO_DTYPE[output_img.format], shape=[output_img.height, output_img.width, output_img.bands])
        return np_output

    def number_of_regions(self, region_dims):

        #Example: 512x512 region dimensions for a 1024x1024 image results in 4 512x512 regions
        width, height = region_dims
        return (self._width // width) * (self._height // height)
        