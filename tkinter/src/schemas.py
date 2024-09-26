import json
import re
from abc import ABC, abstractmethod
from typing import Any

email_validate_pattern = r"^\S+@\S+\.\S+$"


class Serializable(ABC):
    """
    Abstract base class that defines methods for serializing objects to and from various formats.

    Methods:
        to_treeview_record: Convert object data to a tuple for tree view representation.
        to_dict: Serialize object data to a dictionary.
        parse_json: Parse JSON-formatted string data.
        parse_csv: Parse CSV-formatted string data.
        from_dict: Create an object from a dictionary.
        serialize_json: Convert the object to a JSON-formatted string.
        serialize_csv: Convert the object data to a CSV-formatted string.
        headers: Get a list of headers (fields) from the object.
        header_csv: Get a CSV-formatted string of headers.
    """

    @abstractmethod
    def to_treeview_record(self) -> tuple:
        """
        Convert the object to a tuple for tree view representation.

        :return: A tuple representing the object's key attributes.
        :rtype: tuple
        """
        raise NotImplementedError("Must implement to_treeview_record()")

    @abstractmethod
    def to_dict(self, *args, **kwargs) -> dict:
        """
        Serialize the object to a dictionary.

        :return: Dictionary representation of the object.
        :rtype: dict
        """
        raise NotImplementedError("Must implement to_dict()")

    @staticmethod
    @abstractmethod
    def parse_json(content: str, *args, **kwargs) -> Any:
        """
        Parse a JSON string to create an object.

        :param content: JSON-formatted string.
        :type content: str
        :return: Parsed object.
        :rtype: Any
        """
        raise NotImplementedError("Must implement parse_json()")

    @staticmethod
    @abstractmethod
    def parse_csv(content: str, *args, **kwargs) -> Any:
        """
        Parse a CSV string to create an object.

        :param content: CSV-formatted string.
        :type content: str
        :return: Parsed object.
        :rtype: Any
        """
        raise NotImplementedError("Must implement parse_csv()")

    @staticmethod
    @abstractmethod
    def from_dict(content: dict, *args, **kwargs) -> Any:
        """
        Create an object from a dictionary.

        :param content: Dictionary containing object data.
        :type content: dict
        :return: Created object.
        :rtype: Any
        """
        raise NotImplementedError("Must implement from_dict()")

    def serialize_json(self) -> str:
        """
        Serialize the object to a JSON-formatted string.

        :return: JSON string representation of the object.
        :rtype: str
        """
        return json.dumps(self.to_dict(), indent=4, default=vars)

    def serialize_csv(self) -> str:
        """
        Serialize the object to a CSV-formatted string.

        :return: CSV string representation of the object.
        :rtype: str
        """
        content = list(self.to_dict().items())
        content.sort(key=lambda item: item[0])
        return ",".join([cont[1] for cont in content])

    def headers(self) -> list[str]:
        """
        Get the list of headers (fields) from the object.

        :return: Sorted list of field names.
        :rtype: list[str]
        """
        content = list(self.to_dict().keys())
        content.sort()
        return sorted(content)

    def header_csv(self) -> str:
        """
        Get a CSV-formatted string of headers.

        :return: CSV string of field names.
        :rtype: str
        """
        return ",".join([header for header in self.headers()])


