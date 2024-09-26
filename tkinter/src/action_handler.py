from src.db.db import CourseTable, PersonTable
from src.schemas import Course, Instructor, Student


class ActionHandler:
    """
    A handler class for managing courses, students, and instructors.

    Handles the operations related to courses, students, and instructors, including adding,
    editing, and deleting these entities in the system.

    :param courses: Dictionary of courses, keyed by course ID.
    :type courses: dict[str, Course]
    :param students: Dictionary of students, keyed by student ID.
    :type students: dict[str, Student]
    :param instructors: Dictionary of instructors, keyed by instructor ID.
    :type instructors: dict[str, Instructor]
    :param course_table: Database table for courses.
    :type course_table: CourseTable
    :param person_table: Database table for people (students, instructors).
    :type person_table: PersonTable
    """

    def __init__(self, courses: dict[str, Course], students: dict[str, Student],
                 instructors: dict[str, Instructor], course_table: CourseTable, person_table: PersonTable) -> None:
        self.courses: dict[str, Course] = courses
        self.students: dict[str, Student] = students
        self.instructors: dict[str, Instructor] = instructors

        self.course_table: CourseTable = course_table
        self.person_table: PersonTable = person_table

    def add_course(self, course: Course) -> None:
        """
        Add a new course to the system.

        Adds the given course to the local dictionary and updates the course table in the database.

        :param course: The course object to add.
        :type course: Course
        :return: None
        """
        self.courses[course.course_id] = course
        self.course_table.upsert_row(course)

    def add_student(self, student: Student) -> None:
        """
        Add a new student to the system.

        Adds the given student to the local dictionary and updates the person table in the database.

        :param student: The student object to add.
        :type student: Student
        :return: None
        """
        self.students[student.student_id] = student
        self.person_table.upsert_row(student)

    def add_instructor(self, instructor: Instructor) -> None:
        """
        Add a new instructor to the system.

        Adds the given instructor to the local dictionary and updates the person table in the database.

        :param instructor: The instructor object to add.
        :type instructor: Instructor
        :return: None
        """
        self.instructors[instructor.instructor_id] = instructor
        self.person_table.upsert_row(instructor)

    def edit_course(self, course_id: str, new_course: Course) -> None:
        """
        Edit an existing course's details.

        Updates the course's name, instructor, and enrolled students based on the provided new course details.

        :param course_id: The ID of the course to edit.
        :type course_id: str
        :param new_course: The new course object with updated details.
        :type new_course: Course
        :return: None
        """
        old_course: Course = self.courses[course_id]
        # name
        old_course.set_name(new_course.get_name())

        # instructor_id
        old_instructor_id = old_course.get_instructor()
        new_instructor_id = new_course.get_instructor()

        if old_instructor_id != new_instructor_id:
            if old_instructor_id in self.instructors:
                self.instructors[old_instructor_id].remove_course(course_id)
                self.person_table.upsert_row(self.instructors[old_instructor_id])

            if new_instructor_id in self.instructors:
                self.instructors[new_instructor_id].assign_course(course_id)
                self.person_table.upsert_row(self.instructors[new_instructor_id])
            old_course.set_instructor(new_instructor_id)

        # enrolled_students
        removed_students = old_course.get_enrolled_students() - new_course.get_enrolled_students()
        for student in removed_students:
            self.students[student].remove_course(course_id)
            # self.person_table.upsert
            self.person_table.upsert_row(self.students[student])
            old_course.remove_student(student)

        add_students = new_course.get_enrolled_students() - old_course.get_enrolled_students()
        for student in add_students:
            self.students[student].register_course(student)
            # self.person_table.upsert
            self.person_table.upsert_row(self.students[student])
            old_course.add_student(student)

        self.course_table.upsert_row(old_course)

    def edit_student(self, old_student_id: str, new_student: Student) -> None:
        """
        Edit an existing student's details.

        Updates the student's name, email, age, and registered courses based on the new student details.

        :param old_student_id: The ID of the student to edit.
        :type old_student_id: str
        :param new_student: The new student object with updated details.
        :type new_student: Student
        :return: None
        """
        old_student: Student = self.students[old_student_id]

        # Updating fields
        old_student.set_name(new_student.get_name())
        old_student.set_email(new_student.get_email())
        old_student.set_age(new_student.get_age())

        # removed courses
        removed_courses = old_student.get_courses() - new_student.get_courses()
        for course in removed_courses:
            self.courses[course].remove_student(old_student_id)
            # UPDATE DB
            self.course_table.upsert_row(self.courses[course])

            old_student.remove_course(course)

        # added courses
        new_courses = new_student.get_courses() - old_student.get_courses()
        for course in new_courses:
            old_student.register_course(course)
            # self.person.upsert
            self.courses[course].add_student(old_student_id)
            self.course_table.upsert_row(self.courses[course])

        # UPDATE STUDENT
        self.person_table.upsert_row(old_student)

    def edit_instructor(self, old_instructor_id: str, new_instructor: Instructor) -> None:
        """
        Edit an existing instructor's details.

        Updates the instructor's name, age, and assigned courses based on the new instructor details.

        :param old_instructor_id: The ID of the instructor to edit.
        :type old_instructor_id: str
        :param new_instructor: The new instructor object with updated details.
        :type new_instructor: Instructor
        :return: None
        """
        old_instructor: Instructor = self.instructors[old_instructor_id]
        old_instructor.set_age(new_instructor.get_age())
        old_instructor.set_name(new_instructor.get_name())

        # removed courses
        removed_courses = old_instructor.get_courses() - new_instructor.get_courses()
        for course in removed_courses:
            self.courses[course].instructor_id = None
            old_instructor.remove_course(course)
            self.course_table.upsert_row(self.courses[course])

        # add new courses
        new_courses = new_instructor.get_courses() - old_instructor.get_courses()
        for course in new_courses:
            old_course_instructor_id = self.courses[course].instructor_id
            if old_course_instructor_id:
                self.instructors[old_course_instructor_id].remove_course(course)
            self.courses[course].set_instructor(old_instructor_id)
            old_instructor.assign_course(course)

            self.course_table.upsert_row(self.courses[course])

        self.person_table.upsert_row(old_instructor)

    def delete_course(self, course_id: str) -> None:
        """
        Delete a course from the system.

        Removes the course from the local dictionary, unenrolls students, and updates the database.

        :param course_id: The ID of the course to delete.
        :type course_id: str
        :return: None
        """
        course = self.courses.get(course_id)
        if not course:
            return
        # remove assigned enrolled students
        for student in course.get_enrolled_students():
            self.students[student].remove_course(course_id)
            self.person_table.upsert_row(self.students[student])

        # remove instructors
        instructor_id = course.get_instructor()
        if instructor_id:
            self.instructors[instructor_id].remove_course(course_id)
            self.person_table.upsert_row(self.instructors[instructor_id])

        # remove from global dictionary
        self.course_table.delete_record(course_id)
        self.courses.pop(course_id)

    def delete_student(self, student_id: str) -> None:
        """
        Delete a student from the system.

        Removes the student from the local dictionary, unassigns them from courses, and updates the database.

        :param student_id: The ID of the student to delete.
        :type student_id: str
        :return: None
        """
        student = self.students.get(student_id)
        if not student:
            pass
        # remove courses
        for course in student.get_courses():
            if course in self.courses:
                self.courses[course].remove_student(student_id)
                self.course_table.upsert_row(self.courses[course])

        self.person_table.delete_record(student_id)
        self.students.pop(student_id)

    def delete_instructor(self, instructor_id: str) -> None:
        """
        Delete an instructor from the system.

        Removes the instructor from the local dictionary, unassigns them from courses, and updates the database.

        :param instructor_id: The ID of the instructor to delete.
        :type instructor_id: str
        :return: None
        """
        instructor = self.instructors.get(instructor_id)
        if not instructor:
            return
        # remove course.instructor id
        for course in instructor.get_courses():
            self.courses[course].instructor_id = None
            self.course_table.upsert_row(self.courses[course])

        self.person_table.delete_record(instructor_id)
        self.instructors.pop(instructor_id)
