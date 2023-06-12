import sys
import random
import threading

import pygame as pg
pg.init()


class Block:
    def __init__(self, surf, x, y, w, num, color) -> None:
        self.surf = surf
        self.x = x
        self.y = y
        self.w = w
        self.num = num
        self.color = color
        self.was_merge = False

    def draw(self):
        font = pg.font.Font(None, int(self.w//3))
        r = self.w//10 + 1
        _x = self.x
        _y = self.y
        for i in range(2):
            for j in range(2):
                x = (r, self.w - r)[i] + _x
                y = (r, self.w - r)[j] + _y
                pg.draw.circle(self.surf, self.color, (x, y), r)
            x = (0, r)[i] + _x
            w = (self.w, self.w - r*2)[i] + 1
            y = (r, 0)[i] + _y
            h = (self.w - r*2, self.w)[i] + 1
            pg.draw.rect(self.surf, self.color, (x, y, w, h))
        text = font.render(str(self.num), True, "black")
        self.surf.blit(text, text.get_rect(center=(self.w/2 + _x, self.w/2 + _y)))


class Game2048:
    def __init__(self, *args, **kwargs):
        self.main_surf = kwargs.get("main_surf")
        self.x, self.y = kwargs.get("xy")
        self.size = kwargs.get("size")
        self.blocks = []
        for _ in range(self.size[1]):
            self.blocks.append([])
            for _ in range(self.size[0]):
                self.blocks[-1].append(None)
        self.surf = kwargs.get("surf")
        self.compute_size()
        self.palette = kwargs.get("palette")

    def compute_size(self):
        w, _ = self.surf.get_size()
        x, _ = self.size
        grid_w = w//100
        block_w = (w-grid_w*(x+1))//x
        self.sizes = {
            "grid_w": grid_w,
            "block_w": block_w
        }

    def draw(self, fill: bool = True, grid: bool = True, blocks: bool = True):
        if fill:
            self.surf.fill(self.palette["bg_color"])
        if grid:
            self.draw_grid()
        if blocks:
            self.draw_all_blocks()
        self.main_surf.blit(self.surf, (self.x, self.y))

    def draw_grid(self):
        grid_w = self.sizes["grid_w"]
        block_w = self.sizes["block_w"]
        color = self.palette["grid_color"]

        # vertical
        w, h = grid_w, grid_w*(self.size[1] + 1) + block_w*self.size[1]
        for i in range(self.size[0] + 1):
            x = (grid_w + block_w) * i
            y = 0
            pg.draw.rect(self.surf, color, (x, y, w, h))

        # horizontal
        w, h = grid_w*(self.size[1] + 1) + block_w*self.size[1], grid_w
        for i in range(self.size[1] + 1):
            x = 0
            y = (grid_w + block_w) * i
            pg.draw.rect(self.surf, color, (x, y, w, h))

    def draw_all_blocks(self):
        for line in self.blocks:
            for block in line:
                if block:
                    block.draw()

    """# def draw_block(self, _x: float, _y: float, num: int):
    #     colors = {
    #         2: "yellow",
    #         4: "green",
    #         8: "blue",
    #         16: "grey",
    #         32: "red",
    #         64: "gray50",
    #         128: "violet",
    #         256: "orange ",
    #         512: "white",
    #         1024: "brown"
    #     }
    #     color = colors[num]
    #     block_w = self.sizes["block_w"]
    #     font = pg.font.Font(None, int(block_w//3))
    #     r = block_w//10 + 1
    #     for i in range(2):
    #         for j in range(2):
    #             x = (r, block_w - r)[i] + _x
    #             y = (r, block_w - r)[j] + _y
    #             pg.draw.circle(self.surf, color, (x, y), r)
    #         x = (0, r)[i] + _x
    #         w = (block_w, block_w - r*2)[i] + 1
    #         y = (r, 0)[i] + _y
    #         h = (block_w - r*2, block_w)[i] + 1
    #         pg.draw.rect(self.surf, color, (x, y, w, h))
    #     text = font.render(str(num), True, "black")
    #     self.surf.blit(text, text.get_rect(center=(block_w/2 + _x, block_w/2 + _y)))"""


    def create_block(self, xy, num):
        colors = {
            2: "yellow",
            4: "green",
            8: "blue",
            16: "grey",
            32: "red",
            64: "gray50",
            128: "violet",
            256: "orange ",
            512: "white",
            1024: "brown"
        }
        grid_w = self.sizes["grid_w"]
        block_w = self.sizes["block_w"]
        x = grid_w*(xy[0] + 1) + block_w*xy[0]
        y = grid_w*(xy[1] + 1) + block_w*xy[1]
        w = block_w
        return Block(self.surf, x, y, w, num, colors[num])


def main_game():
    bg_color = "black"
    grid_color = "white"
    palette = {
        "bg_color": bg_color,
        "grid_color": grid_color
    }
    grid_size = (5, 5)
    W, H = sc.get_size()
    game_surf_size = (H, H)
    game_surf = pg.Surface(game_surf_size)
    game = Game2048(
        xy=((W - game_surf_size[0])/2, (H - game_surf_size[1])/2),
        main_surf=sc,
        size=grid_size,
        surf=game_surf,
        palette=palette
    )
    game.add_block(True)

    was_pressed = end = False
    swipe_side = None
    while not end:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                sys.exit()
            swipe_side, was_pressed = get_swipe(ev, was_pressed)
            if swipe_side is not None:
                game.move(swipe_side)
        game.draw()
        pg.display.flip()


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

if __name__ == "__main__":
    # sc = pg.display.set_mode((0, 0))
    # main_game()
    blocks = [
        [Block1(4), None, None],
        [Block1(4), None, None],
        [Block1(4), None, None],
        [Block1(4), None, None],
    ]
    ans = Game2048.move(blocks, "up")
    for i in ans:
        for j in i:
            for k in j:
                try:
                    print(k, end=" ")
                except:
                    try:
                        print(k[0], end=" ")
                    except:
                        print(k, end=" ")
            print()
        print()
