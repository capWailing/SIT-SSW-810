import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

DB_FILE = '/Users/zituoyan/Documents/GitHub/SIT-SSW-810/810_startup.db'


@app.route('/')
def index():
    return render_template('main_page.html',
                           title='Stevens Repository',
                           author='Zituo Yan')


@app.route('/main')
def main_page():
    return render_template(
        'main_page.html',
        title='Stevens Repository',
        author='Zituo Yan'
    )


@app.route('/students')
def student_courses():
    try:
        db = sqlite3.connect(DB_FILE)
    except sqlite3.OperationalError:
        return f"Error: Unable to open database at {DB_FILE}"
    else:
        query = """ select s.cwid, s.name, s.major, count(g.Course) as complete from
                    students s join grades g on s.cwid=g.StudentCWID group by s.cwid,
                    s.name, s.major """
        data = [
            {'cwid': cwid, 'name': name, 'major': major, 'complete': complete}
            for cwid, name, major, complete in db.execute(query)
        ]
        db.close()
        return render_template(
            'student_courses.html',
            title='Stevens Repository',
            table_title='Number of completed courses by Student',
            students=data
        )


@app.route('/instructors')
def instructors():
    try:
        db = sqlite3.connect(DB_FILE)
    except sqlite3.OperationalError:
        return f"Error: Unable to open database at {DB_FILE}"
    else:
        query = """ select cwid, name, dept from instructors """
        data = [
            {'cwid': cwid, 'name': name, 'dept': dept}
            for cwid, name, dept in db.execute(query)
        ]
        db.close()
        return render_template(
            'instructor_form.html',
            title='Stevens Repository',
            table_title='Instructors',
            instructors=data
        )


@app.route('/show_instructors')
def course_counts():
    try:
        db = sqlite3.connect(DB_FILE)
    except sqlite3.OperationalError:
        return f"Error: Unable to open database at {DB_FILE}"
    else:
        query = """select i.CWID, i.Name, i.Dept, g.Course, count(*) as cnt from instructors i join grades g 
                on i.CWID = g.InstructorCWID group by i.CWID, g.Course"""
        data = [
            {'cwid': cwid, 'name': name, 'dept': dept, 'course': course, 'cnt': cnt}
            for cwid, name, dept, course, cnt in db.execute(query)
        ]
        db.close()
        return render_template(
            'course_students.html',
            title='Stevens Repository',
            table_title='Courses and students counts',
            instructors=data
        )


@app.route('/choose_student')
def choose_student():
    query = "select cwid, name from students group by cwid, name"
    try:
        db = sqlite3.connect(DB_FILE)
    except sqlite3.OperationalError:
        return f"Error: Unable to open database at {DB_FILE}"
    else:
        results = db.execute(query)
        students = [{'cwid': cwid, 'name': name} for cwid, name in results]
        db.close()
        return render_template('student_form.html', students=students)


@app.route('/show_student', methods=['POST'])
def show_student():
    if request.method == 'POST':
        cwid = request.form['cwid']
        query = "select course, grade from grades where studentCWID=?"
        args = (cwid,)
        table_title = f"Courses/Grades for CWID {cwid}"

        try:
            db = sqlite3.connect(DB_FILE)
        except sqlite3.OperationalError:
            return f"Error: Unable to open database at {DB_FILE}"
        else:
            results = db.execute(query, args)
            rows = [{'course': course, 'grade': grade} for course, grade in results]
            db.close()
            return render_template('grade_form.html',
                                   table_title=table_title, rows=rows)


app.run(debug=True)
