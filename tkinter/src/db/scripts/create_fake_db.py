import json
import random
from faker import Faker
from src.schemas import Student, Instructor, Course

fake = Faker()

# Sets to store unique ids
generated_student_ids = set()
generated_instructor_ids = set()
generated_course_ids = set()


# Helper function to ensure unique IDs
def generate_unique_id(existing_ids: set, name: str) -> str:
    unique_id = "-".join(name.lower().split())
    while unique_id in existing_ids:
        unique_id = f"{unique_id}-{random.randint(1, 1000)}"
    existing_ids.add(unique_id)
    return unique_id


# Helper functions to generate random data for students, instructors, and courses
def generate_random_student() -> Student:
    name = fake.name()
    student_id = generate_unique_id(generated_student_ids, name)
    return Student(
        student_id=student_id,
        name=name,
        age=random.randint(10, 100),
        _email=fake.email()
    )


def generate_random_instructor() -> Instructor:
    name = fake.name()
    instructor_id = generate_unique_id(generated_instructor_ids, name)
    return Instructor(
        instructor_id=instructor_id,
        name=name,
        age=random.randint(10, 100),
        _email=fake.email()
    )


def generate_random_course(instructors: list[Instructor], students: list[Student]) -> Course:
    instructor = random.choice(instructors)
    course_name = fake.bs().title()
    course_id = generate_unique_id(generated_course_ids, course_name)

    random.shuffle(students)
    enrolled_students: list[Student] = students[:random.randint(1, 5)]

    course = Course(
        course_id=course_id,
        course_name=course_name,
        instructor_id=instructor.instructor_id,
    )
    instructor.assign_course(course_id)

    for enrolled_student in enrolled_students:
        course.add_student(enrolled_student.student_id)
        enrolled_student.register_course(course_id)

    return course


if __name__ == "__main__":
    students = [generate_random_student() for _ in range(20)]
    instructors = [generate_random_instructor() for _ in range(20)]
    courses = [generate_random_course(instructors, students) for _ in range(20)]

    students_json = {student.student_id: student.to_dict() for student in students}
    instructors_json = {instructor.instructor_id: instructor.to_dict() for instructor in instructors}
    courses = {course.course_id: course.to_dict() for course in courses}

    with open("../students.json", "w") as f:
        f.write(json.dumps(students_json, indent=4, default=vars))
    with open("../instructors.json", "w") as f:
        f.write(json.dumps(instructors_json,indent=4,default=vars))
    with open("../courses.json", "w") as f:
        f.write(json.dumps(courses,indent=4,default=vars))

