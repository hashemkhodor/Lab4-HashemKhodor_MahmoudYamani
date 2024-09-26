"""
student_window.py

This module contains the student form for adding new students to the system.

Functions:
- create_student_form
"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QListWidget,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from main import Student
from database import add_student, get_courses, add_registration

def create_student_form():
    """
    Creates the student form widget.

    :return: The student form widget.
    :rtype: QWidget
    """
    student_tab = QWidget()
    registered_courses = []

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

    # student ID Input
    student_id_label = QLabel("Student ID:")
    student_id_input = QLineEdit()
    student_id_layout = QHBoxLayout()
    student_id_layout.addWidget(student_id_label)
    student_id_layout.addWidget(student_id_input)
    layout.addLayout(student_id_layout)

    # courses ComboBox
    course_label = QLabel("Register for Courses:")
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

    # registered Courses List
    courses_list = QListWidget()
    layout.addWidget(courses_list)

    def add_course_to_student():
        """
        Adds a selected course to the student's registered courses.
        """
        selected_course_id = course_combobox.currentText()
        if selected_course_id and selected_course_id not in registered_courses:
            registered_courses.append(selected_course_id)
            courses_list.addItem(selected_course_id)
        else:
            QMessageBox.warning(student_tab, "Error", "Course already added or not selected.")

    add_course_button = QPushButton("Add Course")
    add_course_button.clicked.connect(add_course_to_student)
    layout.addWidget(add_course_button)

    # add Student Button
    def add_student_to_db():
        """
        Adds the student to the database.
        """
        name = name_input.text()
        age = age_input.text()
        email = email_input.text()
        student_id = student_id_input.text()

        if not name or not age or not email or not student_id:
            QMessageBox.warning(student_tab, "Error", "All fields are required.")
            return

        try:
            age = int(age)
        except ValueError:
            QMessageBox.warning(student_tab, "Error", "Age must be a number.")
            return

        try:
            student = Student(name, age, email, student_id)
            add_student(student)
            for course_str in registered_courses:
                course_id = course_str.split(" - ")[0]
                add_registration(student_id, course_id)
            QMessageBox.information(student_tab, "Success", "Student added successfully!")
            name_input.clear()
            age_input.clear()
            email_input.clear()
            student_id_input.clear()
            courses_list.clear()
            registered_courses.clear()
        except Exception as e:
            QMessageBox.warning(student_tab, "Error", str(e))

    add_student_button = QPushButton("Add Student")
    add_student_button.clicked.connect(add_student_to_db)
    layout.addWidget(add_student_button)

    student_tab.setLayout(layout)
    return student_tab
