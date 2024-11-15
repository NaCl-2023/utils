# File       : test___init__.py
# Time       ：2024/11/15 17:47
# Author     ：nacl
# version    ：python 3.12
import unittest

from file_utils import convert_path


class TestConvertPath(unittest.TestCase):

    def test_basic_functionality(self):
        path = "C:\\path\\to\\file//"
        expected = "C:/path/to/file"
        self.assertEqual(convert_path(path), expected)

    def test_windows_style_path(self):
        path = "C:\\Program Files\\Folder\\"
        expected = "C:/Program Files/Folder"
        self.assertEqual(convert_path(path), expected)

    def test_unix_style_path(self):
        path = "/var/log/syslog"
        expected = "/var/log/syslog"
        self.assertEqual(convert_path(path), expected)

    def test_mixed_style_path(self):
        path = "C:\\Users\\Name\\Documents\\file"
        expected = "C:/Users/Name/Documents/file"
        self.assertEqual(convert_path(path), expected)

    def test_relative_path(self):
        path = "folder/subfolder/file"
        expected = "folder/subfolder/file"
        self.assertEqual(convert_path(path), expected)

    def test_empty_path(self):
        path = ""
        expected = "."
        self.assertEqual(convert_path(path), expected)

    def test_special_characters(self):
        path = "C:/path with spaces/to/file"
        expected = "C:/path with spaces/to/file"
        self.assertEqual(convert_path(path), expected)

    def test_repeated_separators(self):
        path = "C:\\path\\\\to\\\\file"
        expected = "C:/path/to/file"
        self.assertEqual(convert_path(path), expected)


if __name__ == '__main__':
    unittest.main()
