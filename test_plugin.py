import unittest

from unittest.mock import MagicMock

import sys

for mockedModules in [
    "qt",
    "qt.core",
    "calibre",
    "calibre.gui2",
    "calibre.gui2.tweak_book",
    "calibre.gui2.tweak_book.plugin",
    "calibre.ebooks",
    "calibre.ebooks.oeb",
    "calibre.ebooks.oeb.base",
    "calibre.ebooks.oeb.polish",
    "calibre.ebooks.oeb.polish.replace",
    "calibre_plugins",
    "calibre_plugins.bulk_img_resizer",
    "calibre_plugins.bulk_img_resizer.ui",
    "calibre_plugins.bulk_img_resizer.image",
]:
    sys.modules[mockedModules] = MagicMock()


from main import replace_extension


class TestReplaceExtension(unittest.TestCase):

    def test_replace_standard_extension(self):
        self.assertEqual(replace_extension("example.txt", ".jpg"), "example.jpg")

    def test_replace_no_extension(self):
        self.assertEqual(replace_extension("example", ".jpg"), "example.jpg")

    def test_replace_with_empty_new_extension(self):
        self.assertEqual(replace_extension("example.txt", ""), "example")

    def test_replace_extension_with_dotless_extension(self):
        self.assertEqual(replace_extension("example.txt", "jpg"), "examplejpg")


if __name__ == "__main__":
    unittest.main()
