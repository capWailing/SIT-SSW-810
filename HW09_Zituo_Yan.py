"""
    author: Zituo Yan
    description: student system
    date: 10/30/19
"""
import os
from collections import defaultdict
from prettytable import PrettyTable


def list_difference(l1, l2):
    """
        return difference of two lists
    :param l1:
    :param l2:
    :return:
    """
    return [i for i in l1 if i not in l2]


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
        print(f"File {path} is not found")
    else:
        with fp:
            if header:
                next(fp)
            for offset, line in enumerate(fp):
                lines = line.strip().split(sep)
                if len(lines) != fields:
                    raise ValueError(f"{path} has wrong fields. Should be {fields} fields, separate by '{sep}'.")
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
        self._cwid = args[0]
        self._name = args[1]
        self.major = args[2]
        self._course_grade = defaultdict(str)
        self._required = list()
        self._electives = list()
        self._completed_courses = list()

    def add_course_grade(self, course, grade):
        """
            add course grade to individual student
        :param course:
        :param grade:
        :return:
        """
        self._course_grade[course] = grade
        if grade != "F" and grade != '':
            self._completed_courses.append(course)

    def add_remaining(self, major):
        """
            add remaining required courses and remaining elective courses
        :param major:
        :return:
        """
        self._required = list_difference(major.required, self._completed_courses)
        self._electives = None if set(major.electives) & set(self._completed_courses) else major.electives

    def get_summary(self):
        """
            return summary for pretty table
        :return:
        """
        return [self._cwid, self._name, self._completed_courses, self._required, self._electives]


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


class Major:
    """
        Major class
        methods:    add_required
                    add_electives
                    get_summary
    """

    def __init__(self, major):
        """
            initiate major class
        :param major:
        """
        self._major = major
        self.required = list()
        self.electives = list()

    def add_courses(self, course, attitude):
        """
            add required course for single major
        :param attitude:
        :param course:
        :return:
        """
        self.required.append(course) if attitude == "R" else self.electives.append(course)

    def get_summary(self):
        """
            return summary for prettytable
        :return:
        """
        return [self._major, self.required, self.electives]


class Repository:
    """
            repository class for collect data and print from students.txt instructors.txt and grades.txt
            methods:    storage_student
                        storage_instructor
                        storage_grade
                        summary
                        repository
    """

    student_table = PrettyTable()
    student_table.field_names = ['CWID', 'Name', 'Completed Courses', 'Remaining Required', 'Remaining Elective']
    instructor_table = PrettyTable()
    instructor_table.field_names = ['CWID', 'Name', 'Dept', 'Courses', 'Students']
    major_table = PrettyTable()
    major_table.field_names = ['Major', 'Required', 'Electives']

    def __init__(self, dir_path, default_print=True):
        """
            initiate repository
        :param dir_path:
        """
        self._student_directory = os.path.join(dir_path, "students.txt")
        self._instructor_directory = os.path.join(dir_path, "instructors.txt")
        self._grade_directory = os.path.join(dir_path, "grades.txt")
        self._major_directory = os.path.join(dir_path, "majors.txt")
        self._student = dict()
        self._instructor = dict()
        self._major = dict()
        self.repository(default_print)

    def storage_student(self):
        """
            read and save data from students.txt
        :return:
        """
        for students in file_reading_gen(self._student_directory, 3, ';', True):
            for values in students:
                if len(values) == 0:
                    raise ValueError("Students table has empty value!")
            self._student[students[0]] = Student(*students)

    def storage_instructor(self):
        """
            read and save data from instructors.txt
        :return:
        """
        for instructors in file_reading_gen(self._instructor_directory, 3, '|', True):
            for values in instructors:
                if len(values) == 0:
                    raise ValueError("Instructors table has empty value!")
                else:
                    self._instructor[instructors[0]] = Instructor(*instructors)

    def storage_grade(self):
        """
            read and process grade
        :return:
        """
        for records in file_reading_gen(self._grade_directory, 4, '|', True):
            try:
                student = self._student[records[0]]
            except KeyError:
                raise KeyError(f"{records[0]} are not in student table!")
            if records[2] not in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'F', '']:
                raise ValueError("Grades invalid, should be 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C' and 'F'.")
            else:
                student.add_course_grade(records[1], records[2])
                student.add_remaining(self._major[student.major])
            try:
                instructor = self._instructor[records[3]]
            except KeyError:
                raise KeyError(f"{records[3]} are not in instructors table!")
            instructor.add_student_to_course(records[1])

    def storage_major(self):
        """
            read and process major
        :return:
        """
        for major in file_reading_gen(self._major_directory, 3, '\t', True):
            if not self._major.get(major[0]):
                self._major[major[0]] = Major(major[0])
            if major[1] != "R" and major[1] != "E":
                raise ValueError(f"Major's required or elective field should be R or E!")
            else:
                self._major[major[0]].add_courses(major[2], major[1])

    def summary(self):
        """
            form and print prettytable
        :return:
        """
        for students in self._student.values():
            self.student_table.add_row(students.get_summary())
        for instructors in self._instructor.values():
            for record in instructors.get_summary():
                self.instructor_table.add_row(record)
        for major in self._major.values():
            self.major_table.add_row(major.get_summary())
        print(self.student_table)
        print(self.instructor_table)
        print(self.major_table)

    def repository(self, default_print):
        """
            start process the class
        :return:
        """
        try:
            self.storage_major()
            self.storage_student()
            self.storage_instructor()
            self.storage_grade()
        except KeyError as e:
            print(e)
        except ValueError as e:
            print(e)
        else:
            if default_print:
                self.summary()


def main():
    Repository('./stevens')
    # Repository('./test')


if __name__ == '__main__':
    main()
