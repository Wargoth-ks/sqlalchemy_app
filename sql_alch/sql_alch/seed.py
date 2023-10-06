from datetime import datetime
from random import randint, choice
import faker
from sqlalchemy import select

from models import Teachers, Students, Subjects, Grades, Groups
from settings.db import session
from sqlalchemy.exc import IntegrityError


def insert_data():
    subjects = [
        "English",
        "IT",
        "Economics",
        "Marketing",
        "Management",
        "Finance",
        "Art",
        "Alchemy",
    ]

    groups = ["101", "201", "301"]

    fake = faker.Faker()
    number_of_teachers = randint(5, 8)
    number_of_students = randint(30, 50)

    def seed_teachers():
        for _ in range(number_of_teachers):
            teacher = Teachers(name=fake.name())
            session.add(teacher)
        session.commit()

    def seed_subjects():
        teacher_ids = session.scalars(select(Teachers.id)).all()
        for subject in subjects:
            session.add(Subjects(name=subject, teacher_id=choice(teacher_ids)))
        session.commit()

    def seed_groups():
        for group in groups:
            session.add(Groups(name=group))
        session.commit()

    def seed_students():
        group_ids = session.scalars(select(Groups.id)).all()
        for _ in range(number_of_students):
            student = Students(name=fake.name(), group_id=choice(group_ids))
            session.add(student)
        session.commit()

    def seed_grades():
        current_year = datetime.now().year
        student_ids = session.scalars(select(Students.id)).all()
        subject_ids = session.scalars(select(Subjects.id)).all()

        for student_id in student_ids:
            
            for subject_id in subject_ids:
                
                for _ in range(randint(1, 20 // len(subject_ids))):
                    date_received = fake.date_between_dates(
                        date_start=datetime(current_year, 1, 1),
                        date_end=datetime(current_year, 12, 31),
                    )

                    grade = Grades(
                        grade=randint(1, 5),
                        date_received=date_received,
                        student_id=student_id,
                        subject_id=subject_id,
                    )
                    session.add(grade)
                try:
                    session.commit()
                except IntegrityError:
                    session.rollback()

    seed_teachers()
    seed_subjects()
    seed_groups()
    seed_students()
    seed_grades()


if __name__ == "__main__":
    insert_data()
