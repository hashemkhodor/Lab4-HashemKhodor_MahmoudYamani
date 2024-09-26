import re
import json

class Person(object):
    def __init__(self, name, age, email):
        assert isinstance(name, str) and isinstance(age, int) and isinstance(email, str), "WRONG INPUT FORMAT"
        assert age > 0, "Age should be positive"
        self.name = name
        self.age = age
        self.email = self.__validate_email(email) #made it public to edit it after/and to use in DB; alt we can use the self.__email
    
    def __validate_email(self, email):
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w{2,3}$'
        if re.match(email_regex, email):
            return email
        else:
            raise ValueError("Invalid email format")

    def introduce(self):
        print("Name is "+str(self.name)+", aged "+str(self.age))
    
    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "email": self.__email
        }

class Student(Person):
    def __init__(self, name, age, email, student_id, registered_courses=[]):
        super().__init__(name, age, email)
        assert isinstance(student_id, str), "student_id should be a string"
        assert isinstance(registered_courses, list), "registered_courses should be a list"
        for course in registered_courses:
            assert isinstance(course, Course), "Each registered course should be a Course object"
        self.student_id = student_id
        self.registered_courses = registered_courses

    def register_course(self, course):
        assert isinstance(course, Course), "The course should be a Course object"
        self.registered_courses.append(course)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'student_id': self.student_id,
            'registered_courses': [course.course_id for course in self.registered_courses],
        })
        return data

    @classmethod
    def from_dict(cls, data, courses):
        registered_courses = [next((c for c in courses if c.course_id == cid), None) for cid in data.get('registered_courses', [])]
        return cls(data['name'], data['age'], data['email'], data['student_id'], registered_courses)

class Instructor(Person):
    def __init__(self, name, age, email, instructor_id, assigned_courses=[]):
        super().__init__(name, age, email)
        assert isinstance(instructor_id, str), "instructor_id should be a string"
        assert isinstance(assigned_courses, list), "assigned_courses should be a list"
        for course in assigned_courses:
            assert isinstance(course, Course), "Each assigned course should be a Course object"

        self.instructor_id = instructor_id
        self.assigned_courses = assigned_courses

    def assign_course(self, course):
        assert isinstance(course, Course), "The course should be a Course object"
        self.assigned_courses.append(course)
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'instructor_id': self.instructor_id,
            'assigned_courses': [course.course_id for course in self.assigned_courses],
        })
        return data

    @classmethod
    def from_dict(cls, data, courses):
        assigned_courses = [next((c for c in courses if c.course_id == cid), None) for cid in data.get('assigned_courses', [])]
        return cls(data['name'], data['age'], data['email'], data['instructor_id'], assigned_courses)

class Course(object):
    def __init__(self, course_id, course_name, instructor, enrolled_students=[]):
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
        assert isinstance(student, Student), "The student should be a Student object"
        self.enrolled_students.append(student)

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "instructor_id": self.instructor.instructor_id if self.instructor else None,
            "enrolled_students": [student.student_id for student in self.enrolled_students]
        }
    
    @classmethod
    def from_dict(cls, data, instructors, students):
        instructor = next((i for i in instructors if i.instructor_id == data.get('instructor_id')), None)
        enrolled_students = [next((s for s in students if s.student_id == sid), None) for sid in data.get('enrolled_students', [])]
        return cls(data['course_id'], data['course_name'], instructor, enrolled_students)
