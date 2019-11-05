import unittest
from HW09_Zituo_Yan import *


class TestFileReadingGen(unittest.TestCase):
    def test_file_reading_gen(self):
        self.assertEqual(list(file_reading_gen('../student_majors.txt', 3, sep='|', header=True)),
                         [('123', 'Jin He', 'Computer Science'), ('234', 'Nanda Koka', 'Software Engineering'),
                          ('345', 'Benji Cai', 'Software Engineering')])
        self.assertEqual(list(file_reading_gen('../student_majors_without_header.txt', 3, sep='|', header=False)),
                         [('123', 'Jin He', 'Computer Science'), ('234', 'Nanda Koka', 'Software Engineering'),
                          ('345', 'Benji Cai', 'Software Engineering')])
        with self.assertRaises(FileNotFoundError):
            for a in file_reading_gen('../123.txt', 3, ' ', True):
                print(a)


class TestRepository(unittest.TestCase):
    def test_repository(self):
        # test file with no grade in grades.txt
        with self.assertRaises(ValueError):
            Repository('./test1')
        with self.assertRaises(FileNotFoundError):
            Repository('./test2')

        stevens = Repository('./stevens')
        self.assertEqual(stevens.student['10103'].cwid, '10103')
        self.assertEqual(stevens.student['10103'].name, 'Baldwin, C')
        self.assertEqual(stevens.student['10103'].get_summary(), ['10103', 'Baldwin, C', ['SSW 567', 'SSW 564', 'SSW 687', 'CS 501']])
        self.assertEqual(stevens.instructor['98765'].cwid, '98765')
        self.assertEqual(stevens.instructor['98765'].name, 'Einstein, A')
        self.assertEqual(stevens.instructor['98765'].get_summary(), [['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4],
                         ['98765', 'Einstein, A', 'SFEN', 'SSW 540', 3]])


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
