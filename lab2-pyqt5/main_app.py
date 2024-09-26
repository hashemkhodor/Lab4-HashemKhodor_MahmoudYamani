import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QAction, QMessageBox
from student_window import create_student_form
from instructor_window import create_instructor_form
from course_window import create_course_form
from records_window import create_records_tab
from data_manager import save_data, load_data

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 800, 600)

        self.students = []
        self.instructors = []
        self.courses = []

        # load data
        load_data(self.students, self.instructors, self.courses)

        # create tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Student Tab
        self.student_tab = create_student_form(self.students, self.courses)
        self.tabs.addTab(self.student_tab, "Students")

        # Instructor Tab
        self.instructor_tab = create_instructor_form(self.instructors, self.courses)
        self.tabs.addTab(self.instructor_tab, "Instructors")

        # Course Tab
        self.course_tab = create_course_form(self.courses, self.instructors)
        self.tabs.addTab(self.course_tab, "Courses")

        # Records Tab
        self.records_tab = create_records_tab(self.students, self.instructors, self.courses)
        self.tabs.addTab(self.records_tab, "Records")

        # Menu
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        save_action = QAction('Save Data', self)
        save_action.triggered.connect(lambda: save_data(self.students, self.instructors, self.courses))
        file_menu.addAction(save_action)

        load_action = QAction('Load Data', self)
        load_action.triggered.connect(lambda: load_data(self.students, self.instructors, self.courses))
        file_menu.addAction(load_action)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
