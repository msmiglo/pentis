
from unittest import main, TestCase

from pentis import DisplayData


class TestDisplayData(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_creation(self):
        dd = DisplayData(4, (20, 10), Piece(5), 30)


if __name__ == "__main__":
    main()
