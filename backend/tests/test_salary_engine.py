import pytest
from app import salary_engine
from decimal import Decimal

def test_tax_compute():
    tax = salary_engine.compute_tax(Decimal(600000))
    assert tax > 0

def test_generate_payrun_creates_files(tmp_path, monkeypatch):
    from app.database import Base, engine, SessionLocal
    from app import models
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    e = models.Employee(emp_code='T100', first_name='Test', last_name='User', email='t@example.com', post='GR-A', base_pay=Decimal('40000'), is_active=True)
    db.add(e); db.commit()
    created = salary_engine.generate_payrun(db, 2025, 10)
    assert len(created) == 1
