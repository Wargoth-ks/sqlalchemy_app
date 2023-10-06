from sqlalchemy import func, select, text, desc
from tabulate import tabulate
from models import Teachers, Students, Subjects, Grades, Groups
from settings.db import session


def select_1():
    # Знаходимо 5 студентів з найвищим середнім балом
    stmt = (
        select(Students.name, func.round(func.avg(Grades.grade), 2).label("avg_grade"))
        .select_from(Grades)
        .join(Students)
        .group_by(Students.id)
        .order_by(text("avg_grade DESC"))
        .limit(5)
    )

    result = session.execute(stmt).all()

    headers = ["Student name", "AVG Grade"]
    return tabulate(result, headers, tablefmt="pretty")


def select_2():
    # Отримуємо випадковий предмет
    random_subject = session.execute(
        select(Subjects.name).order_by(func.random()).limit(1)
    ).scalar_one()

    # Знаходимо студента з найвищим середнім балом з цього предмета
    stmt = (
        select(
            text("'{}'".format(random_subject)),
            Students.name,
            func.round(func.avg(Grades.grade), 2).label("avg_grade"),
        )
        .select_from(Grades)
        .join(Students)
        .join(Subjects)
        .where(Subjects.name == random_subject)
        .group_by(Students.id, Subjects.name)
        .order_by(desc("avg_grade"))
        .limit(1)
    )

    result = session.execute(stmt).all()

    headers = ["Subjects", "Student name", "AVG Grade"]
    return tabulate(result, headers, tablefmt="pretty")


def select_3():
    # Отримуємо випадковий предмет
    random_subject = session.execute(
        select(Subjects.name).order_by(func.random()).limit(1)
    ).scalar_one()

    # Знаходимо середній бал за цей предмет для кожної групи
    stmt = (
        select(
            Groups.name,
            text("'{}'".format(random_subject)),
            func.avg(Grades.grade).label("Avg_grade"),
        )
        .select_from(Grades)
        .join(Students)
        .join(Groups)
        .join(Subjects)
        .where(Subjects.name == random_subject)
        .group_by(Groups.name)
    )

    result = session.execute(stmt).all()

    headers = ["Group name", "Subject name", "Average grade"]
    return tabulate(result, headers, tablefmt="pretty")


def select_4():
    # Знаходимо середній бал за всі предмети
    stmt = select(func.avg(Grades.grade))

    result = session.execute(stmt).all()

    headers = ["Average grade"]
    return tabulate(result, headers, tablefmt="pretty")


def select_5():
    # Отримуємо випадкового вчителя
    random_teacher = session.execute(
        select(Teachers.name).order_by(func.random()).limit(1)
    ).scalar_one()

    # Знаходимо всі предмети, які викладає цей вчитель
    stmt = (
        select(Subjects.name, text("'{}'".format(random_teacher)))
        .select_from(Subjects)
        .join(Teachers)
        .where(Teachers.name == random_teacher)
    )

    result = session.execute(stmt).all()

    headers = ["Subject names", "Teacher name"]
    return tabulate(result, headers, tablefmt="pretty")


def select_6():
    # Отримуємо випадкову групу
    random_group = session.execute(
        select(Groups.name).order_by(func.random()).limit(1)
    ).scalar_one()

    # Знаходимо всіх студентів з цієї групи
    stmt = (
        select(Groups.name.label("Group_name"), Students.name.label("Student_name"))
        .select_from(Students)
        .join(Groups)
        .where(Groups.name == random_group)
        .distinct()
    )

    result = session.execute(stmt).all()

    headers = ["Group name", "Student name"]
    return tabulate(result, headers, tablefmt="pretty")


def select_7():
    # Отримуємо випадкову групу
    random_group = session.execute(
        select(Groups.name).order_by(func.random()).limit(1)
    ).scalar_one()

    # Знаходимо всіх студентів з цієї групи
    stmt = (
        select(Groups.name.label("Group_name"), Students.name.label("Student_name"))
        .select_from(Students)
        .join(Groups)
        .where(Groups.name == random_group)
        .distinct()
    )

    result = session.execute(stmt).all()

    headers = ["Group name", "Student name"]
    return tabulate(result, headers, tablefmt="pretty")


def select_8():
    # Отримуємо випадкового вчителя, який викладає хоча б один предмет, за який були виставлені оцінки
    random_teacher = session.execute(
        select(Teachers.name)
        .where(
            Teachers.id.in_(
                select(Subjects.teacher_id).where(
                    Subjects.id.in_(select(Grades.subject_id))
                )
            )
        )
        .order_by(func.random())
        .limit(1)
    ).scalar_one()

    # Знаходимо середній бал за кожний предмет, який викладає цей вчитель
    stmt = (
        select(
            Teachers.name.label("Teacher_name"),
            Subjects.name.label("Subject_name"),
            func.avg(Grades.grade).label("Average_grade"),
        )
        .select_from(Grades)
        .join(Subjects)
        .join(Teachers)
        .where(Teachers.name == random_teacher)
        .group_by(Teachers.name, Subjects.name)
    )

    result = session.execute(stmt).all()

    headers = ["Teacher name", "Subject name", "Average grade"]
    return tabulate(result, headers, tablefmt="pretty")


def select_9():
    # Отримуємо випадкового студента
    random_student = session.execute(
        select(Students.name).order_by(func.random()).limit(1)
    ).scalar_one()

    # Знаходимо всі предмети, за які цей студент отримав оцінки
    stmt = (
        select(Students.name, Subjects.name)
        .where(Students.name == random_student)
        .distinct()
    )

    result = session.execute(stmt).all()

    headers = ["Student name", "Subjects"]
    return tabulate(result, headers, tablefmt="pretty")


def select_10():
    # Отримуємо випадкового вчителя і студента
    random_teacher = session.execute(
        select(Teachers.name).order_by(func.random()).limit(1)
    ).scalar_one()
    random_student = session.execute(
        select(Students.name).order_by(func.random()).limit(1)
    ).scalar_one()

    # Знаходимо всі предмети, які викладає цей вчитель і за які цей студент отримав оцінки
    stmt = (
        select(Teachers.name, Subjects.name, text("'{}'".format(random_student)))
        .where(Teachers.name == random_teacher, Students.name == random_student)
        .distinct()
    )

    result = session.execute(stmt).all()

    headers = ["Teacher name", "Subjects", "Student name"]
    return tabulate(result, headers, tablefmt="pretty")
