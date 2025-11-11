import os
from email.message import EmailMessage
import smtplib

EMAIL_FROM = os.environ.get('EMAIL_FROM', 'no-reply@example.gov')

def send_payslip_email(to_email, pdf_path, context):
    # Simple SMTP stub - replace with your SMTP provider (use env vars)
    print(f"[mailer] Sending payslip to {to_email}, attachment: {pdf_path}")
    # The following is commented because default containers may not have SMTP reachable.
    # Uncomment and configure for real emails.
    '''
    msg = EmailMessage()
    msg['Subject'] = f"Payslip {context['month']}/{context['year']}"
    msg['From'] = EMAIL_FROM
    msg['To'] = to_email
    msg.set_content('Attached is your payslip.')
    with open(pdf_path, 'rb') as f:
        data = f.read()
    msg.add_attachment(data, maintype='application', subtype='pdf', filename=os.path.basename(pdf_path))
    with smtplib.SMTP('smtp.example.com', 587) as s:
        s.starttls()
        s.login(os.environ.get('SMTP_USER'), os.environ.get('SMTP_PASS'))
        s.send_message(msg)
    '''
    return True
