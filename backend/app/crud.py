from sqlalchemy.orm import Session
from . import models
from decimal import Decimal

def create_employee(db: Session, emp: dict):
    e = models.Employee(
        emp_code=emp.get('emp_code'),
        first_name=emp.get('first_name'),
        last_name=emp.get('last_name'),
        email=emp.get('email'),
        post=emp.get('post'),
        base_pay=Decimal(emp.get('base_pay', 0))
    )
    db.add(e)
    db.commit()
    db.refresh(e)
    return {'id': e.id, 'emp_code': e.emp_code}

def get_employees(db: Session):
    return db.query(models.Employee).filter(models.Employee.is_active==True).all()
