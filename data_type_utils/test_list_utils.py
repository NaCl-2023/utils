# File       : test_list_utils.py
# Time       ：2024/11/15 17:28
# Author     ：nacl
# version    ：python 3.12
from unittest import TestCase, main

from data_type_utils.list_utils import list_subtract, list_weightlessness


class TestListSubtract(TestCase):

    def test_basic_functionality(self):
        list1 = [1, 2, 3, 4]
        list2 = [3, 4]
        expected = [1, 2]
        self.assertEqual(list_subtract(list1, list2), expected)

    def test_empty_list1(self):
        list1 = []
        list2 = [1, 2, 3]
        expected = []
        self.assertEqual(list_subtract(list1, list2), expected)

    def test_empty_list2(self):
        list1 = [1, 2, 3]
        list2 = []
        expected = [1, 2, 3]
        self.assertEqual(list_subtract(list1, list2), expected)

    def test_duplicate_elements(self):
        list1 = [1, 2, 2, 3]
        list2 = [2]
        expected = [1, 3]
        self.assertEqual(list_subtract(list1, list2), expected)

    def test_identical_lists(self):
        list1 = [1, 2, 3]
        list2 = [1, 2, 3]
        expected = []
        self.assertEqual(list_subtract(list1, list2), expected)

    def test_non_list_input(self):
        with self.assertRaises(TypeError):
            list_subtract([1, 2], 'not a list')

    def test_large_lists(self):
        list1 = list(range(1000))
        list2 = list(range(500, 1000))
        expected = list(range(0, 500))
        self.assertEqual(list_subtract(list1, list2), expected)

    def test_non_numeric_elements(self):
        list1 = ['a', 'b', 'c']
        list2 = ['b']
        expected = ['a', 'c']
        self.assertEqual(list_subtract(list1, list2), expected)


class TestListWeightlessness(TestCase):

    def test_basic_functionality(self):
        _list = [1, 2, 2, 3, 4, 4, 5]
        expected = [1, 2, 3, 4, 5]
        self.assertEqual(list_weightlessness(_list), expected)

    def test_empty_list(self):
        _list = []
        expected = []
        self.assertEqual(list_weightlessness(_list), expected)

    def test_no_duplicates(self):
        _list = [1, 2, 3, 4, 5]
        expected = [1, 2, 3, 4, 5]
        self.assertEqual(list_weightlessness(_list), expected)

    def test_multiple_duplicates(self):
        _list = [1, 2, 2, 2, 3, 3, 4, 4, 4, 4]
        expected = [1, 2, 3, 4]
        self.assertEqual(list_weightlessness(_list), expected)

    def test_all_duplicates(self):
        _list = [1, 1, 1, 1]
        expected = [1]
        self.assertEqual(list_weightlessness(_list), expected)

    def test_non_list_input(self):
        with self.assertRaises(TypeError):
            list_weightlessness('not a list')

    def test_non_numeric_elements(self):
        _list = ['a', 'b', 'a', 'c', 'b', 'c']
        expected = ['a', 'b', 'c']
        self.assertEqual(list_weightlessness(_list), expected)


if __name__ == '__main__':
    main()
