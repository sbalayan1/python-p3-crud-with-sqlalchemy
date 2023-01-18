#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, Column, Integer, DateTime, String, desc, Index, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    Index('index_name', 'name') #indexes are used to speed up lookups on certain column values. This sets up an index for the name property. 

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String())
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date= Column(DateTime(), default=datetime.now())

    #the repr method determines the standard output value of a class. All python classes have them. 
    def __repr__(self):
        return f"Student {self.id}: {self.name}, Grade: {self.grade}"
    
if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    albert_einstein = Student(
        name = "Albert Einstein",
        email = "albert.einstein@gmail.com",
        grade = 6, 
        birthday = datetime(
            year=1996,
            month=1,
            day=1
        )
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )

    session.add(albert_einstein)
    session.add(alan_turing)
    session.commit()

    students = session.query(Student).all()
    student = session.query(Student.name, Student.birthday).order_by(desc(Student.grade)).limit(1).all()

        #w/o all() prints SELECT students.name as student_name, students.birthday as student_birthday FROM students ORDER_BY students.grade DESC LIMIT ? OFFSET ?
        #w/ all() prints [('Alan Turing', datetime.datetime(1912, 6, 23, 0, 0))]

    # student = session.query(Student.name, Student.birthday).order_by(desc(Student.grade)).first()
        #prints ('Alan Turing', datetime.datetime(1912, 6, 23, 0, 0))

    # print(students)
    # print(student)

    # print(session.query(func.count(Student.id).all()))
    # => [(2,)]

    # print(session.query(Student).filter(Student.name.like('%Alan%'), Student.grade == 11))
        #the above will print the sql statement unless we include the all() method

    # query = session.query(Student).filter(Student.name.like('%Alan%'), Student.grade == 11).all()

    # for record in query:
    #     print(record.name)

    for student in session.query(Student).all(): #note that the all() method is not necessary here, likely because python interprets the sql statement as a list?
        student.grade += 1
        # print(student)

    session.commit()
    session.query(Student).update({Student.grade: Student.grade + 1})
    # print([(student.name, student.grade) for student in session.query(Student)])
    #=> [('Albert Einstein', 8), ('Alan Turing', 13)]

    query = session.query(Student).filter(Student.name == "Albert Einstein")
    albert_einstein = query.first()
    session.delete(albert_einstein)
    session.commit()
    print(query.first())
    #=> None
