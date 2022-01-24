
import abc
import numpy as np
import os

class UnsupportedFormatException(Exception):

    def __init__(self, format): super().__init__(format)

class ImageReader(abc.ABC):

    def __init__(self, filepath: str):

        assert os.path.isfile(filepath), f"filepath is not a file --> {filepath}"
        self.filepath = filepath
    
    @classmethod
    def get_reader(cls, filepath: str, format: str):

        print(filepath, format)

        for reader_class in cls.__subclasses__():
            print(reader_class)
            print(dir(reader_class))
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

class ImageReaderTIFF(ImageReader):

    def __init__(self, filepath: str):

        super().__init__(filepath)

        # TODO - maybe you need to keep a reference to the image file here? PIL's Image initializer is a good example of why
        raise NotImplementedError()

    def get_region(self, region_identifier, region_dims) -> np.ndarray:

        # TODO
        raise NotImplementedError()
    
    def number_of_regions(self, region_dims) -> int:

        # TODO
        raise NotImplementedError()
    
    @classmethod
    def accepted_formats(cls):
        return ["tiff", "tif"]

if __name__ == "__main__":

    reader = ImageReader.get_reader("test.tiff", "tif")

    print(reader)
