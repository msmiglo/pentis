
from enum import Enum
import random
from threading import Thread
from time import sleep

import tkinter


class Key(Enum):
    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3
    ESCAPE = 4


class PieceType(Enum):
    EMPTY = 0


class Piece:
    pass


class Coordinates:
    pass
    # get neighbours()


class Playfield:
    pass


class Window:
    def __init__(self):
        pass

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
        pass


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
        # check if lost (piece overlaps blocks)
        # turn piece into blocks if touches ground
        # burn full lines
        # update time_step
        # check max time
        if self.time > 10.5:
            self.set_dead()
        pass

    def step(self):
        print(".", end="")
        self.position_y -= 1
        self.update()

    def draw_view(self, display):
        display.clear()
        display.draw_playfield()
        display.draw_blocks(self.blocks)
        display.draw_piece(self.piece_type, self.position_x, self.position_y, self.rotation)
        display.show()


class Context:
    def __init__(self, game, display):
        self.game = game
        self.display = display


class App:
    def __init__(self, context):
        self.context = context

    def register_event_listener(self, event_listener):
        pass

    def start_event_loop(self):
        pass

    def close(self):
        self.context.display.close()


def game_physics(context):
    while context.game.is_alive():
        sleep(context.game.time_step)
        context.game.time += context.game.time_step
        context.game.step()
        context.game.draw_view(context.display)


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
    context.game.draw_view(context.display)


def main():
    # create game engine
    game = Game()
    display = Window()
    context = Context(game=game, display=display)
    # create window
    app = App(context)
    # register event listener
    app.register_event_listener(event_listener)
    # start game physics
    thread = Thread(target=game_physics, args=(context,))
    # start event loop
    app.start_event_loop()
    thread.start()
    # close app
    thread.join()
    app.close()
    # pass
    pass



if __name__ == "__main__":
    main()
