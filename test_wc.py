from unittest import TestCase
from wc import get_chars
from wc import get_words
from wc import get_lines
from wc import get_appends
from wc import get_file_recursive
from wc import get_file


class TestGet_chars(TestCase):
    def test_get_chars(self):
        get_chars(r'D:\test\test1.txt')


class TestGet_words(TestCase):
    def test_get_words(self):
        get_words(r'D:\test\test1.txt')


class TestGet_lines(TestCase):
    def test_get_lines(self):
        get_lines(r'D:\test\test1.txt')


class TestGet_appends(TestCase):
    def test_get_appends(self):
        file = r'D:\test\test1.txt'
        get_appends(file)


class TestGet_file_recursive(TestCase):
    def test_get_file_recursive(self):
        file_list = get_file_recursive("D:\\test", "*.cpp")
        TestCase.assertTrue(self, len(file_list) > 0)


class TestGet_file(TestCase):
    def test_get_file(self):
        file_list = get_file("D:\\test", "*.cpp")
        TestCase.assertTrue(self, len(file_list) > 0)
