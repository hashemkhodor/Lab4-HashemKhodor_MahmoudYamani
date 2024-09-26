from abc import ABC, abstractmethod
import os
import sqlite3
import json
from typing import Any

from src.schemas import Student, Instructor, Course


class Table(ABC):
    """
    Abstract base class for representing database tables.

    :param db_path: Path to the SQLite database file.
    :type db_path: str

    :ivar db_path: The database path.
    :vartype db_path: str
    :ivar conn: The SQLite connection object.
    :vartype conn: sqlite3.Connection
    :ivar cursor: The SQLite cursor for executing SQL commands.
    :vartype cursor: sqlite3.Cursor

    :raises AssertionError: If the database path does not exist.

    Methods:
        - :meth:`delete_record`: Abstract method for deleting a record from the table.
        - :meth:`create_table`: Abstract static method for creating the table in the database.
        - :meth:`upsert_row`: Abstract method for inserting or updating a row in the table.
        - :meth:`query`: Abstract method for querying records from the table.
        - :meth:`close_connection`: Closes the database connection.
    """

    def __init__(self, db_path: str) -> None:
        """
        Initializes a Table object and connects to the SQLite database.

        :param db_path: Path to the SQLite database file.
        :type db_path: str
        """
        assert os.path.exists(db_path), "Database path doesn't exist"
        self.db_path: str = db_path
        self.conn: sqlite3.Connection = sqlite3.connect(db_path)
        self.cursor: sqlite3.Cursor = self.conn.cursor()

    @abstractmethod
    def delete_record(self, *args, **kwargs) -> None:
        """
        Abstract method for deleting a record from the table.

        :raises NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError("Please implement this method")

    @staticmethod
    @abstractmethod
    def create_table(db_path: str) -> None:
        """
        Abstract static method for creating the table in the database.

        :param db_path: Path to the SQLite database file.
        :type db_path: str

        :raises NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError("Please implement this method")

    @abstractmethod
    def upsert_row(self, row: Any) -> None:
        """
        Abstract method for inserting or updating a row in the table.

        :param row: The row data to insert or update.
        :type row: Any

        :raises NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError("Please implement this method")

    @abstractmethod
    def query(self, *args, **kwargs) -> list[Any]:
        """
        Abstract method for querying records from the table.

        :returns: A list of query results.
        :rtype: list[Any]

        :raises NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError("Please implement this method")

    def close_connection(self):
        """
        Closes the database connection.
        """
        self.conn.close()