class Person(Serializable, ABC):
    """
    Abstract base class representing a person.

    :param name: Name of the person.
    :type name: str
    :param age: Age of the person.
    :type age: int
    :param _email: Email address of the person.
    :type _email: str

    :ivar name: Name of the person.
    :vartype name: str
    :ivar age: Age of the person.
    :vartype age: int
    :ivar _email: Email address of the person.
    :vartype _email: str
    """

    def __init__(self, name: str, age: int, _email: str, *args, **kwargs) -> None:
        """
        Initialize a Person object.

        :param name: Name of the person.
        :type name: str
        :param age: Age of the person.
        :type age: int
        :param _email: Email address of the person.
        :type _email: str
        :raises AssertionError: If input types are incorrect or age is out of range.
        """
        assert isinstance(name, str), "Name must be a string"
        assert isinstance(age, int) and 0 < age <= 101, "Age must be an integer between 0 and 101"
        assert isinstance(_email, str) and re.match(email_validate_pattern, _email), "Email must be a valid string"
        self.name: str = name
        self.age: int = age
        self._email: str = _email

    def introduce(self) -> None:
        """
        Print an introduction message for the person.
        """
        print(
            f"Hello, I'm {self.name} and I'm {self.age} years old. If you want to contact me, send an email to {self._email}")

    def get_name(self) -> str:
        """
        Get the name of the person.

        :return: Name of the person.
        :rtype: str
        """
        return self.name

    def get_age(self) -> int:
        """
        Get the age of the person.

        :return: Age of the person.
        :rtype: int
        """
        return self.age

    def get_email(self) -> str:
        """
        Get the email address of the person.

        :return: Email address of the person.
        :rtype: str
        """
        return self._email

    def set_name(self, name: str) -> None:
        """
        Set the name of the person.

        :param name: Name of the person.
        :type name: str
        :raises AssertionError: If name is not a string.
        """
        assert isinstance(name, str), "Name must be a string"
        self.name = name

    def set_age(self, age: int) -> None:
        """
        Set the age of the person.

        :param age: Age of the person.
        :type age: int
        :raises AssertionError: If age is not an integer or out of range.
        """
        assert isinstance(age, int) and 0 < age < 101, "Age must be an integer between 1 and 100"
        self.age = age

    def set_email(self, email: str) -> None:
        """
        Set the email address of the person.

        :param email: Email address of the person.
        :type email: str
        :raises AssertionError: If email is not a valid string.
        """
        assert isinstance(email, str) and re.match(email_validate_pattern, email), "Email must be a valid string"
        self._email = email

    @staticmethod
    def get_fields() -> list:
        """
        Get a list of fields for the Person class.

        :return: List of field names.
        :rtype: list[str]
        """
        return ["name", "age", "email"]

    def to_dict(self) -> dict:
        """
        Serialize the Person object to a dictionary.

        :return: Dictionary representation of the object.
        :rtype: dict
        """
        return {"name": self.name, "age": self.age, "email": self._email}


class Student(Person):
    """
    A class representing a student, inheriting from Person.

    :param name: Name of the student.
    :type name: str
    :param age: Age of the student.
    :type age: int
    :param _email: Email address of the student.
    :type _email: str
    :param student_id: The student's unique identifier.
    :type student_id: str

    :ivar student_id: The unique identifier for the student.
    :vartype student_id: str
    :ivar registered_courses: Set of registered course IDs.
    :vartype registered_courses: set[str]
    """

    def __init__(self, name: str, age: int, _email: str, student_id: str, *args, **kwargs) -> None:
        """
        Initialize a Student object.

        :param name: Name of the student.
        :type name: str
        :param age: Age of the student.
        :type age: int
        :param _email: Email address of the student.
        :type _email: str
        :param student_id: The student's unique identifier.
        :type student_id: str
        :raises AssertionError: If student_id is not a string.
        """
        super().__init__(name=name, age=age, _email=_email, *args, **kwargs)
        assert isinstance(student_id, str), "student_id must be a string"
        self.student_id: str = student_id
        self.registered_courses: set[str] = set()  # contains the IDs of the registered courses

    def register_course(self, course: str) -> None:
        """
        Register a course for the student.

        :param course: The course ID.
        :type course: str
        """
        self.registered_courses.add(course)

    def remove_course(self, course: str) -> None:
        """
        Remove a course from the student's registered courses.

        :param course: The course ID.
        :type course: str
        """
        self.registered_courses.discard(course)

    def get_id(self) -> str:
        """
        Get the student's ID.

        :return: Student ID.
        :rtype: str
        """
        return self.student_id

    def get_courses(self) -> set[str]:
        """
        Get the set of registered courses.

        :return: Set of registered course IDs.
        :rtype: set[str]
        """
        return self.registered_courses.copy()

    def to_dict(self) -> dict:
        """
        Serialize the Student object to a dictionary.

        :return: Dictionary representation of the Student object.
        :rtype: dict
        """
        return {**super().to_dict(), "student_id": self.student_id, "registered_courses": list(self.registered_courses)}

    def to_treeview_record(self) -> tuple:
        """
        Convert the Student object to a tuple for tree view representation.

        :return: Tuple containing student information.
        :rtype: tuple
        """
        return self.student_id, self.name, self.age, self._email, list(self.registered_courses)

    @staticmethod
    def from_dict(content: dict, *args, **kwargs) -> "Student":
        """
        Create a Student object from a dictionary.

        :param content: Dictionary containing the student's data.
        :type content: dict
        :return: The created Student object.
        :rtype: Student
        """
        student: Student = Student(**content)
        student.registered_courses = set(content["registered_courses"])
        return student

    @staticmethod
    def parse_json(content: str, *args, **kwargs) -> str:
        """
        Parse a JSON string to create a Student object.

        :param content: JSON-formatted string.
        :type content: str
        :return: Parsed object (not implemented).
        :rtype: str
        """
        pass

    @staticmethod
    def parse_csv(content: str, *args, **kwargs) -> str:
        """
        Parse a CSV string to create a Student object.

        :param content: CSV-formatted string.
        :type content: str
        :return: Parsed object (not implemented).
        :rtype: str
        """
        pass


