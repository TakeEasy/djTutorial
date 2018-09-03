# -*- coding:utf-8 -*-
# Author:YEAR
import sys

sys.path.append(r"A:\development\source_code\oldBoyPython\lowChouti\backend")
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

mail_host = "smtp.qq.com"
mail_user = "2198358321@qq.com"
mail_pass = "dhwcfjyqcezfebfc"


def mail(email_list, content, subject="Low_Chouti新用户注册"):
    msg = MIMEText(content, "html", "utf-8")
    msg['From'] = formataddr(["Low_Chouti", "lowchouti@year.cool"])
    msg['Subject'] = subject

    server = smtplib.SMTP_SSL(mail_host,465)
    server.login(mail_user, mail_pass)
    server.sendmail("2198358321@qq.com", email_list, msg.as_string())
    server.quit()


if __name__ == "__main__":
    mail(["yi_zhou1@jabil.com"], "模块测试", "模块测试")
    print("测试成功")
