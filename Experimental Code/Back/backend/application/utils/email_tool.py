from smtplib import SMTP_SSL
from email.mime.text import MIMEText
import random

from sqlalchemy import false, true

email_code = dict()

def sendMailCode(addrs):
    email_user = '2268074178@qq.com'
    email_password = 'vpwpbuuhwyzleaib'
    code = random.randint(100000,999999)
    global email_code
    email_code[addrs] = code
    msg = MIMEText("LDSS-BC验证码:{0}".format(code), 'plain', _charset="utf-8")
    msg["Subject"] = "LDSS-BC验证码"
    msg["from"] = "LDSS-BC"
    msg["to"] = addrs
    with SMTP_SSL(host="smtp.qq.com",port=465) as smtp:
        try:
            smtp.login(user = email_user, password = email_password)
            smtp.sendmail(from_addr = email_user, to_addrs=addrs, msg=msg.as_string())
            return True
        except:
            return False

def verifyMailCode(addrs,mail_code):
    global email_code
    if(addrs in email_code.keys() and email_code[addrs] == int(mail_code)):
        return True
    else:
        return False
