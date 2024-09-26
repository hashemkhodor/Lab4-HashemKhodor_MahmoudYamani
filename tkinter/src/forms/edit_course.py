import copy
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from typing import Optional

from src.schemas import Student, Instructor, Course
from src.action_handler import ActionHandler
from src.components.multiselectdropdown import MultiSelectDropdown
import re

"""
Student & Instructor form:

> Name: str
> Age: int
> Email: str - email format

Course Form:
> CourseName: str - course name
> Instructor: str - instructors id

"""


class EditCourseForm(tk.Toplevel):
    """
    A Tkinter-based form for editing course details.

    This class creates a window with form fields for editing course information,
    including the course name, assigned instructor, and enrolled students.

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
    :param course_id: The ID of the course to be edited.
    :type course_id: str
    """
    def __init__(self, students: dict[str, Student], instructors: dict[str, Instructor],
                 courses: dict[str, Course], callback, action_handler: ActionHandler,
                 course_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.config(text=title)
        self.geometry("500x350")
        self.grab_set()

        self.students: dict[str, Student] = students
        self.instructors: dict[str, Instructor] = instructors
        self.courses: dict[str, Course] = courses


        self._selected_students: list[str] = []

        self.action_handler: ActionHandler = action_handler

        self.callback = callback

        self._students: list[str] = []
        self._vars: dict = {
            "Course ID": tk.StringVar(value=course_id),
            "Name": tk.StringVar(value=self.courses[course_id].course_name),
            "Instructor ID": tk.StringVar(value=self.courses[course_id].instructor_id)
        }

        ttk.Label(self, text="Course ID").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(self, textvariable=self._vars["Course ID"], state="readonly").grid(row=0, column=1, padx=5, pady=5)

        # Name
        ttk.Label(self, text="Course Name").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(self, textvariable=self._vars["Name"]).grid(row=2, column=1, padx=5, pady=5)

        # Instructor ID
        ttk.Label(self, text="Reassign Instructor ID").grid(row=4, column=0, padx=5, pady=5)
        ttk.Combobox(self, textvariable=self._vars["Instructor ID"], values=list(self.instructors.keys())).grid(
            row=4, column=1, padx=5, pady=5)
        # ttk.Entry(self, textvariable=self._vars["Instructor ID"], state="readonly").grid(row=4, column=1, padx=5,
        #                                                                                  pady=5)

        # Course
        ttk.Label(self, text=f"Remove Enrolled Students").grid(row=7, column=0, padx=5,
                                                               pady=5)
        MultiSelectDropdown(self, list(self.courses[course_id].enrolled_students),
                            selected_options=self._selected_students
                            ).grid(row=7, column=1, padx=5,
                                   pady=5)

        ttk.Button(self, text="Edit", command=self.add_action).grid(row=8, column=0, padx=5,
                                                                    pady=5)
        ttk.Button(self, text="Delete", command=self.delete_action).grid(row=8, column=1, padx=5,
                                                                         pady=5)

    def delete_action(self):
        """
        Deletes the Course from the system.

        This method removes the course's record from the system, updates the students and instructors that
        they were registered or assigned to, and deletes their entry from the action handler.

        :return: None
        """
        course_id = self._vars["Course ID"].get()

        self.action_handler.delete_course(course_id=course_id)
        messagebox.showinfo(title="Course Deletion successful",
                            message=f"Successfully deleted course {course_id}")
        self.callback()
        # self.destroy()

    def add_action(self) -> Optional[Course]:
        """
        Updates the course's record with new details.

        This method validates the input fields, updates the course's information,
        and updates the students and instructors they are registered or assigned to.

        :return: The updated Course object if successful, or None if validation fails.
        :rtype: Optional[Course]
        """
        course_id = self._vars["Course ID"].get()
        new_course_name = self._vars["Name"].get()
        new_course_instructor = self._vars["Instructor ID"].get()

        removed_students: set[str] = set(self._selected_students)

        validation_message = self.validate_fields()
        if validation_message:
            messagebox.showerror(title="Record Edit Failed", message=validation_message)
            return None

        new_course = Course(course_id=course_id, course_name=new_course_name, instructor_id=new_course_instructor)
        new_course.enrolled_students = self.courses[course_id].get_enrolled_students() - removed_students
        self.action_handler.edit_course(course_id=course_id, new_course=new_course)


        messagebox.showinfo(title="Course Edit successful",
                            message=f"Successfully edited {new_course.course_id} record")

        for var in self._vars:
            self._vars[var].set("")

        self.callback()

    def validate_fields(self):
        """
        Validates the input fields of the form.

        Ensures that the course name, and instructor ID are filled out correctly.

        :return: An empty string if all fields are valid, or an error message string detailing the issues.
        :rtype: str
        """
        # validate
        course_id = self._vars["Course ID"].get()
        new_course_name = self._vars["Name"].get()
        new_course_instructor = self._vars["Instructor ID"].get()

        errors = {}

        if new_course_name is None or not isinstance(new_course_name, str):
            errors["Name"] = "Invalid Name - Expected string"

        if new_course_instructor is None or not isinstance(new_course_instructor,
                                                           str) or not new_course_instructor in self.instructors:
            errors["Instructor"] = "Invalid Instructor - Expected to be a valid instructor"

        if not errors:
            return ""
        return "Record edit failed with errors:\n" + "\n".join([f"{error}:\t{errors[error]}" for error in errors])
