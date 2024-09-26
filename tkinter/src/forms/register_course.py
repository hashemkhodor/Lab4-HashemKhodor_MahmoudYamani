import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from typing import Optional

from src.action_handler import ActionHandler
from src.schemas import Student, Instructor, Course

"""
Course registration for student:
1. Student ID. Dropdown
2. Course ID. Dropdown

Course assignment for instructors
1. Instructor ID. Dropdown.
2. Course ID. Dropdown.
"""


class RegisterCourseForm(ttk.LabelFrame):
    """
    A Tkinter-based form for course registration or assignment.

    This class creates a form for either registering students for courses
    or assigning courses to instructors, depending on the title provided.

    :param title: The title of the form, determines if it's for students or instructors.
    :type title: str
    :param students: A dictionary of student objects keyed by student ID.
    :type students: dict[str, Student]
    :param instructors: A dictionary of instructor objects keyed by instructor ID.
    :type instructors: dict[str, Instructor]
    :param courses: A dictionary of course objects keyed by course ID.
    :type courses: dict[str, Course]
    :param callback: A function to be called after successful form submission.
    :type callback: callable
    :param action_handler: An instance of ActionHandler for performing actions.
    :type action_handler: ActionHandler
    """
    def __init__(self, title: str, students: dict[str, Student], instructors: dict[str, Instructor],
                 courses: dict[str, Course], callback, action_handler: ActionHandler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(text=title)
        self.is_student: bool = (title == "Student Course Registration")

        self.students: dict[str, Student] = students
        self.instructors: dict[str, Instructor] = instructors
        self.courses: dict[str, Course] = courses

        self.action_handler: ActionHandler = action_handler

        self.callback = callback

        self._vars: dict = {
            "Person": tk.StringVar(),
            "Course": tk.StringVar()
        }

        # Student or Instructor
        ttk.Label(self, text="Student" if self.is_student else "Instructor").grid(row=0, column=0, padx=5, pady=5)
        ttk.Combobox(self, textvariable=self._vars["Person"],
                     values=list(self.students.keys() if self.is_student else self.instructors.keys())).grid(row=0,
                                                                                                             column=1,
                                                                                                             padx=5,
                                                                                                             pady=5)

        # Course
        ttk.Label(self, text="Course").grid(row=1, column=0, padx=5, pady=5)
        ttk.Combobox(self, textvariable=self._vars["Course"], values=list(self.courses.keys())).grid(row=1, column=1,
                                                                                                     padx=5, pady=5)

        ttk.Button(self, text="Register" if self.is_student else "Assign", command=self.add_action).grid(row=2,
                                                                                                         columnspan=2,
                                                                                                         padx=5,
                                                                                                         pady=5)

    def add_action(self) -> Optional[Student | Instructor]:
        """
        Perform the registration or assignment action.

        This method validates the input, registers a student for a course or assigns
        a course to an instructor, and updates the relevant records.

        :return: The ID of the student or instructor if successful, None otherwise.
        :rtype: Optional[str]
        """
        person = self._vars["Person"].get()
        course = self._vars["Course"].get()
        validation_message = self.validate_fields()
        if validation_message:
            messagebox.showerror(title=f"Course {'Registration' if self.is_student else 'Assignment'} Failed",
                                 message=validation_message)
            return None

        if self.is_student:
            if course in self.students[person].registered_courses:
                messagebox.showerror(title=f"Course Already Registered",
                                     message=f"Student {person} already is registered")
                return
            self.courses[course].add_student(person)
            self.students[person].register_course(course)

            self.action_handler.edit_course(course, self.courses[course])
            self.action_handler.edit_student(person, self.students[person])
        else:
            if course in self.instructors[person].assigned_courses:
                messagebox.showerror(title=f"Course Already Assigned",
                                     message=f"Instructor {person} already is assigned to {course}")
                return

            if self.courses[course].instructor_id:
                self.instructors[self.courses[course].instructor_id].assigned_courses.discard(course)

            self.courses[course].instructor_id = person
            self.instructors[person].assign_course(course)

            self.action_handler.edit_course(course, course)
            self.action_handler.edit_instructor(person, self.instructors[person])

        messagebox.showinfo(title=f"Course {'Registration' if self.is_student else 'Assignment'} was successful!",
                            message=f"Course {'Registration' if self.is_student else 'Assignment'} of {course} was successful to {person}!")
        for var in self._vars:
            self._vars[var].set("")

        self.callback()

        return person

    def validate_fields(self):
        """
        Validate the input fields of the form.

        This method checks if the selected person (student or instructor) and course are valid.

        :return: An error message if validation fails, an empty string otherwise.
        :rtype: str
        """
        person = self._vars["Person"].get()
        course = self._vars["Course"].get()
        # validate

        errors = {}
        if not person or not isinstance(person, str):
            errors["Person"] = f"Invalid {'Student' if self.is_student else 'Instructor'} ID"
        elif (self.is_student and person not in self.students) or (
                not self.is_student and person not in self.instructors):
            errors["Person"] = f"Invalid {'Student' if self.is_student else 'Instructor'} ID isn't valid"

        if not course or not isinstance(course, str):
            errors["Course"] = f"Invalid Course ID"
        elif course not in self.courses:
            errors["Course"] = f"Invalid Course ID isn't valid"

        elif not self.is_student and self.courses[course].instructor_id not in self.instructors:
            self.courses[course].instructor_id = None

        if not errors:
            return ""
        return f"Course {'Registration' if self.is_student else 'Assignment'} failed with errors:\n" + "\n".join(
            [f"{error}:\t{errors[error]}" for error in errors])
