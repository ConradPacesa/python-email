import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import csv
from tabulate import tabulate
import os
from datetime import datetime

def send_test_email():
  dt = datetime.now()
  date_string = dt.strftime("%Y-%m-%d")

  files = './results/' + date_string
  filenames = [os.path.join(files, f) for f in os.listdir(files)]
  
  fromaddr = "<from email address>"
  toaddr = "<to email address>"
  
  msg = MIMEMultipart()
  
  msg['From'] = fromaddr
  msg['To'] = toaddr
  msg['Subject'] = 'Report'
  
  body = """
  <html>
  <head>
  <style> 
    table, th, td {{ border: 1px solid black; border-collapse: collapse; }}
    th, td {{ padding: 10px; }}
  </style>
  </head>
  <body>
  <p>Daily Report:</p>
  {table}
  <br>
  <img src="cid:plot1">
  <br>
  <img src="cid:plot2">
  <br>
  <img src="cid:plot3">
  </body>
  </html>
  """

  with open('./results/2018-02-22/report.csv') as input_file:
    reader = csv.reader(input_file)
    data = list(reader)

  body = body.format(table=tabulate(data, headers="firstrow", tablefmt="html"))
  
  msg.attach(MIMEText(body, 'html'))

  for i, file in enumerate(filenames):
    if file.endswith('.png'):
      path = './results/2018-02-22/plot' + str(i+1) + '.png'
      fp = open(path, 'rb')
      msgImage = MIMEImage(fp.read())
      fp.close()
      imgID = '<plot' + str(i+1) + '>'
      msgImage.add_header('Content-ID', imgID)
      msg.attach(msgImage)

  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(fromaddr, '<password>')
  text = msg.as_string()
  server.sendmail(fromaddr, toaddr, text)
  server.quit()


