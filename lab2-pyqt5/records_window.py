from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QHBoxLayout, QMessageBox, QMenu, QAction, QDialog, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt
from main import Student, Instructor, Course

class EditStudentDialog(QDialog):
    def __init__(self, student, courses, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Student")
        self.student = student
        self.courses = courses
        self.registered_courses = student.registered_courses.copy()
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
        for course in self.registered_courses:
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
        course_list = [f"{c.course_id} - {c.course_name}" for c in self.courses]
        self.course_combobox.clear()
        self.course_combobox.addItems(course_list)

    def add_course(self):
        selected_course = self.course_combobox.currentText()
        course = next((c for c in self.courses if f"{c.course_id} - {c.course_name}" == selected_course), None)
        if course and course not in self.registered_courses:
            self.registered_courses.append(course)
            self.courses_list.addItem(selected_course)
        else:
            QMessageBox.warning(self, "Error", "Course already added or not found.")

    def remove_selected_course(self):
        selected_items = self.courses_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "No course selected.")
            return
        for item in selected_items:
            course_id = item.text().split(" - ")[0]
            course = next((c for c in self.registered_courses if c.course_id == course_id), None)
            if course:
                self.registered_courses.remove(course)
            self.courses_list.takeItem(self.courses_list.row(item))

    def save_changes(self):
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
            self.student.registered_courses = self.registered_courses.copy()
            QMessageBox.information(self, "Success", "Student updated successfully.")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))


class EditInstructorDialog(QDialog):
    def __init__(self, instructor, courses, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Instructor")
        self.instructor = instructor
        self.courses = courses
        self.assigned_courses = instructor.assigned_courses.copy()
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
        for course in self.assigned_courses:
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
        course_list = [f"{c.course_id} - {c.course_name}" for c in self.courses]
        self.course_combobox.clear()
        self.course_combobox.addItems(course_list)

    def add_course(self):
        selected_course = self.course_combobox.currentText()
        course = next((c for c in self.courses if f"{c.course_id} - {c.course_name}" == selected_course), None)
        if course and course not in self.assigned_courses:
            self.assigned_courses.append(course)
            self.courses_list.addItem(selected_course)
        else:
            QMessageBox.warning(self, "Error", "Course already added or not found.")

    def remove_selected_course(self):
        selected_items = self.courses_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "No course selected.")
            return
        for item in selected_items:
            course_id = item.text().split(" - ")[0]
            course = next((c for c in self.assigned_courses if c.course_id == course_id), None)
            if course:
                self.assigned_courses.remove(course)
            self.courses_list.takeItem(self.courses_list.row(item))

    def save_changes(self):
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
            self.instructor.assigned_courses = self.assigned_courses.copy()
            QMessageBox.information(self, "Success", "Instructor updated successfully.")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))


class EditCourseDialog(QDialog):
    def __init__(self, course, instructors, parent=None):
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
        instructor_list = [f"{i.instructor_id} - {i.name}" for i in self.instructors]
        self.instructor_combobox.clear()
        self.instructor_combobox.addItems(instructor_list)

    def assign_instructor(self):
        selected_instructor = self.instructor_combobox.currentText()
        instructor = next((i for i in self.instructors if f"{i.instructor_id} - {i.name}" == selected_instructor), None)
        if instructor:
            self.course.instructor = instructor
            QMessageBox.information(self, "Success", "Instructor assigned successfully.")
        else:
            QMessageBox.warning(self, "Error", "Instructor not found.")

    def save_changes(self):
        course_name = self.course_name_input.text().strip()

        if not course_name:
            QMessageBox.warning(self, "Error", "Course name is required.")
            return

        # Update course data
        try:
            self.course.course_name = course_name
            # Instructor is already assigned via assign_instructor
            QMessageBox.information(self, "Success", "Course updated successfully.")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))


def create_records_tab(students, instructors, courses):
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

    # Populate Tree
    def populate_treeview(records):
        tree.clear()
        for record in records:
            if isinstance(record, Student):
                registered_courses = ', '.join([c.course_id for c in record.registered_courses])
                item = QTreeWidgetItem(["Student", record.student_id, record.name, f"Courses: {registered_courses}"])
                tree.addTopLevelItem(item)
            elif isinstance(record, Instructor):
                assigned_courses = ', '.join([c.course_id for c in record.assigned_courses])
                item = QTreeWidgetItem(["Instructor", record.instructor_id, record.name, f"Courses: {assigned_courses}"])
                tree.addTopLevelItem(item)
            elif isinstance(record, Course):
                instructor_name = record.instructor.name if record.instructor else "None"
                item = QTreeWidgetItem(["Course", record.course_id, record.course_name, f"Instructor: {instructor_name}"])
                tree.addTopLevelItem(item)

    # Initial population of the tree with current data
    populate_treeview(students + instructors + courses)

    # Search Function
    def search_records():
        role = role_combobox.currentText()
        term = search_term_input.text().lower()
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

    # Refresh Function
    def refresh_treeview():
        all_records = students + instructors + courses
        populate_treeview(all_records)
        search_term_input.clear()
        role_combobox.setCurrentIndex(0)

    refresh_button.clicked.connect(refresh_treeview)

    # Context Menu
    def on_tree_context_menu(point):
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
            record_type = item.text(0)
            record_id = item.text(1)

            if record_type == "Student":
                record = next((s for s in students if s.student_id == record_id), None)
                if record:
                    dialog = EditStudentDialog(record, courses, parent=records_tab)
                    if dialog.exec_():
                        populate_treeview(students + instructors + courses)
            elif record_type == "Instructor":
                record = next((i for i in instructors if i.instructor_id == record_id), None)
                if record:
                    dialog = EditInstructorDialog(record, courses, parent=records_tab)
                    if dialog.exec_():
                        populate_treeview(students + instructors + courses)
            elif record_type == "Course":
                record = next((c for c in courses if c.course_id == record_id), None)
                if record:
                    dialog = EditCourseDialog(record, instructors, parent=records_tab)
                    if dialog.exec_():
                        populate_treeview(students + instructors + courses)

        def delete_record():
            record_type = item.text(0)
            record_id = item.text(1)
            confirm = QMessageBox.question(records_tab, "Delete", "Are you sure you want to delete this record?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                if record_type == "Student":
                    record = next((s for s in students if s.student_id == record_id), None)
                    if record:
                        # Remove student from enrolled_courses in all courses
                        for course in courses:
                            if record in course.enrolled_students:
                                course.enrolled_students.remove(record)
                        students.remove(record)
                elif record_type == "Instructor":
                    record = next((i for i in instructors if i.instructor_id == record_id), None)
                    if record:
                        # Remove instructor from assigned_courses in all courses
                        for course in courses:
                            if course.instructor == record:
                                course.instructor = None
                        instructors.remove(record)
                elif record_type == "Course":
                    record = next((c for c in courses if c.course_id == record_id), None)
                    if record:
                        # Remove course from students' registered_courses and instructors' assigned_courses
                        for student in students:
                            if record in student.registered_courses:
                                student.registered_courses.remove(record)
                        for instructor in instructors:
                            if record in instructor.assigned_courses:
                                instructor.assigned_courses.remove(record)
                        courses.remove(record)
                refresh_treeview()
                QMessageBox.information(records_tab, "Deleted", "Record deleted successfully.")

        edit_action.triggered.connect(edit_record)
        delete_action.triggered.connect(delete_record)
        menu.exec_(tree.viewport().mapToGlobal(point))

    tree.customContextMenuRequested.connect(on_tree_context_menu)
    records_tab.setLayout(layout)
    return records_tab
