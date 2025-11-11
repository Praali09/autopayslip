from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Numeric, JSON
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, index=True)
    emp_code = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, index=True)
    post = Column(String)
    base_pay = Column(Numeric, default=0)
    is_active = Column(Boolean, default=True)

class PayRun(Base):
    __tablename__ = 'payruns'
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    month = Column(Integer)
    status = Column(String, default='draft')

class PaySlip(Base):
    __tablename__ = 'payslips'
    id = Column(Integer, primary_key=True, index=True)
    payrun_id = Column(Integer, ForeignKey('payruns.id'))
    employee_id = Column(Integer, ForeignKey('employees.id'))
    gross = Column(Numeric)
    total_deductions = Column(Numeric)
    net = Column(Numeric)
    pdf_path = Column(String)
    employee_email = Column(String)
