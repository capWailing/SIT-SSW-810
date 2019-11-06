import unittest
from HW09_Zituo_Yan import *


class TestRepository(unittest.TestCase):
    def test_repository(self):
        # test file with no grade in grades.txt
        with self.assertRaises(ValueError):
            Repository('./test1')
        with self.assertRaises(FileNotFoundError):
            Repository('./test2')

        stevens = Repository('./stevens')
        self.assertEqual(stevens._student['10103'].cwid, '10103')
        self.assertEqual(stevens._student['10103'].name, 'Baldwin, C')
        self.assertEqual(stevens._student['10103'].get_summary(), ['10103', 'Baldwin, C', ['SSW 567', 'SSW 564', 'SSW 687', 'CS 501']])
        self.assertEqual(stevens._instructor['98765'].cwid, '98765')
        self.assertEqual(stevens._instructor['98765'].name, 'Einstein, A')
        self.assertEqual(stevens._instructor['98765'].get_summary(), [['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4],
                                                                      ['98765', 'Einstein, A', 'SFEN', 'SSW 540', 3]])


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
