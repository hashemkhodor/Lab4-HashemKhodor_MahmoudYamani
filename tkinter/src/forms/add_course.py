from tkinter import ttk, messagebox
import tkinter as tk
from typing import Optional

from src.schemas import Course, Instructor
from src.action_handler import ActionHandler


class AddCourseForm(ttk.LabelFrame):
    """
    A form for adding a new course in a Tkinter GUI.

    This form allows the user to input details for a new course, including a unique course ID,
    course name, and instructor ID. The form validates the input, adds the course to the system,
    and updates the associated action handler.

    :param title: The title of the form.
    :type title: str
    :param courses: Dictionary of courses, keyed by course ID.
    :type courses: dict[str, Course]
    :param instructors: Dictionary of instructors, keyed by instructor ID.
    :type instructors: dict[str, Instructor]
    :param callback: A function to call once the course has been added successfully. This function refreshes all the widgets
    :type callback: function
    :param action_handler: Instance of the ActionHandler to manage the addition of the course.
    :type action_handler: ActionHandler
    :param args: Additional positional arguments for the parent `ttk.LabelFrame`.
    :param kwargs: Additional keyword arguments for the parent `ttk.LabelFrame`.
    """
    def __init__(self, title: str, courses: dict[str, Course], instructors: dict[str, Instructor], callback,
                 action_handler: ActionHandler, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.config(text=title)

        self.courses: dict[str, Course] = courses
        self.instructors: dict[str, Instructor] = instructors
        self.callback = callback

        self.action_handler: ActionHandler = action_handler

        self._vars: dict = {
            "ID": tk.StringVar(),
            "Name": tk.StringVar(),
            "Instructor": tk.StringVar(),
        }

        # Username
        ttk.Label(self, text="Unique ID").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(self, textvariable=self._vars["ID"]).grid(row=0, column=1, padx=5, pady=5)

        # Name
        ttk.Label(self, text="Name").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(self, textvariable=self._vars["Name"]).grid(row=2, column=1, padx=5, pady=5)

        # Instructor
        ttk.Label(self, text="Instructor ID").grid(row=4, column=0, padx=5, pady=5)
        ttk.Combobox(self, textvariable=self._vars["Instructor"], values=list(self.instructors.keys())).grid(row=4,
                                                                                                             column=1,
                                                                                                             padx=5,
                                                                                                             pady=5)

        ttk.Button(self, text="Add", command=self.add_action).grid(row=7, columnspan=2, padx=5,
                                                                   pady=5)

    def add_action(self) -> Optional[Course]:
        """
        Adds a new course to the system.

        This method retrieves user input from the form, validates it, and adds the course
        to the `courses` dictionary and updates the instructor and the database via the `ActionHandler`.

        :return: The added Course object if successful, or None if validation fails.
        :rtype: Optional[Course]
        """
        ID = self._vars["ID"].get()
        name = self._vars["Name"].get()
        instructor = self._vars["Instructor"].get()

        validation_message = self.validate_fields()
        if validation_message:
            messagebox.showerror(title="Registration Failed", message=validation_message)
            return None

        course = Course(ID, name, instructor)
        self.action_handler.add_course(course)
        # self.courses[ID] = course

        # # Handle database stuff
        self.instructors[instructor].assign_course(ID)
        self.action_handler.edit_instructor(instructor, self.instructors[instructor])


        messagebox.showinfo(title="Adding Course was Successful", message="Added course successfully")
        self.callback()

    def validate_fields(self):
        """
        Validates the input fields of the form.

        Ensures that the course ID, course name, and instructor ID are filled out correctly,
        that the course ID is unique, and that the instructor ID exists.

        :return: An empty string if all fields are valid, or an error message string detailing the issues.
        :rtype: str
        """
        ID = self._vars["ID"].get()
        name = self._vars["Name"].get()
        instructor = self._vars["Instructor"].get()

        # validate
        errors = {}

        if not ID or not isinstance(ID, str):
            errors["Course ID"] = "Invalid course id"
        elif ID in set(self.courses.keys()):
            errors["Course ID"] = "Course ID is already taken - choose another one"

        if not name or not isinstance(name, str):
            errors["Name"] = "Invalid course name - enter your name as string"

        if not instructor or not isinstance(instructor, str):
            errors["Instructor"] = "Invalid instructors id - expected string"
        elif instructor not in set(self.instructors.keys()):
            errors["Instructor"] = f"Invalid instructors id - no instructors has this id {instructor}"

        if not errors:
            return ""
        return "Registration failed with errors:\n" + "\n".join([f"{error}:\t{errors[error]}" for error in errors])
