from typing import Literal, TypeVar

T = TypeVar("T")

BoxDimensionsKey = Literal["w"] | Literal["h"]
BoxDimensions = dict[BoxDimensionsKey, int]

CoordKey = Literal["y"] | Literal["x"]
Coords = dict[CoordKey, int]

Cell = str
Grid = list[list[Cell]]

Matrix = list[list[T]]

Coefficients = set[Cell]
CoefficientMatrix = Matrix[Coefficients]

GroupNames = Literal["row"] | Literal["col"] | Literal["box"]
GroupConstraints = dict[GroupNames, Coefficients]
