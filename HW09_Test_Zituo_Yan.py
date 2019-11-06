import unittest
from HW09_Zituo_Yan import *


class TestRepository(unittest.TestCase):
    def test_repository(self):
        # test file with no grade in grades.txt

        stevens = Repository('./stevens')
        student_a = stevens._student['10103'].get_summary()
        self.assertEqual(student_a[0], '10103')
        self.assertEqual(student_a[1], 'Baldwin, C')
        self.assertEqual(sorted(student_a[2]), sorted(['SSW 567', 'SSW 564', 'SSW 687', 'CS 501']))
        self.assertEqual(sorted(student_a[3]), sorted(['SSW 540', 'SSW 555']))
        self.assertEqual(student_a[4], None)

        major_a = stevens._major['SYEN'].get_summary()
        self.assertEqual(major_a[0], 'SYEN')
        self.assertEqual(sorted(major_a[1]), sorted(['SYS 671', 'SYS 612', 'SYS 800']))
        self.assertEqual(sorted(major_a[2]), sorted(['SSW 810', 'SSW 565', 'SSW 540']))

        instructor_a = stevens._instructor['98765'].get_summary()
        self.assertEqual(sorted(instructor_a),
                         sorted([['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4],
                                 ['98765', 'Einstein, A', 'SFEN', 'SSW 540', 3]]))


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
