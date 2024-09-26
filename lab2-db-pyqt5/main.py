"""
main.py

This module contains the class definitions for the School Management System.

Classes:
- Person
- Student
- Instructor
- Course
"""

import re
import json

class Person(object):
    """
    The Person class represents a generic person with basic attributes.

    :param name: The name of the person.
    :type name: str
    :param age: The age of the person.
    :type age: int
    :param email: The email address of the person.
    :type email: str

    :raises AssertionError: If input types are incorrect.
    :raises ValueError: If email format is invalid.
    """

    def __init__(self, name, age, email):
        assert isinstance(name, str) and isinstance(age, int) and isinstance(email, str), "WRONG INPUT FORMAT"
        assert age > 0, "Age should be positive"
        self.name = name
        self.age = age
        self.email = self.__validate_email(email) # I made it public here cause it's needed for the database
        
    def __validate_email(self, email):
        """
        Validates the email format.

        :param email: The email to validate.
        :type email: str
        :return: The validated email.
        :rtype: str
        :raises ValueError: If email format is invalid.
        """
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w{2,3}$'
        if re.match(email_regex, email):
            return email
        else:
            raise ValueError("Invalid email format")

    def introduce(self):
        """
        Prints the introduction of the person.
        """
        print(f"Name is {self.name}, aged {self.age}")
        
    def to_dict(self):
        """
        Converts the object to a dictionary.

        :return: Dictionary representation of the object.
        :rtype: dict
        """
        return {
            "name": self.name,
            "age": self.age,
            "email": self.__email
        }

class Student(Person):
    """
    The Student class represents a student, inheriting from Person.

    :param name: The name of the student.
    :type name: str
    :param age: The age of the student.
    :type age: int
    :param email: The email address of the student.
    :type email: str
    :param student_id: The unique ID of the student.
    :type student_id: str
    :param registered_courses: List of courses the student is registered in.
    :type registered_courses: list

    :raises AssertionError: If input types are incorrect.
    """

    def __init__(self, name, age, email, student_id, registered_courses=None):
        super().__init__(name, age, email)
        if registered_courses is None:
            registered_courses = []
        assert isinstance(student_id, str), "student_id should be a string"
        assert isinstance(registered_courses, list), "registered_courses should be a list"
        for course in registered_courses:
            assert isinstance(course, Course), "Each registered course should be a Course object"
        self.student_id = student_id
        self.registered_courses = registered_courses

    def register_course(self, course):
        """
        Registers the student in a course.

        :param course: The course to register.
        :type course: Course
        :raises AssertionError: If the course is not a Course object.
        """
        assert isinstance(course, Course), "The course should be a Course object"
        self.registered_courses.append(course)

    def to_dict(self):
        """
        Converts the object to a dictionary.

        :return: Dictionary representation of the student.
        :rtype: dict
        """
        data = super().to_dict()
        data.update({
            'student_id': self.student_id,
            'registered_courses': [course.course_id for course in self.registered_courses],
        })
        return data

    @classmethod
    def from_dict(cls, data, courses):
        """
        Creates a Student object from a dictionary.

        :param data: The data dictionary.
        :type data: dict
        :param courses: List of available courses.
        :type courses: list
        :return: A Student object.
        :rtype: Student
        """
        registered_courses = [next((c for c in courses if c.course_id == cid), None) for cid in data.get('registered_courses', [])]
        return cls(data['name'], data['age'], data['email'], data['student_id'], registered_courses)

class Instructor(Person):
    """
    The Instructor class represents an instructor, inheriting from Person.

    :param name: The name of the instructor.
    :type name: str
    :param age: The age of the instructor.
    :type age: int
    :param email: The email address of the instructor.
    :type email: str
    :param instructor_id: The unique ID of the instructor.
    :type instructor_id: str
    :param assigned_courses: List of courses assigned to the instructor.
    :type assigned_courses: list

    :raises AssertionError: If input types are incorrect.
    """

    def __init__(self, name, age, email, instructor_id, assigned_courses=None):
        super().__init__(name, age, email)
        if assigned_courses is None:
            assigned_courses = []
        assert isinstance(instructor_id, str), "instructor_id should be a string"
        assert isinstance(assigned_courses, list), "assigned_courses should be a list"
        for course in assigned_courses:
            assert isinstance(course, Course), "Each assigned course should be a Course object"
        self.instructor_id = instructor_id
        self.assigned_courses = assigned_courses

    def assign_course(self, course):
        """
        Assigns a course to the instructor.

        :param course: The course to assign.
        :type course: Course
        :raises AssertionError: If the course is not a Course object.
        """
        assert isinstance(course, Course), "The course should be a Course object"
        self.assigned_courses.append(course)
        
    def to_dict(self):
        """
        Converts the object to a dictionary.

        :return: Dictionary representation of the instructor.
        :rtype: dict
        """
        data = super().to_dict()
        data.update({
            'instructor_id': self.instructor_id,
            'assigned_courses': [course.course_id for course in self.assigned_courses],
        })
        return data

    @classmethod
    def from_dict(cls, data, courses):
        """
        Creates an Instructor object from a dictionary.

        :param data: The data dictionary.
        :type data: dict
        :param courses: List of available courses.
        :type courses: list
        :return: An Instructor object.
        :rtype: Instructor
        """
        assigned_courses = [next((c for c in courses if c.course_id == cid), None) for cid in data.get('assigned_courses', [])]
        return cls(data['name'], data['age'], data['email'], data['instructor_id'], assigned_courses)

class Course(object):
    """
    The Course class represents a course in the system.

    :param course_id: The unique ID of the course.
    :type course_id: str
    :param course_name: The name of the course.
    :type course_name: str
    :param instructor: The instructor teaching the course.
    :type instructor: Instructor
    :param enrolled_students: List of students enrolled in the course.
    :type enrolled_students: list

    :raises AssertionError: If input types are incorrect.
    """

    def __init__(self, course_id, course_name, instructor, enrolled_students=None):
        if enrolled_students is None:
            enrolled_students = []
        assert isinstance(course_id, str), "course_id should be a string"
        assert isinstance(course_name, str), "course_name should be a string"
        assert isinstance(instructor, Instructor), "instructor should be an Instructor object"
        assert isinstance(enrolled_students, list), "enrolled_students should be a list"
        for student in enrolled_students:
            assert isinstance(student, Student), "Each enrolled student should be a Student object"
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = enrolled_students

    def add_student(self, student):
        """
        Adds a student to the course.

        :param student: The student to add.
        :type student: Student
        :raises AssertionError: If the student is not a Student object.
        """
        assert isinstance(student, Student), "The student should be a Student object"
        self.enrolled_students.append(student)

    def to_dict(self):
        """
        Converts the object to a dictionary.

        :return: Dictionary representation of the course.
        :rtype: dict
        """
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "instructor_id": self.instructor.instructor_id if self.instructor else None,
            "enrolled_students": [student.student_id for student in self.enrolled_students]
        }
        
    @classmethod
    def from_dict(cls, data, instructors, students):
        """
        Creates a Course object from a dictionary.

        :param data: The data dictionary.
        :type data: dict
        :param instructors: List of available instructors.
        :type instructors: list
        :param students: List of available students.
        :type students: list
        :return: A Course object.
        :rtype: Course
        """
        instructor = next((i for i in instructors if i.instructor_id == data.get('instructor_id')), None)
        enrolled_students = [next((s for s in students if s.student_id == sid), None) for sid in data.get('enrolled_students', [])]
        return cls(data['course_id'], data['course_name'], instructor, enrolled_students)
