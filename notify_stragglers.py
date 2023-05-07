import gspread

import os

from email.mime.text import MIMEText

import smtplib

from pathlib import Path

sa = gspread.service_account()
# make sure to change spreadsheet name depending on year/whatever
sh = sa.open("INSERT GOOGLE SPREADSHEET NAME HERE")
kraken_roster = sh.worksheet("Kraken")

"""
TODO:
Automatically update depending how many people in platoon, same as krackemails grabber
Automatically update depending how many rows of stuff there are
"""
account = kraken_roster.get("C3:J40")
absent = []
temp = []
full_roster = sh.worksheet("Current Roster")
val = 0
count = 0

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

while [] in account:
    account.remove([])

# this is the incorrect way to do this, it is stupid, I don't feel like fixing it
for i in account:
    temp = i[1:8]
    if len(temp) != 7:
            absent.append(count)
    if '' in temp:
        absent.append(count)
    count += 1

for indx,num in enumerate(absent):
    absent[indx] = krackemails[num][0]

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

subject = "Fill Out Accountability [URGENT]"
# this is the post accoutabillity email
body = Path('notify.txt').read_text()
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
send_email(subject, body, EMAIL_ADDRESS, absent, EMAIL_PASSWORD)
