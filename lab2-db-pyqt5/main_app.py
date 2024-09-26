"""
main_app.py

This module contains the main application window for the School Management System using PyQt5.

Classes:
- MainWindow
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QAction, QFileDialog, QMessageBox
from student_window import create_student_form
from instructor_window import create_instructor_form
from course_window import create_course_form
from records_window import create_records_tab
from database import create_tables, backup_database

class MainWindow(QMainWindow):
    """
    The main window of the School Management System application.
    """

    def __init__(self):
        """
        Initializes the main window and sets up the UI components.
        """
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Student Tab
        self.student_tab = create_student_form()
        self.tabs.addTab(self.student_tab, "Students")

        # Instructor Tab
        self.instructor_tab = create_instructor_form()
        self.tabs.addTab(self.instructor_tab, "Instructors")

        # Course Tab
        self.course_tab = create_course_form()
        self.tabs.addTab(self.course_tab, "Courses")

        # Records Tab
        self.records_tab = create_records_tab()
        self.tabs.addTab(self.records_tab, "Records")

        # Menu
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        backup_action = QAction('Backup Database', self)
        backup_action.triggered.connect(self.backup_database)
        file_menu.addAction(backup_action)

    def backup_database(self):
        """
        Initiates the database backup process.
        """
        options = QFileDialog.Options()
        backup_path, _ = QFileDialog.getSaveFileName(self, "Backup Database", "", "Database Files (*.db);;All Files (*)", options=options)
        if backup_path:
            backup_database(backup_path)
            QMessageBox.information(self, "Backup", "Database backed up successfully.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    create_tables()  # initializing the database tables
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
