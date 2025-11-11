from . import models
from .database import SessionLocal
from decimal import Decimal, ROUND_HALF_UP
from jinja2 import Template
from weasyprint import HTML
import os, json

# sample tax slabs (configurable)
TAX_SLABS = [
    (250000, 0),
    (500000, 5),
    (750000, 10),
    (1000000, 15),
    (float('inf'), 20)
]

def cents(x):
    return Decimal(x).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def working_days_in_month(year, month):
    # simple default - configurable later
    return 26

def compute_tax(annual_taxable):
    # Compute simple slab-based tax on annual taxable income.
    tax = Decimal('0')
    prev = 0
    for upper, rate in TAX_SLABS:
        if annual_taxable <= prev:
            break
        slab_amount = min(annual_taxable, Decimal(str(upper))) - Decimal(prev)
        if slab_amount > 0:
            tax += slab_amount * Decimal(rate) / Decimal(100)
        prev = upper
    return cents(tax)

def load_pay_scale_config(db):
    # Return a small in-memory mapping for pay scales.
    return {
        'GR-A': {
            'base_pay': Decimal('40000'),
            'allowances': [
                {'name':'HRA','type':'percent','value':20},
                {'name':'Medical','type':'fixed','value':1250}
            ],
            'deductions': [
                {'name':'PF','type':'percent','value':12},
                {'name':'Professional Tax','type':'fixed','value':200}
            ]
        },
        'GR-B': {
            'base_pay': Decimal('30000'),
            'allowances': [
                {'name':'HRA','type':'percent','value':18},
                {'name':'Transport','type':'fixed','value':800}
            ],
            'deductions': [
                {'name':'PF','type':'percent','value':12},
                {'name':'Professional Tax','type':'fixed','value':150}
            ]
        }
    }

def generate_payrun(db, year, month):
    created = []
    pr = models.PayRun(year=year, month=month, status='draft')
    db.add(pr); db.commit(); db.refresh(pr)
    employees = db.query(models.Employee).filter(models.Employee.is_active==True).all()

    pay_scales = load_pay_scale_config(db)

    for e in employees:
        scale_key = e.post or None
        if scale_key and scale_key in pay_scales:
            config = pay_scales[scale_key]
            base = cents(config['base_pay'])
            allowances = config.get('allowances', [])
            deductions_cfg = config.get('deductions', [])
        else:
            base = cents(e.base_pay or 0)
            allowances = []
            deductions_cfg = []

        wd = Decimal(working_days_in_month(year, month))
        per_day = (base / wd).quantize(Decimal('0.01'))
        leave_days = getattr(e, 'leave_days', 0) if hasattr(e, 'leave_days') else 0
        leave_deduction = per_day * Decimal(leave_days)

        gross = base
        for a in allowances:
            if a['type'] == 'fixed':
                gross += Decimal(a['value'])
            elif a['type'] == 'percent':
                gross += (base * Decimal(a['value']) / Decimal(100))
        gross = cents(gross)

        total_deductions = Decimal(0)
        total_deductions += leave_deduction
        for d in deductions_cfg:
            if d['type'] == 'fixed':
                total_deductions += Decimal(d['value'])
            elif d['type'] == 'percent':
                total_deductions += (gross * Decimal(d['value']) / Decimal(100))
        total_deductions = cents(total_deductions)

        monthly_taxable = gross - total_deductions
        annual_taxable = monthly_taxable * Decimal(12)
        annual_tax = compute_tax(annual_taxable)
        monthly_tax = (annual_tax / Decimal(12)).quantize(Decimal('0.01'))
        total_deductions += monthly_tax
        total_deductions = cents(total_deductions)

        net = cents(gross - total_deductions)

        context = {
            'employee': {'name': f"{e.first_name} {e.last_name}", 'emp_code': e.emp_code},
            'year': year, 'month': month,
            'base': str(base), 'gross': str(gross), 'deductions': str(total_deductions), 'net': str(net),
            'breakdown': {
                'allowances': allowances,
                'deductions': deductions_cfg,
                'leave_days': leave_days,
                'monthly_tax': str(monthly_tax)
            }
        }
        pdf_path = render_payslip_to_pdf(context, e.emp_code, year, month)
        ps = models.PaySlip(payrun_id=pr.id, employee_id=e.id, gross=gross, total_deductions=total_deductions, net=net, pdf_path=pdf_path, employee_email=e.email)
        db.add(ps)
        db.commit()
        created.append({'employee_id': e.id, 'net': str(net), 'pdf_path': pdf_path})
    return created

def approve_payrun(db, year, month):
    pr = db.query(models.PayRun).filter(models.PayRun.year==year, models.PayRun.month==month).first()
    if not pr:
        return []
    pr.status = 'approved'
    db.commit()
    slips = db.query(models.PaySlip).filter(models.PaySlip.payrun_id==pr.id).all()
    result = []
    for s in slips:
        result.append({'employee_id': s.employee_id, 'employee_email': s.employee_email, 'pdf_path': s.pdf_path})
    return result

def render_payslip_to_pdf(context, emp_code, year, month):
    template_path = os.path.join(os.path.dirname(__file__), 'payslip_template.html')
    with open(template_path) as f:
        html_t = f.read()
    tmpl = Template(html_t)
    html = tmpl.render(context=context)
    out_dir = os.path.join(os.getcwd(), 'payslips')
    os.makedirs(out_dir, exist_ok=True)
    filename = f"payslip_{emp_code}_{year}_{month}.pdf"
    out_path = os.path.join(out_dir, filename)
    HTML(string=html).write_pdf(out_path)
    return out_path