class PersonTable(Table):
    """
    A class representing the Person table in the database, inheriting from Table.

    Methods:
        - :meth:`query`: Queries the Person table based on whether the person is a student or an instructor.
        - :meth:`delete_record`: Deletes a record from the Person table.
        - :meth:`upsert_row`: Inserts or updates a row in the Person table.
        - :meth:`create_table`: Creates the Person table in the database.
    """

    def __init__(self, db_path: str) -> None:
        """
        Initializes a PersonTable object and connects to the SQLite database.

        :param db_path: Path to the SQLite database file.
        :type db_path: str
        """
        super().__init__(db_path=db_path)

    def query(self, is_student: bool) -> dict[str, Student] | dict[str, Instructor]:
        """
        Queries the Person table based on whether the person is a student or an instructor.

        :param is_student: True to query students, False to query instructors.
        :type is_student: bool

        :returns: A dictionary mapping person IDs to Student or Instructor objects.
        :rtype: dict[str, Student] | dict[str, Instructor]
        """
        self.cursor.execute(f'SELECT * FROM Person WHERE is_student = {int(is_student)}')
        rows = self.cursor.fetchall()
        results = {}
        for row in rows:
            courses = set(json.loads(row[4]))
            if is_student:
                person = Student(student_id=row[0], name=row[1], age=int(row[2]), _email=row[3])
                person.registered_courses = courses
            else:
                person = Instructor(instructor_id=row[0], name=row[1], age=int(row[2]), _email=row[3])
                person.assigned_courses = courses
            results[person.get_id()] = person

        return results

    def delete_record(self, person_id: str) -> None:
        """
        Deletes a record from the Person table.

        :param person_id: The ID of the person to delete.
        :type person_id: str
        """
        self.cursor.execute('''DELETE FROM Person WHERE id = ?''', (person_id,))
        self.conn.commit()

    def upsert_row(self, row: Student | Instructor) -> None:
        """
        Inserts or updates a row in the Person table.

        :param row: A Student or Instructor object.
        :type row: Student | Instructor

        :raises AssertionError: If the provided row is not a Student or Instructor.
        """
        assert isinstance(row, Student) or isinstance(row, Instructor), "Invalid Type."
        self.cursor.execute('''
                INSERT INTO Person (id, name, age, email, courses, is_student)
                VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET
                                name=excluded.name,
                                age=excluded.age,
                                email=excluded.email,
                                courses=excluded.courses,
                                is_student=excluded.is_student
                ''', (row.get_id(), row.get_name(), row.get_age(), row.get_email(),
                      json.dumps(list(row.get_courses())), int(isinstance(row, Student))))
        self.conn.commit()

    @staticmethod
    def create_table(db_path: str) -> None:
        """
        Creates the Person table in the database.

        :param db_path: Path to the SQLite database file.
        :type db_path: str
        """
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Person (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age TEXT NOT NULL,
                email TEXT NOT NULL,
                courses TEXT,
                is_student INTEGER
            )
            ''')
        connection.commit()


class CourseTable(Table):
    """
    A class representing the Course table in the database, inheriting from Table.

    Methods:
        - :meth:`query`: Queries the Course table.
        - :meth:`delete_record`: Deletes a record from the Course table.
        - :meth:`upsert_row`: Inserts or updates a row in the Course table.
        - :meth:`create_table`: Creates the Course table in the database.
    """

    def __init__(self, db_path: str) -> None:
        """
        Initializes a CourseTable object and connects to the SQLite database.

        :param db_path: Path to the SQLite database file.
        :type db_path: str
        """
        super().__init__(db_path=db_path)

    def query(self) -> dict[str, Course]:
        """
        Queries the Course table.

        :returns: A dictionary mapping course IDs to Course objects.
        :rtype: dict[str, Course]
        """
        self.cursor.execute(f'SELECT * FROM Course')
        rows = self.cursor.fetchall()
        results = {}
        for row in rows:
            course = Course(course_id=row[0], course_name=row[1], instructor_id=row[2])
            course.enrolled_students = set(json.loads(row[3]))
            results[course.course_id] = course
        return results

    def delete_record(self, course_id: str) -> None:
        """
        Deletes a record from the Course table.

        :param course_id: The ID of the course to delete.
        :type course_id: str
        """
        self.cursor.execute('''DELETE FROM Course WHERE course_id = ?''', (course_id,))
        self.conn.commit()

    def upsert_row(self, row: Course) -> None:
        """
        Inserts or updates a row in the Course table.

        :param row: A Course object.
        :type row: Course
        """
        self.cursor.execute('''
                INSERT INTO Course (course_id, course_name, instructor_id, enrolled_students)
                VALUES (?, ?, ?, ?)  ON CONFLICT(course_id) DO UPDATE SET
                            course_name=excluded.course_name,
                            instructor_id=excluded.instructor_id,
                            enrolled_students=excluded.enrolled_students
                ''', (
            row.get_id(), row.get_name(), row.get_instructor(), json.dumps(list(row.get_enrolled_students()))))
        self.conn.commit()

    @staticmethod
    def create_table(db_path: str) -> None:
        """
        Creates the Course table in the database.

        :param db_path: Path to the SQLite database file.
        :type db_path: str
        """
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute(
            '''
                CREATE TABLE IF NOT EXISTS Course (
                    course_id TEXT PRIMARY KEY,
                    course_name TEXT NOT NULL,
                    instructor_id TEXT,
                    enrolled_students TEXT
                )
                '''
        )
        connection.commit()


if __name__ == "__main__":
    course_table = CourseTable("school.db")
    person_table = PersonTable("school.db")

    print(course_table.query())
    print(person_table.query(is_student=True))

    # print(course_table.delete_record("CS101"))
    print(course_table.query())
