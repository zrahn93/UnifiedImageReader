
"""
    Utility functions and classes for the Unified Image Reader
"""

from typing import NewType, Tuple, Union

RegionDimensions = NewType('RegionDimensions', Tuple[int, int])

RegionIndex = NewType('RegionIndex', int)
RegionCoordinates = NewType('RegionCoordinates', Tuple[int, int])
RegionIdentifier = NewType(
    'RegionIdentifier', Union[RegionIndex, RegionCoordinates])

FilePath = NewType('FilePath', str)
