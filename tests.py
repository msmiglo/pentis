
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
