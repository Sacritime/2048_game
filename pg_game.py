from logic import get_moves, add_block, make_extra_container, can_move

import pygame as pg
pg.init()


def get_swipe(event, was_pressed):
    if event.type == pg.MOUSEBUTTONDOWN:
        if event.button == 1:
            was_pressed = True
    elif event.type == pg.KEYDOWN and 78 < event.scancode < 83:
        keys = {
            79: "right",
            80: "left",
            81: "down",
            82: "up"
        }
        return keys[event.scancode], False
    elif event.type == pg.MOUSEBUTTONUP:
        if event.button == 1:
            was_pressed = False
    elif event.type == pg.MOUSEMOTION:
        (x, y) = pg.mouse.get_rel()
        if was_pressed:
            if abs(x) > 20:
                return ("left", "right")[x > 0], False
            elif abs(y) > 20:
                return ("up", "down")[y > 0], False
    return None, was_pressed


def draw_new_block(size: int,
                   color: tuple[int, int, int] = (0, 0, 0),
                   num: int | None = None):
    surf = pg.Surface((size, size), pg.SRCALPHA, 32)

    pg.draw.rect(surface=surf,
                 color=color,
                 rect=(0, 0, surf.get_width(), surf.get_height()),
                 border_radius=int(size*0.1))

    if num is not None:
        # if bg color is dark
        if sum(color) < 200:
            text_color = "white"

        # if bg color is light
        else:
            text_color = "black"

        font_size = int(size/2)
        font = pg.font.Font(None, font_size)
        text_surf = font.render(str(num), True, text_color)

        # while text surface's width is more than 80% of surf's width
        while text_surf.get_width() > size*0.8:
            # make text size 90% of previous size
            font_size = int(font_size * 0.9)
            font = pg.font.Font(None, font_size)
            text_surf = font.render(str(num), True, text_color)

        surf.blit(text_surf, text_surf.get_rect(center=(size/2, size/2)))

    return surf


def draw_static(surf: pg.Surface,
                palette: dict[str: tuple | str],
                sizes: dict[str: int],
                blocks: list[list]):
    surf.fill(palette["grid_color"])
    grid_w = sizes["grid_w"]
    block_w = sizes["block_w"]
    for y_, line in enumerate(blocks):
        for x_, block in enumerate(line):
            x = grid_w * (x_ + 1) + block_w * x_
            y = grid_w * (y_ + 1) + block_w * y_
            if block is None:
                surf.blit(draw_new_block(block_w), (x, y))
            else:
                surf.blit(block.surf, (x, y))


def draw_move(palette: dict[str: tuple | str],
              sizes: dict[str: float],
              blocks: list[list],
              side: str,
              moves: list[int]):

    flag = False
    for line in moves:
        if any(line):
            flag = True
            break

    if not flag:
        return

    global game_surf_wh, game_surf_xy, WIDTH, HEIGHT, sc
    grid_w = sizes["grid_w"]
    block_w = sizes["block_w"]
    moving_blocks = []
    template_surf = pg.Surface(game_surf_wh)

    blocks_ = make_extra_container(HEIGHT, WIDTH, None)

    draw_static(template_surf, palette, sizes, blocks_)
    for y_, *line in zip(range(HEIGHT), blocks, moves):
        for x_, block, move in zip(range(WIDTH), *line):
            x = grid_w * (x_ + 1) + block_w * x_
            y = grid_w * (y_ + 1) + block_w * y_
            if move == 0 and block is not None:
                template_surf.blit(block.surf, (x, y))
            elif move != 0:
                moving_blocks.append((x, y, block, move))

    fps = 40
    if side == "up":
        dx = 0
        dy = - game_surf_wh[1]/HEIGHT/fps
    elif side == "down":
        dx = 0
        dy = game_surf_wh[1]/HEIGHT/fps
    elif side == "left":
        dx = - game_surf_wh[0]/WIDTH/fps
        dy = 0
    elif side == "right":
        dx = game_surf_wh[0]/WIDTH/fps
        dy = 0

    clock = pg.time.Clock()
    for i in range(fps):
        surf = template_surf.copy()
        for x, y, block, move_count in moving_blocks:
            surf.blit(block.surf, (x + dx*i*move_count, y + dy*i*move_count))
        sc.blit(surf, (game_surf_xy))
        clock.tick(fps*3)
        pg.display.flip()


class Block:
    def __init__(self, num, was_merge=False):
        global block_w, block_colors
        self.num = num
        self.was_merge = was_merge
        self.surf = draw_new_block(block_w, block_colors[num], num)


def main():
    global block_w, block_colors, WIDTH, HEIGHT, game_surf_wh, game_surf_xy, sc
    W, H = (0, 0)
    sc = pg.display.set_mode((W, H))
    W, H = sc.get_size()
    WIDTH, HEIGHT = 3, 3
    cell_w = min(W//WIDTH, H//HEIGHT)
    game_surf_wh = (cell_w*WIDTH, cell_w*HEIGHT)
    game_surf = pg.Surface(game_surf_wh)
    game_surf_xy = (W - game_surf_wh[0])/2, (H - game_surf_wh[1])/2

    palette = {
        "bg_color": "black",
        "grid_color": "grey20"
    }

    block_colors = {
        2: (255, 255, 255),
        4: (255, 0, 0),
        8: (0, 255, 0),
        16: (0, 0, 255),
        32: (255, 255, 0),
        64: (255, 0, 255),
        128: (0, 255, 255),
        256: (0, 0, 0)
    }

    blocks = make_extra_container(HEIGHT, WIDTH, None)

    a = max(WIDTH, HEIGHT)
    grid_w = game_surf_wh[0]//a//40
    block_w = (game_surf_wh[0]-grid_w*(a+1))/a

    blocks = add_block(blocks, Block)
    blocks = add_block(blocks, Block)

    sizes = {
        "grid_w": grid_w,
        "block_w": block_w
    }

    draw_static(game_surf, palette, sizes, blocks)
    was_pressed = False
    end = False
    while not end:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            swipe_side, was_pressed = get_swipe(event, was_pressed)
            if swipe_side is not None:
                moves, final = get_moves(blocks, swipe_side, Block)
                draw_move(palette, sizes, blocks, swipe_side, moves)
                if blocks != final:
                    blocks = add_block(final, Block)
                    if not can_move(blocks):
                        pg.time.delay(3000)
                        print("Game Over!")
                        end = True

        draw_static(game_surf, palette, sizes, blocks)
        sc.blit(game_surf, game_surf_xy)
        pg.display.flip()


if __name__ == "__main__":
    main()
