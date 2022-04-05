from cs50 import get_int


x = get_int("Height: ")

if x < 1 or x > 8:
    while x < 1 or x > 8:
        x = get_int("Height: ")

for row in range(x):

        for space in range(x - row - 1, 0, -1):
            print(" ", end="")

        for hash in range(0, row+1, 1):
            print("#", end="")

        print("  ", end="")

        for hash in range(0, row+1, 1):
            print("#", end="")

        print()

