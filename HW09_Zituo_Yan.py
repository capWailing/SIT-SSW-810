"""
    author: Zituo Yan
    description: student system
    date: 10/30/19
"""
import os
from collections import defaultdict
from prettytable import PrettyTable


def file_reading_gen(path, fields, sep=',', header=False):
    """
        field separated file reader
    :param path:
    :param fields:
    :param sep:
    :param header:
    :return:
    """
    try:
        fp = open(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {path} is not found")
    else:
        with fp:
            if header:
                next(fp)
            for offset, line in enumerate(fp):
                lines = line.strip().split(sep)
                if len(lines) != fields:
                    raise ValueError(f'{path} has {len(lines)} fields on line {offset + 1} but expected {fields}')
                else:
                    yield tuple(lines)


class Student:
    """
        Student Class
        methods: add_course_grade
                get_summary
    """
    def __init__(self, *args):
        """
            initiate student class
        :param args:
        """
        self.cwid = args[0]
        self.name = args[1]
        self.major = args[2]
        self._course_grade = defaultdict(str)

    def add_course_grade(self, course, grade):
        """
            add course grade to individual student
        :param course:
        :param grade:
        :return:
        """
        self._course_grade[course] = grade

    def get_summary(self):
        """
            return summary for pretty table
        :return:
        """
        return [self.cwid, self.name, [key for key in self._course_grade.keys()]]


class Instructor:
    """
        instructor class
        methods:    add_student_to_course
                    get_summary
    """
    def __init__(self, *args):
        """
            initiate instructor class
        :param args:
        """
        self.cwid = args[0]
        self.name = args[1]
        self.department = args[2]
        self._course_student = defaultdict(int)

    def add_student_to_course(self, course_name):
        """
            increment 1 for course of student
        :param course_name:
        :return:
        """
        self._course_student[course_name] += 1

    def get_summary(self):
        """
            return summary for prettytable
        :return:
        """
        return [[self.cwid, self.name, self.department, key, value] for key, value in self._course_student.items()]


class Repository:
    """
        repository class for collect data and print from students.txt instructors.txt and grades.txt
        methods:    storage_student
                    storage_instructor
                    storage_grade
                    summary
                    repository
    """
    def __init__(self, dir_path):
        """
            initiate repository
        :param dir_path:
        """
        self.student_directory = os.path.join(dir_path, "students.txt")
        self.instructor_directory = os.path.join(dir_path, "instructors.txt")
        self.grade_directory = os.path.join(dir_path, "grades.txt")
        self.student = dict()
        self.instructor = dict()
        self.repository()

    def storage_student(self):
        """
            read and save data from students.txt
        :return:
        """
        for students in file_reading_gen(self.student_directory, 3, '\t'):
            self.student[students[0]] = Student(*students)

    def storage_instructor(self):
        """
            read and save data from instructors.txt
        :return:
        """
        for instructors in file_reading_gen(self.instructor_directory, 3, '\t'):
            self.instructor[instructors[0]] = Instructor(*instructors)

    def storage_grade(self):
        """
            read and process grade
        :return:
        """
        for records in file_reading_gen(self.grade_directory, 4, '\t'):
            student = self.student[records[0]]
            student.add_course_grade(records[1], records[2])
            instructor = self.instructor[records[3]]
            instructor.add_student_to_course(records[1])

    def summary(self):
        """
            form and print prettytable
        :return:
        """
        student_table = PrettyTable()
        student_table.field_names = ['CWID', 'Name', 'Completed Courses']
        instructor_table = PrettyTable()
        instructor_table.field_names = ['CWID', 'Name', 'Dept', 'Courses', 'Students']
        for students in self.student.values():
            student_table.add_row(students.get_summary())
        for instructors in self.instructor.values():
            for record in instructors.get_summary():
                instructor_table.add_row(record)
        print(student_table)
        print(instructor_table)

    def repository(self):
        """
            start process the class
        :return:
        """
        self.storage_student()
        self.storage_instructor()
        self.storage_grade()
        self.summary()


def main():
    Repository('./stevens')
    # Repository('./test')


if __name__ == '__main__':
    main()
