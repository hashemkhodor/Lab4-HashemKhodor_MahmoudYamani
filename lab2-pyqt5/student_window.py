from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QListWidget,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from main import Student

def create_student_form(students, courses):
    student_tab = QWidget()
    registered_courses = []

    layout = QVBoxLayout()

    # Name
    name_label = QLabel("Name:")
    name_input = QLineEdit()
    name_layout = QHBoxLayout()
    name_layout.addWidget(name_label)
    name_layout.addWidget(name_input)
    layout.addLayout(name_layout)

    # Age
    age_label = QLabel("Age:")
    age_input = QLineEdit()
    age_layout = QHBoxLayout()
    age_layout.addWidget(age_label)
    age_layout.addWidget(age_input)
    layout.addLayout(age_layout)

    # Email
    email_label = QLabel("Email:")
    email_input = QLineEdit()
    email_layout = QHBoxLayout()
    email_layout.addWidget(email_label)
    email_layout.addWidget(email_input)
    layout.addLayout(email_layout)

    # Student ID
    student_id_label = QLabel("Student ID:")
    student_id_input = QLineEdit()
    student_id_layout = QHBoxLayout()
    student_id_layout.addWidget(student_id_label)
    student_id_layout.addWidget(student_id_input)
    layout.addLayout(student_id_layout)

    # Courses
    course_label = QLabel("Register for Courses:")
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

    # Add Course Button
    add_course_button = QPushButton("Add Course")
    courses_list = QListWidget()

    def add_course_to_student():
        selected_course_id = course_combobox.currentText()
        course = next((c for c in courses if f"{c.course_id} - {c.course_name}" == selected_course_id), None)
        if course and course not in registered_courses:
            registered_courses.append(course)
            courses_list.addItem(selected_course_id)
        else:
            QMessageBox.warning(student_tab, "Error", "Course already added or not found.")

    add_course_button.clicked.connect(add_course_to_student)
    layout.addWidget(add_course_button)
    layout.addWidget(courses_list)

    # Add Student Button
    add_student_button = QPushButton("Add Student")

    def add_student():
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
            student = Student(name, age, email, student_id, registered_courses.copy())
            students.append(student)
            QMessageBox.information(student_tab, "Success", "Student added successfully!")

            # Clear fields
            name_input.clear()
            age_input.clear()
            email_input.clear()
            student_id_input.clear()
            courses_list.clear()
            registered_courses.clear()
        except Exception as e:
            QMessageBox.warning(student_tab, "Error", str(e))

    add_student_button.clicked.connect(add_student)
    layout.addWidget(add_student_button)

    student_tab.setLayout(layout)
    return student_tab
