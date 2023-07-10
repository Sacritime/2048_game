import random


def make_extra_container(n: int, m: int, defalt_value):
    """
    returns n*m matrix with default value

    for example:
        n = 2, m = 3
        default_value = 0
    =>
        [[0, 0, 0],
         [0, 0, 0]]

    """

    container = []
    for _ in range(n):
        container.append([])
        for _ in range(m):
            container[-1].append(defalt_value)

    return container


def move_up(blocks, block_):

    # for i in blocks:
    #     for j in i:
    #         if j is None:
    #             print(0, end=" ")
    #         else:
    #             print(j.num, end=" ")
    #     print()
    # print()
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
                    blocks_final[index][x] = block_(up.num*2, True)

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
    # for i in blocks_moves:
    #     for j in i:
    #         print(j, end=" ")
    #     print()
    # print()
    return blocks_moves, blocks_final


def vertical_move(blocks, side, block_):
    """
    returns MOVES and FINAL positions of blocks
    after moving it up or down
    """
    # flip horizontally, so "top" will be on bottom
    if side == "down":
        blocks = blocks[::-1]

    blocks_moves, blocks_final = move_up(blocks, block_)

    # and flip again
    if side == "down":
        return blocks_moves[::-1], blocks_final[::-1]

    return blocks_moves, blocks_final


def horizontal_move(blocks, side, block_):
    """
    returns MOVES and FINAL positions of blocks
    after moving it left or right
    """
    # create blank containers
    blocks1 = make_extra_container(len(blocks[0]), len(blocks), None)
    blocks_moves = make_extra_container(len(blocks), len(blocks[0]), 0)
    blocks_final = make_extra_container(len(blocks), len(blocks[0]), None)

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

    # v v flip horizontally

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
    blocks_moves1, blocks_final1 = move_up(blocks, block_)

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


def get_moves(blocks, side, block_):
    """
    Returns MOVES that blocks have to do
    to achive FINAL ones' positions.
    block_ is a class that takes 2 arguments: num, was_merge
    """
    if side in ("down", "up"):
        moves, final = vertical_move(blocks, side, block_)
    else:
        moves, final = horizontal_move(blocks, side, block_)

    for line in final:
        for block in line:
            if block is not None:
                block.was_merge = False

    for i in moves:
        for j in i:
            print(j, end=" ")
        print()
    print()
    return moves, final


def add_block(blocks, block_):
    """
    adds random block to given list of blocks.
    block_ is a class that takes 2 arguments: num, was_merge
    """

    extra_container = []
    for line in blocks:
        extra_container.append(line.copy())

    y = []

    for i, line in enumerate(extra_container):
        # if at least one cell in row is None
        if not all(line):
            # we can add block to it, so we save this row
            y.append((i, line))
    # then choose random row from all, where we can add block
    try:
        chosen_y = random.choice(y)
    except IndexError:
        return None

    # do the same with "x" in chosen row
    x = []
    for i, cell in enumerate(chosen_y[1]):
        if not cell:
            x.append(i)
    chosen_x = random.choice(x)

    # chosen_y = (y, [...]), now we need only "y"
    chosen_y = chosen_y[0]

    num = random.choice((2, 2, 2, 2, 4))
    extra_container[chosen_y][chosen_x] = block_(num, False)
    return extra_container


def can_move(blocks):
    len_y = len(blocks)
    len_x = len(blocks[0])
    for y in range(len_y - 1):
        for x in range(len_x):
            bl1 = blocks[y][x]
            bl2 = blocks[y+1][x]
            if bl1 is not None and bl2 is not None:
                if bl1.num == bl2.num:
                    return True
            else:
                return True

    for y in range(len_y):
        for x in range(len_x - 1):
            bl1 = blocks[y][x]
            bl2 = blocks[y][x+1]
            if bl1.num == bl2.num:
                return True

    return False
