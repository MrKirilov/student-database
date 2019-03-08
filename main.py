from student import Student
from base import Session, engine, Base
from course import Course
from sqlalchemy import exc
import sys
import re
import signal

Base.metadata.create_all(engine)

session = Session()

course_list = [
    'Computer Systems',
    'Networking Concepts',
    'Programming Concepts',
    'Website Design',
    'Personal Skills Development',
    'Object Oriented Design',
    'Database Analysis and Design',
    'Object Oriented Programming'
]


def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Exiting program...".format(signal))
    exit(0)


signal.signal(signal.SIGINT, keyboardInterruptHandler)


def nameValidator():
    while True:
        name = str(input("Enter Student Name: "))

        checker = all([x.isalpha() or x == ' ' for x in name])

        if checker == False:
            print("Invalid Input")
            continue
        else:
            break
    return name


def menuOptionValidator():
    while True:
        try:
            x = int(input("Enter option number [0-5]: "))
            if x in range(6):
                return x
        except ValueError:
            print("Invalid option.  Try again...")


def printSummary(student_name):
    student = session.query(Student).filter(
        Student.name == student_name).first()

    grades = session.query(Course).filter(
        Course.student_id == student.id).all()

    print("\nID | Name")
    print("-" * 40)
    print("{}  | {}".format(student.id, student.name))
    print("-" * 40)

    for course in grades:
        print("{}: {}".format(course.title, course.grade))

    print("-" * 40)


def listStudents():
    students = session.query(Student).all()
    print("ID | Name")
    print("-" * 40)
    for student in students:
        print("{}  | {}".format(student.id, student.name))

    print("-" * 40)


def viewStudent():
    try:
        student = nameValidator()
        printSummary(student)
    except AttributeError:
        print("Entry not found")


def addStudent():
    student_name = nameValidator()
    new_student = Student(name=student_name)
    session.add(new_student)
    session.commit()

    for course in course_list:
        new_course = Course(title=course, grade='NOT GRADED',
                            student_id=new_student.id)
        session.add(new_course)
        session.commit()

    print("{} has been successfully enrolled!".format(new_student.name))


def editStudent():
    student_name = nameValidator()
    student = session.query(Student).filter(
        Student.name == student_name).first()
    courses = session.query(Course).filter(
        Course.student_id == student.id).all()

    print("Enter the scores for the following subjects [0-100]:")

    for course in courses:
        switch = True
        while switch:
            try:
                score = eval(input("{}: ".format(course.title)))
                if score >= 0 and score <= 100:
                    course.grade = gradeChecker(score)

                    session.add(course)
                    session.commit()

                    print(course.grade)
                    switch = False
            except (ValueError, NameError):
                print("Enter a score [0-100]: ")

    printSummary(student_name)


def removeStudent():
    try:
        student_id = eval(input("Enter Student ID Number: "))
        student = session.query(Student).filter(
            Student.id == student_id).first()
        courses = session.query(Course).filter(
            Course.student_id == student.id).all()

        session.delete(student)
        session.commit()

        for course in courses:
            session.delete(course)
            session.commit()
    except:
        print("Invalid Student ID")


def mainMenu():
    print('''Welcome to the Student Database!
Select an option from the following menu.
    [1] List Students
    [2] Add Student
    [3] Edit Student
    [4] View Student
    [5] Remove Student
    [0] Quit
             ''')

    selection = menuOptionValidator()
    print("\n")

    if selection == 1:
        # List Students
        listStudents()

    elif selection == 2:
        # Add Student
        addStudent()

    elif selection == 3:
        # Edit Student
        editStudent()

    elif selection == 4:
        # Show Student
        viewStudent()
    elif selection == 5:
        # Remove Student
        removeStudent()
    elif selection == 0:
        print("Goodbye!")
        sys.exit()
    else:
        print("Invalid Input!")


def gradeChecker(score):
    if score >= 75:
        return 'DISTINCTION'
    elif score >= 65 and score < 75:
        return 'MERIT'
    elif score >= 50 and score < 65:
        return 'PASS'
    elif score >= 35 and score < 50:
        return 'REFERRED'
    elif score >= 10 and score < 35:
        return 'WITHHELD'
    elif score >= 5 and score < 10:
        return 'UNREASONABLE SUBMISSION'


while True:
    mainMenu()

    prompt = str(input("Do you want to continue? [Y/N]:")).lower()

    if prompt == "y" or prompt == 'yes':
        continue
    else:
        break


session.close()
