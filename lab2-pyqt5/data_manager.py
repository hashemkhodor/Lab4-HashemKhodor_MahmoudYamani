import json
from main import Student, Instructor, Course

DATA_PATH = "data.json"

def save_data(students, instructors, courses):
    data = {
        'students': [student.to_dict() for student in students],
        'instructors': [instructor.to_dict() for instructor in instructors],
        'courses': [course.to_dict() for course in courses],
    }
    try:
        with open(DATA_PATH, 'w') as f:
            json.dump(data, f, indent=4)
        print("Data saved successfully.")
    except Exception as e:
        print(f"Error saving data: {e}")

def load_data(students, instructors, courses):
    try:
        with open(DATA_PATH, 'r') as f:
            data = json.load(f)
        # clear existing data
        students.clear()
        instructors.clear()
        courses.clear()

        for instructor_data in data.get('instructors', []):
            instructor = Instructor.from_dict(instructor_data, courses)
            instructors.append(instructor)

        for student_data in data.get('students', []):
            student = Student.from_dict(student_data, courses)
            students.append(student)

        for course_data in data.get('courses', []):
            course = Course.from_dict(course_data, instructors, students)
            courses.append(course)

        print("Data loaded successfully.")
    except FileNotFoundError:
        print("Data file not found. Starting with empty data.")
    except Exception as e:
        print(f"Error loading data: {e}")
