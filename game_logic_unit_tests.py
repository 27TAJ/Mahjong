import unittest
from game_logic import find_break

class GameLogicUnitTests(unittest.TestCase):

    def test_find_break(self):
        self.assertEqual(find_break(8),63)
        self.assertEqual(find_break(3),50)
        self.assertEqual(find_break(12),59)
        self.assertEqual(find_break(6),29)
        self.assertEqual(find_break(7),46)
        self.assertEqual(find_break(5),12)


if __name__ == "__main__":
    unittest.main()