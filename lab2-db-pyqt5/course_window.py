"""
course_window.py

This module contains the course form for adding new courses to the system.

Functions:
- create_course_form
"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from main import Course
from database import add_course, get_instructors

def create_course_form():
    """
    Creates the course form widget.

    :return: The course form widget.
    :rtype: QWidget
    """
    course_tab = QWidget()
    layout = QVBoxLayout()

    # course ID Input
    course_id_label = QLabel("Course ID:")
    course_id_input = QLineEdit()
    course_id_layout = QHBoxLayout()
    course_id_layout.addWidget(course_id_label)
    course_id_layout.addWidget(course_id_input)
    layout.addLayout(course_id_layout)

    # course Name Input
    course_name_label = QLabel("Course Name:")
    course_name_input = QLineEdit()
    course_name_layout = QHBoxLayout()
    course_name_layout.addWidget(course_name_label)
    course_name_layout.addWidget(course_name_input)
    layout.addLayout(course_name_layout)

    # ComboBox for instructor
    instructor_label = QLabel("Instructor:")
    instructor_combobox = QComboBox()
    refresh_instructors_button = QPushButton("Refresh Instructors")

    def update_instructor_combobox():
        """
        Updates the instructors available in the combo box.
        """
        instructors = get_instructors()
        instructor_list = [f"{i.instructor_id} - {i.name}" for i in instructors]
        instructor_combobox.clear()
        instructor_combobox.addItems(instructor_list)

    update_instructor_combobox()
    refresh_instructors_button.clicked.connect(update_instructor_combobox)
    instructor_layout = QHBoxLayout()
    instructor_layout.addWidget(instructor_label)
    instructor_layout.addWidget(instructor_combobox)
    instructor_layout.addWidget(refresh_instructors_button)
    layout.addLayout(instructor_layout)

    # add course button
    def add_course_to_db():
        """
        Adds the course to the database.
        """
        course_id = course_id_input.text()
        course_name = course_name_input.text()
        instructor_id_text = instructor_combobox.currentText()

        instructor = next((i for i in get_instructors() if f"{i.instructor_id} - {i.name}" == instructor_id_text), None)
        if not instructor:
            QMessageBox.warning(course_tab, "Error", "Instructor not found!")
            return

        try:
            course = Course(course_id, course_name, instructor)
            add_course(course)
            QMessageBox.information(course_tab, "Success", "Course added successfully!")
            course_id_input.clear()
            course_name_input.clear()
            instructor_combobox.setCurrentIndex(0)
        except Exception as e:
            QMessageBox.warning(course_tab, "Error", str(e))

    add_course_button = QPushButton("Add Course")
    add_course_button.clicked.connect(add_course_to_db)
    layout.addWidget(add_course_button)

    course_tab.setLayout(layout)
    return course_tab
