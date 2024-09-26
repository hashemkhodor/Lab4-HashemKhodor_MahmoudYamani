import copy
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from typing import Optional

from src.action_handler import ActionHandler
from src.schemas import Student, Instructor, email_validate_pattern, Course
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


class EditPersonForm(tk.Toplevel):
    """
    A form for editing an existing student or instructor's details in a Tkinter GUI.

    This form allows users to modify details for an existing student or instructor,
    including their name, age, email, and the courses they are registered or assigned to.
    Users can also delete the student's or instructor's record.

    :param is_student: Whether the person being edited is a student (True) or an instructor (False).
    :type is_student: bool
    :param students: Dictionary of students, keyed by student ID.
    :type students: dict[str, Student]
    :param instructors: Dictionary of instructors, keyed by instructor ID.
    :type instructors: dict[str, Instructor]
    :param courses: Dictionary of courses, keyed by course ID.
    :type courses: dict[str, Course]
    :param callback: A function to call after the edit or delete action is completed.
    :type callback: function
    :param action_handler: Instance of the ActionHandler to manage the edit and delete actions.
    :type action_handler: ActionHandler
    :param person_id: The ID of the student or instructor being edited.
    :type person_id: str
    :param args: Additional positional arguments for the parent `tk.Toplevel`.
    :param kwargs: Additional keyword arguments for the parent `tk.Toplevel`.
    """
    def __init__(self, is_student: bool, students: dict[str, Student], instructors: dict[str, Instructor],
                 courses: dict[str, Course],callback, action_handler:ActionHandler,
                 person_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.config(text=title)
        self.geometry("500x350")
        self.grab_set()

        self.is_student: bool = is_student

        self.students: dict[str, Student] = students
        self.instructors: dict[str, Instructor] = instructors
        self.courses: dict[str, Course] = courses

        self.action_handler: ActionHandler = action_handler
        self.callback = callback

        SET = self.students if is_student else self.instructors
        person_id = str(person_id)
        print(SET)

        self._selected_courses: list[str] = []
        self._vars: dict = {
            "Username": tk.StringVar(value=person_id),
            "Name": tk.StringVar(value=SET[person_id].name),
            "Age": tk.IntVar(value=SET[person_id].age),
            "Email": tk.StringVar(value=SET[person_id]._email)
        }

        ttk.Label(self, text="Username").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(self, textvariable=self._vars["Username"], state="readonly").grid(row=0, column=1, padx=5, pady=5)

        # Name
        ttk.Label(self, text="Name").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(self, textvariable=self._vars["Name"]).grid(row=2, column=1, padx=5, pady=5)

        # Age
        ttk.Label(self, text="Age").grid(row=4, column=0, padx=5, pady=5)
        ttk.Spinbox(self, from_=0, to=101, textvariable=self._vars["Age"]).grid(row=4, column=1, padx=5, pady=5)

        # Email
        ttk.Label(self, text="Email").grid(row=6, column=0, padx=5, pady=5)
        ttk.Entry(self, textvariable=self._vars["Email"], state="readonly").grid(row=6, column=1, padx=5, pady=5)

        # Course
        ttk.Label(self, text=f"{'Register' if self.is_student else 'Assigned'} Courses").grid(row=7, column=0, padx=5,
                                                                                              pady=5)
        MultiSelectDropdown(self, list(self.students[person_id].registered_courses if self.is_student
                                       else self.instructors[person_id].assigned_courses),
                            selected_options=self._selected_courses
                            ).grid(row=7, column=1, padx=5,
                                   pady=5)

        ttk.Button(self, text="Edit", command=self.add_action).grid(row=8, column=0, padx=5,
                                                                    pady=5)
        ttk.Button(self, text="Delete", command=self.delete_action).grid(row=8, column=1, padx=5,
                                                                      pady=5)

    def delete_action(self):
        """
        Deletes the student or instructor from the system.

        This method removes the student's or instructor's record from the system, updates the courses
        they are registered or assigned to, and deletes their entry from the action handler.

        :return: None
        """

        username = self._vars["Username"].get()
        if self.is_student:
            for course in self.students[username].registered_courses:
                if course in self.courses:
                    self.courses[course].enrolled_students.discard(username)
                    self.action_handler.edit_course(course, self.courses[course])
            self.action_handler.delete_student(username)
        #     self.action
        else:
            for course in self.instructors[username].assigned_courses:
                if course in self.courses:
                    self.courses[course].instructor_id = None
                    self.action_handler.edit_course(course, self.courses[course])
            self.action_handler.delete_instructor(username)

        messagebox.showinfo(title="Record Deletion successful",
                            message=f"Successfully deleted {username} a {'Student' if self.is_student else 'Instructor'} record")
        self.callback()
        # self.destroy()

    def add_action(self) -> Optional[Student | Instructor]:
        """
        Updates the student's or instructor's record with new details.

        This method validates the input fields, updates the student's or instructor's information,
        and updates the courses they are registered to or assigned to.

        :return: The updated Student or Instructor object if successful, or None if validation fails.
        :rtype: Optional[Student | Instructor]
        """
        username = self._vars["Username"].get()
        name = self._vars["Name"].get()
        age = self._vars["Age"].get()
        email = self._vars["Email"].get()

        validation_message = self.validate_fields()
        if validation_message:
            messagebox.showerror(title="Record Edit Failed", message=validation_message)
            return None

        username = username.strip()
        name = name.strip()
        email = email.strip()

        kwargs = {"name": name, "age": age, "_email": email}

        print(self._selected_courses)


        if self.is_student:
            courses = set(self.students[username].registered_courses).difference(set(self._selected_courses))
            person = Student(student_id=username, **kwargs)
            person.registered_courses = copy.deepcopy(courses)
            self.action_handler.edit_student(old_student_id=username, new_student=person)

        else:
            courses = set(self.instructors[username].assigned_courses).difference(set(self._selected_courses))
            person = Instructor(instructor_id=username, **kwargs)
            person.assigned_courses = copy.deepcopy(courses)
            self.action_handler.edit_instructor(username, new_instructor=person)

        messagebox.showinfo(title="Record Edit successful",
                            message=f"Successfully edit {person.name} a {'Student' if self.is_student else 'Instructor'} record")

        for var in self._vars:
            self._vars[var].set("")

        self.callback()
        # self.destroy()

    def validate_fields(self):
        """
        Validates the input fields for the student's or instructor's details.

        Ensures that the name, age, and email fields are filled out correctly. Also checks if the email
        format is valid.

        :return: An empty string if all fields are valid, or an error message string detailing the issues.
        :rtype: str
        """
        name = self._vars["Name"].get()
        age = self._vars["Age"].get()
        email = self._vars["Email"].get()

        # validate
        errors = {}

        if not name or not isinstance(name, str):
            errors["Name"] = "Invalid name - enter your name as string"

        if not age or not isinstance(age, int):
            errors["Age"] = "Invalid age type, expected integer"
        elif age < 0 or age > 101:
            errors["Age"] = "Invalid age range, expected between 0 and 101"

        if not email or not isinstance(email, str):
            errors["Email"] = "Invalid email type, expected str"
        elif not re.match(email_validate_pattern, email):
            errors["Email"] = "Invalid email format. Please enter valid email."

        if not errors:
            return ""
        return "Record edit failed with errors:\n" + "\n".join([f"{error}:\t{errors[error]}" for error in errors])
