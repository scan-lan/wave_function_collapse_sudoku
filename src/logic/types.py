from typing import Literal, TypeVar

T = TypeVar("T")

BoxDimensionsKey = Literal["w", "h"]
BoxDimensions = dict[BoxDimensionsKey, int]

CoordKey = Literal["y", "x"]
Coords = dict[CoordKey, int]

Cell = str
Grid = list[list[Cell]]

Matrix = list[list[T]]

Coefficients = set[Cell]
CoefficientMatrix = Matrix[Coefficients]

# rename to groupname
GroupName = Literal["row", "col", "box"]
GroupConstraints = dict[GroupName, Coefficients]
