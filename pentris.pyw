
import random
from threading import Thread
from time import sleep
import tkinter


WIDTH = 20
HEIGHT = 32
SQUARE_SIDE = 22
MARGIN = 10

PIECE_SIZE = 5


"""
TODO - update

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

    def __repr__(self):
        return f"Coords({self.x}, {self.y})"

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
        versor_1 = Coordinates(1, 0)
        versor_2 = Coordinates(0, 1)
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

    def __repr__(self):
        return f"Block({self.coordinates.x}, {self.coordinates.y})"

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

    def __repr__(self):
        return f"Square({self.coordinates.x}, {self.coordinates.y})"

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

    def copy(self):
        square_copy = Square(self.coordinates.x, self.coordinates.y)
        return square_copy

    def get_color(self):
        return "lightblue"


class Piece:
    def __init__(self, squares):
        self.squares = squares
        self.center = None
        self._determine_center()

    def extent(self):
        xs = [sq.coordinates.x for sq in self.squares]
        ys = [sq.coordinates.y for sq in self.squares]
        min_x = min(xs)
        max_x = max(xs)
        min_y = min(ys)
        max_y = max(ys)
        return {"x": (min_x, max_x), "y": (min_y, max_y),
                "min": (min_x, min_y), "max": (max_x, max_y)}

    def _move_to_zero(self):
        min_x, min_y = self.extent()["min"]
        translation_vector = Coordinates(-min_x, -min_y)
        self._move_by_vector(translation_vector)

    def __str__(self):
        copy = self.copy()
        copy._move_to_zero()
        max_x, max_y = copy.extent()["max"]
        grid = [["." for j in range(max_x + 3)] for i in range(max_y + 3)]
        for sq in copy.squares:
            grid[sq.coordinates.y + 1][sq.coordinates.x + 1] = "X"
        grid[copy.center.y + 1][copy.center.x + 1] = "O"
        grid = [" ".join(line) for line in grid]
        grid = "\n".join(grid[::-1])
        return grid

    def __eq__(self, other):
        # check type
        if type(other) != type(self):
            return False
        # check if identical
        if set(self.squares) == set(other.squares):
            return True

        # try rotating and shifting before comparison:
        # 1) make copies
        original = self.copy()
        comparison = other.copy()
        # 2) move comparison piece to center of playfield
        x, y = Block._playfield_size
        center_of_playfield = Coordinates(x // 2, y // 2)
        comparison.move_to(center_of_playfield)
        # 3) make copies for all rotations
        rotation_copies = []
        for i in range(4):
            rotation_copies.append(comparison.copy())
            comparison.rotate()
        # 4) move all copies to same position
        original._move_to_zero()
        for piece_i in rotation_copies:
            piece_i._move_to_zero()
        # 5) compare to all four
        for piece_i in rotation_copies:
            if set(piece_i.squares) == set(original.squares):
                return True
        # 6) no comparison passed
        return False

    def _determine_center(self):
        n_squares = len(self.squares)
        weighted_position = Coordinates(0, 0)
        for sq in self.squares:
            weighted_position += sq.coordinates
        x_center = weighted_position.x / n_squares
        y_center = weighted_position.y / n_squares
        self.center = Coordinates(int(x_center + 0.5), int(y_center + 0.5))

    def _move_by_vector(self, vector):
        for sq in self.squares:
            sq.move_by(vector)
            sq.check_out_of_playfield()
        self.center += vector

    def move_left(self):
        vector = Coordinates(-1, 0)
        self._move_by_vector(vector)

    def move_right(self):
        vector = Coordinates(1, 0)
        self._move_by_vector(vector)

    def move_down(self):
        vector = Coordinates(0, -1)
        self._move_by_vector(vector)

    def move_to(self, coords):
        vector = coords - self.center
        self._move_by_vector(vector)

    def rotate(self):
        for sq in self.squares:
            sq.rotate(self.center)
            sq.check_out_of_playfield()

    def copy(self, with_center=False):
        squares_copy = [sq.copy() for sq in self.squares]
        piece_copy = Piece(squares_copy)
        if with_center:
            piece_copy.center = Coordinates(self.center.x, self.center.y)
        return piece_copy

    def get_blocks(self):
        blocks = [Block(sq.coordinates.x, sq.coordinates.y) for sq in self.squares]
        return blocks


class PieceGenerator:
    piece_library = None

    @staticmethod
    def extend_piece(piece):
        assert type(piece) == Piece, f"got piece of type: `{type(piece)}`"

        # get piece neighbouring squares
        neighbours = []
        for sq in piece.squares:
            neighbours += sq.get_neighbours()
        neighbours = set(neighbours).difference(set(piece.squares))

        # make new pieces by adding neighbouring square - one for each
        new_pieces = []
        for nb in neighbours:
            new_squares = piece.copy().squares
            new_squares.append(nb)
            new_piece = Piece(new_squares)
            if new_piece not in new_pieces:
                new_pieces.append(new_piece)

        return new_pieces

    @staticmethod
    def extend_library(library):
        if not library:
            x, y = Block._playfield_size
            square = Square(x // 2, y // 2)
            piece = Piece([square])
            return [piece]

        new_library = []
        for old_piece in library:
            new_pieces = PieceGenerator.extend_piece(old_piece)
            for new_piece in new_pieces:
                if new_piece not in new_library:
                    new_library.append(new_piece)

        return new_library

    @classmethod
    def create_piece_library(cls, piece_size):
        # make library of unique pieces
        library = None
        for i in range(piece_size):
            library = cls.extend_library(library)

        # rotate pieces that are standing vertically
        for pc in library:
            extent = pc.extent()
            x_span = extent["x"][1] - extent["x"][0]
            y_span = extent["y"][1] - extent["y"][0]
            if y_span > x_span:
                pc.rotate()

        # shift pieces to starting position
        y_playfield_limit = Block._playfield_size[1] - 1
        x_playfield_middle = Block._playfield_size[0] // 2
        for pc in library:
            y_max = pc.extent()["y"][1]
            y_center = pc.center.y
            # upper edge (y_max) should be moved to the playfield limit
            new_y_center = y_center + (y_playfield_limit - y_max)
            new_coords = Coordinates(x_playfield_middle, new_y_center)
            pc.move_to(new_coords)

        # assign pieces libary to class property
        cls.piece_library = library

    def __init__(self):
        if PieceGenerator.piece_library is None:
            raise RuntimeError("Piece library must be created first.")

    def make_piece(self):
        piece = random.choice(self.piece_library).copy()
        return piece


class Playfield:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self._piece = None
        self._blocks = None
        self._piece_generator = None

        self.reset()

    def reset(self):
        self._blocks = []
        self._piece_generator = PieceGenerator()
        self._piece = self._piece_generator.make_piece()

    def rotate_piece(self):
        piece_copy = self._piece.copy(with_center=True)
        # if this operation will cause error - ignore it
        try:
            piece_copy.rotate()
            self._check_colission(piece_copy)
        except ValueError:
            return
        # everything ok, perform action on actual piece
        self._piece.rotate()

    def move_piece_left(self):
        piece_copy = self._piece.copy()
        # if this operation will cause error - ignore it
        try:
            piece_copy.move_left()
            self._check_colission(piece_copy)
        except ValueError:
            return
        # everything ok, perform action on actual piece
        self._piece.move_left()

    def move_piece_right(self):
        piece_copy = self._piece.copy()
        # if this operation will cause error - ignore it
        try:
            piece_copy.move_right()
            self._check_colission(piece_copy)
        except ValueError:
            return
        # everything ok, perform action on actual piece
        self._piece.move_right()

    def move_piece_down(self):
        piece_copy = self._piece.copy()
        # if moving down will cause error or colision - turn into blocks
        try:
            piece_copy.move_down()
            self._check_colission(piece_copy)
        except ValueError:
            self._turn_piece_into_blocks()
            self._burn_lines()
            self._make_new_piece()
            return
        # everything ok, perform action on actual piece
        self._piece.move_down()

    def _update(self):
        """ TODO - FINISH """
        pass

    def _check_game_over(self):
        try:
            self._check_colission(self._piece)
            return False
        except ValueError:
            return True

    def _check_colission(self, piece):
        blocks_coords = [bl.coordinates for bl in self._blocks]
        for sq in piece.squares:
            if sq.coordinates in blocks_coords:
                raise ValueError("Piece is coliding with existing blocks!")

    def _turn_piece_into_blocks(self):
        blocks = self._piece.get_blocks()
        self._piece = None
        self._blocks += blocks

    def _burn_lines(self):
        max_x, max_y = Block._playfield_size
        # find lines to burn
        rows = {i: 0 for i in range(max_y)}
        for bl in self._blocks:
            rows[bl.coordinates.y] += 1
        burn_discount = max(0, PIECE_SIZE - 4)
        rows_to_burn = [i for i in rows if rows[i] >= max_x - burn_discount]
        if len(rows_to_burn) == 0:
            return

        # display a flash effect - TODO (could be difficult)

        # calculate displacement for blocks
        rows_displacement = {}
        current_displacement = 0
        for row_i in range(max_y):
            if row_i in rows_to_burn:
                rows_displacement[row_i] = None
                current_displacement -= 1
            else:
                vector = Coordinates(0, current_displacement)
                rows_displacement[row_i] = vector

        # burn lines and move down the other blocks
        new_blocks = []
        for bl in self._blocks:
            y = bl.coordinates.y
            displacement = rows_displacement[y]
            if displacement is None:
                continue
            bl.move_by(displacement)
            new_blocks.append(bl)
        self._blocks = new_blocks

    def _make_new_piece(self):
        if self._piece is not None:
            raise RuntimeError("There is already a piece in the playfield.")
        self._piece = self._piece_generator.make_piece()

    def get_display_data(self):
        return DisplayData(self.size_x, self.size_y, self._piece, self._blocks)


class Game:
    def __init__(self, size_x, size_y):
        self._playfield = Playfield(size_x, size_y)
        self.time = None
        self.time_step = None
        self.alive = False
        self.pause = False
        self._refresh_view_callback = None

        self._reset()

    def _reset(self):
        self._playfield.reset()
        self.time = 0.0
        self.time_step = 0.3
        self.alive = True
        self.pause = False

    def _is_alive(self):
        return bool(self.alive)

    def _set_dead(self):
        self.alive = False

    def start_loop(self):
        while self._is_alive():
            self._step()
        print("ok")

    def _step(self):
        sleep(self.time_step)
        if self.pause:
            return
        self.time += self.time_step
        self._playfield.move_piece_down()
        self._update()
        print(".", end="", flush=True)

    def _update(self):
        """ TODO - FINISH """
        self._refresh_view_callback()
        if self._playfield._check_game_over():
            self._reset()
        # place piece in the playfield if there is none
        # check if game over (piece overlaps blocks)
        # turn piece into blocks if touches ground
        # burn full lines
        # update time_step
        # check max time

    def stop(self):
        self._set_dead()

    def handle_event(self, event):
        # hangle controls
        if event.keysym == Key.PAUSE:
            self.pause = not self.pause
            return
        elif event.keysym in ["r", "R"]:
            self._reset()
            self._update()

        if self.pause:
            # IF SWITCHED OFF - YOU CAN PLAY ON PAUSE!
            #return
            pass

        # handle arrow keys
        if event.keysym == Key.UP:
            self._playfield.rotate_piece()
        elif event.keysym == Key.LEFT:
            self._playfield.move_piece_left()
        elif event.keysym == Key.RIGHT:
            self._playfield.move_piece_right()
        elif event.keysym == Key.DOWN:
            self._playfield.move_piece_down()
        else:
            return

        # refresh view
        self._update()

    def get_display_data(self):
        data = self._playfield.get_display_data()
        data.time = int(self.time)
        return data

    def register_callback(self, callback):
        self._refresh_view_callback = callback


# ===========================
# ======= WINDOW GUI ========
# ===========================

class Key:
    PAUSE = "space"
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
        self.window.title("Pentris by MŚ")

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
        y_position = (HEIGHT - y - 1) * SQUARE_SIDE

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
            x = block.coordinates.x
            y = block.coordinates.y
            self.__draw_square(x, y, is_piece=False)

    def __draw_piece(self, piece):
        if piece is not None:
            for sq in piece.squares:
                x = sq.coordinates.x
                y = sq.coordinates.y
                self.__draw_square(x, y, is_piece=True)

    def show(self):
        self.window.update()

    def draw(self, display_data):
        # Unfortunately tkinter is thread-agnostic, and drawing anything
        # from outside the main thread will cause problems with
        # updating the window. Therefore the separate thread used
        # to tick-tock the game steps causes massive lags with
        # drawing objects on canvas. Probable solution is to make some
        # clock generating events and bind some handler to them.
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
        PieceGenerator.create_piece_library(PIECE_SIZE)
        self._game = Game(WIDTH, HEIGHT)
        self._game.register_callback(self.refresh_view)
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
