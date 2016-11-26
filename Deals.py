import MySQLdb
import sys
import pandas as pd
import smtplib
from smtplib import SMTP_SSL as SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import databases


connection = MySQLdb.connect(**databases.ProdDBDetails)
cursor = connection.cursor()


deals = pd.read_sql("select id, short_description, end_date from deal where date(end_date)=date(current_timestamp)", con=connection)
message = deals.to_html(index=False).encode('utf-8')


def send_mail(send_from, send_to, subject, text, user, passwd, files=None):
   assert isinstance(send_to, list)

   msg = MIMEMultipart()
   msg['From'] = send_from
   msg['To'] = COMMASPACE.join(send_to)
   msg['Date'] = formatdate(localtime=True)
   msg['Subject'] = subject

   msg.attach(MIMEText(text, 'html'))
   print 'Started adding file'
   for f in files or []:
       with open(f, "rb") as fil:
           part = MIMEApplication(
               fil.read(),
               Name=basename(f)
           )
           part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
           msg.attach(part)


   smtpserver = smtplib.SMTP("smtp.gmail.com:587")
   # smtpserver.set_debuglevel(False)
   smtpserver.ehlo()
   smtpserver.starttls()
   # smtpserver.ehlo
   smtpserver.login(user, passwd)
   print 'Logged in'
   smtpserver.sendmail(send_from, send_to, msg.as_string())
   print 'sent mail'
   smtpserver.close()


send_mail('sindhujab@enixta.com',['sindhujab@enixta.com'], 'Deals going to be expired today!', message, 'sindhujab@enixta.com', 'poicbminfyxkrkjk')
