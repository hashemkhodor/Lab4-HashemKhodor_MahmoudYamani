import csv
import json
import os
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Optional

from src.action_handler import ActionHandler
from src.db.db import CourseTable, PersonTable
from src.forms.add_course import AddCourseForm
from src.forms.add_person import AddPersonForm
from src.forms.register_course import RegisterCourseForm
from src.schemas import Instructor, Student, Course
from src.views.table_view import TableView


class Application(tk.Tk):
    def __init__(self, db_path: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.person_table: Optional[PersonTable] = None
        self.courses_table: Optional[CourseTable] = None

        self.title("School Management System")

        self.students: dict[str, Student] = {}
        self.courses: dict[str, Course] = {}
        self.instructors: dict[str, Instructor] = {}

        self.db_path: str = db_path

        self.load()

        self.action_handler: ActionHandler = ActionHandler(courses=self.courses, students=self.students,
                                                           instructors=self.instructors,
                                                           course_table=self.courses_table,
                                                           person_table=self.person_table)

        self.create_widgets()

    def create_widgets(self):
        """Creates and places widgets in the window."""
        menubar = tk.Menu(self)

        # Create the "File" menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Load Data", command=self.load_data)  # Add Export Data option
        file_menu.add_command(label="Export Data", command=self.save_local)  # Add Export Data option
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)  # Option to exit the application

        # Add the File menu to the menubar
        menubar.add_cascade(label="File", menu=file_menu)

        # Set the menubar as the window's menu
        self.config(menu=menubar)

        AddPersonForm(title="Add Student", master=self, students=self.students, instructors=self.instructors,
                      callback=self.recreate, action_handler=self.action_handler).grid(
            row=0, column=0, sticky=tk.EW)
        AddPersonForm(title="Add Instructor", master=self, students=self.students, instructors=self.instructors,
                      callback=self.recreate, action_handler=self.action_handler).grid(
            row=0, column=1, sticky=tk.EW)
        AddCourseForm(title="Add Course", master=self, courses=self.courses, instructors=self.instructors,
                      callback=self.recreate, action_handler=self.action_handler).grid(row=0,
                                                                                       column=2,
                                                                                       sticky=tk.EW)

        RegisterCourseForm(title="Student Course Registration", master=self, courses=self.courses,
                           instructors=self.instructors,
                           students=self.students, callback=self.recreate, action_handler=self.action_handler).grid(
            row=1, column=0, sticky=tk.W)
        RegisterCourseForm(title="Instructor Course Assignment", master=self, courses=self.courses,
                           instructors=self.instructors,
                           students=self.students, callback=self.recreate, action_handler=self.action_handler).grid(
            row=1, column=1, sticky=tk.W)

        TableView(students=self.students, instructors=self.instructors, courses=self.courses, title="Records",
                  callback=self.recreate, action_handler=self.action_handler).grid(
            row=10, columnspan=3)

    #     Add some functionality to save files on desktop either json or csv

    def load_data(self):
        """Prompts the user to load data from SQLite or JSON."""
        file_path = filedialog.askopenfilename(
            title="Select SQLite Database",
            filetypes=[("SQLite Files", "*.db"), ("All Files", "*.*")]
        )
        if file_path:
            # Load data from the chosen SQLite file
            self.db_path = file_path
            self.load()
            self.recreate()

    def load(self) -> bool:
        """Loads the data from the database related to courses, students and instructors."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        if not os.path.isfile(self.db_path):
            CourseTable.create_table(self.db_path)
            PersonTable.create_table(self.db_path)

        self.courses_table: CourseTable = CourseTable(db_path=self.db_path)
        self.person_table: PersonTable = PersonTable(db_path=self.db_path)

        self.courses = self.courses_table.query()
        self.students = self.person_table.query(is_student=True)
        self.instructors = self.person_table.query(is_student=False)
        return True

    def load_from_json(self, file_path: str = "src/db/db.json") -> bool:
        if not os.path.isfile(file_path):
            return False
        with open(file_path, "r") as f:
            data = json.loads(f.read())
            self.courses = data["courses"]

            self.instructors = data["instructors"]
            self.students = data["students"]

            for course in self.courses:
                self.courses[course] = Course.from_dict(self.courses[course])

            for student in self.students:
                self.students[student]["_email"] = self.students[student]["email"]
                self.students[student] = Student.from_dict(self.students[student])

            for instructor in self.instructors:
                self.instructors[instructor]["_email"] = self.instructors[instructor]["email"]
                self.instructors[instructor] = Instructor.from_dict(self.instructors[instructor])

    def save_local(self) -> bool:
        """Allows saving the data to a local file as JSON or CSV."""
        file_types = [("JSON files", "*.json"), ("CSV files", "*.csv"), ("SQL files", "*.sqlite3")]
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=file_types)

        if file_path:
            try:
                if file_path.endswith(".json"):
                    # Save as JSON
                    data = {
                        "students": {key: value.to_dict() for key, value in self.students.items()},
                        "courses": {key: value.to_dict() for key, value in self.courses.items()},
                        "instructors": {key: value.to_dict() for key, value in self.instructors.items()},
                    }
                    with open(file_path, "w") as f:
                        json.dump(data, f, indent=4)
                elif file_path.endswith(".csv"):
                    # Save as CSV (for each entity: students, courses, instructors)
                    self.save_as_csv(file_path)
                elif file_path.endswith(".sqlite3"):
                    shutil.copy(self.db_path, file_path)
                messagebox.showinfo("Success", "Data saved successfully!")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save the file: {e}")
                return False
        return False

    def save_as_csv(self, file_path):
        """Saves the data as CSV files (one for students, courses, and instructors)."""
        try:
            # Save students
            with open(file_path.replace(".csv", "_students.csv"), "w", newline='') as f:
                writer = csv.DictWriter(f, fieldnames=Student.get_fields())
                writer.writeheader()
                for student in self.students.values():
                    writer.writerow(student.to_dict())

            # Save courses
            with open(file_path.replace(".csv", "_courses.csv"), "w", newline='') as f:
                writer = csv.DictWriter(f, fieldnames=Course.get_fields())
                writer.writeheader()
                for course in self.courses.values():
                    writer.writerow(course.to_dict())

            # Save instructors
            with open(file_path.replace(".csv", "_instructors.csv"), "w", newline='') as f:
                writer = csv.DictWriter(f, fieldnames=Instructor.get_fields())
                writer.writeheader()
                for instructor in self.instructors.values():
                    writer.writerow(instructor.to_dict())
        except Exception as e:
            raise e

    def save(self, output: str = "src/db/db.json") -> bool:
        """Saves the data of all the content"""
        default = vars

        os.makedirs(os.path.dirname(output), exist_ok=True)
        with open(output, "w") as f:
            out = {
                "courses": {key: value.to_dict() for key, value in self.courses.items()},
                "students": {key: value.to_dict() for key, value in self.students.items()},
                "instructors": {key: value.to_dict() for key, value in self.instructors.items()}
            }
            f.write(json.dumps(out, indent=4, default=default))

        return True

    def recreate(self):
        """Recreates the application by clearing existing widgets and reinitializing."""
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Recreate widgets
        self.create_widgets()


if __name__ == "__main__":
    app = Application(db_path="src/db/school.db")
    try:
        app.mainloop()
    finally:
        app.save()
        print("SAVED")

# Add student, instructors, course
# Student registers course
# Assign instructors to course
# Display all students, instructors and course
# Search functionality, filter records by Name, ID, or course.
