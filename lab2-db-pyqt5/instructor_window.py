"""
instructor_window.py

This module contains the instructor form for adding new instructors to the system.

Functions:
- create_instructor_form
"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QListWidget,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from main import Instructor
from database import add_instructor, get_courses

def create_instructor_form():
    """
    Creates the instructor form widget.

    :return: The instructor form widget.
    :rtype: QWidget
    """
    instructor_tab = QWidget()
    assigned_courses = []

    layout = QVBoxLayout()

    # name Input
    name_label = QLabel("Name:")
    name_input = QLineEdit()
    name_layout = QHBoxLayout()
    name_layout.addWidget(name_label)
    name_layout.addWidget(name_input)
    layout.addLayout(name_layout)

    # age Input
    age_label = QLabel("Age:")
    age_input = QLineEdit()
    age_layout = QHBoxLayout()
    age_layout.addWidget(age_label)
    age_layout.addWidget(age_input)
    layout.addLayout(age_layout)

    # email Input
    email_label = QLabel("Email:")
    email_input = QLineEdit()
    email_layout = QHBoxLayout()
    email_layout.addWidget(email_label)
    email_layout.addWidget(email_input)
    layout.addLayout(email_layout)

    # instructor ID Input
    instructor_id_label = QLabel("Instructor ID:")
    instructor_id_input = QLineEdit()
    instructor_id_layout = QHBoxLayout()
    instructor_id_layout.addWidget(instructor_id_label)
    instructor_id_layout.addWidget(instructor_id_input)
    layout.addLayout(instructor_id_layout)

    # courses ComboBox
    course_label = QLabel("Assign Courses:")
    course_combobox = QComboBox()
    refresh_courses_button = QPushButton("Refresh Courses")

    def update_courses_combobox():
        """
        Updates the courses available in the combo box.
        """
        courses = get_courses()
        course_list = [f"{c.course_id} - {c.course_name}" for c in courses]
        course_combobox.clear()
        course_combobox.addItems(course_list)

    update_courses_combobox()
    refresh_courses_button.clicked.connect(update_courses_combobox)
    course_layout = QHBoxLayout()
    course_layout.addWidget(course_label)
    course_layout.addWidget(course_combobox)
    course_layout.addWidget(refresh_courses_button)
    layout.addLayout(course_layout)

    # assigned Courses List
    courses_list = QListWidget()
    layout.addWidget(courses_list)

    def add_course_to_instructor():
        """
        Adds a selected course to the instructor's assigned courses.
        """
        selected_course_id = course_combobox.currentText()
        if selected_course_id and selected_course_id not in assigned_courses:
            assigned_courses.append(selected_course_id)
            courses_list.addItem(selected_course_id)
        else:
            QMessageBox.warning(instructor_tab, "Error", "Course already added or not selected.")

    add_course_button = QPushButton("Add Course")
    add_course_button.clicked.connect(add_course_to_instructor)
    layout.addWidget(add_course_button)

    # add Instructor Button
    def add_instructor_to_db():
        """
        Adds the instructor to the database.
        """
        name = name_input.text()
        age = age_input.text()
        email = email_input.text()
        instructor_id = instructor_id_input.text()

        if not name or not age or not email or not instructor_id:
            QMessageBox.warning(instructor_tab, "Error", "All fields are required.")
            return

        try:
            age = int(age)
        except ValueError:
            QMessageBox.warning(instructor_tab, "Error", "Age must be a number.")
            return

        try:
            instructor = Instructor(name, age, email, instructor_id)
            add_instructor(instructor)
            QMessageBox.information(instructor_tab, "Success", "Instructor added successfully!")
            name_input.clear()
            age_input.clear()
            email_input.clear()
            instructor_id_input.clear()
            courses_list.clear()
            assigned_courses.clear()
        except Exception as e:
            QMessageBox.warning(instructor_tab, "Error", str(e))

    add_instructor_button = QPushButton("Add Instructor")
    add_instructor_button.clicked.connect(add_instructor_to_db)
    layout.addWidget(add_instructor_button)

    instructor_tab.setLayout(layout)
    return instructor_tab
