from logic.types import Cell, Weights


def initialise_weights(size: int) -> Weights:
    return {str(n): size for n in range(1, size + 1)}


def update_weights(weights: Weights, value: Cell):
    weights[value] -= 1
