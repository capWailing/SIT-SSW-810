import unittest
from HW11_Zituo_Yan import *


class TestRepository(unittest.TestCase):
    def test_repository(self):
        # test file with no grade in grades.txt

        stevens = Repository('./stevens')
        student_a = stevens._student['10103'].get_summary()
        self.assertEqual(student_a[0], '10103')
        self.assertEqual(student_a[1], 'Jobs, S')
        self.assertEqual(sorted(student_a[2]), sorted(['SSW 810', 'CS 501']))
        self.assertEqual(sorted(student_a[3]), sorted(['SSW 555', 'SSW 540']))
        self.assertEqual(student_a[4], None)

        major_a = stevens._major['SFEN'].get_summary()
        self.assertEqual(major_a[0], 'SFEN')
        self.assertEqual(sorted(major_a[1]), sorted(['SSW 810', 'SSW 540', 'SSW 555']))
        self.assertEqual(sorted(major_a[2]), sorted(['CS 501', 'CS 546']))

        instructor_a = stevens._instructor['98764'].get_summary()
        self.assertEqual(sorted(instructor_a),
                         [['98764', 'Cohen, R', 'SFEN', 'CS 546', 1]])

        db_path = "/Applications/DataGrip.app/Contents/bin/810_startup.db"
        db = sqlite3.connect(db_path)
        query = "select i.CWID, i.Name, i.Dept, g.Course, count(*) as cnt from instructors i join grades g " \
                "on i.CWID = g.InstructorCWID group by i.CWID, g.Course"
        result = list()
        for row in db.execute(query):
            result.append(row)
        self.assertEqual(result, sorted([(98762, 'Hawking, S', 'CS', 'CS 501', 1),
                                        (98762, 'Hawking, S', 'CS', 'CS 546', 1),
                                        (98762, 'Hawking, S', 'CS', 'CS 570', 1),
                                        (98763, 'Rowland, J', 'SFEN', 'SSW 555', 1),
                                        (98763, 'Rowland, J', 'SFEN', 'SSW 810', 4),
                                        (98764, 'Cohen, R', 'SFEN', 'CS 546', 1)]))


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
