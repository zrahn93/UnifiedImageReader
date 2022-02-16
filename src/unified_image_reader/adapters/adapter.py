
import abc
from typing import Iterable

import numpy as np

class Adapter(abc.ABC):
    
    @abc.abstractmethod
    def get_region(self, region_coordinates: Iterable, region_dims: Iterable) -> np.ndarray: pass

    @abc.abstractmethod
    def get_width() -> int: pass

    @abc.abstractmethod
    def get_height() -> int: pass
