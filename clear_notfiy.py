import gspread

import os

from email.mime.text import MIMEText

import smtplib

from pathlib import Path

sa = gspread.service_account()
# make sure to change spreadsheet name depending on year/whatever
sh = sa.open("INSERT GOOGLE SPREADSHEET NAME HERE")
kraken_roster = sh.worksheet("Kraken")
kraken_roster.batch_clear(["D3:J40"])

full_roster = sh.worksheet("Current Roster")
val = 0

fullemails = full_roster.get('F45:F')
krackemails = []

for email in fullemails:
    if email == []:
        pass
        val += 1
    else:
        krackemails.append(email)
    if email != [] and val == 1:
        val = 0
    if val == 3:
        break

krackemails_LoS = [''.join(ele) for ele in krackemails]

# beginning SMTP magic
def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()

subject = "Accountability"
# this is the clear + initial accoutability txt
body = Path('cleared.txt').read_text()
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
send_email(subject, body, EMAIL_ADDRESS, krackemails_LoS, EMAIL_PASSWORD)
 