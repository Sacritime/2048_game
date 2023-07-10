from logic import get_moves, add_block, can_move
import time


def hello():
    """
    Hello :)
    """
    print("Hello!")
    time.sleep(1)
    print("Please, choose size of your game field.")
    time.sleep(2)
    print("For example: 3 3 or 4 5 (4 rows, 5 columns)")
    size = input(">>> ")
    while True:
        try:
            x, y = map(int, size.split(maxsplit=1))
            if x > 0 and y > 0:
                break
            else:
                size = input("X and y must be greater than 0. Try again\n>>> ")
        except ValueError:
            size = input("Something went wrong. Try again\n>>> ")

    for i in "|/-\\|/-\\|":
        print("\r" + i, end="")
        time.sleep(0.5)

    print("\rUhmm...")
    time.sleep(2)
    print("Can you help me a little, please?")
    time.sleep(2)
    print("It's my logo:\n"
          "╔═══╤═══╗\n"
          "║ 2 │ 0 ║\n"
          "╟───┼───╢\n"
          "║ 4 │ 8 ║\n"
          "╚═══╧═══╝\n")
    print("Do you see borders?")
    ans = input("Y or n >>> ").lower().strip()
    while True:
        if ans not in ("yes", "y", "no", "n"):
            ans = input("Please, be more careful. Try again\n>>> ")
        else:
            break
    if ans in "yes":
        flag = 0
        print("Oh! It's pretty good. Thank you very much!")
    else:
        flag = 1
        print("Oh... It's bad... But may be repaired!")
        time.sleep(2)
        print("And now, borders will be:\n"
              "+---+---+\n"
              "| 2 | 0 |\n"
              "+---+---+\n"
              "| 4 | 8 |\n"
              "+---+---+\n")
    time.sleep(3)
    print("Let's start our game!")
    return ("╔╗╚╝═─║│╤╧╟╢┼", "++++--||+++++")[flag], (x, y)


def i_have_already_seen_the_hello_scene():
    """
    idk how to name this func
    """
    print("Choose borders:")
    print("╔═╗   +-+\n"
          "║ ║   | |\n"
          "╚═╝   +-+")
    print("1 or 2?")
    ans = input(">>> ")
    while True:
        try:
            if int(ans) < 1:
                [][0]
            borders = ("╔╗╚╝═─║│╤╧╟╢┼",
                       "++++--||+++++")[int(ans)-1]
            break
        except ValueError:
            ans = input("Something went wrong. Try again\n>>> ")
        except IndexError:
            ans = input("Choose 1 or 2. Try again\n>>> ")
    print("Choose size of game field")
    ans = input(">>> ")
    while True:
        try:
            x, y = map(int, ans.split(maxsplit=1))
            if x > 0 and y > 0:
                break
            else:
                ans = input("X and y must be greater than 0. Try again\n>>> ")
        except ValueError:
            ans = input("Something went wrong. Try again\n>>> ")

    return borders, (x, y)


def print_field(blocks: list, borders: str | tuple | list):
    """
    prints list[list[None | Block]] matrix
    using given border signs (borders)
    """
    max_ = 100
    for line in blocks:
        for block in line:
            if block is not None:
                if max_ < block.num:
                    max_ = block.num
    len_ = len(str(max_))
    size = len(blocks[0]), len(blocks)
    strings = ""
    for i in range(size[1] + 1):
        for k in range(2):
            string = ""
            for j in range(size[0] + 1):
                if i == 0:
                    borders_ = (borders[0], borders[8], borders[1],
                                borders[4], borders[0])
                elif i != size[1]:
                    borders_ = (borders[6], borders[12], borders[11],
                                borders[5], borders[10])
                else:
                    borders_ = (borders[2], borders[9], borders[3],
                                borders[4], borders[2])
                if k == 0:
                    if j == 0:
                        string += borders_[4] + borders_[3]*len_
                    elif j != size[0]:
                        string += borders_[1] + borders_[3]*len_
                    else:
                        string += borders_[2]
                elif i != size[1]:
                    if j == 0:
                        block = blocks[i][j]
                        if block is None:
                            block = " "
                        else:
                            block = str(block.num)
                        string += borders[6] + block.rjust(len_//2+1
                                                           ).ljust(len_)
                    elif j != size[0]:
                        block = blocks[i][j]
                        if block is None:
                            block = " "
                        else:
                            block = str(block.num)
                        string += borders[7] + block.rjust(len_//2+1
                                                           ).ljust(len_)
                    else:
                        string += borders[6]
            strings += string + "\n"
    print(strings)


def start():
    print("Do you want to see hello scene?\n")
    print("(choose \"y\" if you haven't seen it yet)")
    ans = input("Y or n >>> ").lower().strip()
    while True:
        if ans not in ("yes", "y", "no", "n"):
            ans = input("Please, be more careful. Try again\n>>> ")
        else:
            break
    if ans in ("yes", "y"):
        return hello()
    else:
        return i_have_already_seen_the_hello_scene()


class Block:
    def __init__(self, num, was_merge=False) -> None:
        self.num = num
        self.was_merge = was_merge


def main():
    # borders, (x, y) = start()
    borders, (x, y) = "'''''''''''''", (3, 2)

    # create blank container
    blocks = []
    for _ in range(y):
        blocks.append([])
        for _ in range(x):
            blocks[-1].append(None)

    blocks = add_block(blocks, Block)

    sides = {
            "w": "up",
            "a": "left",
            "s": "down",
            "d": "right"
    }
    print("To \"swipe\" input w, a, s or d")

    while True:
        print_field(blocks, borders)
        ans = input("side >>> ")
        while ans not in ("w", "a", "s", "d"):
            ans = input("side >>> ")

        new = get_moves(blocks, sides[ans], Block)[1]
        if blocks != new:
            blocks = add_block(new, Block)
            if not can_move(blocks):
                print_field(blocks, borders)
                print("Game Over!")
                break


if __name__ == "__main__":
    main()
