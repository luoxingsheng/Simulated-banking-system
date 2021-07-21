#coding=UTF-8
import smtplib
from email.mime.text import MIMEText

msg_from = '3270866558@qq.com'  # 发送方邮箱
passwd = 'ysgblnohdnnjchch'  # 填入发送方邮箱的授权码
# msg_to = '893309066@qq.com'  # 收件人邮箱
# subject = "模拟银行系统重置密码"  # 主题
# content = "重置密码，验证码为：123456"  # 正文

def send_email(msg_to,subject,content):
    """根据传入的收件人地址邮件发送重置密码的邮件"""
    result = False
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print("发送成功")
        result = True
    except s.SMTPException as e:
        print("发送失败",e)
        result = False
    finally:
        return result
        s.quit()


