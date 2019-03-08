from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from base import Base


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    grade = Column(String)
    student_id = Column(Integer, ForeignKey('students.id'))
    student = relationship("Student", backref="contact_details")

    def __init__(self, title, grade, student_id):
        self.title = title
        self.grade = grade
        self.student_id = student_id
