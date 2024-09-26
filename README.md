# School Management System

## Description
The **School Management System** is a desktop-based GUI application developed using `Tkinter` and `PyQt5`. This application allows for comprehensive management of students, instructors, and courses, making it easier to handle university data through an intuitive interface. Users can perform CRUD (Create, Read, Update, Delete) operations, register students for courses, assign instructors to courses, and view all records in a structured format. The application also supports saving data to files and exporting it for external use.

## Features

### 1. **Basic Window Setup**
   - The main window is titled **"School Management System"**.
   - A user-friendly interface provides navigation for various forms and actions.

### 2. **Student, Instructor, and Course Forms**
   - Separate forms are provided to manage Students, Instructors, and Courses.
   - Each form contains:
     - Labels and input fields for required information.
     - Buttons to add new entries into the system.
     
### 3. **Student Registration for Courses**
   - Students can be registered for courses using a dropdown list that displays all available courses.
   - Registration records are maintained and can be reviewed.

### 4. **Instructor Assignment to Courses**
   - Instructors can be assigned to courses using a similar dropdown list of available courses.
   - Assignment details can be managed and updated.

### 5. **Display All Records**
   - A tableview is used to show all students, instructors, and course details.
   - The table format allows for quick viewing and sorting of records.

### 6. **Search Functionality**
   - Users can search through records using filters such as:
     - Name
     - ID
   - This makes locating specific entries efficient.

### 7. **Edit and Delete Records**
   - Options to edit or delete existing records are provided through dedicated buttons.
   - Users can update information or remove obsolete records.

### 8. **Save and Load Data**
   - Data can be saved to a file for persistence.
   - Saved data can be reloaded into the application to restore the previous state.

### 9. **Export to CSV**
   - Records can be exported to a CSV file, facilitating easy sharing and analysis outside the application.

## Installation and Setup

### PyQt5


### Tkinter

#### Prerequisites
- Python 3.11 or higher.
- `Tkinter` library.
- Other dependencies specified in `requirements.txt`.

#### Steps
1. **Navigate to the project directory:**
   ```bash
   cd tkinter
   ```

2. **Create and activate a virtual environment:**
   - On Windows:
     ```bash
     py -3.11 -m venv venv
     venv\scripts\activate
     ```
   - On Unix or MacOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

5. **Load Custom Database (Optional):**
   - You can load your custom database from any compatible file format as required by the application.

## Usage
- Start the application and use the provided interface to add, edit, view, and manage Students, Instructors, and Courses.
- Save your changes, and export data as needed.

## License
- This project is licensed under the MIT License.

## Contact
- For any queries or suggestions, feel free to contact:
    - `Hashem Khodor` : hmk57@mail.aub.edu.
    - `Mahmoud Yamani`: mmy29@mail.aub.edu