import slideio

class RegionOutOfBoundsException(Exception):
    def __init__(self, region_identifier): super().__init__(region_identifier)

class SLIDEIOAdapter:

    def __init__(self, filepath):
        
        self._image = slideio.open_slide(filepath, "SVS").get_scene(0)
        self._width, self._height = self._image.size

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
        
        np_array = self._image.read_block((left, top, width, height))
        return np_array
    
    def number_of_regions(self, region_dims):
        # Example: 512x512 region dimensions for a 1024x1024 image results in 4 512x512 regions
        width, height = region_dims
        return (self._width // width) * (self._height // height)

        
