
from unittest import main, TestCase

from pentis import Block, Coordinates, DisplayData
from pentis import Piece, Playfield, PieceGenerator, Square


class TestCoordinates(TestCase):
    def setUp(self):
        Coordinates.set_playfield_size(10, 5)

    def tearDown(self):
        Coordinates.playfield_size = None

    def test_set_playfield_size(self):
        self.tearDown()
        self.assertIsNone(Coordinates.playfield_size)
        Coordinates.set_playfield_size(10, 5)
        self.assertTupleEqual(Coordinates.playfield_size, (10, 5))

    def test_create(self):
        vector = Coordinates(2, 4)
        self.assertEqual(vector.x, 2)
        self.assertEqual(vector.y, 4)
        with self.assertRaises(ValueError):
            vector_2 = Coordinates(2, 9)
        with self.assertRaises(ValueError):
            vector_3 = Coordinates(-2, 2)

    def test_out_of_playfield(self):
        vector = Coordinates(2, 4)
        vector.check_out_of_playfield()
        vector.x = 10
        with self.assertRaises(ValueError):
            vector.check_out_of_playfield()

    def test_neighbours(self):
        vector = Coordinates(2, 3)
        neighbours = vector.get_neighbours()
        self.assertEqual(len(neighbours), 4)
        expected = set([(2, 4), (2, 2), (1, 3), (3, 3)])
        for neighbour in neighbours:
            x = neighbour.x
            y = neighbour.y
            self.assertTrue((x, y) in expected)

    def test_neighbours_edge(self):
        vector = Coordinates(0, 1)
        neighbours = vector.get_neighbours()
        self.assertEqual(len(neighbours), 3)
        expected = set([(0, 0), (0, 2), (1, 1)])
        for neighbour in neighbours:
            x = neighbour.x
            y = neighbour.y
            self.assertTrue((x, y) in expected)

    def test_neighbours_corner(self):
        vector = Coordinates(9, 4)
        neighbours = vector.get_neighbours()
        self.assertEqual(len(neighbours), 2)
        expected = set([(8, 4), (9, 3)])
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

    def test_adding(self):
        vector = Coordinates(5, 3)
        increment = Coordinates(0, 1)
        result = vector + increment
        self.assertEqual(result.x, 5)
        self.assertEqual(result.y, 4)

    def test_substractions(self):
        vector = Coordinates(5, 3)
        decrement = Coordinates(1, 0)
        result = vector - decrement
        self.assertEqual(result.x, 4)
        self.assertEqual(result.y, 3)

    def test_making_set(self):
        pass


class TestSquare(TestCase):
    def setUp(self):
        Coordinates.set_playfield_size(10, 5)

    def tearDown(self):
        Coordinates.playfield_size = None

    def test_creation(self):
        square = Square(5, 3)
        self.assertEqual(square.coordinates.x, 5)
        self.assertEqual(square.coordinates.y, 3)
        with self.assertRaises(ValueError):
            square = Square(-2, 2)

    def test_move_by(self):
        square = Square(5, 3)
        vector = Coordinates(1, 1)
        square.move_by(vector)
        self.assertEqual(square.coordinates.x, 6)
        self.assertEqual(square.coordinates.y, 4)

    def test_move_by_error(self):
        square = Square(5, 3)
        vector = Coordinates(1, 2)
        with self.assertRaises(ValueError):
            square.move_by(vector)

    def test_rotate(self):
        square = Square(5, 3)
        center = Coordinates(3, 4)
        square.rotate(center)
        self.assertEqual(square.coordinates.x, 2)
        self.assertEqual(square.coordinates.y, 2)

    def test_rotate_error(self):
        pass



class TestDisplayData(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_creation(self):
        dd = DisplayData(4, (20, 10), Piece(5), 30)


if __name__ == "__main__":
    main()
