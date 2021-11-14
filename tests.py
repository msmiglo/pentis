
from unittest import main, skip, TestCase
from unittest.mock import MagicMock

from pentis import Block, Coordinates, DisplayData
from pentis import Piece, Playfield, PieceGenerator, Square


class TestCoordinates(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create(self):
        vector = Coordinates(-2, 4)
        self.assertEqual(vector.x, -2)
        self.assertEqual(vector.y, 4)

    def test_neighbours(self):
        vector = Coordinates(-2, 3)
        neighbours = vector.get_neighbours()
        self.assertEqual(len(neighbours), 4)
        expected = set([(-2, 4), (-2, 2), (-1, 3), (-3, 3)])
        for neighbour in neighbours:
            x = neighbour.x
            y = neighbour.y
            self.assertTrue((x, y) in expected)

    def test_neighbours_edge(self):
        vector = Coordinates(0, 0)
        neighbours = vector.get_neighbours()
        self.assertEqual(len(neighbours), 4)
        expected = set([(-1, 0), (1, 0), (0, 1), (0, -1)])
        for neighbour in neighbours:
            x = neighbour.x
            y = neighbour.y
            self.assertTrue((x, y) in expected)

    def test_eq(self):
        vector_1 = Coordinates(5, 3)
        vector_2 = Coordinates(2, 4)
        vector_3 = Coordinates(5, 3)
        self.assertFalse(vector_1 == vector_2)
        self.assertTrue(vector_2 == vector_2)
        self.assertNotEqual(vector_2, vector_3)
        self.assertEqual(vector_1, vector_3)

    def test_eq_other_type(self):
        vector = Coordinates(5, 3)
        self.assertFalse(vector == "writing")

    def test_eq_other_type(self):
        class _Derivative(Coordinates):
            pass

        vector = Coordinates(5, 3)
        other = _Derivative(5, 3)
        self.assertFalse(vector == other)

    def test_adding(self):
        vector = Coordinates(5, 3)
        increment = Coordinates(-1, 1)
        result = vector + increment
        self.assertEqual(result.x, 4)
        self.assertEqual(result.y, 4)

    def test_substractions(self):
        vector = Coordinates(-5, 3)
        decrement = Coordinates(1, 0)
        result = vector - decrement
        self.assertEqual(result.x, -6)
        self.assertEqual(result.y, 3)

    def test_making_set(self):
        vector_1 = Coordinates(5, 3)
        vector_2 = Coordinates(2, 4)
        vector_3 = Coordinates(5, 3)
        vector_set = set([vector_1, vector_2, vector_3])
        self.assertEqual(len(vector_set), 2)
        self.assertSetEqual(vector_set, set([vector_1, vector_2]))


class TestBlock(TestCase):
    def setUp(self):
        Block.set_playfield_size(10, 5)

    def tearDown(self):
        Block._playfield_size = None

    def test_set_playfield_size(self):
        self.tearDown()
        self.assertIsNone(Block._playfield_size)
        Block.set_playfield_size(10, 5)
        self.assertTupleEqual(Block._playfield_size, (10, 5))

    def test_create(self):
        block = Block(2, 4)
        self.assertEqual(block.coordinates.x, 2)
        self.assertEqual(block.coordinates.y, 4)
        with self.assertRaises(ValueError):
            block_2 = Block(2, 9)
        with self.assertRaises(ValueError):
            block_3 = Block(-2, 2)

    def test_out_of_playfield(self):
        block = Block(2, 4)
        block.check_out_of_playfield()
        block.coordinates.x = 10
        with self.assertRaises(ValueError):
            block.check_out_of_playfield()

    def test_neighbours(self):
        block = Block(2, 3)
        neighbours = block.get_neighbours()
        self.assertEqual(len(neighbours), 4)
        expected = set([(2, 4), (2, 2), (1, 3), (3, 3)])
        for neighbour in neighbours:
            x = neighbour.coordinates.x
            y = neighbour.coordinates.y
            self.assertTrue((x, y) in expected)

    def test_neighbours_edge(self):
        block = Block(0, 1)
        neighbours = block.get_neighbours()
        self.assertEqual(len(neighbours), 3)
        expected = set([(0, 0), (0, 2), (1, 1)])
        for neighbour in neighbours:
            x = neighbour.coordinates.x
            y = neighbour.coordinates.y
            self.assertTrue((x, y) in expected)

    def test_neighbours_corner(self):
        block = Block(9, 4)
        neighbours = block.get_neighbours()
        self.assertEqual(len(neighbours), 2)
        expected = set([(8, 4), (9, 3)])
        for neighbour in neighbours:
            x = neighbour.coordinates.x
            y = neighbour.coordinates.y
            self.assertTrue((x, y) in expected)

    def test_eq(self):
        block_1 = Block(5, 3)
        block_2 = Block(2, 4)
        block_3 = Block(5, 3)
        self.assertFalse(block_1 == block_2)
        self.assertTrue(block_2 == block_2)
        self.assertNotEqual(block_2, block_3)
        self.assertEqual(block_1, block_3)

    def test_move_by(self):
        block = Block(5, 3)
        increment = Coordinates(0, 1)
        block.move_by(increment)
        self.assertEqual(block.coordinates.x, 5)
        self.assertEqual(block.coordinates.y, 4)

    def test_move_by_error(self):
        block = Block(5, 3)
        increment = Coordinates(0, 2)
        with self.assertRaises(ValueError):
            block.move_by(increment)

    def test_hash(self):
        block_1 = Block(5, 2)
        block_2 = Block(7, 2)
        square = Square(5, 2)
        self.assertNotEqual(hash(block_1), hash(square))
        self.assertNotEqual(hash(block_2), hash(square))
        self.assertNotEqual(hash(block_1), hash(block_2))

    def test_making_set(self):
        block_1 = Block(5, 3)
        block_2 = Block(2, 4)
        block_3 = Block(5, 3)
        block_set = set([block_1, block_2, block_3])
        self.assertEqual(len(block_set), 2)
        self.assertSetEqual(block_set, set([block_1, block_2]))


class TestSquare(TestCase):
    def setUp(self):
        Block.set_playfield_size(10, 5)

    def tearDown(self):
        Block._playfield_size = None

    def test_creation(self):
        square = Square(5, 3)
        self.assertEqual(square.coordinates.x, 5)
        self.assertEqual(square.coordinates.y, 3)
        with self.assertRaises(ValueError):
            square = Square(-2, 2)

    def test_get_neighbours(self):
        square = Square(2, 3)
        neighbours = square.get_neighbours()
        self.assertEqual(len(neighbours), 4)
        expected = set([(1, 3), (3, 3), (2, 4), (2, 2)])
        for neighbour in neighbours:
            x = neighbour.coordinates.x
            y = neighbour.coordinates.y
            self.assertTrue((x, y) in expected)
            self.assertEqual(type(neighbour), Square)

    def test_rotate(self):
        square = Square(5, 3)
        center = Coordinates(3, 4)
        square.rotate(center)
        self.assertEqual(square.coordinates.x, 2)
        self.assertEqual(square.coordinates.y, 2)

    def test_rotate_error(self):
        square = Square(5, 3)
        center = Coordinates(3, 1)
        with self.assertRaises(ValueError):
            square.rotate(center)

    def test_copy(self):
        square = Square(5, 2)
        copy_square = square.copy()
        self.assertEqual(square, copy_square)
        self.assertIsNot(square, copy_square)
        self.assertIsNot(square.coordinates, copy_square.coordinates)
        self.assertEqual(type(copy_square), Square)
        copy_square.coordinates.x = 4
        self.assertEqual(square.coordinates.x, 5)

    def test_eq(self):
        square_1 = Square(5, 3)
        square_2 = Square(2, 4)
        square_3 = Square(5, 3)
        self.assertFalse(square_1 == square_2)
        self.assertTrue(square_2 == square_2)
        self.assertNotEqual(square_2, square_3)
        self.assertEqual(square_1, square_3)


class TestPiece(TestCase):
    def setUp(self):
        Block.set_playfield_size(8, 8)
        self.piece_left = Piece([Square(0, 2), Square(1, 2), Square(1, 1)])
        self.piece_right = Piece([Square(7, 2), Square(6, 2)])
        self.piece_down = Piece([Square(4, 0), Square(4, 1), Square(3, 0)])
        self.piece_pento = Piece([
            Square(0, 1), Square(1, 1), Square(1, 0),
            Square(2, 1), Square(2, 2)
        ])
        self.long_piece = Piece([
            Square(0, 1), Square(0, 2), Square(0, 3),
            Square(0, 4), Square(0, 5)
        ])
        self.piece_L_shape = Piece([
            Square(2, 1), Square(3, 1), Square(4, 1), Square(4, 2)])

    def tearDown(self):
        Block._playfield_size = None

    def test_determine_center(self):
        # arrange
        piece_mock = MagicMock()
        square = Square(4, 4)
        piece_mock.squares = [square]
        piece_mock.center = None
        # act
        Piece._determine_center(piece_mock)
        # assert
        center = piece_mock.center
        self.assertIsInstance(center, Coordinates)
        self.assertEqual(center, square.coordinates)

    def test_determine_center_2(self):
        # arrange
        piece_mock = MagicMock()
        piece_mock.center = None
        piece_mock.squares = self.piece_pento.squares
        # act
        Piece._determine_center(piece_mock)
        # assert
        self.assertEqual(self.piece_pento.center, Coordinates(1, 1))
        center = piece_mock.center
        self.assertIsInstance(center, Coordinates)
        self.assertEqual(center.x, 1)
        self.assertEqual(center.y, 1)

    def test_create(self):
        squares = [Square(5, 2), Square(6, 2)]
        piece = Piece(squares)
        self.assertListEqual(piece.squares, squares)
        self.assertEqual(piece.center, Coordinates(6, 2))

    def test_move_left(self):
        with self.assertRaises(ValueError):
            self.piece_left.move_left()
        self.piece_right.move_left()

    def test_move_right(self):
        with self.assertRaises(ValueError):
            self.piece_right.move_right()
        self.piece_down.move_left()

    def test_move_down(self):
        with self.assertRaises(ValueError):
            self.piece_down.move_down()
        self.piece_right.move_left()

    def test_move_to_error(self):
        bad_coords = Coordinates(-5, 6)
        with self.assertRaises(ValueError):
            self.piece_left.move_to(bad_coords)

    def test_move_to(self):
        # arrange
        coords = Coordinates(3, 4)
        expected_squares = [Square(2, 4), Square(3, 4), Square(3, 3),
                            Square(4, 4), Square(4, 5)]
        # act
        self.piece_pento.move_to(coords)
        # assert
        self.assertSetEqual(
            set(self.piece_pento.squares),
            set(expected_squares)
        )
        self.assertEqual(self.piece_pento.center, coords)

    def test_rotate(self):
        expected_squares = [Square(1, 2), Square(1, 1), Square(0, 1),
                            Square(1, 0), Square(2, 0)]
        self.piece_pento.rotate()
        self.assertSetEqual(
            set(self.piece_pento.squares),
            set(expected_squares)
        )
        self.assertEqual(self.piece_pento.center, Coordinates(1, 1))

    def test_rotate_error(self):
        with self.assertRaises(ValueError):
            self.long_piece.rotate()

    def test_copy(self):
        piece_copy = self.piece_pento.copy()
        self.assertIsNot(self.piece_pento, piece_copy)
        for sq_1, sq_2 in zip(self.piece_pento.squares, piece_copy.squares):
            self.assertIsNot(sq_1, sq_2)
            self.assertEqual(sq_1, sq_2)

    def test_get_blocks(self):
        blocks = self.piece_right.get_blocks()
        expected = [Block(7, 2), Block(6, 2)]
        self.assertListEqual(blocks, expected)
        for block in blocks:
            self.assertEqual(type(block), Block)

    def test_move_to_zero(self):
        # arrange
        expected_squares = [Square(0, 1), Square(1, 1), Square(1, 0),
                            Square(2, 1), Square(2, 2)]
        coords = Coordinates(1, 1)
        # act
        self.piece_pento._move_to_zero()
        # assert
        self.assertSetEqual(
            set(self.piece_pento.squares),
            set(expected_squares)
        )
        self.assertEqual(self.piece_pento.center, coords)

    def test_move_to_zero_2(self):
        # arrange
        expected_squares = [Square(1, 0), Square(0, 0)]
        coords = Coordinates(1, 0)
        # act
        self.piece_right._move_to_zero()
        # assert
        self.assertSetEqual(
            set(self.piece_right.squares),
            set(expected_squares)
        )
        self.assertEqual(self.piece_right.center, coords)

    def test_equal_other_type(self):
        other = Square(4, 4)
        self.assertNotEqual(self.piece_L_shape, other)

    def test_equal_other_shape(self):
        other = Piece([
            Square(2, 1), Square(3, 1), Square(4, 1), Square(4, 0)])
        self.assertNotEqual(self.piece_L_shape, other)

    def test_equal_shifted(self):
        other = Piece([
            Square(1, 4), Square(2, 4), Square(3, 4), Square(3, 5)])
        self.assertEqual(self.piece_L_shape, other)

    def test_equal_rotated(self):
        other = Piece([
            Square(6, 1), Square(6, 2), Square(6, 3), Square(5, 3)])
        self.assertEqual(self.piece_L_shape, other)

    def test_equal_rotated_other_shape(self):
        other = Piece([
            Square(6, 2), Square(6, 3), Square(6, 4), Square(7, 4)])
        self.assertNotEqual(self.piece_L_shape, other)

    def test_equal_same(self):
        other = Piece([
            Square(2, 1), Square(3, 1), Square(4, 1), Square(4, 2)])
        self.assertEqual(self.piece_L_shape, other)


class TestPieceGenerator(TestCase):
    def setUp(self):
        Block.set_playfield_size(12, 30)

    def tearDown(self):
        Block._playfield_size = None
        PieceGenerator.piece_library = None

    def test_extend_piece(self):
        piece = Piece([Square(3, 1), Square(3, 2), Square(3, 3)])
        pieces = PieceGenerator.extend_piece(piece)
        self.assertEqual(len(pieces), 4)

    def test_extend_library(self):
        piece_1 = Piece([Square(3, 1), Square(3, 2)])
        piece_2 = Piece([Square(3, 1)])
        new_library = PieceGenerator.extend_library([piece_1, piece_2])
        self.assertEqual(len(new_library), 3)
        self.assertIn(
            Piece([Square(3, 1), Square(3, 2)]),
            new_library
        )
        self.assertIn(
            Piece([Square(3, 1), Square(3, 2), Square(3, 3)]),
            new_library
        )
        self.assertIn(
            Piece([Square(3, 1), Square(3, 2), Square(2, 2)]),
            new_library
        )

    def test_create_piece_library(self):
        piece = Piece([Square(3, 1), Square(3, 2)])
        PieceGenerator.create_piece_library(2)
        library = PieceGenerator.piece_library
        self.assertEqual(len(library), 1)
        self.assertEqual(library[0], piece)
        self.assertEqual(type(library[0]), Piece)

    def test_create_piece_library(self):
        PieceGenerator.create_piece_library(5)
        library = PieceGenerator.piece_library
        self.assertEqual(len(library), 18)

    def test_create_piece_3(self):
        PieceGenerator.create_piece_library(3)
        pg = PieceGenerator()
        for i in range(10):
            new_piece = pg.make_piece()
            self.assertIn(new_piece, PieceGenerator.piece_library)
            self.assertEqual(new_piece.center.x, 6)
            self.assertEqual(new_piece.extent()["y"][1], 29)

    def test_create_piece_5(self):
        PieceGenerator.create_piece_library(5)
        pg = PieceGenerator()
        for i in range(3):
            new_piece = pg.make_piece()
            self.assertIn(new_piece, PieceGenerator.piece_library)
            self.assertEqual(new_piece.center.x, 6)
            self.assertEqual(new_piece.extent()["y"][1], 29)


class TestDisplayData(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_error(self):
        with self.assertRaises(TypeError):
            dd = DisplayData(12, 20)

    def test_creation(self):
        mock_piece = MagicMock()
        mock_block_1 = MagicMock()
        mock_block_2 = MagicMock()
        dd = DisplayData(12, 20, mock_piece, [mock_block_1, mock_block_2])
        self.assertTupleEqual(dd.playfield_size, (12, 20))
        self.assertIs(dd.piece, mock_piece)
        self.assertEqual(dd.blocks, [mock_block_1, mock_block_2])
        self.assertIsNone(dd.time)


if __name__ == "__main__":
    main()
