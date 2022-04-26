from logic.create_grid import create_grid

def main():
    grid = create_grid(3, 4)
    print(grid)

    for i in range(len(grid.grid)):
        print(grid.box(i))

if __name__ == "__main__":
    main()
