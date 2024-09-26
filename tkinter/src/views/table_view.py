import tkinter as tk
from tkinter import ttk
from typing import Literal

from src.action_handler import ActionHandler
from src.forms.edit_course import EditCourseForm
from src.forms.edit_person import EditPersonForm
from src.schemas import Student, Instructor, Course


class TableView(ttk.LabelFrame):
    """
    A table view for displaying students, instructors, and courses in a Tkinter application.

    This class allows for filtering and editing of records.

    :param title: The title of the table view.
    :type title: str
    :param students: A dictionary of students, keyed by their IDs.
    :type students: dict[str, Student]
    :param instructors: A dictionary of instructors, keyed by their IDs.
    :type instructors: dict[str, Instructor]
    :param courses: A dictionary of courses, keyed by their IDs.
    :type courses: dict[str, Course]
    :param callback: A callback function to be executed after actions.
    :type callback: callable
    :param action_handler: An instance of ActionHandler to manage actions.
    :type action_handler: ActionHandler
    :param args: Additional positional arguments for the parent class.
    :param kwargs: Additional keyword arguments for the parent class.
    """
    def __init__(self, title: str, students: dict[str, Student], instructors: dict[str, Instructor],
                 courses: dict[str, Course], callback, action_handler: ActionHandler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(text=title)

        # Filter Vars
        self._filter_vars = {
            "ID": tk.StringVar(),
            "Name": tk.StringVar()
        }
        self._filter_labels = {
            "ID Label": tk.StringVar(),
            "Name Label": tk.StringVar()
        }
        self.current_page: Literal["Student", "Instructor", "Course"] = "Student"
        self.action_handler: ActionHandler = action_handler
        self.students: dict[str, Student] = students
        self.instructors: dict[str, Instructor] = instructors
        self.courses: dict[str, Course] = courses
        self.callback = callback

        self.tree_view: ttk.Treeview = ttk.Treeview(master=self)
        self.tree_view.grid(row=1, column=0, columnspan=4)

        ttk.Button(master=self, text="Display Students", command=self.display_student).grid(row=2, column=0)
        ttk.Button(master=self, text="Display Instructors", command=self.display_instructor).grid(row=2, column=1)
        ttk.Button(master=self, text="Display Courses", command=self.display_course).grid(row=2, column=2)

        self.display_person(is_student=True)
        self.display_course()

        # Filters
        self.filter_frame: ttk.LabelFrame = ttk.LabelFrame(master=self, text="Filters")
        self.filter_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")
        row, column = 0, 0
        for key, var in self._filter_vars.items():
            var.trace_add("write", self.on_filter_change)
            ttk.Label(master=self.filter_frame, textvariable=self._filter_labels[f"{key} Label"]
                      ).grid(row=row, column=column, padx=5, pady=5)
            ttk.Entry(master=self.filter_frame, textvariable=var).grid(row=row, column=column + 1, padx=5, pady=5)
            column += 2

            # Bind a click event to the "Action" column
        self.tree_view.bind("<Button-1>", self.on_treeview_click)

    def on_treeview_click(self, event):
        """
        Detects when a user clicks the 'Action' column and performs an action which is to create popoff window for updating content.

        :param event: The event object containing information about the click event.
        :type event: tk.Event
        """
        # Get the region where the click occurred
        region = self.tree_view.identify_region(event.x, event.y)
        column = self.tree_view.identify_column(event.x)
        row_id = self.tree_view.identify_row(event.y)

        if region == "cell":
            # MyDialog(parent=self)
            item = self.tree_view.item(row_id)
            if self.current_page in ("Student", "Instructor"):
                person_id = item['values'][0]
                print(person_id)
                EditPersonForm(master=self.master, is_student=self.current_page == "Student", students=self.students,
                               instructors=self.instructors,
                               courses=self.courses, person_id=person_id, callback=self.callback,
                               action_handler=self.action_handler)
            elif self.current_page == "Course":
                course_id = item['values'][0]
                EditCourseForm(master=self.master, course_id=course_id, instructors=self.instructors,
                               students=self.students, courses=self.courses, callback=self.callback,
                               action_handler=self.action_handler)
            # print(f"Button clicked in row with ID: {item['values'][0]} - Name: {item['values'][1]}")
            # You can trigger any action here, e.g., opening a new window, updating data, etc.

    def on_filter_change(self, var_name, index, mode):
        """
        Called whenever a filter value changes, refreshing the displayed records.

        :param var_name: The name of the variable that changed.
        :type var_name: str
        :param index: The index of the variable that changed.
        :type index: int
        :param mode: The mode of the change.
        :type mode: str
        """
        # for key, val in self._filter_vars.items():
        #     print(f"Filter {key}: {val.get()}")
        if self.current_page == "Student":
            self.display_student(keep_filters=True)
        elif self.current_page == "Instructor":
            self.display_instructor(keep_filters=True)
        elif self.current_page == "Course":
            self.display_course(keep_filters=True)

    def display_student(self, keep_filters: bool = False):
        """
        Displays the student records in the tree view.

        :param keep_filters: Flag indicating whether to keep the current filters.
        :type keep_filters: bool
        """
        if not keep_filters:
            self.clear_filters()
        self._filter_labels["ID Label"].set("Student ID Filter")
        self._filter_labels["Name Label"].set("Student Name Filter")

        self.current_page = "Student"
        self.display_person(is_student=True)

    def display_instructor(self, keep_filters: bool = False):
        """
        Displays the instructor records in the tree view.

        :param keep_filters: Flag indicating whether to keep the current filters.
        :type keep_filters: bool
        """
        if not keep_filters:
            self.clear_filters()

        self._filter_labels["ID Label"].set("Instructor ID Filter")
        self._filter_labels["Name Label"].set("Instructor Name Filter")

        self.current_page = "Instructor"
        self.display_person(is_student=False)

    def clear_filters(self):
        for var in self._filter_vars.values():
            var.set("")

    def display_person(self, is_student: bool = True) -> None:
        """
        Displays either student or instructor records based on the is_student flag.

        :param is_student: Flag indicating whether to display students (True) or instructors (False).
        :type is_student: bool
        """

        ID_FILTER = self._filter_vars["ID"].get()
        NAME_FILTER = self._filter_vars["Name"].get()

        for child in self.tree_view.get_children():
            self.tree_view.delete(child)
        headers = (f"{'Student' if is_student else 'Instructor'} ID", "Name", "Age", "Email",
                   f"{'Registered' if is_student else 'Assigned'} Courses")
        self.tree_view['columns'] = headers
        for header in headers:
            self.tree_view.heading(header, text=header)

        for person in (self.students if is_student else self.instructors).values():
            content = person.to_treeview_record()
            if ID_FILTER and not ID_FILTER.lower() in content[0].lower():
                continue
            if NAME_FILTER and not NAME_FILTER.lower() in content[1].lower():
                continue

            row = content[:-1] + ("" if len(content[-1]) < 1 else content[-1][0],)
            child_rows = []
            if content[-1]:
                child_rows = [tuple("" for _ in range(4)) + (course,) for course in content[-1][1:]]
            parent = self.tree_view.insert("", "end", values=row)
            for child in child_rows:
                parent = self.tree_view.insert(parent, "end", values=child)

    def display_course(self, keep_filters: bool = False) -> None:
        """
        Displays the course records in the tree view.

        :param keep_filters: Flag indicating whether to keep the current filters.
        :type keep_filters: bool
        """
        self.current_page = "Course"
        if not keep_filters:
            self.clear_filters()
        self._filter_labels["ID Label"].set("Course ID Filter")
        self._filter_labels["Name Label"].set("Course Name Filter")

        ID_FILTER = self._filter_vars["ID"].get()
        NAME_FILTER = self._filter_vars["Name"].get()

        for child in self.tree_view.get_children():
            self.tree_view.delete(child)
        headers = ("Course ID", "Course Name", "Instructor ID", "Enrolled Students")
        self.tree_view['columns'] = headers
        for header in headers:
            self.tree_view.heading(header, text=header)

        for course in self.courses.values():
            content = course.to_treeview_record()
            if ID_FILTER and not ID_FILTER.lower() in content[0].lower():
                continue
            if NAME_FILTER and not NAME_FILTER.lower() in content[1].lower():
                continue

            row = content[:-1] + ("" if len(content[-1]) < 1 else content[-1][0],)
            child_rows = []
            if content[-1]:
                child_rows = [tuple("" for _ in range(len(content) - 1)) + (course,) for course in content[-1][1:]]
            parent = self.tree_view.insert("", "end", values=row)
            for child in child_rows:
                parent = self.tree_view.insert(parent, "end", values=child)
