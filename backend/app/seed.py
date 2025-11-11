from .database import SessionLocal, engine
from . import models
from decimal import Decimal

def seed():
    db = SessionLocal()
    # create 10 sample employees across two grades
    sample = [
        ('E1001','Alice','Sharma','alice.sharma@example.gov','GR-A',Decimal('40000')),
        ('E1002','Ravi','Kumar','ravi.kumar@example.gov','GR-A',Decimal('40000')),
        ('E1003','Sunita','Patel','sunita.patel@example.gov','GR-B',Decimal('30000')),
        ('E1004','Anil','Joshi','anil.joshi@example.gov','GR-B',Decimal('30000')),
        ('E1005','Neha','Singh','neha.singh@example.gov','GR-A',Decimal('40000')),
        ('E1006','Pratik','Desai','pratik.desai@example.gov','GR-B',Decimal('30000')),
        ('E1007','Meera','Iyer','meera.iyer@example.gov','GR-A',Decimal('40000')),
        ('E1008','Karan','Mehta','karan.mehta@example.gov','GR-B',Decimal('30000')),
        ('E1009','Divya','Rao','divya.rao@example.gov','GR-A',Decimal('40000')),
        ('E1010','Vijay','Nair','vijay.nair@example.gov','GR-B',Decimal('30000')),
    ]
    for code, fn, ln, email, post, base in sample:
        e = models.Employee(emp_code=code, first_name=fn, last_name=ln, email=email, post=post, base_pay=base, is_active=True)
        db.add(e)
    db.commit()
    print('Seeded employees.')
    db.close()

if __name__ == '__main__':
    models.Base.metadata.create_all(bind=engine)
    seed()