class Instructor(Person):
    """
    A class representing an instructor, inheriting from Person.

    :param name: Name of the instructor.
    :type name: str
    :param age: Age of the instructor.
    :type age: int
    :param _email: Email address of the instructor.
    :type _email: str
    :param instructor_id: The instructor's unique identifier.
    :type instructor_id: str

    :ivar instructor_id: The unique identifier for the instructor.
    :vartype instructor_id: str
    :ivar assigned_courses: Set of course IDs that the instructor is assigned to teach.
    :vartype assigned_courses: set[str]
    """

    def __init__(self, name: str, age: int, _email: str, instructor_id: str, *args, **kwargs) -> None:
        """
        Initialize an Instructor object.

        :param name: Name of the instructor.
        :type name: str
        :param age: Age of the instructor.
        :type age: int
        :param _email: Email address of the instructor.
        :type _email: str
        :param instructor_id: The instructor's unique identifier.
        :type instructor_id: str
        :raises AssertionError: If instructor_id is not a string.
        """
        super().__init__(name=name, age=age, _email=_email)
        assert isinstance(instructor_id, str), "instructor_id must be a string"
        self.instructor_id: str = instructor_id
        self.assigned_courses: set[str] = set()

    def assign_course(self, course: str) -> None:
        """
        Assign a course to the instructor.

        :param course: The course ID to assign.
        :type course: str
        """
        self.assigned_courses.add(course)

    def remove_course(self, course: str) -> None:
        """
        Remove a course from the instructor's assigned courses.

        :param course: The course ID to remove.
        :type course: str
        """
        self.assigned_courses.discard(course)

    def get_id(self) -> str:
        """
        Get the instructor's ID.

        :return: Instructor ID.
        :rtype: str
        """
        return self.instructor_id

    def get_courses(self) -> set[str]:
        """
        Get the set of assigned courses.

        :return: Set of assigned course IDs.
        :rtype: set[str]
        """
        return self.assigned_courses.copy()

    def to_dict(self) -> dict:
        """
        Serialize the Instructor object to a dictionary.

        :return: Dictionary representation of the Instructor object.
        :rtype: dict
        """
        return {**super().to_dict(), "instructor_id": self.instructor_id,
                "assigned_courses": list(self.assigned_courses)}

    def to_treeview_record(self) -> tuple:
        """
        Convert the Instructor object to a tuple for tree view representation.

        :return: A tuple containing the instructor's ID, name, age, email, and assigned courses.
        :rtype: tuple
        """
        return self.instructor_id, self.name, self.age, self._email, list(self.assigned_courses)

    @staticmethod
    def from_dict(content: dict, *args, **kwargs) -> "Instructor":
        """
        Create an Instructor object from a dictionary.

        :param content: Dictionary containing the instructor's data.
        :type content: dict
        :return: The created Instructor object.
        :rtype: Instructor
        """
        instructor: Instructor = Instructor(**content)
        instructor.assigned_courses = set(content["assigned_courses"])
        return instructor

    @staticmethod
    def parse_json(content: str, *args, **kwargs) -> str:
        """
        Parse a JSON string to create an Instructor object.

        :param content: JSON-formatted string.
        :type content: str
        :return: Parsed object (not implemented).
        :rtype: str
        """
        pass

    @staticmethod
    def parse_csv(content: str, *args, **kwargs) -> str:
        """
        Parse a CSV string to create an Instructor object.

        :param content: CSV-formatted string.
        :type content: str
        :return: Parsed object (not implemented).
        :rtype: str
        """
        pass


