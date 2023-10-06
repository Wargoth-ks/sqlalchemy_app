from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import List


class Base(DeclarativeBase):
    pass


class Groups(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(130), nullable=False)
    students: Mapped[List["Students"]] = relationship(back_populates="group")


class Students(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(130), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Groups"] = relationship(back_populates="students")
    grade: Mapped[List["Grades"]] = relationship(back_populates="student")


class Teachers(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(130), nullable=False)
    subjects: Mapped[List["Subjects"]] = relationship(back_populates="teacher")


class Subjects(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(130), nullable=False)

    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    teacher: Mapped["Teachers"] = relationship(back_populates="subjects")
    grade: Mapped[List["Grades"]] = relationship(back_populates="subject")


class Grades(Base):
    __tablename__ = "grades"

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), primary_key=True)
    student: Mapped["Students"] = relationship(back_populates="grade")

    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), primary_key=True)
    subject: Mapped["Subjects"] = relationship(back_populates="grade")

    grade: Mapped[int] = mapped_column(nullable=False)
    date_received: Mapped[datetime] = mapped_column(primary_key=True)
