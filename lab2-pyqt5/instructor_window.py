from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QListWidget,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from main import Instructor

def create_instructor_form(instructors, courses):
    instructor_tab = QWidget()
    assigned_courses = []

    layout = QVBoxLayout()

    # name
    name_label = QLabel("Name:")
    name_input = QLineEdit()
    name_layout = QHBoxLayout()
    name_layout.addWidget(name_label)
    name_layout.addWidget(name_input)
    layout.addLayout(name_layout)

    # age
    age_label = QLabel("Age:")
    age_input = QLineEdit()
    age_layout = QHBoxLayout()
    age_layout.addWidget(age_label)
    age_layout.addWidget(age_input)
    layout.addLayout(age_layout)

    # email
    email_label = QLabel("Email:")
    email_input = QLineEdit()
    email_layout = QHBoxLayout()
    email_layout.addWidget(email_label)
    email_layout.addWidget(email_input)
    layout.addLayout(email_layout)

    # instructor ID
    instructor_id_label = QLabel("Instructor ID:")
    instructor_id_input = QLineEdit()
    instructor_id_layout = QHBoxLayout()
    instructor_id_layout.addWidget(instructor_id_label)
    instructor_id_layout.addWidget(instructor_id_input)
    layout.addLayout(instructor_id_layout)

    # courses
    course_label = QLabel("Assign Courses:")
    course_combobox = QComboBox()
    course_list = [f"{c.course_id} - {c.course_name}" for c in courses]
    course_combobox.addItems(course_list)
    refresh_courses_button = QPushButton("Refresh Courses")

    def update_courses_combobox():
        course_list = [f"{c.course_id} - {c.course_name}" for c in courses]
        course_combobox.clear()
        course_combobox.addItems(course_list)

    refresh_courses_button.clicked.connect(update_courses_combobox)

    course_layout = QHBoxLayout()
    course_layout.addWidget(course_label)
    course_layout.addWidget(course_combobox)
    course_layout.addWidget(refresh_courses_button)
    layout.addLayout(course_layout)

    # add Course Button
    add_course_button = QPushButton("Add Course")
    courses_list = QListWidget()

    def add_course_to_instructor():
        selected_course_id = course_combobox.currentText()
        course = next((c for c in courses if f"{c.course_id} - {c.course_name}" == selected_course_id), None)
        if course and course not in assigned_courses:
            assigned_courses.append(course)
            courses_list.addItem(selected_course_id)
        else:
            QMessageBox.warning(instructor_tab, "Error", "Course already added or not found.")

    add_course_button.clicked.connect(add_course_to_instructor)
    layout.addWidget(add_course_button)
    layout.addWidget(courses_list)

    # add Instructor Button
    add_instructor_button = QPushButton("Add Instructor")

    def add_instructor():
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
            instructor = Instructor(name, age, email, instructor_id, assigned_courses.copy())
            instructors.append(instructor)
            QMessageBox.information(instructor_tab, "Success", "Instructor added successfully!")

            # Clear fields
            name_input.clear()
            age_input.clear()
            email_input.clear()
            instructor_id_input.clear()
            courses_list.clear()
            assigned_courses.clear()
        except Exception as e:
            QMessageBox.warning(instructor_tab, "Error", str(e))

    add_instructor_button.clicked.connect(add_instructor)
    layout.addWidget(add_instructor_button)

    instructor_tab.setLayout(layout)
    return instructor_tab
