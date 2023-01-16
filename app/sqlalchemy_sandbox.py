#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, Column, Integer, DateTime, String, desc, Index)
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

    print(alan_turing.id, albert_einstein.id)