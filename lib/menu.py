"""Create "Menu" objects that contain a multiple selection items.

Contains Menu class and related functions for the creation and
manipulation of generic menus."""


class Menu:
    """A class for the creation of menus

    Attributes
    ----------
    selections : list
        one of the selectable menu items

    Methods
    -------
    has_selection(selection):
        check if selection is in menu
    add_selection(new_selection):
        add given selection to menu
    del_selection(selection):
        remove selection from menu
    replace_selection(new_selection, index):
        replace menu selection at index with new_selection"""

    def __init__(self):
        self._selections = []

    def __str__(self):
        """Return a string of the printout of sorted menu options"""
        menu_string = []
        for idx, selection in enumerate(self._selections, start=1):
            menu_string.append(f"{idx}. {selection}")
        return "\n".join(menu_string)

    @property
    def selections(self):
        """One of the selectable options in a menu"""
        return self._selections

    def has_selection(self, selection):
        """Return True if selection is in menu, else False"""
        return True if self._selections.count(selection) > 0 else False

    def add_selection(self, new_selection):
        """Add the given selection to the menu"""
        self._selections.append(new_selection)

    def del_selection(self, selection):
        """Remove the given selection from the menu"""
        self._selections.remove(selection)

    def replace_selection(self, new_selection, index):
        """Replaces the menu item at index"""
        self._selections[index] = new_selection
