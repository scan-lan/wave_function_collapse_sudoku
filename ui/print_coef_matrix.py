from logic.types import BoxDimensions, Cell, Coefficients, CoefficientMatrix

def pad_cell(cell: Cell, cell_width: int) -> str:
    return (' ' * (cell_width - len(cell))) + cell

def print_coef_matrix(matrix: CoefficientMatrix, box_dimensions: BoxDimensions) -> None:
    matrix_str = ""
    # just for brevity
    width = box_dimensions["w"]
    height = box_dimensions["h"]
    num_coefficients = width * height
    valid_coefficients: Coefficients = {str(n) for n in range(1, num_coefficients + 1)}
    cell_width = len(str(num_coefficients))
    grid_line_coefficient = (width * cell_width + 1) * width * height + (height - 1) * 2

    for row_num, row in enumerate(matrix):
        for n, m in enumerate(range(1, height + 1)):
            string_row: list[str] = []
            for i, coefficients in enumerate(row):
                sorted_coefficient = [pad_cell(cell if cell in coefficients else " ", cell_width) for cell in sorted(list(valid_coefficients), key=int)[n*width:width*m]]
                string_row.append("".join(sorted_coefficient) + (" | " if i % width == width - 1 and i != len(row) - 1 else " "))
            matrix_str += "".join(string_row) + "\n"
        matrix_str += ("—" if row_num % height == height - 1 and row_num != len(matrix) - 1 else " ") * grid_line_coefficient + "\n"

    print(matrix_str)
