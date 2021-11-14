
import random
from threading import Thread
from time import sleep
import tkinter


WIDTH = 10
HEIGHT = 20
SQUARE_SIDE = 25
MARGIN = 10

PIECE_SIZE = 4


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
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash(("Coordinates", self.x, self.y))

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Coordinates(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Coordinates(x, y)

    def get_neighbours(self):
        versor_1 = Coordinates(0, 1)
        versor_2 = Coordinates(1, 0)
        neighbours = [self + versor_1, self - versor_1,
                      self + versor_2, self - versor_2]
        return neighbours


class Block:
    _playfield_size = None

    @classmethod
    def set_playfield_size(cls, height, width):
        cls._playfield_size = (height, width)

    def __init__(self, x, y):
        if Block._playfield_size is None:
            raise RuntimeError("Playfield size must be initiated.")
        self.coordinates = Coordinates(x, y)
        self.check_out_of_playfield()

    def __hash__(self):
        return hash(("Block", self.coordinates.x, self.coordinates.y))

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.coordinates == other.coordinates

    def __add__(self, vector):
        new_coords = self.coordinates + vector
        x = new_coords.x
        y = new_coords.y
        return Block(x, y)

    def check_out_of_playfield(self):
        width, height = Square._playfield_size
        x = self.coordinates.x
        y = self.coordinates.y
        if x < 0 or x >= width or y < 0 or y >= height:
            raise ValueError("Coordinates are outside the playfield.")

    def move_by(self, vector):
        self.coordinates += vector
        self.check_out_of_playfield()

    def get_neighbours(self):
        neighbours = []
        neigbour_coordinates = self.coordinates.get_neighbours()
        for coords in neigbour_coordinates:
            try:
                block = Block(coords.x, coords.y)
                neighbours.append(block)
            except ValueError:
                pass
        return neighbours

    def get_color(self):
        return "red"


class Square(Block):
    def __hash__(self):
        return hash(("Square", self.coordinates.x, self.coordinates.y))

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
        self.check_out_of_playfield()

    def get_neighbours(self):
        neighbour_blocks = super().get_neighbours()
        neighbours = [Square(nb.coordinates.x, nb.coordinates.y)
                      for nb in neighbour_blocks]
        return neighbours

    def get_color(self):
        return "lightblue"


class Piece:
    def __init__(self, squares):
        self.squares = squares
        self.center = self._determine_center(squares)

    def _determine_center(self, squares):
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

        self.reset()

    def reset(self):
        self._piece = Piece([])
        self._blocks = []
        self._piece_generator = PieceGenerator()

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
        return DisplayData(self.size_x, self.size_y, self._piece, self._blocks)


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
        print(".", end="", flush=True)
        self.position_y -= 1
        self._update()

    def register_callback(callback):
        pass

    def start_loop(self):
        while self._is_alive():
            sleep(0.5)
            print(".", end="")
        print("ok")
        return

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

    def stop(self):
        self._set_dead()

    def handle_event(self, event):
        """
        make event in game
        update game
        take a display data
        update display

        dir of event:
            'char', 'delta', 'height', 'keycode',
            'keysym', 'keysym_num', 'num', 'serial',
            'state', 'time', 'type', 'widget', 'width',
            'x', 'x_root', 'y', 'y_root'

        dict of event:
        {
            'serial': 15,
            'num': '??',
            'height': '??',
            'keycode': 40,
            'state': 262152,
            'time': 1567058625,
            'width': '??',
            'x': 171,
            'y': -13,
            'char': '',
            'keysym': 'Down',
            'keysym_num': 65364,
            'type': <EventType.KeyPress: '2'>,
            'widget': <tkinter.Tk object .>,
            'x_root': 205,
            'y_root': 44,
            'delta': 0
        }
        """
        '''print(event)
        print()
        print(dir(event))
        print()
        print(event.__dict__)
        print("=============")'''
        return
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
        data = self._playfield.get_display_data()
        data.time = int(self.time)
        return data


# ===========================
# ======= WINDOW GUI ========
# ===========================

class Key:
    DOWN = "Down"
    UP = "Up"
    LEFT = "Left"
    RIGHT = "Right"
    ESCAPE = "Escape"


class Window:
    """
    Wrapper class for tkinter.Tk
    """
    def __init__(self, width, height):
        # make window
        width_pixels = width * SQUARE_SIDE
        height_pixels = height * SQUARE_SIDE
        self.window = tkinter.Tk()
        self.window.resizable(False, False)
        self.window.title("Pentis by MŚ")

        # add canvas
        self.canvas = tkinter.Canvas(
            self.window,
            width=width_pixels + 2*MARGIN,
            height=height_pixels + 2*MARGIN,
            background='black'
        )
        self.canvas.pack()

        # other data
        self.event_handler = None
        self._alive = False

    def register_event_handler(self, callback):
        self.event_handler = callback

    def start_loop(self):
        self.window.bind("<Key>", self.event_handler)
        self._alive = True
        self.window.mainloop()  # blocking
        self._alive = False

    def clear_display(self):
        self.canvas.delete("all")

    def __draw_square(self, x, y, is_piece=False):
        if is_piece:
            color = "lightblue"
        else:
            color = "red"
        offset = 2 + MARGIN
        x_position = x * SQUARE_SIDE
        y_position = y * SQUARE_SIDE

        self.canvas.create_rectangle(
            x_position + 2 + offset,
            y_position + 2 + offset,
            x_position + SQUARE_SIDE - 2 + offset,
            y_position + SQUARE_SIDE - 2 + offset,
            outline="white", width=2, fill=color)

    def __draw_playfield(self, playfield_size):
        x, y = playfield_size
        offset = 2 + MARGIN
        boundary_colors = [
            "green", "green",
            "yellow", "yellow",
            "grey", "grey",
            "red", "red",
            "cyan", "cyan",
            "blue", "blue",
        ]
        for thickness_px, color in enumerate(2*boundary_colors):
            self.canvas.create_rectangle(
                0 + offset - thickness_px,
                0 + offset - thickness_px,
                x * SQUARE_SIDE - 1 + offset + thickness_px,
                y * SQUARE_SIDE - 1 + offset + thickness_px,
                outline=color, fill=None)

    def __draw_blocks(self, blocks):
        for block in blocks:
            x = block.coodinates.x
            y = block.coodinates.y
            self.__draw_square(x, y, is_piece=False)

    def __draw_piece(self, piece):
        for sq in piece.squares:
            x = sq.coodinates.x
            y = sq.coodinates.y
            self.__draw_square(x, y, is_piece=True)
        for i in range(20):
            x = random.randint(0, WIDTH-1)
            y = random.randint(0, HEIGHT-1)
            self.__draw_square(x, y)

    def show(self):
        self.window.update()

    def draw(self, display_data):
        self.clear_display()
        self.__draw_playfield(display_data.playfield_size)
        self.__draw_blocks(display_data.blocks)
        self.__draw_piece(display_data.piece)
        self.show()

    def close(self):
        if self._alive is False:
            return
        if self.window.state() == "normal":
            self._alive = False
            self.window.destroy()  # this will wait until the main thread ends


# ===========================
# ====== APPLICATION ========
# ===========================

class DisplayData:
    def __init__(self, playfield_x_size, playfield_y_size,
                 piece, blocks, time=None):
        self.playfield_size = (playfield_x_size, playfield_y_size)
        self.piece = piece
        self.blocks = blocks
        self.time = time


class Application:
    def __init__(self):
        Block.set_playfield_size(WIDTH, HEIGHT)
        PieceGenerator.create_piece_library()
        self._game = Game(WIDTH, HEIGHT)
        self._window = Window(WIDTH, HEIGHT)
        self._window.register_event_handler(self.handle_event)

    def _start_game(self):
        self._game.start_loop()
        "waiting until game loop ends..."
        # when the game is stopped - close the window as well
        self._window.close()

    def _start_window(self):
        self._window.start_loop()
        "waiting until window loop ends..."
        # when the window is closed - close the game as well
        self._game.stop()

    def start(self):
        # put game loop in side thread
        game_thread = Thread(target=self._start_game)
        game_thread.start()
        # keep window event loop in main thread
        self._start_window()

    def stop(self):
        self._game.stop()
        self._window.close()

    def handle_event(self, event):
        if event.keysym == Key.ESCAPE:
            self.stop()
        else:
            self._game.handle_event(event)
            self.refresh_view()

    def refresh_view(self):
        display_data = self._game.get_display_data()
        self._window.draw(display_data)


# ===========================
# ========== MAIN ===========
# ===========================

def main():
    app = Application()
    app.start()


if __name__ == "__main__":
    main()
