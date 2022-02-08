
import abc
import os
import numpy as np

from adapters import vips, slideio

# TODO: Add pydoc to top of file, to each class, and each method


class UnsupportedFormatException(Exception):

    def __init__(self, format): super().__init__(format)


class ImageReader(abc.ABC):

    def __init__(self, filepath: str):

        assert os.path.isfile(
            filepath), f"filepath is not a file --> {filepath}"
        self.filepath = filepath

    @classmethod
    def get_reader(cls, filepath: str, format: str):

        for reader_class in cls.__subclasses__():
            if format.lower() in reader_class.accepted_formats():
                return reader_class(filepath)

        raise UnsupportedFormatException(format)

    @classmethod
    @abc.abstractmethod
    def accepted_formats(cls) -> list: pass

    @abc.abstractmethod
    def get_region(self, region_identifier, region_dims) -> np.ndarray: pass

    @abc.abstractmethod
    def number_of_regions(self, region_dims) -> int: pass

    @abc.abstractmethod
    def get_width(self) -> int: pass

    @abc.abstractmethod
    def get_height(self) -> int: pass


class ImageReaderTIFF(ImageReader):

    def __init__(self, filepath: str):

        super().__init__(filepath)

        # TODO - maybe you need to keep a reference to the image file here? PIL's Image initializer is a good example of why
        # The image reference is currently unused here
        self._adapter = VIPS.VIPSAdapter(filepath)
        self._image = self._adapter.get_image()

    def get_region(self, region_identifier, region_dims) -> np.ndarray:

        return self._adapter.get_region(region_identifier, region_dims)

    def number_of_regions(self, region_dims) -> int:

        return self._adapter.number_of_regions(region_dims)

    def get_width(self):

        return self._adapter.get_width()

    def get_height(self):

        return self._adapter.get_height()

    @classmethod
    def accepted_formats(cls):
        return ["tiff", "tif"]


class ImageReaderSVS(ImageReader):

    def __init__(self, filepath):

        super().__init__(filepath)
        self._adapter = slideio.SLIDEIOAdapter(filepath)
        self._image = self._adapter.get_image()

    def get_region(self, region_identifier, region_dims) -> np.ndarray:

        return self._adapter.get_region(region_identifier, region_dims)

    def number_of_regions(self, region_dims) -> int:

        return self._adapter.number_of_regions(region_dims)

    def get_width(self):

        return self._adapter.get_width()

    def get_height(self):

        return self._adapter.get_height()

    @classmethod
    def accepted_formats(cls):
        return ["svs"]
