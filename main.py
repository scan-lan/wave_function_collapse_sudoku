from logic.create_grid import create_grid

def main():
    grid = create_grid(1)
    print(grid)
    for i in range(len(grid.grid)):
        print(" ".join(grid.box(i)))

if __name__ == "__main__":
    main()
