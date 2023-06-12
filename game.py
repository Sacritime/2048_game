import random
import time
from copy import deepcopy


def move_up(blocks):
    """
    returns MOVES and FINAL positions of blocks
    after moving it up
    """
    blocks_moves = []
    blocks_final = []

    for y, line in enumerate(blocks):
        # create rows
        blocks_moves.append(moves := [])
        blocks_final.append(final := [])

        for x, block in enumerate(line):
            # if (x, y) is not block or stays on top
            if block is None or y == 0:
                moves.append(0)
                final.append(block)
                continue

            # "count" is how many blocks up to top or another blocks
            count = 0
            while y - count > 1 and blocks_final[y - 1 - count][x] is None:
                count += 1

            # y_index of topmost block
            index = y - 1 - count
            # and the block itself
            up = blocks_final[index][x]

            # if the topmost block is block and not void
            if up is not None:

                # if value of the topmost block equal (x, y) one
                # and it hasn't been merged yet
                if up.num == block.num and not up.was_merge:
                    blocks_final[index][x].num *= 2
                    blocks_final[index][x].was_merge = True

                    # (x, y) block merges with the topmost,
                    #   so it has to move 1 cell more
                    count += 1
                else:
                    # if (x, y) block can't move up, it stays in the same place
                    if count == 0:
                        final.append(block)

                    # else, it moves 1 cell below the topmost
                    else:
                        blocks_final[index + 1][x] = block

            # if the topmost block is void
            else:
                # the (x, y) block moves to the very top
                blocks_final[index][x] = block
                # so it has to move 1 cell more
                count += 1

            # how many moves (x, y) block has to do
            moves.append(count)

            # if (x, y) block moves (more than 0 cells)
            if count != 0:
                # (x, y) cell becomes void
                final.append(None)

    return blocks_moves, blocks_final


def vertical_move(blocks, side):
    """
    returns MOVES and FINAL positions of blocks
    after moving it up or down
    """
    # flip horizontally, so "top" will be on bottom
    if side == "down":
        blocks = blocks[::-1]

    blocks_moves, blocks_final = move_up(blocks)

    # and flip again
    if side == "down":
        return blocks_moves[::-1], blocks_final[::-1]

    return blocks_moves, blocks_final


def horizontal_move(blocks, side):
    """
    returns MOVES and FINAL positions of blocks
    after moving it left or right
    """
    # create blank containers
    blocks1 = []
    blocks_moves = []
    blocks_final = []

    size = (range(len(blocks[0])), range(len(blocks)))
    for _ in size[0]:
        blocks1.append([])
        for _ in size[1]:
            blocks1[-1].append(None)

    for _ in size[1]:
        blocks_moves.append([])
        blocks_final.append([])
        for _ in size[0]:
            blocks_moves[-1].append(0)
            blocks_final[-1].append(None)

    # rotate blocks 90 degrees CCW, so "right" will be on top
    #   (we need it, because we have only "move_up" function)
    # and flip horizontally (idk why, but without flipping it doesn't work)

    # example:
    # 1 0 3
    # 2 2 2

    # v v v  rotate 90 CCW

    # 3 2
    # 0 2
    # 1 2

    # v v reflect horizontally

    # 2 3
    # 2 0
    # 2 1

    for i, line in enumerate(blocks):
        for j, block in enumerate(reversed(line)):
            blocks1[j][i] = block

    # replace given blocks with rotated ones
    blocks = blocks1
    del blocks1

    # flip vertically, so "left" will be on top
    if side == "left":
        blocks = blocks[::-1]

    # get MOVES that blocks have to do to achive FINAL ones' positions
    blocks_moves1, blocks_final1 = move_up(blocks)

    # fill containers with got values
    #   (rotate and flip again)
    for i, moves_, blocks_ in zip(
                                  range(len(blocks_moves)),
                                  reversed(blocks_moves1),
                                  reversed(blocks_final1)
                                  ):
        for j, move, block in zip(range(len(moves_)), moves_, blocks_):
            blocks_moves[j][i] = move
            blocks_final[j][i] = block

    del blocks_moves1, blocks_final1

    # flip verticlally, so "left" will be right and vice versa
    if side == "left":
        moves = []
        final = []
        for i, j in zip(blocks_moves, blocks_final):
            moves.append(i[::-1])
            final.append(j[::-1])
        return moves, final

    return blocks_moves, blocks_final


def get_moves(blocks, side):
    """
    Returns MOVES that blocks have to do
    to achive FINAL ones' positions
    """
    if side in ("down", "up"):
        moves, final = vertical_move(blocks, side)
    else:
        moves, final = horizontal_move(blocks, side)

    for line in final:
        for block in line:
            if block is not None:
                block.was_merge = False

    return moves, final


def add_block(blocks):
    """
    adds random block to given list of blocks
    """

    y = []

    for i, line in enumerate(blocks):
        # if at least one cell in row is None
        if not all(line):
            # we can add block to it, so we save this row
            y.append((i, line))
    # then choose random row from all, where we can add block
    try:
        chosen_y = random.choice(y)
    except IndexError:
        return 1

    # do the same with "x" in chosen row
    x = []
    for i, cell in enumerate(chosen_y[1]):
        if not cell:
            x.append(i)
    chosen_x = random.choice(x)

    # chosen_y = (y, [...]), now we need only "y"
    chosen_y = chosen_y[0]

    num = random.choice((2, 2, 2, 2, 4))
    blocks[chosen_y][chosen_x] = Block1(num)
    return 0


class Block1:
    def __init__(self, num, was_merge=False) -> None:
        self.num = num
        self.was_merge = was_merge


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
    return flag, (x, y)


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
                        string += borders[6] + block.rjust(len_//2+1).ljust(len_)
                    elif j != size[0]:
                        block = blocks[i][j]
                        if block is None:
                            block = " "
                        else:
                            block = str(block.num)
                        string += borders[7] + block.rjust(len_//2+1).ljust(len_)
                    else:
                        string += borders[6]
            strings += string + "\n"
    print(strings)


def main():
    print("Do you want to see hello scene?\n(choose \"y\" if you haven't seen it yet)")
    ans = input("Y or n >>> ").lower().strip()
    while True:
        if ans not in ("yes", "y", "no", "n"):
            ans = input("Please, be more careful. Try again\n>>> ")
        else:
            break
    if ans in ("yes", "y"):
        borders, (x, y) = hello()
        borders = ("╔╗╚╝═─║│╤╧╟╢┼",
               "++++--||+++++")[borders]
    else:
        borders, (x, y) = i_have_already_seen_the_hello_scene()

    blocks = []
    for _ in range(y):
        blocks.append([])
        for _ in range(x):
            blocks[-1].append(None)

    add_block(blocks)
    side = {
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

        new = get_moves(blocks, side[ans])[1]
        if blocks != new:
            blocks = new
            add_block(blocks)

        if all(
                [add_block(get_moves(deepcopy(new), i)[1]
                           ) for i in ("up", "down", "right", "left")]):
            print_field(blocks, borders)
            print("Game Over!")
            break



if __name__ == "__main__":
    main()
