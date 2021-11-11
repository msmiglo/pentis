
from enum import Enum
import random
from threading import Thread
from time import sleep

import tkinter


"""
Playfield is a rectangular lattice consisting of Spaces.
Spaces form rows horizontally and columns vertically.
Each Space has Coordinates.
Space can be empty or filled with a Square or with a Block.
Square is the smallest entity in game, it can fill exactly one Space.
Piece is a game entity which is consisted of 5 orthogonally adjacent Squares.
Pieces can move downward or be rotated during their freefall.
When a Piece hits the ground its Squares turn into Blocks.
Block is a Square with fixed position in the Playfield.
When the whole row is filled with Blocks, it is removed.
Exactly one Piece is present on the playfield.
When a Piece is turned into Blocks, the next Piece is generated on top of Playfield.

"""


class Key(Enum):
    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3
    ESCAPE = 4


class PieceType(Enum):
    # to be deprecated probably
    EMPTY = 0


class Piece:
    pass


class Square:
    pass


class Block:
    pass


class Coordinates:
    pass
    # get neighbours()


class Playfield:
    pass


class Window:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Pentis by MŚ")

    def draw_playfield(self):
        pass

    def draw_blocks(self, blocks):
        pass

    def draw_piece(self, type_, x, y, rotation):
        pass

    def clear(self):
        pass

    def show(self):
        pass

    def close(self):
        print("close windows")
        self.window.destroy()
        print("window destroyed")


class Game:
    def __init__(self):
        self.alive = True
        self.time = None
        self.position_x = None
        self.position_y = None
        self.rotation = None
        self.time_step = 1.0
        self.blocks = []
        self.piece_type = None

        self.reset()

    def reset(self):
        self.alive = True
        self.time = 0.0
        self.position_x = 5
        self.position_y = 20
        self.rotation = 0
        self.time_step = 1.0
        self.blocks = []
        self.piece_type = PieceType.EMPTY

    def is_alive(self):
        return bool(self.alive)

    def set_dead(self):
        self.alive = False

    def update(self):
        # place piece in the playfield if there is none
        # check if game over (piece overlaps blocks)
        # turn piece into blocks if touches ground
        # burn full lines
        # update time_step
        # check max time
        if self.time > 5.5:
            self.set_dead()
        pass

    def step(self):
        print(".", end="")
        self.position_y -= 1
        self.update()

    def draw_view(self, window):
        window.clear()
        window.draw_playfield()
        window.draw_blocks(self.blocks)
        window.draw_piece(self.piece_type, self.position_x, self.position_y, self.rotation)
        window.show()


class Context:
    def __init__(self, game, window):
        self.game = game
        self.window = window


class App:
    def __init__(self, context):
        self.context = context

    def register_event_listener(self, event_listener):
        pass

    def start_event_loop(self):
        self.context.window.window.mainloop()

    def close(self):
        self.context.window.close()


def game_physics(context):
    while context.game.is_alive():
        sleep(context.game.time_step)
        context.game.time += context.game.time_step
        context.game.step()
        context.game.draw_view(context.window)
    context.window.close()


def handle_event(game, event):
    if event.type == "key_stroke":
        key = event.key
        if key == Key.DOWN:
            game.position_y -= 1
        elif key == Key.UP:
            game.rotation += 1
        elif key == Key.LEFT:
            game.position_x -= 1
        elif key == Key.RIGHT:
            game.position_x += 1
        elif key == Key.ESCAPE:
            game.set_dead()
        else:
            pass
    else:
        pass
    game.update()


def event_listener(context, event):
    handle_event(context.game, event)
    context.game.draw_view(context.window)


def main():
    # create game engine
    game = Game()
    window = Window()
    context = Context(game=game, window=window)
    # create window
    app = App(context)
    # register event listener
    app.register_event_listener(event_listener)
    # start game physics
    thread = Thread(target=game_physics, args=(context,))
    # start event loop
    print("initializing game physics thread")
    thread.start()
    print("game started")
    app.start_event_loop()
    print("app main loop started")
    # close app
    print("waiting for thread...")
    thread.stop()
    thread.join()
    print("thread joined.")
    app.close()
    # pass
    pass



if __name__ == "__main__":
    main()
