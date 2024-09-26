"""
database.py

This module handles all database interactions, including CRUD operations and database backup.

Functions:
- create_connection
- create_tables
- add_student
- get_students
- update_student
- delete_student
- add_instructor
- get_instructors
- update_instructor
- delete_instructor
- add_course
- get_courses
- update_course
- delete_course
- add_registration
- get_student_courses
- remove_registration
- backup_database
"""

import sqlite3
import shutil
from main import Student, Instructor, Course

DB_PATH = 'school_management.db'

def create_connection():
    """
    Creates a connection to the SQLite database.

    :return: SQLite connection object.
    :rtype: sqlite3.Connection
    """
    return sqlite3.connect(DB_PATH)

def create_tables():
    """
    Creates the necessary tables in the database if they do not exist.
    """
    conn = create_connection()
    cursor = conn.cursor()

    # create students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL
        )
    ''')

    # create instructors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS instructors (
            instructor_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL
        )
    ''')

    # create courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id TEXT PRIMARY KEY,
            course_name TEXT NOT NULL,
            instructor_id TEXT,
            FOREIGN KEY(instructor_id) REFERENCES instructors(instructor_id)
        )
    ''')

    # create registrations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            student_id TEXT,
            course_id TEXT,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY(student_id) REFERENCES students(student_id),
            FOREIGN KEY(course_id) REFERENCES courses(course_id)
        )
    ''')

    conn.commit()
    conn.close()

# CRUD operations for students
def add_student(student):
    """
    Adds a student to the database.

    :param student: The student to add.
    :type student: Student
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO students (student_id, name, age, email)
        VALUES (?, ?, ?, ?)
    ''', (student.student_id, student.name, student.age, student.email))
    conn.commit()
    conn.close()

def get_students():
    """
    Retrieves all students from the database.

    :return: List of Student objects.
    :rtype: list of Student
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    rows = cursor.fetchall()
    conn.close()
    students = [Student(row[1], row[2], row[3], row[0]) for row in rows]
    return students

def update_student(student):
    """
    Updates a student's information in the database.

    :param student: The student with updated information.
    :type student: Student
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE students
        SET name = ?, age = ?, email = ?
        WHERE student_id = ?
    ''', (student.name, student.age, student.email, student.student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    """
    Deletes a student from the database.

    :param student_id: The ID of the student to delete.
    :type student_id: str
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM students WHERE student_id = ?
    ''', (student_id,))
    conn.commit()
    conn.close()

# CRUD operations for instructors
def add_instructor(instructor):
    """
    Adds an instructor to the database.

    :param instructor: The instructor to add.
    :type instructor: Instructor
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO instructors (instructor_id, name, age, email)
        VALUES (?, ?, ?, ?)
    ''', (instructor.instructor_id, instructor.name, instructor.age, instructor.email))
    conn.commit()
    conn.close()

def get_instructors():
    """
    Retrieves all instructors from the database.

    :return: List of Instructor objects.
    :rtype: list of Instructor
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM instructors')
    rows = cursor.fetchall()
    conn.close()
    instructors = [Instructor(row[1], row[2], row[3], row[0]) for row in rows]
    return instructors

def update_instructor(instructor):
    """
    Updates an instructor's information in the database.

    :param instructor: The instructor with updated information.
    :type instructor: Instructor
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE instructors
        SET name = ?, age = ?, email = ?
        WHERE instructor_id = ?
    ''', (instructor.name, instructor.age, instructor.email, instructor.instructor_id))
    conn.commit()
    conn.close()

def delete_instructor(instructor_id):
    """
    Deletes an instructor from the database.

    :param instructor_id: The ID of the instructor to delete.
    :type instructor_id: str
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM instructors WHERE instructor_id = ?
    ''', (instructor_id,))
    conn.commit()
    conn.close()

# CRUD operations for courses
def add_course(course):
    """
    Adds a course to the database.

    :param course: The course to add.
    :type course: Course
    """
    conn = create_connection()
    cursor = conn.cursor()
    instructor_id = course.instructor.instructor_id if course.instructor else None
    cursor.execute('''
        INSERT INTO courses (course_id, course_name, instructor_id)
        VALUES (?, ?, ?)
    ''', (course.course_id, course.course_name, instructor_id))
    conn.commit()
    conn.close()

def get_courses():
    """
    Retrieves all courses from the database.

    :return: List of Course objects.
    :rtype: list of Course
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM courses')
    rows = cursor.fetchall()
    conn.close()
    instructors = get_instructors()
    courses = []
    for row in rows:
        instructor = next((i for i in instructors if i.instructor_id == row[2]), None)
        course = Course(row[0], row[1], instructor)
        courses.append(course)
    return courses

def update_course(course):
    """
    Updates a course's information in the database.

    :param course: The course with updated information.
    :type course: Course
    """
    conn = create_connection()
    cursor = conn.cursor()
    instructor_id = course.instructor.instructor_id if course.instructor else None
    cursor.execute('''
        UPDATE courses
        SET course_name = ?, instructor_id = ?
        WHERE course_id = ?
    ''', (course.course_name, instructor_id, course.course_id))
    conn.commit()
    conn.close()

def delete_course(course_id):
    """
    Deletes a course from the database.

    :param course_id: The ID of the course to delete.
    :type course_id: str
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM courses WHERE course_id = ?
    ''', (course_id,))
    conn.commit()
    conn.close()

# Registration operations
def add_registration(student_id, course_id):
    """
    Adds a registration entry for a student and a course.

    :param student_id: The ID of the student.
    :type student_id: str
    :param course_id: The ID of the course.
    :type course_id: str
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO registrations (student_id, course_id)
        VALUES (?, ?)
    ''', (student_id, course_id))
    conn.commit()
    conn.close()

def get_student_courses(student_id):
    """
    Retrieves all courses a student is registered in.

    :param student_id: The ID of the student.
    :type student_id: str
    :return: List of course IDs.
    :rtype: list of str
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT course_id FROM registrations WHERE student_id = ?
    ''', (student_id,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

def remove_registration(student_id, course_id):
    """
    Removes a registration entry for a student and a course.

    :param student_id: The ID of the student.
    :type student_id: str
    :param course_id: The ID of the course.
    :type course_id: str
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM registrations WHERE student_id = ? AND course_id = ?
    ''', (student_id, course_id))
    conn.commit()
    conn.close()

def backup_database(backup_path):
    """
    Backs up the database to a specified file path.

    :param backup_path: The path to save the backup.
    :type backup_path: str
    """
    try:
        shutil.copyfile(DB_PATH, backup_path)
        print(f"Database backed up to {backup_path}")
    except Exception as e:
        print(f"Error backing up database: {e}")
