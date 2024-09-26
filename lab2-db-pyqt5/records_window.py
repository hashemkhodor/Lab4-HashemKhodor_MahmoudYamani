"""
records_window.py

This module contains the records tab for displaying and managing all records in the system.

Functions:
- create_records_tab
"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QHBoxLayout, QMessageBox, QMenu, QAction, QDialog, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt
from database import (
    get_students, get_instructors, get_courses, get_student_courses,
    update_student, update_instructor, update_course,
    delete_student, delete_instructor, delete_course
)
from main import Student, Instructor, Course

class EditStudentDialog(QDialog):
    """
    Dialog for editing a Student's information.
    """
    def __init__(self, student, courses, parent=None):
        """
        Initializes the EditStudentDialog.

        :param student: The Student object to edit.
        :type student: Student
        :param courses: List of all Course objects.
        :type courses: list
        :param parent: The parent widget.
        :type parent: QWidget, optional
        """
        super().__init__(parent)
        self.setWindowTitle("Edit Student")
        self.student = student
        self.courses = courses
        self.registered_courses = [c.course_id for c in get_student_courses(student.student_id)]
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Name
        name_label = QLabel("Name:")
        self.name_input = QLineEdit(self.student.name)
        name_layout = QHBoxLayout()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Age
        age_label = QLabel("Age:")
        self.age_input = QLineEdit(str(self.student.age))
        age_layout = QHBoxLayout()
        age_layout.addWidget(age_label)
        age_layout.addWidget(self.age_input)
        layout.addLayout(age_layout)

        # Email
        email_label = QLabel("Email:")
        self.email_input = QLineEdit(self.student.email)
        email_layout = QHBoxLayout()
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        layout.addLayout(email_layout)

        # Student ID (Assuming it's not editable)
        student_id_label = QLabel("Student ID:")
        self.student_id_display = QLabel(self.student.student_id)
        student_id_layout = QHBoxLayout()
        student_id_layout.addWidget(student_id_label)
        student_id_layout.addWidget(self.student_id_display)
        layout.addLayout(student_id_layout)

        # Registered Courses
        courses_label = QLabel("Registered Courses:")
        self.courses_list = QListWidget()
        for course_id in self.registered_courses:
            course = next((c for c in self.courses if c.course_id == course_id), None)
            if course:
                item = QListWidgetItem(f"{course.course_id} - {course.course_name}")
                self.courses_list.addItem(item)

        # Add Course
        self.course_combobox = QComboBox()
        course_list = [f"{c.course_id} - {c.course_name}" for c in self.courses]
        self.course_combobox.addItems(course_list)
        self.refresh_courses_button = QPushButton("Refresh Courses")
        self.add_course_button = QPushButton("Add Course")
        add_course_layout = QHBoxLayout()
        add_course_layout.addWidget(self.course_combobox)
        add_course_layout.addWidget(self.refresh_courses_button)
        add_course_layout.addWidget(self.add_course_button)

        # Remove Course
        self.remove_course_button = QPushButton("Remove Selected Course")

        layout.addWidget(courses_label)
        layout.addWidget(self.courses_list)
        layout.addLayout(add_course_layout)
        layout.addWidget(self.remove_course_button)

        # Save and Cancel Buttons
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        # Connections
        self.refresh_courses_button.clicked.connect(self.update_courses_combobox)
        self.add_course_button.clicked.connect(self.add_course)
        self.remove_course_button.clicked.connect(self.remove_selected_course)
        self.save_button.clicked.connect(self.save_changes)
        self.cancel_button.clicked.connect(self.reject)

    def update_courses_combobox(self):
        """
        Updates the courses combobox with the latest courses from the database.
        """
        course_list = [f"{c.course_id} - {c.course_name}" for c in self.courses]
        self.course_combobox.clear()
        self.course_combobox.addItems(course_list)

    def add_course(self):
        """
        Adds a selected course to the student's registered courses.
        """
        selected_course = self.course_combobox.currentText()
        course_id = selected_course.split(" - ")[0]
        if course_id not in self.registered_courses:
            self.registered_courses.append(course_id)
            self.courses_list.addItem(selected_course)
        else:
            QMessageBox.warning(self, "Error", "Course already added.")

    def remove_selected_course(self):
        """
        Removes the selected course from the student's registered courses.
        """
        selected_items = self.courses_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "No course selected.")
            return
        for item in selected_items:
            course_text = item.text()
            course_id = course_text.split(" - ")[0]
            if course_id in self.registered_courses:
                self.registered_courses.remove(course_id)
            self.courses_list.takeItem(self.courses_list.row(item))

    def save_changes(self):
        """
        Saves the changes made to the student's information to the database.
        """
        name = self.name_input.text().strip()
        age_text = self.age_input.text().strip()
        email = self.email_input.text().strip()

        if not name or not age_text or not email:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        try:
            age = int(age_text)
            if age <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "Age must be a positive integer.")
            return

        # Update student data
        try:
            self.student.name = name
            self.student.age = age
            self.student.email = email
            update_student(self.student, self.registered_courses)  # Assuming this function updates the student and their courses
            QMessageBox.information(self, "Success", "Student updated successfully.")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to update student: {str(e)}")

class EditInstructorDialog(QDialog):
    """
    Dialog for editing an Instructor's information.
    """
    def __init__(self, instructor, courses, parent=None):
        """
        Initializes the EditInstructorDialog.

        :param instructor: The Instructor object to edit.
        :type instructor: Instructor
        :param courses: List of all Course objects.
        :type courses: list
        :param parent: The parent widget.
        :type parent: QWidget, optional
        """
        super().__init__(parent)
        self.setWindowTitle("Edit Instructor")
        self.instructor = instructor
        self.courses = courses
        self.assigned_courses = [c.course_id for c in instructor.assigned_courses]
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Name
        name_label = QLabel("Name:")
        self.name_input = QLineEdit(self.instructor.name)
        name_layout = QHBoxLayout()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Age
        age_label = QLabel("Age:")
        self.age_input = QLineEdit(str(self.instructor.age))
        age_layout = QHBoxLayout()
        age_layout.addWidget(age_label)
        age_layout.addWidget(self.age_input)
        layout.addLayout(age_layout)

        # Email
        email_label = QLabel("Email:")
        self.email_input = QLineEdit(self.instructor.email)
        email_layout = QHBoxLayout()
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        layout.addLayout(email_layout)

        # Instructor ID (Assuming it's not editable)
        instructor_id_label = QLabel("Instructor ID:")
        self.instructor_id_display = QLabel(self.instructor.instructor_id)
        instructor_id_layout = QHBoxLayout()
        instructor_id_layout.addWidget(instructor_id_label)
        instructor_id_layout.addWidget(self.instructor_id_display)
        layout.addLayout(instructor_id_layout)

        # Assigned Courses
        courses_label = QLabel("Assigned Courses:")
        self.courses_list = QListWidget()
        for course_id in self.assigned_courses:
            course = next((c for c in self.courses if c.course_id == course_id), None)
            if course:
                item = QListWidgetItem(f"{course.course_id} - {course.course_name}")
                self.courses_list.addItem(item)

        # Add Course
        self.course_combobox = QComboBox()
        course_list = [f"{c.course_id} - {c.course_name}" for c in self.courses]
        self.course_combobox.addItems(course_list)
        self.refresh_courses_button = QPushButton("Refresh Courses")
        self.add_course_button = QPushButton("Add Course")
        add_course_layout = QHBoxLayout()
        add_course_layout.addWidget(self.course_combobox)
        add_course_layout.addWidget(self.refresh_courses_button)
        add_course_layout.addWidget(self.add_course_button)

        # Remove Course
        self.remove_course_button = QPushButton("Remove Selected Course")

        layout.addWidget(courses_label)
        layout.addWidget(self.courses_list)
        layout.addLayout(add_course_layout)
        layout.addWidget(self.remove_course_button)

        # Save and Cancel Buttons
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        # Connections
        self.refresh_courses_button.clicked.connect(self.update_courses_combobox)
        self.add_course_button.clicked.connect(self.add_course)
        self.remove_course_button.clicked.connect(self.remove_selected_course)
        self.save_button.clicked.connect(self.save_changes)
        self.cancel_button.clicked.connect(self.reject)

    def update_courses_combobox(self):
        """
        Updates the courses combobox with the latest courses from the database.
        """
        course_list = [f"{c.course_id} - {c.course_name}" for c in self.courses]
        self.course_combobox.clear()
        self.course_combobox.addItems(course_list)

    def add_course(self):
        """
        Adds a selected course to the instructor's assigned courses.
        """
        selected_course = self.course_combobox.currentText()
        course_id = selected_course.split(" - ")[0]
        if course_id not in self.assigned_courses:
            self.assigned_courses.append(course_id)
            self.courses_list.addItem(selected_course)
        else:
            QMessageBox.warning(self, "Error", "Course already assigned.")

    def remove_selected_course(self):
        """
        Removes the selected course from the instructor's assigned courses.
        """
        selected_items = self.courses_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "No course selected.")
            return
        for item in selected_items:
            course_text = item.text()
            course_id = course_text.split(" - ")[0]
            if course_id in self.assigned_courses:
                self.assigned_courses.remove(course_id)
            self.courses_list.takeItem(self.courses_list.row(item))

    def save_changes(self):
        """
        Saves the changes made to the instructor's information to the database.
        """
        name = self.name_input.text().strip()
        age_text = self.age_input.text().strip()
        email = self.email_input.text().strip()

        if not name or not age_text or not email:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        try:
            age = int(age_text)
            if age <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "Age must be a positive integer.")
            return

        # Update instructor data
        try:
            self.instructor.name = name
            self.instructor.age = age
            self.instructor.email = email
            update_instructor(self.instructor, self.assigned_courses)  # Assuming this function updates the instructor and their courses
            QMessageBox.information(self, "Success", "Instructor updated successfully.")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to update instructor: {str(e)}")

class EditCourseDialog(QDialog):
    """
    Dialog for editing a Course's information.
    """
    def __init__(self, course, instructors, parent=None):
        """
        Initializes the EditCourseDialog.

        :param course: The Course object to edit.
        :type course: Course
        :param instructors: List of all Instructor objects.
        :type instructors: list
        :param parent: The parent widget.
        :type parent: QWidget, optional
        """
        super().__init__(parent)
        self.setWindowTitle("Edit Course")
        self.course = course
        self.instructors = instructors
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Course ID (Assuming it's not editable)
        course_id_label = QLabel("Course ID:")
        self.course_id_display = QLabel(self.course.course_id)
        course_id_layout = QHBoxLayout()
        course_id_layout.addWidget(course_id_label)
        course_id_layout.addWidget(self.course_id_display)
        layout.addLayout(course_id_layout)

        # Course Name
        course_name_label = QLabel("Course Name:")
        self.course_name_input = QLineEdit(self.course.course_name)
        course_name_layout = QHBoxLayout()
        course_name_layout.addWidget(course_name_label)
        course_name_layout.addWidget(self.course_name_input)
        layout.addLayout(course_name_layout)

        # Instructor
        instructor_label = QLabel("Instructor:")
        self.instructor_combobox = QComboBox()
        instructor_list = [f"{i.instructor_id} - {i.name}" for i in self.instructors]
        self.instructor_combobox.addItems(instructor_list)
        self.refresh_instructors_button = QPushButton("Refresh Instructors")
        self.assign_instructor_button = QPushButton("Assign Instructor")
        instructor_layout = QHBoxLayout()
        instructor_layout.addWidget(instructor_label)
        instructor_layout.addWidget(self.instructor_combobox)
        instructor_layout.addWidget(self.refresh_instructors_button)
        layout.addLayout(instructor_layout)

        # Assign Instructor Button
        layout.addWidget(self.assign_instructor_button)

        # Save and Cancel Buttons
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        # Set current instructor
        if self.course.instructor:
            current_instructor = f"{self.course.instructor.instructor_id} - {self.course.instructor.name}"
            index = self.instructor_combobox.findText(current_instructor)
            if index >= 0:
                self.instructor_combobox.setCurrentIndex(index)

        # Connections
        self.refresh_instructors_button.clicked.connect(self.update_instructor_combobox)
        self.assign_instructor_button.clicked.connect(self.assign_instructor)
        self.save_button.clicked.connect(self.save_changes)
        self.cancel_button.clicked.connect(self.reject)

    def update_instructor_combobox(self):
        """
        Updates the instructors combobox with the latest instructors from the database.
        """
        instructor_list = [f"{i.instructor_id} - {i.name}" for i in self.instructors]
        self.instructor_combobox.clear()
        self.instructor_combobox.addItems(instructor_list)

    def assign_instructor(self):
        """
        Assigns the selected instructor to the course.
        """
        selected_instructor = self.instructor_combobox.currentText()
        instructor_id = selected_instructor.split(" - ")[0]
        instructor = next((i for i in self.instructors if i.instructor_id == instructor_id), None)
        if instructor:
            self.course.instructor_id = instructor_id
            QMessageBox.information(self, "Success", "Instructor assigned successfully.")
        else:
            QMessageBox.warning(self, "Error", "Instructor not found.")

    def save_changes(self):
        """
        Saves the changes made to the course's information to the database.
        """
        course_name = self.course_name_input.text().strip()

        if not course_name:
            QMessageBox.warning(self, "Error", "Course name is required.")
            return

        # Update course data
        try:
            self.course.course_name = course_name
            update_course(self.course)  # Assuming this function updates the course in the database
            QMessageBox.information(self, "Success", "Course updated successfully.")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to update course: {str(e)}")

def create_records_tab():
    """
    Creates the records tab widget with functionalities to display, edit, and delete records.

    :return: The records tab widget.
    :rtype: QWidget
    """
    records_tab = QWidget()
    layout = QVBoxLayout()

    # Search Layout
    search_layout = QHBoxLayout()

    role_label = QLabel("Role:")
    role_combobox = QComboBox()
    role_combobox.addItems(["All", "Students", "Instructors", "Courses"])
    search_layout.addWidget(role_label)
    search_layout.addWidget(role_combobox)

    search_term_label = QLabel("Search Term:")
    search_term_input = QLineEdit()
    search_layout.addWidget(search_term_label)
    search_layout.addWidget(search_term_input)

    search_button = QPushButton("Search")
    search_layout.addWidget(search_button)

    refresh_button = QPushButton("Refresh")
    search_layout.addWidget(refresh_button)

    layout.addLayout(search_layout)

    # Tree Widget
    tree = QTreeWidget()
    tree.setColumnCount(4)
    tree.setHeaderLabels(["Type", "ID", "Name", "Additional Info"])
    tree.setContextMenuPolicy(Qt.CustomContextMenu)
    layout.addWidget(tree)

    def populate_treeview(records):
        """
        Populates the tree widget with records.

        :param records: The records to display.
        :type records: list
        """
        tree.clear()
        for record in records:
            if isinstance(record, Student):
                registered_courses = ', '.join(get_student_courses(record.student_id))
                item = QTreeWidgetItem([
                    "Student",
                    record.student_id,
                    record.name,
                    f"Courses: {registered_courses}"
                ])
                tree.addTopLevelItem(item)
            elif isinstance(record, Instructor):
                item = QTreeWidgetItem([
                    "Instructor",
                    record.instructor_id,
                    record.name,
                    ""
                ])
                tree.addTopLevelItem(item)
            elif isinstance(record, Course):
                instructor = get_instructors()
                instructor_name = "None"
                if record.instructor_id:
                    instructor_obj = next((i for i in instructor if i.instructor_id == record.instructor_id), None)
                    if instructor_obj:
                        instructor_name = instructor_obj.name
                item = QTreeWidgetItem([
                    "Course",
                    record.course_id,
                    record.course_name,
                    f"Instructor: {instructor_name}"
                ])
                tree.addTopLevelItem(item)

    def search_records():
        """
        Searches and displays records based on the search term and role.
        """
        role = role_combobox.currentText()
        term = search_term_input.text().lower()

        students = get_students()
        instructors = get_instructors()
        courses = get_courses()

        filtered_records = []
        if role == "All" or role == "Students":
            for student in students:
                if term in student.name.lower() or term in student.student_id.lower():
                    filtered_records.append(student)
        if role == "All" or role == "Instructors":
            for instructor in instructors:
                if term in instructor.name.lower() or term in instructor.instructor_id.lower():
                    filtered_records.append(instructor)
        if role == "All" or role == "Courses":
            for course in courses:
                if term in course.course_name.lower() or term in course.course_id.lower():
                    filtered_records.append(course)

        populate_treeview(filtered_records)

    search_button.clicked.connect(search_records)

    def refresh_treeview():
        """
        Refreshes the tree view to display the latest records.
        """
        students = get_students()
        instructors = get_instructors()
        courses = get_courses()
        all_records = students + instructors + courses
        populate_treeview(all_records)
        search_term_input.clear()
        role_combobox.setCurrentIndex(0)

    refresh_button.clicked.connect(refresh_treeview)

    # Initial population
    refresh_treeview()

    # Edit and Delete Functionality via Context Menu
    def on_tree_context_menu(point):
        """
        Handles the context menu (right-click) event on the tree widget.

        :param point: The position where the context menu is requested.
        :type point: QPoint
        """
        index = tree.indexAt(point)
        if not index.isValid():
            return

        item = tree.itemAt(point)
        menu = QMenu()

        edit_action = QAction('Edit', tree)
        delete_action = QAction('Delete', tree)
        menu.addAction(edit_action)
        menu.addAction(delete_action)

        def edit_record():
            """
            Opens the appropriate edit dialog based on the selected record type.
            """
            record_type = item.text(0)
            record_id = item.text(1)

            if record_type == "Student":
                students = get_students()
                student = next((s for s in students if s.student_id == record_id), None)
                courses = get_courses()
                if student:
                    dialog = EditStudentDialog(student, courses, parent=records_tab)
                    if dialog.exec_():
                        refresh_treeview()
            elif record_type == "Instructor":
                instructors = get_instructors()
                instructor = next((i for i in instructors if i.instructor_id == record_id), None)
                courses = get_courses()
                if instructor:
                    dialog = EditInstructorDialog(instructor, courses, parent=records_tab)
                    if dialog.exec_():
                        refresh_treeview()
            elif record_type == "Course":
                courses = get_courses()
                course = next((c for c in courses if c.course_id == record_id), None)
                instructors = get_instructors()
                if course:
                    dialog = EditCourseDialog(course, instructors, parent=records_tab)
                    if dialog.exec_():
                        refresh_treeview()

        def delete_record():
            """
            Deletes the selected record after confirmation.
            """
            record_type = item.text(0)
            record_id = item.text(1)
            confirm = QMessageBox.question(
                records_tab,
                "Delete Confirmation",
                f"Are you sure you want to delete this {record_type.lower()}?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                try:
                    if record_type == "Student":
                        delete_student(record_id)
                    elif record_type == "Instructor":
                        delete_instructor(record_id)
                    elif record_type == "Course":
                        delete_course(record_id)
                    QMessageBox.information(records_tab, "Success", f"{record_type} deleted successfully.")
                    refresh_treeview()
                except Exception as e:
                    QMessageBox.warning(records_tab, "Error", f"Failed to delete {record_type.lower()}: {str(e)}")

        edit_action.triggered.connect(edit_record)
        delete_action.triggered.connect(delete_record)
        menu.exec_(tree.viewport().mapToGlobal(point))

    tree.customContextMenuRequested.connect(on_tree_context_menu)
    records_tab.setLayout(layout)
    return records_tab
