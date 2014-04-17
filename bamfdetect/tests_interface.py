import unittest
import bamfdetect


class test_bamf_detect(unittest.TestCase):
    def test_version_returns_result(self):
        v = bamfdetect.get_version()
        self.assertNotEqual(v, None, "Version is None")
        self.assertNotEqual(v.__len__(), 0, "Version length is 0")


if __name__ == '__main__':
    unittest.main()
