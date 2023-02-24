import unittest
from lib.menu import Menu


class TestMenu(unittest.TestCase):
    def test_add_selection(self):
        menu = Menu()
        menu.add_selection("Option 1")
        self.assertIn("Option 1", menu.selections)

    def test_has_selection(self):
        menu = Menu()
        menu.add_selection("Option 1")
        self.assertTrue(menu.has_selection("Option 1"))
        self.assertFalse(menu.has_selection("Option 2"))

    def test_del_selection(self):
        menu = Menu()
        menu.add_selection("Option 1")
        menu.del_selection("Option 1")
        self.assertNotIn("Option 1", menu.selections)

    def test_replace_selection(self):
        menu = Menu()
        menu.add_selection("Option 1")
        menu.replace_selection("New Option", 0)
        self.assertIn("New Option", menu.selections)
        self.assertNotIn("Option 1", menu.selections)


if __name__ == "__main__":
    unittest.main()