class Course(Serializable):
    """
    A class representing a course.

    :param course_id: Unique identifier for the course.
    :type course_id: str
    :param course_name: Name of the course.
    :type course_name: str
    :param instructor_id: ID of the instructor teaching the course.
    :type instructor_id: str

    :ivar course_id: The unique identifier for the course.
    :vartype course_id: str
    :ivar course_name: The name of the course.
    :vartype course_name: str
    :ivar instructor_id: The instructor ID assigned to teach the course.
    :vartype instructor_id: str
    :ivar enrolled_students: Set of student IDs enrolled in the course.
    :vartype enrolled_students: set[str]
    """

    def __init__(self, course_id: str, course_name: str, instructor_id: str, *args, **kwargs) -> None:
        """
        Initialize a Course object.

        :param course_id: Unique identifier for the course.
        :type course_id: str
        :param course_name: Name of the course.
        :type course_name: str
        :param instructor_id: ID of the instructor teaching the course.
        :type instructor_id: str
        :raises AssertionError: If input types are incorrect.
        """
        assert isinstance(course_id, str), "course_id must be a string"
        assert isinstance(course_name, str), "course_name must be a string"
        assert isinstance(instructor_id, str), "instructor_id must be a string"

        self.course_id: str = course_id
        self.course_name: str = course_name
        self.instructor_id: str = instructor_id
        self.enrolled_students: set[str] = set()

    def add_student(self, student: str) -> None:
        """
        Add a student to the course.

        :param student: The student ID to add.
        :type student: str
        """
        self.enrolled_students.add(student)

    def remove_student(self, student: str) -> None:
        """
        Remove a student from the course.

        :param student: The student ID to remove.
        :type student: str
        """
        self.enrolled_students.discard(student)

    def get_enrolled_students(self) -> set[str]:
        """
        Get the set of students enrolled in the course.

        :return: Set of student IDs.
        :rtype: set[str]
        """
        return self.enrolled_students.copy()

    def get_id(self) -> str:
        """
        Get the course ID.

        :return: Course ID.
        :rtype: str
        """
        return self.course_id

    def set_instructor(self, instructor: str) -> None:
        """
        Set the instructor for the course.

        :param instructor: Instructor ID to assign to the course.
        :type instructor: str
        :raises AssertionError: If instructor ID is not a string.
        """
        assert isinstance(instructor, str), "Instructor ID must be a string"
        self.instructor_id = instructor

    def get_instructor(self) -> str:
        """
        Get the instructor's ID.

        :return: Instructor ID.
        :rtype: str
        """
        return self.instructor_id

    def set_name(self, name: str) -> None:
        """
        Set the name of the course.

        :param name: The new name of the course.
        :type name: str
        :raises AssertionError: If course name is not a string.
        """
        assert isinstance(name, str), "Course name must be a string"
        self.course_name = name

    def get_name(self) -> str:
        """
        Get the name of the course.

        :return: Course name.
        :rtype: str
        """
        return self.course_name

    def to_dict(self) -> dict:
        """
        Serialize the Course object to a dictionary.

        :return: Dictionary representation of the Course object.
        :rtype: dict
        """
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "instructor_id": self.instructor_id,
            "enrolled_students": list(self.enrolled_students),
        }

    def to_treeview_record(self) -> tuple:
        """
        Convert the Course object to a tuple for tree view representation.

        :return: A tuple containing the course ID, course name, instructor ID, and enrolled students.
        :rtype: tuple
        """
        return self.course_id, self.course_name, self.instructor_id, list(self.enrolled_students)

    @staticmethod
    def from_dict(content: dict, *args, **kwargs) -> "Course":
        """
        Create a Course object from a dictionary.

        :param content: Dictionary containing the course's data.
        :type content: dict
        :return: The created Course object.
        :rtype: Course
        """
        course: Course = Course(**content)
        course.enrolled_students = set(content["enrolled_students"])
        return course

    @staticmethod
    def parse_json(content: str, *args, **kwargs) -> str:
        """
        Parse a JSON string to create a Course object.

        :param content: JSON-formatted string.
        :type content: str
        :return: Parsed object (not implemented).
        :rtype: str
        """
        pass

    @staticmethod
    def parse_csv(content: str, *args, **kwargs) -> str:
        """
        Parse a CSV string to create a Course object.

        :param content: CSV-formatted string.
        :type content: str
        :return: Parsed object (not implemented).
        :rtype: str
        """
        pass


if __name__ == "__main__":
    student = Student(name="Hashem", age=12, _email="hmk57@mail.com", student_id="<EMAIL>")
    print(student)