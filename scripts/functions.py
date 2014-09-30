import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import configuration

def send_alert(uri):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Possible Intrusion Detected -- {}'.format(time.strftime('%c'))
    msg['From'] = configuration.sender
    msg['To'] = ','.join(configuration.recipients)
    body = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head><title></title></head>
<body>

<img src="{}">
<br><br>
The system has been deactivated.
<br><br>
Click here to activate the alarm system:
<form action="http://alarm.rollingsixes.us:8080/toggle?action=Activate" method="POST"><input type="submit" value="Activate"></form>
</body>
</html>'''.format(uri)
    part1 = MIMEText(body, 'html')
    msg.attach(part1)
    s = smtplib.SMTP('localhost')
    s.sendmail(configuration.sender, configuration.recipients, msg.as_string())
    s.quit()

