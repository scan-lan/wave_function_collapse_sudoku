from typing import Literal, TypeVar

T = TypeVar("T")

DimensionsKey = Literal["w", "h"]
Dimensions = dict[DimensionsKey, int]

Coords = tuple[int, int]

Cell = str
Grid = list[list[Cell]]

Matrix = list[list[T]]

Coefficients = set[Cell]
CoefficientMatrix = Matrix[Coefficients]

Weights = dict[Cell, int]
Collapsed = set[Coords]

GroupName = Literal["row", "col", "box"]
GroupConstraints = dict[GroupName, Coefficients]

HistoryEntry = tuple[Collapsed, Weights, CoefficientMatrix]
History = list[HistoryEntry]
