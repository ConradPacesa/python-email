import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

files = './results/2018-02-22'
filenames = [os.path.join(files, f) for f in os.listdir(files)]
 
fromaddr = "<from email address>"
toaddr = "<to email address>"
 
msg = MIMEMultipart()
 
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Report"
 
body = "Here is the Daily Report"
 
msg.attach(MIMEText(body, 'plain'))

for file in filenames:
  part = MIMEBase('application', 'octet-stream')
  part.set_payload(open(file, 'rb').read())
  encoders.encode_base64(part)
  part.add_header('Content-Disposition', "attachment; filename= %s" % file)
  msg.attach(part)
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "<password>")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()


