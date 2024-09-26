import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from typing import Optional

from src.action_handler import ActionHandler
from src.schemas import Student, Instructor, email_validate_pattern
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


class AddPersonForm(ttk.LabelFrame):
    """
    A form for adding a new student or instructor in a Tkinter GUI.

    This form allows the user to input details for either a student or instructor,
    including a unique username, name, age, and email. The form validates the input,
    adds the person to the system, and updates the associated action handler.

    :param title: The title of the form, either "Add Student" or "Add Instructor".
    :type title: str
    :param students: Dictionary of students, keyed by student ID.
    :type students: dict[str, Student]
    :param instructors: Dictionary of instructors, keyed by instructor ID.
    :type instructors: dict[str, Instructor]
    :param action_handler: Instance of the ActionHandler to manage the addition of the person.
    :type action_handler: ActionHandler
    :param callback: A function to call once the person has been added successfully.
    :type callback: function
    :param args: Additional positional arguments for the parent `ttk.LabelFrame`.
    :param kwargs: Additional keyword arguments for the parent `ttk.LabelFrame`.
    """
    def __init__(self, title: str, students: dict[str, Student], instructors: dict[str, Instructor],
                 action_handler:ActionHandler,callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(text=title)
        self.is_student: bool = (title == "Add Student")

        self.students: dict[str, Student] = students
        self.instructors: dict[str, Instructor] = instructors
        self.action_handler: ActionHandler = action_handler

        self.callback = callback
        self.taken_ids: set[str] = set(self.students.keys()).union(set(self.instructors.keys()))

        self._vars: dict = {
            "Username": tk.StringVar(),
            "Name": tk.StringVar(),
            "Age": tk.IntVar(),
            "Email": tk.StringVar()
        }

        # Username
        ttk.Label(self, text="Username").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(self, textvariable=self._vars["Username"]).grid(row=0, column=1, padx=5, pady=5)

        # Name
        ttk.Label(self, text="Name").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(self, textvariable=self._vars["Name"]).grid(row=2, column=1, padx=5, pady=5)

        # Age
        ttk.Label(self, text="Age").grid(row=4, column=0, padx=5, pady=5)
        ttk.Spinbox(self, from_=0, to=101, textvariable=self._vars["Age"]).grid(row=4, column=1, padx=5, pady=5)

        # Email
        ttk.Label(self, text="Email").grid(row=6, column=0, padx=5, pady=5)
        ttk.Entry(self, textvariable=self._vars["Email"]).grid(row=6, column=1, padx=5, pady=5)

        ttk.Button(self, text="Add", command=self.add_action).grid(row=7, columnspan=2, padx=5,
                                                                   pady=5)

    def add_action(self) -> Optional[Student | Instructor]:
        """
        Adds a new student or instructor to the system.

        This method retrieves user input from the form, validates it, and adds the
        person to the appropriate dictionary (students or instructors) and the
        database via the `ActionHandler`.

        :return: The added Student or Instructor object if successful, or None if validation fails.
        :rtype: Optional[Student | Instructor]
        """
        username = self._vars["Username"].get()
        name = self._vars["Name"].get()
        age = self._vars["Age"].get()
        email = self._vars["Email"].get()

        validation_message = self.validate_fields()
        if validation_message:
            messagebox.showerror(title="Registration Failed", message=validation_message)
            return None

        username = username.strip()
        name = name.strip()
        email = email.strip()

        kwargs = {"name": name, "age": age, "_email": email}

        if self.is_student:
            person = Student(student_id=username, **kwargs)
            self.action_handler.add_student(person)
            # self.students[username] = person
        else:
            person = Instructor(instructor_id=username, **kwargs)
            self.action_handler.add_instructor(instructor=person)
            # self.instructors[username] = person

        self.taken_ids.add(username)

        messagebox.showinfo(title="Registration successful",
                            message=f"Successfully registered {person.name} as a {'Student' if self.is_student else 'Instructor'}")

        for var in self._vars:
            self._vars[var].set("")
        self.callback()
        return person

    def validate_fields(self):
        """
        Validates the input fields of the form.

        Ensures that the username, name, age, and email fields are filled out
        correctly, and that the username is unique.

        :return: An empty string if all fields are valid, or an error message string detailing the issues.
        :rtype: str
        """
        username = self._vars["Username"].get()
        name = self._vars["Name"].get()
        age = self._vars["Age"].get()
        email = self._vars["Email"].get()

        # validate
        errors = {}

        if not username or not isinstance(username, str):
            errors["Username"] = "Invalid username"
        elif username in self.taken_ids:
            errors["Username"] = "Username is already taken - choose another one"

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
        return "Registration failed with errors:\n" + "\n".join([f"{error}:\t{errors[error]}" for error in errors])
