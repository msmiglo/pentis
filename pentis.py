
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

Game is a class containing a state of game and its behaviour.
Window is a class responsible for GUI.
Game and Window are independent and encapsulated classes.
Application is a controller class containing Game and Window.
Application class is responsible for communication between Window and Game.
Application class manages threads.

"root.state()"

"""

# ===========================
# ====== GAME PHYSICS =======
# ===========================

class Coordinates:
    playfield_size = None

    @classmethod
    def set_playfield_size(cls, height, width):
        cls.playfield_size = (height, width)

    def __init__(self, x, y):
        if Coordinates.playfield_size is None:
            raise RuntimeError("Playfield size must be initiated.")

        self.x = x
        self.y = y

        self.check_out_of_playfield()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Coordinates(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Coordinates(x, y)

    def check_out_of_playfield(self):
        width, height = Coordinates.playfield_size
        if self.x < 0 or self.x >= width or self.y < 0 or self.y >= height:
            raise ValueError("Coordinates are outside the playfield.")

    def get_neighbours(self):
        return []


class Square:
    """ todo - unify with Block class """
    def __init__(self, x, y):
        self.coordinates = Coordinates(x, y)

    def move_by(self, vector):
        self.coordinates += vector
        # check if coordinates ok

    def rotate(self, center):
        # get coordinates relative to center of rotation
        relative_coords = self.coordinates - center
        x = relative_coords.x
        y = relative_coords.y
        # rotate clockwise by 90 degrees
        x, y = y, -x
        rotated_coords = Coordinates(x, y)
        # get absolute coordinates
        self.coordinates = rotated_coords + center
        # check if coordinates ok


class Block:
    def __init__(self, x, y):
        self.coordinates = Coordinates(x, y)

    def move_by(self, vector):
        self.coordinates += vector
        # check if coordinates ok


class Piece:
    def __init__(self, squares):
        self.squares = squares
        self.center = self._determine_center(squares)

    def _determine_center(squares):
        pass

    def move_left(self):
        pass

    def move_right(self):
        pass

    def move_down(self):
        pass

    def move_to(self, coords):
        pass

    def rotate(selt):
        pass

    def copy(self):
        squares_copy = [sq.copy() for sq in self.squares]
        return Piece(squares_copy)

    def get_blocks(self):
        blocks = [Block(sq.coordinates.x, sq.coordinates.y) for sq in self.squares]
        return blocks


class PieceGenerator:
    piece_library = None

    @classmethod
    def create_piece_library(cls):
        pass

    def __init__(self):
        if PieceGenerator.piece_library is None:
            PieceGenerator.create_piece_library()

    def make_piece(self):
        pass


class Playfield:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self._piece = None
        self._blocks = None
        self._piece_generator = None

        self._reset()

    def reset(self):
        pass

    def rotate_piece(self):
        pass

    def move_piece_left(self):
        pass

    def move_piece_right(self):
        pass

    def move_piece_down(self):
        pass

    def _update(self):
        pass

    def _check_game_over(self):
        pass

    def _check_colission(self):
        pass

    def _check_hit_ground(self):
        pass

    def _turn_piece_into_blocks(self):
        pass

    def _burn_lines(self):
        pass

    def _make_new_piece(self):
        pass

    def get_display_data(self):
        return {}


class Game:
    def __init__(self, size_x, size_y):
        self._playfield = Playfield(size_x, size_y)
        self._time = 0.0
        self._time_step = 1.0
        self._alive = False
        self._refresh_view_callback = None

        self._reset()

    def _reset(self):
        self.alive = True
        self.time = 0.0
        self.piece = None
        self.position_x = 5
        self.position_y = 20
        self.rotation = 0
        self.time_step = 1.0
        self.blocks = []

    def _is_alive(self):
        return bool(self.alive)

    def _set_dead(self):
        self.alive = False

    def _update(self):
        # place piece in the playfield if there is none
        # check if game over (piece overlaps blocks)
        # turn piece into blocks if touches ground
        # burn full lines
        # update time_step
        # check max time
        if self.time > 5.5:
            self.set_dead()
        pass

    def _step(self):
        print(".", end="")
        self.position_y -= 1
        self._update()

    def register_callback(callback):
        pass

    def start_loop(self):
        while self._is_alive():
            sleep(self._time_step)
            self._time += self._time_step
            self._step()
            self._refresh_view_callback()
            #context.game.draw_view(context.window)
        print("side thread game over, trying to close window..")
        #context.window.close()
        self._refresh_view_callback(end=True)
        print("side thread finished")

    def handle_event(self, event):
        """
        make event in game
        update game
        take a display data
        update display
        """
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
        elif event.type == "window_closed":
            self._set_dead()
        else:
            pass
        game.update()

    def get_display_data(self):
        return {}


def game_physics(context):
    """ to be moved to Game class as `loop` method, remove context """


# ===========================
# ======= WINDOW GUI ========
# ===========================

class Key(Enum):
    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3
    ESCAPE = 4


class Window:
    """
    Wrapper class for tkinter.Tk
    """
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Pentis by MŚ")
        self.event_handler = None

    def register_event_handler(self, callback):
        self.event_handler = callback

    def start_loop(self):
        self.context.window.window.mainloop()

    def clear_display(self):
        pass

    def draw(self, display_data):
        self.clear_display()
        self.__draw_playfield()
        self.__draw_blocks(self.blocks)
        self.__draw_piece(self.piece)
        self.show()

    def __draw_playfield(self):
        pass

    def __draw_blocks(self, blocks):
        pass

    def __draw_piece(self, piece):
        pass

    def show(self):
        pass

    def close(self):
        print("close window")
        #self.window.quit() # to be deleted
        self.window.destroy()  # this will wait until the main thread ends
        print("window destroyed")


# ===========================
# ====== APPLICATION ========
# ===========================

class DisplayData:
    def __init__(self, playfield_x_size, playfield_y_size, piece, blocks, time):
        self.playfield_size = (playfield_x_size, playfield_y_size)
        self.piece = piece
        self.blocks = blocks
        self.time = time


class Application:
    def __init__(self):
        self._game = None
        self._window = None

    def start(self):
        return

    def stop(self):
        pass
        #self.context.window.close()

    def handle_event(self, event):
        self.game.handle_event(event)
        display_data = self.game.get_display_data()
        self.window.draw(display_data)

    def refresh_view(self):
        return


# ===========================
# ========== MAIN ===========
# ===========================


def main():
    app = Application()
    app.start()
    return

##    """ logic to be moved to Application class """
##    # create game engine
##    game = Game()
##    window = Window()
##    context = Context(game=game, window=window)
##    # create window
##    app = App(context)
##    # register event listener
##    app.register_event_listener(event_listener)
##    # start game physics
##    thread = Thread(target=game_physics, args=(context,))
##    # start event loop
##    print("initializing game physics thread")
##    thread.start()
##    print("game started, starting main loop")
##    app.start_event_loop()
##    print("app main loop stopped")
##    print("main thread finished")
##    pass


if __name__ == "__main__":
    main()
