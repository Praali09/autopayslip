from fastapi import FastAPI, Depends, HTTPException
from . import models, database, crud, salary_engine, mailer
from sqlalchemy.orm import Session
import uvicorn
import os

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Gov Payroll - Auto Payslip")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/health')
def health():
    return {'status':'ok'}

@app.post('/employees/')
def create_employee(emp: dict, db: Session = Depends(get_db)):
    return crud.create_employee(db, emp)

@app.get('/employees/')
def list_employees(db: Session = Depends(get_db)):
    return crud.get_employees(db)

@app.post('/payrun/generate/{year}/{month}')
def generate_payrun(year: int, month: int, db: Session = Depends(get_db)):
    # creates payslips (draft) for all active employees
    results = salary_engine.generate_payrun(db, year, month)
    return {'created': len(results), 'details_sample': results[:3]}

@app.post('/payrun/approve/{year}/{month}')
def approve_payrun(year: int, month: int, db: Session = Depends(get_db)):
    approved = salary_engine.approve_payrun(db, year, month)
    # send emails (stub)
    for ps in approved:
        mailer.send_payslip_email(ps['employee_email'], ps['pdf_path'], ps)
    return {'approved': len(approved)}
