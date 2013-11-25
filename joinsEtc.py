#http://www.dwbiconcepts.com/tutorial/24-interview-questions/190-top-20-sql-interview-questions-with-answers.html

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Table, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///:memory:', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    #from stackoverflow
    employees = relationship("Emp", backref = "department")

    def __init__(self, id, name):
        self.id = id
        self.name = name

class Emp(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    mgr_id = Column(Integer, ForeignKey('employee.id'))
    #from stackoverflow
    manager = relationship("Emp", backref="team", remote_side=[id])
    dept_id = Column(Integer, ForeignKey('department.id'))
    name = Column(String(100))
    sal = Column(Integer)
    doj = Column(Date)

    def __init__(self,id,mgr_id,dept_id,name,sal,doj):
        self.id = id
        self.mgr_id = mgr_id
        self.dept_id = dept_id
        self.name = name
        self.sal = sal
        self.doj = doj

Base.metadata.create_all(engine)

session.add_all([Department(1,'HR'), \
                Department(2,'Engineering'), \
                Department(3,'Marketing'), \
                Department(4,'Sales'), \
                Department(5,'Logistics')])


session.add_all([
                Emp(1, None, 2,'Hash', 100, datetime(2012,01,01)), \
                Emp(2, 1, 2, 'Robo', 100, datetime(2012,01,01)), \
                Emp(3, 2, 1, 'Privy', 50, datetime(2012,05,01)), \
                Emp(4, 1, 1, 'Inno', 50, datetime(2012,05,01)), \
                Emp(5, 2, 2, 'Anno', 80, datetime(2012,02,01)), \
                #Emp(6, 1, 2, 'Darl', 80, datetime(2012,02,11)), \
                Emp(6, 1, None, 'Darl', 80, datetime(2012,02,11)), \
                Emp(7, 1, 3, 'Pete', 70, datetime(2012,04,16)), \
                Emp(8, 7, 3, 'Meme', 60, datetime(2012,07,26)), \
                Emp(9, 2, 4, 'Tomiti', 70, datetime(2012,07,07)), \
                Emp(10, 9, 4, 'Bhuti', 60, datetime(2012,8,24)), \
                ])

print '\nDepartment names'
for instance in session.query(Department).order_by(Department.id): 
    print instance.id,instance.name

print '\nEmployee names'
for instance in session.query(Emp).order_by(Emp.id):
    print instance.id,instance.name,instance.doj

print '\nInner Join'
for d, e in session.query(Department, Emp).\
                     filter(Department.id==Emp.dept_id).\
                     all(): 
    print d.name, e.name

"""
print '\nInner Join (method 2) - doesn''t work'
for d in session.query(Department).join(Emp).\
     filter(Department.id==Emp.dept_id).\
     all():
    print d

print '\nInner Join (method 3)'
q = session.query(Emp).join(Emp.dept_id)

print '\nOuter Join'
for d, e in session.query(Department, Emp).\
                     outerjoin(Department.id).\
                     all(): 
    print d.name, e.name
"""

print '\nInner Join2'
for d, e in session.query(Department, Emp).join(Emp):
    print d.name, e.name

print '\nOuter Join' # from Dep -> Emp
for d, e in session.query(Department, Emp).outerjoin(Emp):
    print d.name, e and e.name # NOTE: e Might be None because of the OUTER JOIN

print '\nOuter Join2' # from Emp -> Dep
for e, d in session.query(Emp, Department).outerjoin(Department):
    print e.name, d and d.name # NOTE: d Might be None because of the OUTER JOIN

print '\nThe bosses name'
the_boss = session.query(Emp).get(1)
print the_boss.name
print '\nThe bosses team'
for i in the_boss.team:
    print i.name
print '\nAssert bosses name'
assert the_boss.team[0].manager == the_boss
print '\nBosses department'
print the_boss.department.name
