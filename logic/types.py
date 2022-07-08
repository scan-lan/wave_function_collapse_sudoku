from typing import Callable, Literal, Optional, TypeAlias, TypeVar
from typing_extensions import Protocol

DimensionsKey: TypeAlias = Literal["w", "h"]
Dimensions: TypeAlias = dict[DimensionsKey, int]

Coords: TypeAlias = tuple[int, int]

Cell: TypeAlias = str
Grid: TypeAlias = list[list[Cell]]

T = TypeVar("T")
Matrix: TypeAlias = list[list[T]]

Coefficients: TypeAlias = set[Cell]
CoefficientMatrix: TypeAlias = Matrix[Coefficients]

Weights: TypeAlias = dict[Cell, int]
Collapsed: TypeAlias = set[Coords]

GroupName: TypeAlias = Literal["row", "col", "box"]
GroupConstraints: TypeAlias = dict[GroupName, Coefficients]

HistoryEntry: TypeAlias = tuple[Collapsed, Weights, CoefficientMatrix]
History: TypeAlias = list[HistoryEntry]


class Visualiser(Protocol):
    def __call__(
        self,
        coef_matrix: CoefficientMatrix,
        box_dimensions: Dimensions,
        new_collapse: Optional[Coords] = None,
        constraint_coords: Optional[Coords] = None,
        target_coords: Optional[Coords] = None,
        constraint_value: Optional[Cell] = None,
    ) -> bool:
        ...


OuterVisualiser: TypeAlias = Callable[[CoefficientMatrix, Dimensions], Visualiser]
